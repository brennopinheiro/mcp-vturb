"""Auto-generated VTurb Analytics tools — quota.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def quota_usage() -> Any:
    """Returns the live API quota usage for the authenticated company
    
    GET /quota/usage
    
    Returns the current usage and limits for your API key — one entry per quota window (typically a per-minute and a per-day bucket). Use this endpoint to self-rate-limit before issuing expensive analytics requests.
    
    Notes:
    - When a metric has no cap, the response returns `limit: null` and
      `remaining: null` so you don't divide by zero.
    
    - A single API request may count as more than one query against
      `max_queries_per_minute`, so the `queries` counter can climb faster
      than your request rate. The response includes `queries.note` to flag
      this when a hard limit applies. `read_bytes` reflects the actual
      data scanned and is the more reliable signal for sizing usage.
    
    - This endpoint itself counts as 1 query against `max_queries_per_minute`.
        """

    params: dict = {}
    return await _client.get('/quota/usage', params=params or None)
