# ASD-STE100 dictionary (optional local aid)

The `write-clean`, `deslop`, and `polish-voice` skills can use the official ASD-STE100 dictionary to
flag not-approved words and suggest the approved alternative. That dictionary is **not** included
here, and you must not add it.

## Why the dictionary is not in this repo

ASD-STE100 (Simplified Technical English) is copyright ASD (Aerospace, Security and Defence
Industries Association of Europe). The standard states that no reproduction or publication of it,
in whole or in part, may be made without written authority from an officer of ASD. ASD grants free
reproduction/publication rights only to specific groups (ASD/AIA/AIAC/ICCAIA members and their
customers, Ministries of Defence, A4A, airworthiness authorities, and universities/research
institutes for educational purposes).

So this repo ships **only the mechanism**, never ASD's content:

- The writing rules used by the skills are described in our own words (methods and ideas are not
  copyrightable — only ASD's specific text is).
- The dictionary itself, and any lookup file extracted from it, stay on your machine and are
  git-ignored. A file extracted from the dictionary is a derivative work, so it is treated the same.

## Request a copy of the standard

Request ASD-STE100 from ASD (free, subject to ASD's terms): https://www.asd-ste100.org/

## Build your local lookup

1. Get the standard from ASD: https://www.asd-ste100.org/
2. Install this folder as `~/.claude/ste-dict` (symlink or copy).
3. Build the lookup next to this file:
   ```
   pip install pypdf
   python extract_ste_dict.py "path/to/ASD-STE100_ISSUE9.pdf" -o ste-dictionary.json
   ```
4. `ste-dictionary.json` is written here and is git-ignored. Do not commit it.

The skills look for `~/.claude/ste-dict/ste-dictionary.json`. If it is present, they use it for
exact approved-word and alternative lookups. If it is absent, they fall back to the general rules in
each skill's `reference/writing-rules.md` and still work.

## Trademark

"ASD-STE100" and "Simplified Technical English" are trademarks of ASD. These skills are an
independent tool that implements the STE method. They are not affiliated with, endorsed by, or
sponsored by ASD.
