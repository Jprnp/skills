---
name: write-clean
description: Write NEW text from scratch that is clear, plain, and free of AI-slop, following ASD-STE100 and no-ai-slop rules. Use when the user asks you to write, draft, or compose something original (a post, comment, email, README section, announcement) and wants it to sound human and direct, not AI-generated. Triggers include "write this for me cleanly", "draft X in plain English", "write from scratch, no AI slop", "compose a clean version of...". For rewriting EXISTING text, use `deslop` (LLM text) or `polish-voice` (the user's own text) instead.
---

# Write clean (from zero)

Produce new text that reads like a careful human wrote it. Do not draft in a generic AI style and
then clean up. Write it tight from the first draft.

## Steps

1. Read the shared rulebook: `reference/writing-rules.md` (in this skill folder).
2. Confirm the goal, audience, and length. If the user gave a topic but no constraints, pick a
   sensible length and say so in one line before the text.
3. Write the text. Apply ALL sections of the rulebook fully:
   - Sections A/B: never use the banned words, openers, or slop patterns.
   - Section C/D: short sentences, active voice, simple tenses, plain punctuation.
   - Section F: clean formatting, no decoration.
   - Section H: if the local ASD-STE100 dictionary exists, prefer approved words and approved
     alternatives. If it is absent, use Sections A–F only.
4. Read it back once. Cut any sentence that does not carry a fact.

## Output

- Return only the finished text, ready to paste.
- If you made a length or scope assumption, put it in one short line above the text.
