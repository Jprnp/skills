#!/usr/bin/env python3
"""
extract_ste_dict.py — build a LOCAL ASD-STE100 lookup from your own copy of the PDF.

WHY THIS EXISTS
    ASD-STE100 (Simplified Technical English) is copyright ASD. Its dictionary may NOT be
    republished. This script contains NO ASD content — it only reads a PDF that YOU obtained
    from ASD and writes a lookup file on YOUR machine. That output file is a derivative of the
    copyrighted dictionary, so it must stay local. It is git-ignored on purpose. Do not commit it.

USAGE
    pip install pypdf
    python extract_ste_dict.py "C:/path/to/ASD-STE100_ISSUE9.pdf" -o ste-dictionary.json

OUTPUT (ste-dictionary.json, LOCAL ONLY)
    {
      "meta":     {... , "derivative_of_copyrighted_source": true, "do_not_publish": true},
      "approved": ["A", "BE", ...],                 # approved STE words (UPPERCASE headwords)
      "replace":  {"already": ["IN PROGRESS"], ...} # not-approved word -> approved alternative(s)
    }
"""
import argparse
import json
import re
import sys

POS = r"(?:art|v|n|adj|adv|prep|conj|pron|det|aux|num)"
# A headword row: "word (pos)" possibly followed by "ALTERNATIVE (pos)" in the meaning column.
HEADWORD = re.compile(rf"^\s*([A-Za-z][A-Za-z\-']*)\s*\(\s*{POS}\s*\)", re.M)
ALT_TOKEN = re.compile(rf"([A-Z][A-Z\-'\s]*?)\s*\(\s*{POS}\s*\)")


def extract(pdf_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("Missing dependency. Run: pip install pypdf")

    reader = PdfReader(pdf_path)
    approved = set()
    replace = {}

    for page in reader.pages:
        text = page.extract_text() or ""
        if "Part 2" not in text and "Dictionary" not in text:
            continue
        for line in text.splitlines():
            m = HEADWORD.match(line)
            if not m:
                continue
            word = m.group(1)
            rest = line[m.end():]
            if word.isupper():
                approved.add(word)
                continue
            # lowercase headword => not approved; look for an UPPERCASE alternative on the row
            alts = [a.strip() for a in ALT_TOKEN.findall(rest)]
            alts = [a for a in alts if a and a.upper() == a]
            if alts:
                replace.setdefault(word.lower(), [])
                for a in alts:
                    if a not in replace[word.lower()]:
                        replace[word.lower()].append(a)

    return sorted(approved), replace


def main():
    ap = argparse.ArgumentParser(description="Build a local ASD-STE100 lookup from your own PDF.")
    ap.add_argument("pdf", help="path to your ASD-STE100 PDF")
    ap.add_argument("-o", "--out", default="ste-dictionary.json", help="output JSON (local only)")
    args = ap.parse_args()

    approved, replace = extract(args.pdf)
    data = {
        "meta": {
            "source": "ASD-STE100 (user-supplied PDF)",
            "derivative_of_copyrighted_source": True,
            "do_not_publish": True,
            "note": "Local aid only. ASD-STE100 is copyright ASD; do not commit or redistribute this file.",
            "approved_count": len(approved),
            "replace_count": len(replace),
        },
        "approved": approved,
        "replace": replace,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}: {len(approved)} approved words, {len(replace)} replacement entries.")
    print("REMINDER: this output is git-ignored on purpose. Do not commit or publish it.")


if __name__ == "__main__":
    main()
