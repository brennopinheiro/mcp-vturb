"""Auto-generated VTurb Analytics tools — conversions.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def conversions_active_platforms(start_date: str, timezone: Optional[str] = None) -> Any:
    """Returns the active platforms for a company
    
    POST /conversions/active_platforms
    
    Returns a list with the company active platforms.
    
    Args:
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if start_date is not None:
        json_body['start_date'] = start_date
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/conversions/active_platforms', json_body=json_body or None)


async def conversions_stats_by_day(end_date: str, player_id: str, start_date: str, timezone: Optional[str] = None) -> Any:
    """Returns the totals of conversions for each day in a company and player
    
    POST /conversions/stats_by_day
    
    Returns a list with the company conversions grouped by day in a given period.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/conversions/stats_by_day', json_body=json_body or None)


async def conversions_video_timed(end_date: str, player_id: str, start_date: str, timezone: Optional[str] = None) -> Any:
    """Returns the conversions grouped by timed for a company and player
    
    POST /conversions/video_timed
    
    Returns a list with the company conversions grouped by timed in a given period.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/conversions/video_timed', json_body=json_body or None)
