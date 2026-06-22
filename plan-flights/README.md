# plan-flights

A [Claude Code](https://claude.com/claude-code) skill that turns a flight request
into a ranked, visual **HTML report** backed by *verified single-ticket fares*.

## What it's for

Given a trip's constraints (origins, destination, date windows, budget, time-of-day
prefs, fixed appointments), the skill:

- gathers and restates the inputs (asks for anything missing — currency is required),
- optionally scans candidate dates fast for cheap prices/stops,
- **verifies real fares in the browser on Kayak**, keeping only single-ticket
  itineraries (self-transfer / "Mix" / separate-ticket fares are excluded — a missed
  connection there is the traveler's loss),
- generates an HTML report with a verdict, one section per origin, and three rankings
  each (Balanced, Value-first, Duration-first) with Kayak deep-links.

**Core rule:** single-ticket only. Because the data API can't tell single-ticket from
self-transfer, fares must be confirmed in the browser — so a browser is required.

## How to use

Just ask Claude in natural language; the skill auto-triggers. Examples:

- "plan flights from GYN and BSB to Austin in March, weekends only, under $1200"
- "compare airfare to Lisbon, cheapest, max 1 stop"
- "/plan-flights"

Claude will ask for any missing input, browse Kayak to verify fares, then build and
open the report. Output HTML is written under `C:\devhome\`.

To generate the report manually from a spec:

```bash
python "%USERPROFILE%\.claude\skills\plan-flights\scripts\gen_flights.py" spec.json out.html
```

Spec schema: see [`scripts/example.json`](scripts/example.json). Don't hand-edit the
HTML — edit the JSON and rerun.

## Required tools

| Tool | Status | Purpose |
|------|--------|---------|
| **Browser** — `claude-in-chrome` MCP *or* the `agent-browser` skill | **Required** | Read Kayak result pages to confirm single-ticket fares. Without it the no-risk guarantee can't be met. |
| **Python 3** | **Required** | Runs `scripts/gen_flights.py` to build the HTML report. |
| **docker-mcp `google-flights`** | Optional | Fast first scan of prices/durations across dates. Narrows search only — never quoted as final (no single-ticket flag). Skip if absent. |

Setup details (enabling the browser MCP and docker-mcp, Kayak URL patterns):
see [`reference/tools-setup.md`](reference/tools-setup.md).

## Files

- `SKILL.md` — the skill instructions Claude follows.
- `scripts/gen_flights.py` — JSON → HTML report generator.
- `scripts/example.json` — full spec schema example to copy and adapt.
- `reference/tools-setup.md` — installing/enabling the browser + docker-mcp tools.
