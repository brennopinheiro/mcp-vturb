"""Auto-generated VTurb Analytics tools — times.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def times_user_engagement(player_id: str, video_duration: int, end_date: Optional[str] = None, start_date: Optional[str] = None, timezone: Optional[str] = None) -> Any:
    """Returns the total of users that reached a certain second of the video entire duration
    
    POST /times/user_engagement
    
    Returns an object containing the overall engagement of the users in a given period for the specified player.
    
    Args:
        player_id (required): The ID of the player to search for
        video_duration (required): The total duration of the video in seconds
        end_date (optional): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        start_date (optional): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if player_id is not None:
        json_body['player_id'] = player_id
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    if end_date is not None:
        json_body['end_date'] = end_date
    if start_date is not None:
        json_body['start_date'] = start_date
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/times/user_engagement', json_body=json_body or None)


async def times_user_engagement_by_day(end_date: str, player_id: str, start_date: str, video_duration: int, timezone: Optional[str] = None) -> Any:
    """Returns an array with the engagement rate per day
    
    POST /times/user_engagement_by_day
    
    Returns an array containing the overall engagement of the users in a given period for the specified player per day.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        video_duration (required): The total duration of the video in seconds
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/times/user_engagement_by_day', json_body=json_body or None)


async def times_user_engagement_by_field(end_date: str, field: str, player_id: str, start_date: str, values: list[str], timezone: Optional[str] = None) -> Any:
    """Returns an array with the engagement grouped by a field
    
    POST /times/user_engagement_by_field
    
    Returns an array containing the overall engagement of the users in a given period for the specified player per day.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        field (required): The field to group the engagement by, possible values are 'country', 'browser', 'device_type', 'utm_campain', 'utm_source', 'utm_medium', 'utm_content', 'utm_term' If 'no_attribution' is passed, all values that have been set to null or that are empty strings will be returned.
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" [Format: date]
        values (required): The values to filter the field by, for example ['Brazil', 'Romenia'] or ['Chrome', 'Firefox']
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if field is not None:
        json_body['field'] = field
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if values is not None:
        json_body['values'] = values
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/times/user_engagement_by_field', json_body=json_body or None)


async def times_user_engagement_by_traffic_origin(end_date: str, player_id: str, query_key: str, start_date: str, values: list[str], timezone: Optional[str] = None) -> Any:
    """Returns an array with the engagement grouped by a field
    
    POST /times/user_engagement_by_traffic_origin
    
    Returns an array containing the overall engagement of the users in a given period for the specified player per day.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (required): The ID of the player to search for
        query_key (required): The query param key to group the engagement by, possible values example: 'utm_campain', 'utm_source', 'utm_medium', 'utm_content', 'utm_term'
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        values (required): The values to filter the query key parameter by, for example ['Facebook', 'Google', 'Campaign 1', 'Campaign 2']
        timezone (optional): The timezone to use for the date filtering
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if player_id is not None:
        json_body['player_id'] = player_id
    if query_key is not None:
        json_body['query_key'] = query_key
    if start_date is not None:
        json_body['start_date'] = start_date
    if values is not None:
        json_body['values'] = values
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/times/user_engagement_by_traffic_origin', json_body=json_body or None)
