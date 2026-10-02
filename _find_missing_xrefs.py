import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

DIRS = ['chlewey', 'dvigitt', 'gabisson', 'rataflechera', 'temp', 'wyomee']
NOTES_RE = re.compile(r'\\begin\{notes\}(.*?)\\end\{notes\}', re.DOTALL)
LABEL_RE = re.compile(r'\\label\{(sec:[a-zA-Z0-9-]+)\}')
PAGEREF_RE = re.compile(r'\\pageref\{(sec:[a-zA-Z0-9-]+)\}')
EMPH_RE = re.compile(r'\\emph\{([^}]+)\}')

ADAPT_WORDS = re.compile(
    r'adapt(ed|ation)|translat(ed|ion)|re-?genre|excerpt|arrangement of|'
    r'version of|rework(s|ed)?|based on \\emph|same lyrics|cover of|companion',
    re.IGNORECASE,
)

all_files = []
for d in DIRS:
    for p in sorted(Path(d).glob('*.tex')):
        all_files.append(p)

labels = {}      # slug -> file
pagerefs = {}     # slug -> [files using it]
file_notes = {}   # file -> notes text

for p in all_files:
    text = p.read_text(encoding='utf-8', errors='replace')
    for m in LABEL_RE.finditer(text):
        labels.setdefault(m.group(1), str(p))
    for m in PAGEREF_RE.finditer(text):
        pagerefs.setdefault(m.group(1), []).append(str(p))
    nm = NOTES_RE.search(text)
    if nm:
        file_notes[str(p)] = nm.group(1)

print('=== 1) \\pageref used but no matching \\label anywhere in the project ===')
for slug, users in sorted(pagerefs.items()):
    if slug not in labels:
        print(f'{slug}  (missing label; used by {", ".join(users)})')

print()
print('=== 2) Notes that smell like an adaptation/translation but use plain \\emph{} with no \\pageref nearby ===')
for path, notes in sorted(file_notes.items()):
    if not ADAPT_WORDS.search(notes):
        continue
    if PAGEREF_RE.search(notes):
        continue  # already uses the proper format somewhere in these notes
    embedded_titles = EMPH_RE.findall(notes)
    if not embedded_titles:
        continue
    print(f'-- {path}')
    print(f'   titles mentioned: {embedded_titles}')
    print(f'   notes: {notes.strip()[:220]}')
    print()
