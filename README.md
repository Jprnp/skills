# Claude skills

My authored [Claude Code](https://claude.com/claude-code) / Agent skills.

Each subfolder is one skill (a `SKILL.md` plus any `scripts/` and `reference/`).

## Skills

| Skill | What it does |
|-------|--------------|
| [`plan-flights`](plan-flights/) | Plan, verify, and rank flight options into a visual HTML report (verdict + per-origin sections + rankings), single-ticket fares only. |
| [`write-clean`](write-clean/) | Write NEW text from scratch — clear, plain, no AI slop (ASD-STE100 + no-ai-slop). |
| [`deslop`](deslop/) | Rewrite LLM-generated text to strip AI slop and make it human. Rewrites freely. |
| [`polish-voice`](polish-voice/) | Rewrite your OWN text to be more professional and concise while keeping your voice. Minimum edits. |

### Writing skills — shared notes

`write-clean`, `deslop`, and `polish-voice` share one rulebook (bundled as
`reference/writing-rules.md` inside each). It merges [ASD-STE100](https://www.asd-ste100.org/)
(Simplified Technical English) with [no-ai-slop](https://github.com/petergyang/no-ai-slop) by
Peter Yang.

They can also use the official ASD-STE100 dictionary for exact approved-word checks. That dictionary
is copyright ASD and is **not** shipped here. Request a copy from ASD
(https://www.asd-ste100.org/) and build a local lookup with the [`ste-dict`](ste-dict/) tool. The
generated lookup and any STE PDF are git-ignored on purpose — do not commit them.

## Install

Symlink (or copy) a skill folder into your skills directory. Replace `<skill>` with the folder name
(`plan-flights`, `write-clean`, `deslop`, `polish-voice`):

```bash
# Linux / macOS
ln -s "$(pwd)/<skill>" ~/.claude/skills/<skill>
```

```powershell
# Windows (Developer Mode or admin)
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills\<skill>" -Target "$(Resolve-Path .\<skill>)"
```

Claude Code picks the skill up on next launch.

For exact ASD-STE100 word-checks, also install the `ste-dict` tool at `~/.claude/ste-dict` and build
your local lookup — see [`ste-dict/README.md`](ste-dict/README.md).
