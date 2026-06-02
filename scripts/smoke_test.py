"""Live smoke test — single read-only call against the real API.

Reads VTURB_API_TOKEN from env, calls `GET /quota/usage` (cheapest read-only
endpoint, counts as 1 query against the per-minute limit), prints the result.
Exits non-zero on auth/transport errors.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys

from vturb_mcp.client import VturbClient, VturbError


async def main() -> int:
    if not os.environ.get("VTURB_API_TOKEN"):
        print("ERROR: set VTURB_API_TOKEN before running this script", file=sys.stderr)
        return 2

    client = VturbClient()
    try:
        result = await client.get("/quota/usage")
        print("✓ /quota/usage OK")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except VturbError as e:
        print(f"✗ VturbError {e.status_code}: {e}", file=sys.stderr)
        if e.details:
            print(json.dumps(e.details, indent=2, ensure_ascii=False), file=sys.stderr)
        return 1
    finally:
        await client.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
