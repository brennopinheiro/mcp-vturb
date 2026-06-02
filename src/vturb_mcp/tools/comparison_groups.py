"""Auto-generated VTurb Analytics tools — comparison_groups.

Do not edit by hand. Regenerate via:
    python -m vturb_mcp.generator
"""

from __future__ import annotations

from typing import Any, Optional

from vturb_mcp.client import VturbClient

_client = VturbClient()

async def comparison_groups_list(end_date: Optional[str] = None, start_date: Optional[str] = None, timezone: Optional[str] = None) -> Any:
    """List the AB tests (comparison groups) registered for the authenticated company
    
    POST /comparison_groups/list
    
    Returns every AB test registered for the company, with the players enrolled in each test (including their traffic percentages) and the test start/finish timestamps. Results are ordered by creation date (newest first). Use the optional `start_date`/`end_date` filters to narrow results by the comparison group `created_at`.
    
    Args:
        end_date (optional): Upper bound applied to the comparison group `created_at`. Format `YYYY-MM-DD HH:MM:SS`. Optional — when omitted, no upper bound is applied. [Format: date-time]
        start_date (optional): Lower bound applied to the comparison group `created_at`. Format `YYYY-MM-DD HH:MM:SS`. Optional. [Format: date-time]
        timezone (optional): Timezone used to interpret `start_date`/`end_date`. Defaults to `Etc/UTC`.
        """

    json_body: dict = {}
    if end_date is not None:
        json_body['end_date'] = end_date
    if start_date is not None:
        json_body['start_date'] = start_date
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/comparison_groups/list', json_body=json_body or None)


async def comparison_groups_stats(comparison_group_id: str, items: list[dict], events: Optional[list[str]] = None, timezone: Optional[str] = None) -> Any:
    """Returns the full analytics metrics for up to 2 players of an AB test
    
    POST /comparison_groups/stats
    
    Returns, in a single response, the full set of analytics metrics for up to 2 players of an AB test: views, plays, finishes, clicks, conversions with revenue in USD/BRL/EUR, engagement, pitch audience and pitch retention, as well as the derived play rate, conversion rate and revenue per visitor (RPV). Each item's `start_date` is optional — when omitted, it falls back to the player's own `started_at` (from the comparison group's `players` list) and, if that is not set, to the comparison group's `started_at`. When `end_date` is omitted, results run through the current time.
    
    Args:
        comparison_group_id (required): The AB test (comparison group) id.
        items (required): Up to 2 players to return stats for. Players not enrolled in the AB test are silently ignored.
        events (optional): Event names for the `views`/`plays`/`finishes` aggregates. Defaults to `["started", "viewed", "finished"]`.
        timezone (optional): Timezone used by ClickHouse to interpret every `start_date` / `end_date` string in this request (both caller-provided and the defaults resolved from the comparison group). Defaults to `Etc/UTC`.
        """

    json_body: dict = {}
    if comparison_group_id is not None:
        json_body['comparison_group_id'] = comparison_group_id
    if items is not None:
        json_body['items'] = items
    if events is not None:
        json_body['events'] = events
    if timezone is not None:
        json_body['timezone'] = timezone
    return await _client.post('/comparison_groups/stats', json_body=json_body or None)
