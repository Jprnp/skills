# Tools setup

## Browser (REQUIRED — single-ticket verification)
The skill needs to read Kayak result pages to tell single-ticket fares from
self-transfer. Use one of:
- **claude-in-chrome MCP** (Chrome extension). Load tools in one ToolSearch call:
  `select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__tabs_create_mcp`
  Call `tabs_context_mcp` once (createIfEmpty:true) before other browser tools.
- **agent-browser skill** (CLI), as an alternative driver.

If neither is available: tell the user the single-ticket guarantee cannot be met,
hand them the manual Kayak steps (the report's "how to book" list), and either stop
or proceed only with an explicit "unverified — check each fare yourself" warning.

## docker-mcp google-flights (OPTIONAL — fast first scan)
Provides `get_flights_on_date` / `find_all_flights_in_range` (one-way data,
local currency). It does NOT expose the single-ticket flag and its round-trip
tool errors, so it can only narrow the search — never quote it as final.

Enable (Docker Desktop must be running):
```bash
# claude.exe may not be on PATH; on this machine it is at ~/.local/bin/claude.exe
claude mcp add -s user docker-mcp -- docker mcp gateway run --profile personal
setx MCP_TIMEOUT 30000   # first health-check is slow (cold catalog load); avoids "Failed to connect"
```
Add the `google-flights` server to the Docker MCP Toolkit profile, then restart
Claude Code and check `/mcp`. Load tools when needed:
`select:mcp__docker-mcp__get_flights_on_date,mcp__docker-mcp__find_all_flights_in_range`

If absent, skip it entirely — Kayak browsing in the main flow covers all data.

## Kayak URL patterns (deterministic — preferred over Google's text search)
- Round-trip: `https://www.kayak.com.br/flights/{ORIG}-{DEST}/{OUT}/{RET}?sort=bestflight_a`
- Open-jaw:   `https://www.kayak.com.br/flights/{ORIG}-{DEST}/{OUT}/{DEST}-{HOME}/{RET}?sort=bestflight_a`
- `&fs=stops=-2` caps stops at ≤1 (Kayak rewrites to `stops=0,1`).
- Dates are `YYYY-MM-DD`. Use the local Kayak domain that matches the user's currency.
- Self-transfer markers to EXCLUDE: "Conexão por conta própria", "KAYAK Mix",
  "Bilhetes separados", "Escala independente", or two unrelated airlines sold separately.
