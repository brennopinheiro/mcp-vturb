"""Auto-generated VTurb Analytics tools — events.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def events_leaderboard(company_id: str, leaderboards: list[dict], timezone: Optional[str] = None) -> Any:
    """Returns player leaderboards based on video engagement metrics
    
    POST /events/leaderboard
    
    Provides leaderboard rankings of players based on their video engagement metrics (views, plays, pauses, etc...) within specified time periods. Multiple leaderboards with different player limits can be requested in a single call.
    
    Args:
        company_id (required): The ID of the company to search for
        leaderboards (required): 
        timezone (optional): The timezone to use for date calculations (defaults to 'Etc/UCT' if not provided)
        """

    json_body: dict = {}
    if company_id is not None:
        json_body['company_id'] = company_id
    if leaderboards is not None:
        json_body['leaderboards'] = leaderboards
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/events/leaderboard', json_body=json_body or None)


async def events_total_by_company(events: list[str], end_date: Optional[str] = None, player_id: Optional[str] = None, start_date: Optional[str] = None) -> Any:
    """Returns the number of times the events happened as well as the count considering unique device and sessions
    
    POST /events/total_by_company
    
    Returns a list with the companies and events with the number of times the event happened in a given period.
    
    Args:
        events (required): Names of the events to filter by. Can be ['started', 'finished', 'viewed']
        end_date (optional): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (optional): The ID of the player to filter the results by.
        start_date (optional): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        """

    json_body: dict = {}
    if events is not None:
        json_body['events'] = events
    if end_date is not None:
        json_body['end_date'] = end_date
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    return await _client.post('/events/total_by_company', json_body=json_body or None)


async def events_total_by_company_day(events: list[str], player_id: str, end_date: Optional[str] = None, start_date: Optional[str] = None, timezone: Optional[str] = None) -> Any:
    """Returns the totals of the events for each day in a company
    
    POST /events/total_by_company_day
    
    Returns a list with the companies grouped by day and the number of times each event happened for each day in a given period.
    
    Args:
        events (required): Names of the events to filter by. Can be ['started', 'finished', 'viewed']
        player_id (required): The ID of the player to search for
        end_date (optional): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        start_date (optional): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if events is not None:
        json_body['events'] = events
    if player_id is not None:
        json_body['player_id'] = player_id
    if end_date is not None:
        json_body['end_date'] = end_date
    if start_date is not None:
        json_body['start_date'] = start_date
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/events/total_by_company_day', json_body=json_body or None)


async def events_total_by_company_players(events: list[str], end_date: Optional[str] = None, players_start_date: Optional[list[dict]] = None, start_date: Optional[str] = None) -> Any:
    """Returns the totals of the events for each player in a company
    
    POST /events/total_by_company_players
    
    Returns a list with the companies grouped by its players and the number of times each event happened for each one in a given period.
    
    Args:
        events (required): Names of the events to filter by. Can be ['started', 'finished', 'viewed']
        end_date (optional): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        players_start_date (optional): 
        start_date (optional): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        """

    json_body: dict = {}
    if events is not None:
        json_body['events'] = events
    if end_date is not None:
        json_body['end_date'] = end_date
    if players_start_date is not None:
        json_body['players_start_date'] = players_start_date
    if start_date is not None:
        json_body['start_date'] = start_date
    return await _client.post('/events/total_by_company_players', json_body=json_body or None)
