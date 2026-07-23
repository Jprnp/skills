---
name: polish-voice
description: Rewrite the USER'S OWN text to sound more professional and concise while keeping their personal voice. Use when the user wrote something themselves and wants it tightened, not replaced — fix clunky phrasing, cut filler, raise the register a little, but preserve their vocabulary, cadence, bluntness, and opinions. Make the minimum effective edit. Triggers include "polish my writing", "tighten this that I wrote", "make my text more professional but keep my voice", "clean up my draft without making it sound like AI". For AI-generated text use `deslop`; to write something new use `write-clean`.
---

# Polish (rewrite my own text, keep my voice)

The input is the user's own writing. The job is to make it more professional and concise WITHOUT
turning it into generic prose. Voice preservation wins over strict rules.

## Priority order

1. **Keep the author's voice** (rulebook Section E). Protect their words, rhythm, humor, edge,
   hesitations, and strong opinions. Make the minimum effective edit. Leave strong sentences alone.
2. **Cut filler and raise the register** (Section A): remove empty adverbs, throat-clearing openers,
   and any AI-slop patterns (Section B) that sneaked in.
3. **Tighten for concision** (Section C/D): shorten long sentences, active voice, plain punctuation,
   fewer em-dashes. But do NOT enforce the hard STE limits mechanically — the strict 20-word cap and
   the no-"-ing" rule are relaxed here when they would flatten the author's voice.

## What NOT to do

- Do not rewrite every sentence. If a sentence is already clear and human, keep it.
- Do not remove personality, informal asides, or a deliberate strong word.
- Do not raise the register so far that it stops sounding like the author.

## Steps

1. Read the shared rulebook: `reference/writing-rules.md` (in this skill folder), focus on Section E.
2. Read the input and note the author's voice markers (tone, favorite words, bluntness).
3. Edit line by line. Prefer small fixes over rewrites.
4. Keep every fact, number, name, and quote.

## Output

- Return only the polished text.
- If "more professional" and "your voice" pulled in different directions somewhere, add one short
  line below the text. Otherwise return the text alone.
