#!/usr/bin/env python3
"""MCPB entry point — boots the VTurb FastMCP server.

`uv run --directory <bundle> src/server.py` installs the local project
declared in pyproject.toml (which registers the `vturb_mcp` package),
so the import below resolves to the installed package.
"""

from vturb_mcp.server import main

if __name__ == "__main__":
    main()
