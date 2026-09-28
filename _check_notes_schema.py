import re
from pathlib import Path

dirs = ['chlewey', 'dvigitt', 'gabisson', 'rataflechera', 'temp', 'wyomee']
missing = []
for d in dirs:
    for p in sorted(Path(d).glob('*.tex')):
        text = p.read_text(encoding='utf-8', errors='replace')
        if '\\begin{notes}' not in text:
            missing.append(str(p).replace('\\', '/'))

print(len(missing), 'files without \\begin{notes}')
for m in missing:
    print(m)
