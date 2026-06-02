# mcp-vturb — Project Instructions

MCP server local para a **VTurb Public Analytics API** (`https://analytics.vturb.net`).

Uso: Claude Desktop + Claude Cowork. Tipo: app interno (server-side API key, sem OAuth).

## Stack

- Python 3.10+ · `uv` para venv/install
- FastMCP 3.x com Code Mode (3 meta-tools: `search` / `get_schema` / `execute`)
- `httpx` async client
- 28 tools auto-geradas a partir de `specs/vturb-openapi.json`

## API alvo

- **Base URL**: `https://analytics.vturb.net`
- **Auth**: 2 headers obrigatórios — `X-Api-Token: <token>` + `X-Api-Version: v1`
- **Token**: gerar em `app.vturb.com/settings/analytics-api`
- **Env var**: `VTURB_API_TOKEN`
- **Rate limits**: 60/120/300/800 rpm conforme plano. Self-check via `GET /quota/usage`

## Estrutura

```
mcp-vturb/
├── specs/vturb-openapi.json     # OpenAPI 3.0.2 consolidado (fonte da verdade)
├── src/vturb_mcp/
│   ├── client.py                # httpx async, 2 headers, retry 429
│   ├── generator.py             # OpenAPI → tools/*.py
│   ├── server.py                # FastMCP + CodeMode
│   └── tools/                   # auto-gerados, 1 módulo por categoria
├── scripts/smoke_test.py        # 1 chamada read-only (quota/usage)
└── pyproject.toml
```

## Comandos

```bash
# Setup
uv venv && uv pip install -e .

# Regenerar tools após mudança no spec
.venv/bin/python -m vturb_mcp.generator

# Smoke test
VTURB_API_TOKEN=... .venv/bin/python scripts/smoke_test.py

# Rodar server (Claude Desktop config)
.venv/bin/vturb-mcp
```

## Convenções

- Generator é determinístico: rodar de novo deve produzir output idêntico
- Nunca editar `tools/*.py` à mão — sempre via generator
- `specs/vturb-openapi.json` é vendored: atualizar via fetch do gitbook se a API mudar
- Manter `pydantic-monty==0.0.7` pinned (0.0.8 quebra CodeMode)

## Não comitar

- `.env`, `VTURB_API_TOKEN`
- `.venv/`, `__pycache__/`, `*.egg-info/`
