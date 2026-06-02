"""Auto-generated VTurb Analytics tools — sessions.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def sessions_live_users(player_id: str, minutes: Optional[int] = None) -> Any:
    """Returns the number of live users for a player
    
    GET /sessions/live_users
    
    Returns the number of live users for a player that entered the website in the last X minutes. Disclaimer, this doesn't mean the user is still on the website, it means the user entered the website in the last X minutes.
    
    Args:
        player_id (required): The ID of the player to search for [Format: uuid]
        minutes (optional): The number of minutes to search for live users, defaults to 60 minutes
        """

    params: dict = {}
    if player_id is not None:
        params['player_id'] = player_id
    if minutes is not None:
        params['minutes'] = minutes
    return await _client.get('/sessions/live_users', params=params or None)


async def sessions_stats(end_date: str, player_id: str, start_date: str, pitch_time: Optional[int] = None, timezone: Optional[str] = None, video_duration: Optional[int] = None) -> Any:
    """Returns statistics of all sessions of a player
    
    POST /sessions/stats
    
    Returns statistics of sessions for a player given a date range
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        pitch_time (optional): The time in seconds that the video must be watched to be considered a pitch, if not provided we will use the pitch time of the video based on our database
        timezone (optional): The timezone to use for the date filtering
        video_duration (optional): The total duration of the video in seconds, if not provided we will use the duration of the video based on our database
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if pitch_time is not None:
        json_body['pitch_time'] = pitch_time
    if timezone is not None:
        json_body['timezone'] = timezone
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    return await _client.post('/sessions/stats', json_body=json_body or None)


async def sessions_stats_by_day(end_date: str, player_id: str, start_date: str, pitch_time: Optional[int] = None, timezone: Optional[str] = None, video_duration: Optional[int] = None) -> Any:
    """Returns statistics of all sessions of a player by day
    
    POST /sessions/stats_by_day
    
    Returns statistics of sessions for a player given a date range by day
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        pitch_time (optional): The time in seconds that the video must be watched to be considered a pitch, if not provided we will use the pitch time of the video based on our database
        timezone (optional): The timezone to use for the date filtering
        video_duration (optional): The total duration of the video in seconds, if not provided we will use the duration of the video based on our database
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if pitch_time is not None:
        json_body['pitch_time'] = pitch_time
    if timezone is not None:
        json_body['timezone'] = timezone
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    return await _client.post('/sessions/stats_by_day', json_body=json_body or None)


async def sessions_stats_by_field(end_date: str, field: str, player_id: str, start_date: str, video_duration: int, pitch_time: Optional[int] = None, timezone: Optional[str] = None) -> Any:
    """Returns statistics grouped by a specified field
    
    POST /sessions/stats_by_field
    
    Returns statistics for sessions grouped by a specified field for a given company and player within a date range.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        field (required): The field to group the statistics by
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        video_duration (required): The total duration of the video in seconds
        pitch_time (optional): The time in seconds that the video must be watched to be considered a pitch
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
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    if pitch_time is not None:
        json_body['pitch_time'] = pitch_time
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/sessions/stats_by_field', json_body=json_body or None)


async def sessions_stats_by_field_by_day(end_date: str, field: str, player_id: str, start_date: str, video_duration: int, pitch_time: Optional[int] = None, timezone: Optional[str] = None) -> Any:
    """Returns statistics grouped by a specified field broke by day
    
    POST /sessions/stats_by_field_by_day
    
    Returns statistics for sessions grouped by a specified field for a given company and player within a date range and broke by day.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        field (required): The field to group the statistics by
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        video_duration (required): The total duration of the video in seconds
        pitch_time (optional): The time in seconds that the video must be watched to be considered a pitch
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
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    if pitch_time is not None:
        json_body['pitch_time'] = pitch_time
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/sessions/stats_by_field_by_day', json_body=json_body or None)
