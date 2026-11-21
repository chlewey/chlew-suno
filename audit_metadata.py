"""Audit song notes and tags without changing source files."""
import argparse
import json
import re
from collections import Counter
from pathlib import Path

from extract_notes import DEFAULT_DIRS, extract_notes


def audit(path):
    text = path.read_text(encoding='utf-8-sig')
    # Ignore LaTeX comments, retaining escaped percent signs.
    text = re.sub(r'(?<!\\)%[^\n]*', '', text)
    tags = re.findall(r'\\tag(\*?)(?:\[[^\]]*\])?\{([^{}]*)\}', text)
    notes = extract_notes(text)
    issues = []
    if not notes or not any(n.strip() for n in notes):
        issues.append('missing or empty notes')
    if len(notes) > 1:
        issues.append('multiple notes blocks')
    if not any(not star for star, tag in tags):
        issues.append('no indexed tags')
    years = [tag for star, tag in tags if star and re.fullmatch(r'\d{4}', tag)]
    if not years:
        issues.append('missing composition year (verify before adding)')
    if len(years) > 1:
        issues.append('multiple composition years (review)')
    counts = Counter(tag for star, tag in tags)
    for tag, count in counts.items():
        if count > 1:
            issues.append(f'duplicate tag: {tag}')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', tag):
            issues.append(f'noncanonical tag: {tag}')
    return {'file': path.as_posix(), 'tags': [t for s, t in tags], 'issues': issues}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('dirs', nargs='*', default=DEFAULT_DIRS)
    parser.add_argument('-o', '--output', default='metadata_audit.json')
    args = parser.parse_args()
    paths = sorted({p for d in args.dirs for p in Path(d).glob('*.tex')})
    entries = [audit(p) for p in paths if '\\songtitle{' in p.read_text(encoding='utf-8-sig')]
    report = {'songs': len(entries), 'songs_needing_review': sum(bool(e['issues']) for e in entries),
              'tag_vocabulary': dict(sorted(Counter(t for e in entries for t in set(e['tags'])).items())),
              'entries': entries}
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"{report['songs']} songs; {report['songs_needing_review']} need review. Wrote {args.output}")


if __name__ == '__main__':
    main()
