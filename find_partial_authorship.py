#!/usr/bin/env python3
"""Scan song notes for phrasing suggesting Carlos Thompson wrote SOME but not
all of a song's stanzas (partial/co-authorship), excluding songs that are
plainly full-AI lyrics (notes starting with "Lyrics by <LLM>").

Usage:
    python find_partial_authorship.py [dir ...]
"""
import re
import sys
from pathlib import Path

NOTES_RE = re.compile(r'\\begin\{notes\}(.*?)\\end\{notes\}', re.DOTALL)
DEFAULT_DIRS = ['chlewey', 'dvigitt', 'gabisson', 'rataflechera', 'temp', 'wyomee']

# A note starting with this is a plain declaration of full AI authorship,
# not partial/co-authorship -- exclude regardless of other wording.
FULL_AI_RE = re.compile(r'^(Lyrics|Written)\s+by\s+(Suno|Claude|ChatGPT|Gemini|Grok|GPT-?\d*)\b', re.IGNORECASE)

# Signals that some but not all stanzas/lines were Carlos's own writing.
PARTIAL_SIGNALS = [
    r'\bco-?writ',
    r'\baddition[s]?\s+by\b',
    r'\badding to\b',
    r'\b(intro|verse|chorus|bridge|outro|pre-chorus)[s]?\W+(?:,\W*(?:intro|verse|chorus|bridge|outro|pre-chorus)[s]?\W+)*and\W+(?:intro|verse|chorus|bridge|outro|pre-chorus)[s]?.{0,40}\bby\b',
    r'\bwritten by Carlos Thompson and\b',
    r'\bpart(?:ly|ially)\b',
    r'\bsome (?:lines|stanzas|verses)\b',
    r'\bfixed (?:for|the) rhythm',
    r'\brestyled\b',
    r'\bexpanded (?:by|on)\b',
]
PARTIAL_RE = re.compile('|'.join(PARTIAL_SIGNALS), re.IGNORECASE)


def extract_notes(text):
    return [m.group(1).strip() for m in NOTES_RE.finditer(text)]


def main():
    dirs = sys.argv[1:] or DEFAULT_DIRS
    hits = []
    for d in dirs:
        root = Path(d)
        if not root.is_dir():
            continue
        for path in sorted(root.glob('*.tex')):
            text = path.read_text(encoding='utf-8', errors='replace')
            for notes in extract_notes(text):
                if FULL_AI_RE.match(notes):
                    continue
                if PARTIAL_RE.search(notes):
                    hits.append((str(path).replace('\\', '/'), notes))

    print(f'{len(hits)} candidate(s)\n')
    for path, notes in hits:
        print(f'## {path}\n{notes}\n')


if __name__ == '__main__':
    main()
