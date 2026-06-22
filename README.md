# Claude skills

My authored [Claude Code](https://claude.com/claude-code) / Agent skills.

Each subfolder is one skill (a `SKILL.md` plus any `scripts/` and `reference/`).

## Skills

| Skill | What it does |
|-------|--------------|
| [`plan-flights`](plan-flights/) | Plan, verify, and rank flight options into a visual HTML report (verdict + per-origin sections + rankings), single-ticket fares only. |

## Install

Symlink (or copy) a skill folder into your skills directory:

```bash
# Linux / macOS
ln -s "$(pwd)/plan-flights" ~/.claude/skills/plan-flights
```

```powershell
# Windows (Developer Mode or admin)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\plan-flights" -Target "$(Resolve-Path .\plan-flights)"
```

Claude Code picks the skill up on next launch.
