"""Auto-generated VTurb Analytics tools — custom_metrics.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def custom_metrics_list(player_id: str, end_date: Optional[str] = None, start_date: Optional[str] = None, timezone: Optional[str] = None) -> Any:
    """List all custom metrics of a player
    
    POST /custom_metrics/list
    
    Returns a list of all custom metrics of a player and the calculated engagement rate for them
    
    Args:
        player_id (required): The player being analysed.
        end_date (optional): End date of the period for event querying. [Format: date-time]
        start_date (optional): Start date of the period for event querying. [Format: date-time]
        timezone (optional): The timezone to use for the date filtering, if not provided UTC will be used
        """

    json_body: dict = {}
    if player_id is not None:
        json_body['player_id'] = player_id
    if end_date is not None:
        json_body['end_date'] = end_date
    if start_date is not None:
        json_body['start_date'] = start_date
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/custom_metrics/list', json_body=json_body or None)
