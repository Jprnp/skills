---
name: plan-flights
description: >-
  Plan, verify, and rank flight options into a visual HTML report (verdict +
  per-origin sections + 3 rankings each), using single-ticket fares only.
  Use when the user wants to find/compare/rank flights, build a trip flight
  plan, search airfares under constraints (dates, budget, weekends, time of
  day, fixed appointments), or compare departure/arrival airports. Triggers:
  "plan flights", "find flights", "compare airfare", "flight options to X",
  "/plan-flights", "rank flights", "cheapest flights from X to Y".
---

# Plan Flights

Turn a flight request into a ranked, visual HTML report backed by **verified
single-ticket fares**.

## Core rule (never relax)
**Single-ticket only.** Only recommend itineraries sold as one ticket / one
airline contract. Self-transfer ("Escala independente", "Bilhetes separados",
"Conexão por conta própria", Kayak "Mix") is excluded — a missed connection on
those is the traveler's loss. Because the data API cannot tell single-ticket
from self-transfer, **fares must be confirmed in the browser on Kayak**.

## 1. Gather inputs (ask for whatever is missing)
Ask concise questions (use AskUserQuestion when several at once) for anything not given:
- **Origin(s)** and **destination** (airport codes or cities).
- **Dates / flexibility**: outbound window, return window, min/max stay.
- **Time-of-day** prefs (e.g. night departures), and any **fixed commitments**
  (appointments, "back by Monday") that block certain days/times.
- **Workday rule**: must travel days be weekends? (compute weekdays — don't guess).
- **Currency** (required — **ask if not provided**; do not assume). Drives both the
  price display and which Kayak domain is queried (see step 5). Also capture **budget**.
- **Passengers**, **cabin class** (default 1 adult, economy).
- Convert relative dates to absolute; restate assumptions back.

**Alternate airports:** if the user gives only one origin/destination, **ask
whether to auto-scout nearby alternates** (e.g. a bigger hub 1–3h away that may
have fewer stops / lower fares). Do not auto-scout silently. If yes, include
those as extra sections + a door-to-door verdict (see step 5).

## 2. Check tools
- **Browser (REQUIRED):** `claude-in-chrome` MCP, or the `agent-browser` skill.
  Load the chrome tools with one ToolSearch call (tabs_context_mcp, navigate,
  get_page_text, computer, tabs_create_mcp). **If no browser is available**, tell
  the user you cannot verify single-ticket fares and therefore cannot honor the
  no-risk rule; give them the manual Kayak steps from step 6 and stop, or proceed
  only with an explicit "unverified" warning on every fare.
- **docker-mcp `google-flights` (OPTIONAL accelerator):** if present, use it for a
  fast first scan of prices/durations across candidate dates. If absent, skip it —
  Kayak browsing covers everything. To set it up, see `reference/tools-setup.md`.

## 3. (Optional) Quick scan with docker-mcp
If available, load `mcp__docker-mcp__get_flights_on_date` and probe candidate
dates per origin to find which dates/times are cheap and how many stops exist.
Use `return_cheapest_only:true` to keep output small. This only narrows the
search — it does NOT establish single-ticket; never quote these as final.
(Its round-trip tool tends to error; one-way calls are reliable. Prices already
come in the user's local currency.)

## 4. Compute the allowed date set
From the constraints, list the concrete candidate outbound and return dates
(e.g. only weekends, after a blocking appointment). Verify each date's weekday
with a tiny script — never assume.

## 5. Verify single-ticket fares on Kayak (the heart of the skill)
Kayak is **international** — pick the **domain by the user's currency** so prices come
out right (set `book_domain`/`currency_code` in the JSON; the generator maps them):
`USD→www.kayak.com`, `BRL→www.kayak.com.br`, `EUR→www.kayak.es` (or `.pt`),
`GBP→www.kayak.co.uk`, `CAD→www.kayak.ca`, `AUD→www.kayak.com.au`. When unsure, use
`www.kayak.com` and confirm the price currency on the page.

**Coverage fallback:** if Kayak is blocked or thin for a market (some domestic
routes, China, etc.), switch to **Google Flights** or the dominant **local OTA**
(Despegar/Decolar in Latin America, Trip.com in China, MakeMyTrip in India) — same
rule: keep only single-ticket fares, exclude self-transfer. Tell the user which
source you used.

For each (origin, outbound date, return date) — and open-jaw pairs if relevant —
navigate a deterministic Kayak URL and read results:
- Round-trip: `https://{DOMAIN}/flights/{ORIG}-{DEST}/{YYYY-MM-DD}/{YYYY-MM-DD}?sort=bestflight_a`
- Open-jaw:   `https://{DOMAIN}/flights/{ORIG}-{DEST}/{OUT}/{DEST}-{HOME}/{RET}?sort=bestflight_a`
- Add `&fs=stops=-2` to cap at ≤1 stop (note: Kayak rewrites it to `stops=0,1`).

Steps: navigate → `wait` ~7–9s (results stream in; re-read if "Buscando preços"
/ "% concluído") → `get_page_text`. From the text, collect rows that are **single
ticket**: skip any tagged **"Conexão por conta própria"** or **"KAYAK Mix"** or
showing multiple unrelated airlines sold separately. For each kept row record:
price, operating airline(s), stops + via-airports per leg, each leg duration,
departure time, and flag long layovers / tight (<1h) connections / Basic Economy.

Keep it bounded: a handful of date combos per origin is enough — don't fall into
an endless browse. If a search is flaky after 2–3 tries, stop and tell the user.

## 6. Build the report
Assemble a JSON spec (schema = `scripts/example.json`) and run:
```
python "%USERPROFILE%\.claude\skills\plan-flights\scripts\gen_flights.py" spec.json out.html
```
Write output under `%USERPROFILE%\Documents\` unless the user indicates another
location. The generator produces, per the JSON:
- header + constraint/legend/verified boxes,
- an optional **Verdict** section (door-to-door, see below),
- one **section per origin** (and an **open-jaw** section if used), each with the
  **three rankings**: Balanced, Value-first, Duration-first (price + stops +
  longest-leg, just different weights), top 6 each,
- Kayak deep-link buttons, airlines per leg, longest-single-leg duration (bold) +
  round-trip total, orange flag for legs ≥ ~21h, and a "how to book" list.

Open it (`Start-Process out.html` on Windows) and summarize the winner per ranking.

**Characters/encoding (important):** write all JSON text as **plain UTF-8**
(acentos, →, ✓, etc.) — **never HTML entities** like `&aacute;` or `&rarr;`.
The generator HTML-escapes plain-text fields (`title`, `subtitle` is raw but
others aren't: section `name`, verdict `heading`/`columns`, `out_label`,
`ret_label`, and each leg's `air`/`route`/`lab`), so entities there get
double-escaped and render literally as `&aacute;` on the page. Raw-HTML fields
(`boxes[].html`, section `note`, verdict `rows`/`conclusion_html`, `how_steps`)
accept `<b>` etc., and plain UTF-8 works everywhere — so just use real
characters in every field.

**Per-date fields:** when a report mixes outbound dates (relaxed windows),
set `out_date` + `out_label` on each combo (falls back to section, then spec) —
the Kayak deep link and the date shown in the row follow the combo's own dates.

**Flexible-date sweep:** to scan a window efficiently, Kayak accepts
`{YYYY-MM-DD}-flexible-3days` in place of each date (±3 max). The results page
then includes a date×date price matrix and each result row is labeled with its
dates — two overlapping ±3 grids cover a ±5 window in 2 page loads per origin.
Rows read this way are real single-ticket fares (same skip rules apply).

### Door-to-door Verdict (when alternate airports are in play)
If a cheaper/faster alternate origin needs a ground hop (bus/short flight) to
reach, add a Verdict section that loads the **ground leg's cost + counts it as +1
stop + adds its time** (and any pre-flight overnight). Often this erases a hub's
headline saving versus flying direct from the user's home city — surface that
honestly, as in the GYN/BSB example.

## 7. Wrap up
- State the single best pick and the trade-offs (price vs stops vs hours-in-air).
- Note visa/transit requirements for connection countries.
- Offer to save a `project` memory with the trip's constraints + chosen flight.
- Remind: prices/seats move daily; suggest a Kayak/Google price alert.

## Files
- `scripts/gen_flights.py` — JSON → HTML generator (don't hand-edit HTML; edit JSON + rerun).
- `scripts/example.json` — full schema example (today's trip). Copy and adapt.
- `reference/tools-setup.md` — how to install/enable docker-mcp google-flights + browser.
