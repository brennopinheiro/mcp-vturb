"""Auto-generated VTurb Analytics tools — players.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def players_list(end_date: Optional[str] = None, name: Optional[str] = None, name_match: Optional[str] = None, start_date: Optional[str] = None, timezone: Optional[str] = None) -> Any:
    """List all players
    
    GET /players/list
    
    Returns a list of all players belonging to the authenticated user's company
    
    Args:
        end_date (optional): End date of the period for player filtering. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        name (optional): Filter players by name. Search is case-insensitive (including non-ASCII characters such as `É`/`é`). Special characters `%`, `_`, `\\`, and brackets are matched literally — for example `name=[campaign_1]` returns only players whose names contain that exact tag. Surrounding whitespace is trimmed before matching; the trimmed value must be between 3 and 128 characters.
        name_match (optional): How `name` is matched. `contains` (default) matches anywhere in the name; `starts_with` and `ends_with` anchor to the beginning or end; `exact` requires a full case-insensitive match. Sending `name_match` without `name` returns 400. [Values: contains, starts_with, ends_with, exact Default: contains]
        start_date (optional): Start date of the period for player filtering. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        timezone (optional): The timezone to use for the date filtering
        """

    params: dict = {}
    if end_date is not None:
        params['end_date'] = end_date
    if name is not None:
        params['name'] = name
    if name_match is not None:
        params['name_match'] = name_match
    if start_date is not None:
        params['start_date'] = start_date
    if timezone is not None:
        params['timezone'] = timezone
    return await _client.get('/players/list', params=params or None)
