"""FastMCP server entry point for VTurb Analytics."""

from __future__ import annotations

import importlib
import inspect
from pathlib import Path

from typing import Sequence

from fastmcp import FastMCP
from fastmcp.experimental.transforms.code_mode import CodeMode, MontySandboxProvider
from fastmcp.tools.tool import Tool

from vturb_mcp.apps.dashboard import player_overview


class CodeModeKeepApps(CodeMode):
    """CodeMode variant that preserves Prefab App tools and any tool whose
    name starts with `vturb_`.

    The stock CodeMode collapses every tool into search/get_schema/execute,
    which would hide both our `vturb_player_overview` dashboard and the
    `vturb_help` entry-point tool. App tools carry `meta.ui`; the help tool
    is identified by its name prefix.
    """

    async def transform_tools(self, tools: Sequence[Tool]) -> Sequence[Tool]:
        collapsed = await super().transform_tools(tools)
        collapsed_names = {t.name for t in collapsed}
        preserved = [
            t for t in tools
            if t.name not in collapsed_names
            and ((t.meta or {}).get("ui") or t.name.startswith("vturb_"))
        ]
        return [*collapsed, *preserved]

    async def get_tool(self, name, call_next, *, version=None):
        # Route preserved tools to the underlying catalog instead of CodeMode
        if name.startswith("vturb_") and name not in {self.execute_tool_name}:
            tool = await call_next(name, version=version)
            if tool is not None:
                return tool
        return await super().get_tool(name, call_next, version=version)

INSTRUCTIONS = """\
VTurb Analytics MCP — programmatic access to vturb's analytics database.

ALWAYS call `vturb_help` first when the user mentions VTurb, video analytics,
VSL metrics, conversions/views/plays, or asks about anything available "in vturb".
That tool returns the full catalog and usage flow.

Underlying coverage: all 28 endpoints from https://analytics.vturb.net, grouped
by category (clicks, conversions, events, sessions, traffic_origin, times,
comparison_groups, players, quota, custom_metrics, headlines, turbo).

Code Mode is enabled: use `search` to discover the underlying tools, `get_schema`
to inspect signatures (enum values are included in arg descriptions), and
`vturb_execute` to run them.

Self rate-limit check: call `quota_usage` (via execute) before expensive queries
— it returns used / limit / remaining for the per-minute and per-day buckets.

Visual dashboard: `vturb_player_overview(player_id, start_date, end_date)`
renders an interactive panel with KPIs, daily conversions chart, active
platforms, and current quota usage — bypasses Code Mode.
"""

mcp = FastMCP("vturb-analytics", instructions=INSTRUCTIONS)


@mcp.tool
async def vturb_help() -> str:
    """VTurb Analytics — entry point. Call this FIRST whenever the user mentions
    VTurb, video analytics, VSL metrics, player IDs, conversions, views, plays,
    sessions, traffic origin, AB tests, or anything related to vturb.com.

    Returns the full catalog of 28 underlying API tools, the visual dashboard
    available, and the discovery flow (search → get_schema → vturb_execute).

    No arguments. Always safe to call.
    """
    return """VTurb Analytics MCP — local wrapper around analytics.vturb.net (28 endpoints).

CATEGORIES — call `search('<keyword>')` to find specific tools, then
`get_schema('<tool_name>')` to inspect args, then `vturb_execute(...)` to run.

  • clicks            — total clicks by company/day, by video timed
  • comparison_groups — list AB tests and stats (up to 2 players each)
  • conversions       — active platforms, stats by day, video timed (per second)
  • custom_metrics    — list custom metrics of a player
  • events            — leaderboard, totals by company/day/players
  • headlines         — stats by player (headlines dashboard)
  • players           — list players with optional name search
  • quota             — current API quota (self rate-limit check, call this
                        before heavy queries)
  • sessions          — stats, by day, by field, by field+day, live users
  • times             — user engagement by second/day/field/traffic origin
  • traffic_origin    — stats, by day, valid UTMs
  • turbo             — stats by player (turbo dashboard)

VISUAL DASHBOARD:
  `vturb_player_overview(player_id, start_date, end_date, timezone?)` renders a
  panel with KPIs (views / plays / finishes / conversions / revenue USD+BRL),
  daily conversions bar chart, active platforms table, and current API quota.
  Use this when the user wants a high-level overview of a single player.

DATE FORMAT for all tools: "YYYY-MM-DD" or "YYYY-MM-DD HH:MM:SS".
DEFAULT TIMEZONE: UTC server-side. Pass `timezone="America/Sao_Paulo"` for BR.

RATE LIMITS: 60/120/300/800 req/min depending on the user's VTurb plan. Use
`quota/usage` to check before bursting requests.

If the user gives a player_id and a date range, prefer `vturb_player_overview`
for the visual panel. For specific metrics or custom slicing, use the discovery
flow with `search`."""


def _register_generated_tools() -> int:
    """Auto-discover and register every async function in tools/*.py."""
    tools_dir = Path(__file__).parent / "tools"
    skip = {"__init__"}
    registered = 0
    for module_path in sorted(tools_dir.glob("*.py")):
        stem = module_path.stem
        if stem in skip:
            continue
        module = importlib.import_module(f"vturb_mcp.tools.{stem}")
        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("_"):
                continue
            if not inspect.iscoroutinefunction(obj):
                continue
            mcp.tool(obj)
            registered += 1
    return registered


_register_generated_tools()

# Prefab App dashboards — registered BEFORE CodeMode so they bypass the
# collapse and render as interactive panels. Renamed to vturb_player_overview
# so the tool name self-identifies as part of the VTurb server (otherwise
# Claude Desktop has no name-level signal pointing at this MCP).
mcp.tool(player_overview, app=True, name="vturb_player_overview")

# Code Mode collapses every other registered tool into meta-tools. We rename
# `execute` → `vturb_execute` so a user prompt like "use the vturb MCP" matches
# at least one tool name. `search` and `get_schema` come from internal CodeMode
# factories and stay generic.
_sandbox = MontySandboxProvider(
    limits={"max_duration_secs": 30, "max_memory": 100_000_000},
)
mcp.add_transform(
    CodeModeKeepApps(
        sandbox_provider=_sandbox,
        execute_tool_name="vturb_execute",
    )
)


def main() -> None:
    """CLI entry point (referenced by [project.scripts] vturb-mcp)."""
    mcp.run()


if __name__ == "__main__":
    main()
