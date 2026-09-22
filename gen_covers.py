#!/usr/bin/env python3
"""Generate album cover images from the *-cover-proposals.md docs using the
Gemini API (Nano Banana / Nano Banana 2 image models).

Credentials: reads GEMINI_API_KEY from the environment, or from a .env file
in the project root (KEY=value, git-ignored). Get a key at
https://aistudio.google.com/apikey -- the key is never printed or logged.

Usage:
    python gen_covers.py                          # all three proposal docs
    python gen_covers.py --songbook stories        # just one songbook
    python gen_covers.py --stub drift              # just one album (substring match)
    python gen_covers.py --dry-run                 # list what would be generated
    python gen_covers.py --force                   # regenerate existing covers too
"""

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

PROPOSAL_DOCS = {
    'stories': ROOT / 'covers' / 'stories' / 'stories-cover-proposals.md',
    'ricochets': ROOT / 'covers' / 'ricochets' / 'ricochets-cover-proposals.md',
    'entourage-eco': ROOT / 'covers' / 'entourage-eco' / 'entourage-eco-cover-proposals.md',
    'original': ROOT / 'covers' / 'original' / 'original-cover-proposals.md',
    'electronica': ROOT / 'covers' / 'electronica' / 'electronica-cover-proposals.md',
    'rockola': ROOT / 'covers' / 'rockola' / 'rockola-cover-proposals.md',
    'pop': ROOT / 'covers' / 'pop' / 'pop-cover-proposals.md',
    'generos': ROOT / 'covers' / 'generos' / 'generos-cover-proposals.md',
    'personal': ROOT / 'covers' / 'personal' / 'personal-cover-proposals.md',
}

API_URL_TEMPLATE = 'https://generativelanguage.googleapis.com/v1/models/{model}:generateContent'
DEFAULT_MODEL = 'gemini-2.5-flash-image'

SECTION_RE = re.compile(
    r'^## (?P<album>.+?)\n\n`(?P<stub>[^`]+)`\n\n(?P<prompt>.+?)(?=\n#{1,2} |\Z)',
    re.DOTALL | re.MULTILINE,
)

MIME_EXT = {
    'image/png': '.png',
    'image/jpeg': '.jpg',
    'image/webp': '.webp',
}


class GenError(Exception):
    pass


def load_api_key():
    key = os.environ.get('GEMINI_API_KEY')
    if key:
        return key.strip()

    env_file = ROOT / '.env'
    if env_file.exists():
        for line in env_file.read_text(encoding='utf-8').splitlines():
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            name, _, value = line.partition('=')
            if name.strip() == 'GEMINI_API_KEY':
                value = value.strip()
                if value:
                    return value

    raise GenError(
        'No GEMINI_API_KEY found. Set it as an environment variable, or create '
        'a .env file (copy .env.example) with GEMINI_API_KEY=... in it.'
    )


def parse_proposals(doc_path):
    """Yield (album, stub, prompt) tuples from one *-cover-proposals.md file."""
    text = doc_path.read_text(encoding='utf-8')
    for match in SECTION_RE.finditer(text):
        album = match.group('album').strip()
        stub = match.group('stub').strip()
        prompt = match.group('prompt').strip()
        yield album, stub, prompt


def existing_cover(stub):
    """Return the existing cover path for a stub if a .png/.jpg/.jpeg exists."""
    for ext in ('.png', '.jpg', '.jpeg'):
        candidate = ROOT / (stub + ext)
        if candidate.exists():
            return candidate
    return None


def generate_image(api_key, prompt, model):
    url = API_URL_TEMPLATE.format(model=model)
    body = json.dumps({
        'contents': [{'parts': [{'text': prompt}]}],
    }).encode('utf-8')

    request = urllib.request.Request(
        url,
        data=body,
        method='POST',
        headers={
            'x-goog-api-key': api_key,
            'Content-Type': 'application/json',
        },
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode('utf-8', errors='replace')
        raise GenError(f'HTTP {exc.code} from Gemini API: {detail[:500]}') from exc
    except urllib.error.URLError as exc:
        raise GenError(f'Request failed: {exc.reason}') from exc

    try:
        parts = payload['candidates'][0]['content']['parts']
    except (KeyError, IndexError) as exc:
        raise GenError(f'Unexpected response shape: {json.dumps(payload)[:500]}') from exc

    for part in parts:
        inline = part.get('inlineData')
        if inline and inline.get('data'):
            mime_type = inline.get('mimeType', 'image/png')
            ext = MIME_EXT.get(mime_type, '.png')
            return base64.b64decode(inline['data']), ext

    raise GenError(f'No image data in response: {json.dumps(payload)[:500]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--songbook', choices=sorted(PROPOSAL_DOCS), help='Only process one songbook (default: all).')
    parser.add_argument('--stub', help='Only process albums whose stub contains this substring.')
    parser.add_argument('--model', default=DEFAULT_MODEL, help=f'Gemini image model (default: {DEFAULT_MODEL}).')
    parser.add_argument('--sleep', type=float, default=6.0, help='Seconds to wait between API calls (default: 6).')
    parser.add_argument('--force', action='store_true', help='Regenerate covers that already exist.')
    parser.add_argument('--dry-run', action='store_true', help='List what would be generated, call no API.')
    args = parser.parse_args()

    docs = [PROPOSAL_DOCS[args.songbook]] if args.songbook else list(PROPOSAL_DOCS.values())

    jobs = []
    for doc_path in docs:
        if not doc_path.exists():
            print(f'skip (not found): {doc_path}', file=sys.stderr)
            continue
        for album, stub, prompt in parse_proposals(doc_path):
            if args.stub and args.stub not in stub:
                continue
            jobs.append((doc_path.parent.name, album, stub, prompt))

    if not jobs:
        print('No matching albums found.', file=sys.stderr)
        return 1

    api_key = None
    if not args.dry_run:
        try:
            api_key = load_api_key()
        except GenError as exc:
            print(f'error: {exc}', file=sys.stderr)
            return 1

    total = len(jobs)
    for i, (songbook, album, stub, prompt) in enumerate(jobs, 1):
        prefix = f'[{i}/{total}] {songbook}: {album} ({stub})'

        existing = existing_cover(stub)
        if existing and not args.force:
            print(f'{prefix} -- skip, exists at {existing.relative_to(ROOT)}')
            continue

        if args.dry_run:
            print(f'{prefix} -- would generate ({len(prompt)} char prompt)')
            continue

        print(f'{prefix} -- generating...', end=' ', flush=True)
        try:
            image_bytes, ext = generate_image(api_key, prompt, args.model)
        except GenError as exc:
            print(f'FAILED: {exc}')
            continue

        out_path = ROOT / (stub + ext)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(image_bytes)
        print(f'saved {out_path.relative_to(ROOT)} ({len(image_bytes)} bytes)')

        if i < total:
            time.sleep(args.sleep)

    return 0


if __name__ == '__main__':
    sys.exit(main())
