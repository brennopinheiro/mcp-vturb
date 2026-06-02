"""Auto-generated VTurb Analytics tools — clicks.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def clicks_total_by_company_day(end_date: str, player_id: str, start_date: str, timezone: Optional[str] = None) -> Any:
    """Returns the totals of clicks for each day in a company and player
    
    POST /clicks/total_by_company_day
    
    Returns a list with the company clicks grouped by day in a given period.
    
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
    return await _client.post('/clicks/total_by_company_day', json_body=json_body or None)


async def clicks_total_by_company_timed(end_date: str, player_id: str, start_date: str, timezone: Optional[str] = None) -> Any:
    """Returns the total of user clicks at a time in seconds related to the video
    
    POST /clicks/total_by_company_timed
    
    Returns an object containing the all the clicks grouped by the time in seconds it happened related to the video.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
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
    return await _client.post('/clicks/total_by_company_timed', json_body=json_body or None)
