"""Auto-generated VTurb Analytics tools — traffic_origin.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def traffic_origin_stats(end_date: str, player_id: str, query_key: str, start_date: str, video_duration: int, pitch_time: Optional[int] = None, timezone: Optional[str] = None) -> Any:
    """Returns statistics grouped by a specified field
    
    POST /traffic_origin/stats
    
    Returns statistics for traffic origin grouped by a specified query key for a given company and player within a date range.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (required): The ID of the player to search for
        query_key (required): The query key to group the statistics by
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        video_duration (required): The total duration of the video in seconds
        pitch_time (optional): The time in seconds that the video must be watched to be considered a pitch
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
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    if pitch_time is not None:
        json_body['pitch_time'] = pitch_time
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/traffic_origin/stats', json_body=json_body or None)


async def traffic_origin_stats_by_day(end_date: str, player_id: str, start_date: str, video_duration: int, pitch_time: Optional[int] = None, query_keys: Optional[list[str]] = None, timezone: Optional[str] = None) -> Any:
    """Returns statistics grouped by a specified field and day
    
    POST /traffic_origin/stats_by_day
    
    Returns statistics for traffic origin grouped by a specified query key for a given company and player within a date range and grouped by day.
    
    Args:
        end_date (required): End date of the period for event querying. This will be used as <=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        player_id (required): The ID of the player to search for
        start_date (required): Start date of the period for event querying. This will be used as >=. Format examples "2023-10-26T18:24:05.000+00:00" or "2023-10-26 18:24:05 UTC" or "2023-10-26" [Format: date]
        video_duration (required): The total duration of the video in seconds
        pitch_time (optional): The time in seconds that the video must be watched to be considered a pitch
        query_keys (optional): The query keys to group the statistics by
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
    if pitch_time is not None:
        json_body['pitch_time'] = pitch_time
    if query_keys is not None:
        json_body['query_keys'] = query_keys
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/traffic_origin/stats_by_day', json_body=json_body or None)


async def traffic_origin_valid_utms(player_id: str, start_date: str, end_date: Optional[str] = None) -> Any:
    """Counts the utms of the given player
    
    POST /traffic_origin/valid_utms
    
    Counts the utms of the given player. The values are src, sck, utm_source, utm_medium, utm_campaign, utm_term, utm_content, among any other valid query parameter
    
    Args:
        player_id (required): The player being analysed.
        start_date (required): Start date of the period for event querying. [Format: date]
        end_date (optional): Start date of the period for event querying. [Format: date]
        """

    json_body: dict = {}
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if end_date is not None:
        json_body['end_date'] = end_date
    return await _client.post('/traffic_origin/valid_utms', json_body=json_body or None)
