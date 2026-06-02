"""Auto-generated VTurb Analytics tools — headlines.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def headlines_stats_by_player(player_id: str, start_date: str, video_duration: int, end_date: Optional[str] = None, pitch_time: Optional[int] = None) -> Any:
    """Statistics used by the headlines dashboard
    
    POST /headlines/stats_by_player
    
    Returns several statistics used by the headlines dashboard. Engagement, views and play rate are among these metrics
    
    Args:
        player_id (required): The player being analysed.
        start_date (required): Start date of the period for event querying. [Format: date]
        video_duration (required): The duration of the video
        end_date (optional): End date of the period for event querying. Optional — when omitted, the response is unbounded at the upper end. When provided, inclusive at the end of the minute (e.g. `23:59:59` captures the full minute). [Format: date]
        pitch_time (optional): The time in seconds that the video must be watched to be considered a pitch
        """

    json_body: dict = {}
    if player_id is not None:
        json_body['player_id'] = player_id
    if start_date is not None:
        json_body['start_date'] = start_date
    if video_duration is not None:
        json_body['video_duration'] = video_duration
    if end_date is not None:
        json_body['end_date'] = end_date
    if pitch_time is not None:
        json_body['pitch_time'] = pitch_time
    return await _client.post('/headlines/stats_by_player', json_body=json_body or None)
