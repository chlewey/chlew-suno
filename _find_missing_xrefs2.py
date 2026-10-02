import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

DIRS = ['chlewey', 'dvigitt', 'gabisson', 'rataflechera', 'temp', 'wyomee']
NOTES_RE = re.compile(r'\\begin\{notes\}(.*?)\\end\{notes\}', re.DOTALL)
TITLE_RE = re.compile(r'\\songtitle\{(.*?)\}', re.DOTALL)
LABEL_RE = re.compile(r'\\label\{(sec:[a-zA-Z0-9-]+)\}')
PAGEREF_RE = re.compile(r'\\pageref\{(sec:[a-zA-Z0-9-]+)\}')
EMPH_RE = re.compile(r'\\emph\{([^}]+)\}')

ADAPT_WORDS = re.compile(
    r'adapt(ed|ation)|translat(ed|ion)|re-?genre|excerpt|arrangement of|'
    r'version of|rework(s|ed)?|same lyrics|cover of|companion (piece|arrangement)',
    re.IGNORECASE,
)

all_files = [p for d in DIRS for p in sorted(Path(d).glob('*.tex'))]

title_to_file = {}
labels = {}
file_notes = {}

for p in all_files:
    text = p.read_text(encoding='utf-8', errors='replace')
    tm = TITLE_RE.search(text)
    if tm:
        clean = re.sub(r'\\[a-zA-Z]+\{|\}', '', tm.group(1)).strip()
        title_to_file[clean] = str(p)
    for m in LABEL_RE.finditer(text):
        labels.setdefault(m.group(1), str(p))
    nm = NOTES_RE.search(text)
    if nm:
        file_notes[str(p)] = nm.group(1)

def clean_title(t):
    return re.sub(r'\\[a-zA-Z]+\{|\}', '', t).strip()

print('=== Candidates: adaptation/translation notes naming an actual OTHER SONG, no \\pageref present ===\n')
count = 0
for path, notes in sorted(file_notes.items()):
    if not ADAPT_WORDS.search(notes):
        continue
    if PAGEREF_RE.search(notes):
        continue
    raw_titles = EMPH_RE.findall(notes)
    real_song_titles = []
    for rt in raw_titles:
        ct = clean_title(rt)
        if ct in title_to_file and title_to_file[ct] != path:
            real_song_titles.append((ct, title_to_file[ct]))
    if not real_song_titles:
        continue
    count += 1
    print(f'-- {path}')
    for ct, target in real_song_titles:
        has_label = 'HAS \\label' if any(target == f for f in labels.values()) else 'NO \\label yet'
        print(f'   -> "{ct}"  ({target})  [{has_label}]')
    print()

print(f'Total: {count}')
