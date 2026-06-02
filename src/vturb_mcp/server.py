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
    """CodeMode variant that preserves Prefab App tools.

    The stock CodeMode collapses every tool into search/get_schema/execute,
    which would hide our `player_overview` dashboard. App tools carry a
    `meta.ui` payload — we passthrough those untouched while still collapsing
    the rest.
    """

    async def transform_tools(self, tools: Sequence[Tool]) -> Sequence[Tool]:
        collapsed = await super().transform_tools(tools)
        app_tools = [t for t in tools if (t.meta or {}).get("ui")]
        return [*collapsed, *app_tools]

INSTRUCTIONS = """\
VTurb Analytics MCP — programmatic access to vturb's analytics database.

All 28 endpoints from https://analytics.vturb.net are exposed as tools, grouped
by category (clicks, conversions, events, sessions, traffic_origin, times,
comparison_groups, players, quota, custom_metrics, headlines, turbo).

Code Mode is enabled: use `search` to discover tools, `get_schema` to inspect
signatures (enum values are included in arg descriptions), and `execute` to
run them.

Self rate-limit check: call `quota_usage` before expensive queries — it returns
used / limit / remaining for the per-minute and per-day buckets.

Visual dashboard: `player_overview(player_id, start_date, end_date)` renders an
interactive panel with KPIs, daily conversions chart, active platforms, and
current quota usage — bypasses Code Mode.
"""

mcp = FastMCP("vturb-analytics", instructions=INSTRUCTIONS)


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
# search/get_schema/execute collapse and render as interactive panels.
mcp.tool(player_overview, app=True)

# Code Mode collapses every other registered tool into 3 meta-tools
# (search / get_schema / execute) — scales better than exposing N tools.
_sandbox = MontySandboxProvider(
    limits={"max_duration_secs": 30, "max_memory": 100_000_000},
)
mcp.add_transform(CodeModeKeepApps(sandbox_provider=_sandbox))


def main() -> None:
    """CLI entry point (referenced by [project.scripts] vturb-mcp)."""
    mcp.run()


if __name__ == "__main__":
    main()
