# Writing rules — merged reference

Shared rulebook for the `write-clean`, `deslop`, and `polish-voice` skills. It merges two sources:

- **ASD-STE100** (Simplified Technical English) — clarity, short sentences, controlled grammar.
  ASD-STE100 is copyright ASD. Request a copy from ASD: https://www.asd-ste100.org/
- **no-ai-slop** by Peter Yang (https://github.com/petergyang/no-ai-slop) — cutting AI-tell words
  and patterns.

Each skill says which parts apply and how hard. Read the mode section in the skill, then apply the
relevant rules below. Never change facts, numbers, model names, quotes, or code.

---

## A. Banned words and phrases (cut or replace)

Cut these outright (from no-ai-slop). Replace with a plain word or nothing.

- delve, foster, leverage, utilize, facilitate, empower, streamline, robust, harness, elevate,
  embark, supercharge, ever-evolving, transformative, seamless, powerful, unlock, boasts
- cutting-edge, paradigm shift, game changer, "this is huge", "this changes everything"
- tapestry, realm, beacon, multifaceted, meticulous, intricate, paramount, testament

Often-empty adverbs — cut unless they carry real emphasis, uncertainty, or contrast:

- just, literally, honestly, simply, actually, truly, fundamentally, importantly, crucially,
  inherently, inevitably

Often-empty openers/phrases — cut the throat-clearing:

- "it's worth noting", "it's important to note", "at the end of the day", "when it comes to",
  "at its core", "in today's world", "in the age of", "the reality is", "the truth is",
  "in terms of", "with regard to", "in order to", "going forward", "in this article",
  "let's dive in"

## B. Sentence and structure patterns to remove (no-ai-slop)

- **Binary contrast:** cut "It's not X. It's Y." State Y directly.
- **Throat-clearing openers:** delete "Here's the thing", "Let me be clear", "I'll be honest",
  "The uncomfortable truth is".
- **Faux-insight setups:** delete "What nobody tells you", "The part everyone misses",
  "This is what most people skip".
- **Colon reveals:** rewrite "noun: lowercase reveal" as a plain sentence.
- **Superficial -ing tails:** cut trailing clauses that fake analysis ("highlighting",
  "underscoring", "reflecting", "showcasing"). Replace with a real "so/because" cause, or delete.
- **Importance puffery:** delete "stands as testament", "marks a pivotal moment",
  "plays a vital role", "solidifies its position". State the fact; let the reader judge.
- **Weasel attribution:** name the source or cut it. No "experts agree", "reports suggest",
  "widely regarded as".
- **Fake-strong verbs:** prefer plain "is"/"has" over "serves as", "acts as a hub for".
- **Negative listing:** don't write "Not X. Not Y. Z." Just state Z.
- **Dramatic fragmentation:** avoid "X. And Y. And Z." and "That's it. That's the whole thing."
- **Rhetorical setups:** remove "What if I told you", "Think about it", "Plot twist", and
  self-answered question pairs.
- **Fake-profound kickers:** no final "deep" aphorism. End on a concrete fact.
- **Summary-recap endings:** cut "In conclusion", "Ultimately", "Overall", and restated paragraphs.

## C. Clarity and grammar (ASD-STE100)

- Keep instruction/procedure sentences to about 20 words. Keep descriptive sentences to about 25.
- Put one idea in each sentence. One instruction per sentence in steps.
- Use the active voice.
- Use simple tenses: present, past, future, and the imperative.
- Avoid the "-ing" form (gerund/participle), except in a technical name. (Relax this in personal
  prose — see the polish-voice mode.)
- Use short, common words. Use one word for one meaning.
- Use the same term for the same thing. Do not rotate synonyms for variety.
- Keep the articles ("a", "an", "the"). Do not drop words to look shorter.
- Write in the positive form when you can.
- Put the topic first, then the detail.
- No slang, idioms, or jargon in technical text.

## D. Punctuation

- Prefer the period. Use simple punctuation.
- Em dash "—": use 1–2 at most in a long draft. Remove clusters and decorative use. It is not a
  default rhythm tool. In strict technical text, use none.
- Colons: for lists, labels, or quotes. Not for dramatic reveals. Use sentence case after a colon.
- Do not join two independent clauses with a semicolon or a dash. Use two sentences.
- Hyphen only in a name or a standard term.

## E. Voice and tone (protect the human — matters most for polish-voice)

- Protect the writer's vocabulary, cadence, bluntness, humor, uncertainty, and digressions.
- Keep "I think" and "maybe" when they show real hesitation or natural rhythm.
- Keep useful edge, strong opinions, and self-interruptions.
- Make the minimum effective edit. Leave strong human sentences alone.

## F. Formatting

- No emoji in headings.
- No mid-sentence bold for emphasis.
- Use prose where prose reads better than a list.
- Do not put a header over a two-sentence section.
- Format follows content, not decoration.

## G. Global cautions

- Do not change facts, numbers, model names, code, or quotes.
- Vary sentence length a little, so the text does not read like a machine.

## H. Optional approved-word dictionary

The full ASD-STE100 approved-word list is copyright ASD and is not shipped with these skills. You
can request a copy from ASD (free, subject to ASD's terms): https://www.asd-ste100.org/ — then build
a local lookup with the `ste-dict` tool (see its README).

- Look for `ste-dictionary.json` in the user's ste-dict install (by default
  `~/.claude/ste-dict/ste-dictionary.json`).
- **If it exists:** load it. Use `replace` to swap any not-approved word for its approved
  alternative (keys are lowercase source words; values are approved alternatives). Treat words in
  `approved` as the safe vocabulary. Apply this on top of Sections A–F.
- **If it is absent:** skip this step. Use Sections A–F only. Do not guess the approved list.
- That file is a derivative of the copyrighted dictionary. Never copy its contents into any output
  that gets published, committed, or shared — use it only to guide word choice.
