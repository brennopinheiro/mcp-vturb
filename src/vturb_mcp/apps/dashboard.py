"""Player Overview dashboard — Prefab App tool.

Aggregates sessions stats + conversions by day + quota usage for a single
player and renders an interactive panel inside the MCP client.
"""

from __future__ import annotations

import asyncio
from typing import Any, Optional

from prefab_ui.app import PrefabApp
from prefab_ui.components import Column, DataTable, DataTableColumn, Heading, Row, Text
from prefab_ui.components.charts import BarChart, ChartSeries
from prefab_ui.components.metric import Metric

from vturb_mcp.client import VturbClient, VturbError

_client = VturbClient()


def _g(d: Any, *path: str, default: Any = None) -> Any:
    """Safe nested dict get — returns default if any key is missing."""
    cur = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    return cur


def _num(v: Any, default: float = 0) -> float:
    try:
        return float(v) if v is not None else default
    except (TypeError, ValueError):
        return default


def _fmt_int(v: Any) -> str:
    return f"{int(_num(v)):,}".replace(",", ".")


def _fmt_usd(v: Any) -> str:
    return f"US$ {_num(v):,.2f}"


async def player_overview(
    player_id: str,
    start_date: str,
    end_date: str,
    timezone: Optional[str] = None,
) -> PrefabApp:
    """VTurb Player Overview — aggregated dashboard for a single player.

    Renders views/plays/conversions/revenue KPIs, daily conversions chart,
    active platforms, and current API quota usage.

    Args:
        player_id (required): The VTurb player ID to inspect.
        start_date (required): Period start. Formats: '2026-05-01' or '2026-05-01 00:00:00'.
        end_date (required): Period end. Same formats as start_date.
        timezone (optional): IANA timezone (e.g. 'America/Sao_Paulo'). Defaults to UTC server-side.
    """
    base_body = {
        "player_id": player_id,
        "start_date": start_date,
        "end_date": end_date,
    }
    if timezone:
        base_body["timezone"] = timezone

    async def _safe(coro):
        try:
            return await coro
        except VturbError as e:
            return {"_error": f"{e.status_code}: {e}"}

    sessions, conversions_day, active_platforms, quota = await asyncio.gather(
        _safe(_client.post("/sessions/stats", json_body=dict(base_body))),
        _safe(_client.post("/conversions/stats_by_day", json_body=dict(base_body))),
        _safe(_client.post("/conversions/active_platforms",
                           json_body={"start_date": start_date,
                                      **({"timezone": timezone} if timezone else {})})),
        _safe(_client.get("/quota/usage")),
    )

    views_total = _g(sessions, "views", "total")
    plays_total = _g(sessions, "plays", "total")
    finishes_total = _g(sessions, "finishes", "total")
    conv_total = _g(sessions, "conversions", "total")
    revenue_usd = _g(sessions, "conversions", "total_amount_usd")
    revenue_brl = _g(sessions, "conversions", "total_amount_brl")

    daily_rows = []
    if isinstance(conversions_day, list):
        for row in conversions_day:
            if not isinstance(row, dict):
                continue
            daily_rows.append({
                "day": row.get("day") or row.get("date") or "",
                "conversions": int(_num(row.get("total") or row.get("count"))),
                "revenue_usd": _num(row.get("total_amount_usd") or row.get("amount_usd")),
            })
    elif isinstance(conversions_day, dict) and isinstance(conversions_day.get("data"), list):
        for row in conversions_day["data"]:
            daily_rows.append({
                "day": row.get("day") or row.get("date") or "",
                "conversions": int(_num(row.get("total"))),
                "revenue_usd": _num(row.get("total_amount_usd")),
            })

    platform_rows = []
    if isinstance(active_platforms, list):
        for p in active_platforms:
            platform_rows.append({"platform": str(p)})

    quota_minute = None
    if isinstance(quota, dict):
        for q in quota.get("quotas", []) or []:
            if q.get("interval_seconds") == 60:
                quota_minute = q
                break

    with Column(gap=6, cssClass="p-6") as view:
        Heading("VTurb Player Overview", level=1)
        Text(
            f"Player {player_id} · {start_date} → {end_date}"
            + (f" · {timezone}" if timezone else "")
        )

        with Row(gap=4):
            Metric(label="Views", value=_fmt_int(views_total))
            Metric(label="Plays", value=_fmt_int(plays_total))
            Metric(label="Finishes", value=_fmt_int(finishes_total))
            Metric(label="Conversions", value=_fmt_int(conv_total))
            Metric(label="Revenue (USD)", value=_fmt_usd(revenue_usd))
            if revenue_brl is not None:
                Metric(label="Revenue (BRL)", value=f"R$ {_num(revenue_brl):,.2f}")

        if daily_rows:
            Heading("Conversions by day", level=2)
            BarChart(
                data=daily_rows,
                xAxis="day",
                series=[
                    ChartSeries(dataKey="conversions", name="Conversions"),
                    ChartSeries(dataKey="revenue_usd", name="Revenue (USD)"),
                ],
            )
        else:
            Text("No daily conversion data for this window.")

        if platform_rows:
            Heading("Active platforms", level=2)
            DataTable(
                rows=platform_rows,
                columns=[DataTableColumn(header="Platform", accessor="platform")],
            )

        if quota_minute:
            Heading("API quota — current minute", level=2)
            with Row(gap=4):
                Metric(
                    label="Queries",
                    value=f"{quota_minute.get('queries',{}).get('used','-')}/{quota_minute.get('queries',{}).get('limit','-')}",
                )
                Metric(
                    label="Read bytes used",
                    value=_fmt_int(quota_minute.get("read_bytes", {}).get("used")),
                )
                Metric(
                    label="Resets at",
                    value=str(quota_minute.get("interval_ends_at", "—")),
                )

        # Surface errors at the bottom so the dashboard still renders the parts that worked
        for name, payload in (
            ("sessions/stats", sessions),
            ("conversions/stats_by_day", conversions_day),
            ("conversions/active_platforms", active_platforms),
            ("quota/usage", quota),
        ):
            if isinstance(payload, dict) and "_error" in payload:
                Text(f"⚠ {name}: {payload['_error']}")

    return PrefabApp(view=view)
