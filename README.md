# VTurb Analytics — Claude Desktop Extension

Conecta o Claude direto na sua conta VTurb. Em uma conversa, pergunta tipo:

> "Me dá os números de hoje do player X."

E o Claude busca views, plays, conversões, receita, traffic origin — tudo da API oficial da VTurb. Inclui um **dashboard visual** (`player_overview`) que renderiza KPIs e gráficos dentro da própria conversa.

---

## Instalação (Mac & Windows) — 3 passos

### 1. Baixe o arquivo `.mcpb`

[**⬇️ vturb-analytics-0.1.0.mcpb**](https://github.com/brennopinheiro/mcp-vturb/releases/latest)

### 2. Pegue seu API token da VTurb

Acesse <https://app.vturb.com/settings/analytics-api> → clique em **"Generate New API Key"** → copia o token.

### 3. Instale no Claude Desktop

1. Abra o **Claude Desktop**
2. Vá em **Settings → Extensions** (ou **Configurações → Extensões**)
3. Clique em **"Install Extension…"** e selecione o arquivo `.mcpb` que você baixou
4. Cola seu API token quando ele pedir
5. Pronto. Já pode usar.

Não precisa instalar Python, terminal, nada. O Claude Desktop cuida do resto.

---

## O que dá pra fazer

Exemplos de perguntas que funcionam direto:

- _"Me lista todos os meus players da VTurb."_
- _"Pega as conversões do player 64a5c8072e6fd10009828db2 entre 01/05 e 31/05."_
- _"Mostra o dashboard do player X dos últimos 7 dias."_ → renderiza painel visual
- _"Qual a taxa de play e conversão da semana passada por origem de tráfego?"_
- _"Tenho um AB test rodando — compara os 2 players."_
- _"Quanto da minha quota da API eu já usei nesse minuto?"_

### Cobertura — todos os 28 endpoints da API

| Categoria                        | Endpoints                                                 |
| -------------------------------- | --------------------------------------------------------- |
| **clicks**                       | total por dia · por tempo de vídeo                        |
| **comparison_groups** (AB tests) | listar · stats de até 2 players                           |
| **conversions**                  | plataformas ativas · stats por dia · por segundo do vídeo |
| **custom_metrics**               | listar                                                    |
| **events**                       | leaderboard · total por empresa / dia / player            |
| **headlines**                    | stats por player                                          |
| **players**                      | listar (com busca por nome)                               |
| **quota**                        | uso atual                                                 |
| **sessions**                     | live users · stats · por dia · por campo · campo×dia      |
| **times**                        | engajamento · por dia · campo · origem de tráfego         |
| **traffic_origin**               | stats · por dia · UTMs válidas                            |
| **turbo**                        | stats por player                                          |

Plus: dashboard visual `player_overview` aggregando o mais importante num painel só.

---

## Segurança

- **100% local**: o servidor roda no seu computador, não em servidor remoto. Seu token nunca passa por nenhum lugar exceto direto pra `analytics.vturb.net`.
- **Token criptografado**: o Claude Desktop guarda no keychain do sistema operacional (mesmo lugar onde o macOS guarda suas senhas).
- **Open source**: todo o código tá nesse repo, audite à vontade.

## Suporte

- API VTurb fora do ar / token não funciona → [help.vturb.com](https://help.vturb.com)
- Bug nessa extensão → [abra uma issue](https://github.com/brennopinheiro/mcp-vturb/issues)

---

## Para desenvolvedores

Build do zero (precisa de `uv` e `node`):

```bash
git clone https://github.com/brennopinheiro/mcp-vturb
cd mcp-vturb
uv venv && uv pip install -e .

# Regenera as tools a partir do OpenAPI
.venv/bin/python -m vturb_mcp.generator

# Smoke test live
VTURB_API_TOKEN=seu-token .venv/bin/python scripts/smoke_test.py

# Empacota um novo .mcpb
npm install -g @anthropic-ai/mcpb
mcpb pack . dist/vturb-analytics-0.1.0.mcpb
```

Arquitetura: OpenAPI 3.0.2 consolidado em `specs/vturb-openapi.json` → `generator.py` gera 12 módulos de tools → FastMCP + Code Mode expõe via 3 meta-tools + dashboard Prefab. Detalhes em [`CLAUDE.md`](CLAUDE.md).

## License

MIT
