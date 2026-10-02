import re
import sys
from pathlib import Path
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

DIRS = ['chlewey', 'dvigitt', 'gabisson', 'rataflechera', 'temp', 'wyomee']
TITLE_RE = re.compile(r'\\songtitle\{(.*?)\}', re.DOTALL)

groups = defaultdict(list)
for d in DIRS:
    for p in sorted(Path(d).glob('*.tex')):
        text = p.read_text(encoding='utf-8', errors='replace')
        tm = TITLE_RE.search(text)
        if tm:
            clean = re.sub(r'\\[a-zA-Z]+\{|\}', '', tm.group(1)).strip()
            groups[clean].append(str(p))

for title, files in sorted(groups.items()):
    if len(files) > 1:
        print(f'{title}: {files}')
