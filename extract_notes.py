#!/usr/bin/env python3
"""Extract \\begin{notes}...\\end{notes} blocks from song .tex files into one
searchable document, one heading per file.

Usage:
    python extract_notes.py [dir ...] [-o OUTPUT]

With no directories given, scans the project's known per-song folders
(chlewey, dvigitt, gabisson, rataflechera, temp, wyomee).
"""
import argparse
import re
from pathlib import Path

NOTES_RE = re.compile(r'\\begin\{notes\}(.*?)\\end\{notes\}', re.DOTALL)

DEFAULT_DIRS = ['chlewey', 'dvigitt', 'gabisson', 'rataflechera', 'temp', 'wyomee']


def extract_notes(text):
    return [m.group(1).strip() for m in NOTES_RE.finditer(text)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dirs', nargs='*', default=DEFAULT_DIRS,
                         help='Directories to scan for .tex files (default: known song folders)')
    parser.add_argument('-o', '--output', default='notes_index.md',
                         help='Output file path (default: notes_index.md)')
    args = parser.parse_args()

    entries = []
    for d in args.dirs:
        root = Path(d)
        if not root.is_dir():
            continue
        for path in sorted(root.glob('*.tex')):
            text = path.read_text(encoding='utf-8')
            for notes in extract_notes(text):
                entries.append((str(path).replace('\\', '/'), notes))

    with open(args.output, 'w', encoding='utf-8') as out:
        for path, notes in entries:
            out.write(f'## {path}\n\n{notes}\n\n')

    print(f'Wrote {len(entries)} notes entries to {args.output}')


if __name__ == '__main__':
    main()
