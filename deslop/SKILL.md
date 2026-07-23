---
name: deslop
description: Rewrite LLM-GENERATED text to remove AI slop and make it clear and human, following no-ai-slop and ASD-STE100 rules. Use when the text was produced by an AI (ChatGPT, Claude, Gemini, etc.) and needs a heavy cleanup — banned words, throat-clearing, binary contrasts, em-dash clusters, fake-profound endings. Because no human voice needs protecting, rewrite freely. Triggers include "deslop this", "remove the AI slop", "this was written by an LLM, clean it up", "de-AI this", "make this ChatGPT text sound human". For the user's OWN writing, use `polish-voice` instead (it preserves their voice).
---

# Deslop (rewrite LLM output)

The input is AI-generated. There is no personal voice to protect, so rewrite as much as needed for
a clear, plain, human result.

## Steps

1. Read the shared rulebook: `reference/writing-rules.md` (in this skill folder).
2. Read the input. Keep every fact, number, name, and claim. Change only the wording.
3. Apply the rulebook hard:
   - Section A: delete every banned word and empty adverb/opener.
   - Section B: remove every slop pattern (binary contrasts, faux-insight, colon reveals,
     -ing tails, puffery, fake-profound kickers, recap endings).
   - Section C/D: enforce short sentences, active voice, simple tenses, plain punctuation,
     em-dashes down to 0–2.
   - Section F: strip decorative formatting.
   - Section H: if the local ASD-STE100 dictionary exists, swap not-approved words for their
     approved alternatives. If it is absent, skip this and use Sections A–F only.
4. Rebuild sentences that were built around a slop pattern. Do not just delete the trigger word.
5. Read it back. Vary sentence length so it does not sound mechanical (Section G).

## Output

- Return only the rewritten text.
- If any claim looked false or unverifiable, do not fix it silently — list it in one line below the
  text so the user can check it.
