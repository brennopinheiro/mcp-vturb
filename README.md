# vturb-mcp

Local MCP server for the [VTurb Public Analytics API](https://vturb.gitbook.io/analytics-api/pt). Exposes all 28 analytics endpoints (clicks, conversions, events, sessions, traffic origin, AB tests, etc.) through FastMCP with Code Mode.

## Install

```bash
git clone <repo> && cd mcp-vturb
uv venv && uv pip install -e .
```

## Configure

Get an API token at <https://app.vturb.com/settings/analytics-api>, then set:

```bash
export VTURB_API_TOKEN="your-token-here"
```

## Claude Desktop / Claude Cowork

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (Desktop) or `~/.claude.json` (Cowork):

```json
{
  "mcpServers": {
    "vturb": {
      "command": "/absolute/path/to/mcp-vturb/.venv/bin/vturb-mcp",
      "env": { "VTURB_API_TOKEN": "your-token-here" }
    }
  }
}
```

Restart the client.

## Coverage

| Category               | Endpoints                                                                                                    |
| ---------------------- | ------------------------------------------------------------------------------------------------------------ |
| clicks                 | `total_by_company_day`, `total_by_company_timed`                                                             |
| comparison_groups (AB) | `list`, `stats`                                                                                              |
| conversions            | `active_platforms`, `stats_by_day`, `video_timed`                                                            |
| custom_metrics         | `list`                                                                                                       |
| events                 | `leaderboard`, `total_by_company`, `total_by_company_day`, `total_by_company_players`                        |
| headlines              | `stats_by_player`                                                                                            |
| players                | `list` (with name search)                                                                                    |
| quota                  | `usage` (self rate-limit check)                                                                              |
| sessions               | `live_users`, `stats`, `stats_by_day`, `stats_by_field`, `stats_by_field_by_day`                             |
| times                  | `user_engagement`, `user_engagement_by_day`, `user_engagement_by_field`, `user_engagement_by_traffic_origin` |
| traffic_origin         | `stats`, `stats_by_day`, `valid_utms`                                                                        |
| turbo                  | `stats_by_player`                                                                                            |

## Regenerate tools after spec update

```bash
.venv/bin/python -m vturb_mcp.generator
```

## License

MIT
