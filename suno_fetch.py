import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
SONG_ID_RE = re.compile(r'/song/([0-9a-f-]{36})')
CLIP_API_URL = 'https://studio-api.prod.suno.com/api/clip/{song_id}'


class SunoFetchError(Exception):
    pass


def _get(url, method='GET'):
    request = urllib.request.Request(url, headers={'User-Agent': USER_AGENT}, method=method)
    try:
        return urllib.request.urlopen(request, timeout=15)
    except urllib.error.HTTPError as exc:
        raise SunoFetchError(f'{method} {url} failed: HTTP {exc.code}') from exc
    except urllib.error.URLError as exc:
        raise SunoFetchError(f'{method} {url} failed: {exc.reason}') from exc


def extract_song_id(url):
    """Resolve any suno.com song URL (short /s/<code> link, /song/<uuid>,
    or /song/<uuid>?sh=<code>) to its bare clip id."""
    match = SONG_ID_RE.search(url)
    if match:
        return match.group(1)

    with _get(url, method='HEAD') as response:
        final_url = response.geturl()
    match = SONG_ID_RE.search(final_url)
    if not match:
        raise SunoFetchError(f'Could not resolve a song id from URL: {url}')
    return match.group(1)


def fetch_suno_song(url):
    """Fetch title, style, lyrics, and other metadata for a Suno song.

    Accepts any suno.com song URL: a short link (https://suno.com/s/<code>),
    a canonical link (https://suno.com/song/<uuid>), or the share-link form
    (https://suno.com/song/<uuid>?sh=<code>). Returns a dict.
    """
    song_id = extract_song_id(url)

    with _get(CLIP_API_URL.format(song_id=song_id)) as response:
        data = json.load(response)

    metadata = data.get('metadata') or {}
    model_badges = metadata.get('model_badges') or {}
    songrow_badge = model_badges.get('songrow') or {}

    created_at_raw = data.get('created_at')
    created_at = None
    if created_at_raw:
        created_at = datetime.fromisoformat(created_at_raw.replace('Z', '+00:00'))

    return {
        'id': song_id,
        'title': data.get('title'),
        'creator_display_name': data.get('display_name'),
        'creator_handle': data.get('handle'),
        'style': metadata.get('tags'),
        'lyrics': metadata.get('prompt'),
        'genre_tags': data.get('display_tags'),
        'model_version': data.get('major_model_version'),
        'model_display_name': songrow_badge.get('display_name'),
        'duration_seconds': metadata.get('duration'),
        'play_count': data.get('play_count'),
        'created_at': created_at,
        'is_public': data.get('is_public'),
        'source_url': f'https://suno.com/song/{song_id}',
    }


def format_summary(song):
    created = song['created_at']
    created_str = created.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M UTC') if created else 'unknown'
    lines = [
        f"Title:    {song['title']}",
        f"Creator:  {song['creator_display_name']} (@{song['creator_handle']})",
        f"Model:    {song['model_display_name'] or song['model_version']}",
        f"Created:  {created_str}",
        f"Plays:    {song['play_count']}",
        f"Duration: {song['duration_seconds']:.0f}s" if song['duration_seconds'] else 'Duration: unknown',
        f"URL:      {song['source_url']}",
        '',
        'Style:',
        song['style'] or '(none)',
        '',
        'Lyrics:',
        song['lyrics'] or '(none)',
    ]
    return '\n'.join(lines)


def build_parser():
    parser = argparse.ArgumentParser(
        description='Fetch title, style, lyrics, and metadata for one or more Suno songs.'
    )
    parser.add_argument('urls', nargs='+', help='Suno song URLs (short or canonical).')
    parser.add_argument('-j', '--json', action='store_true', help='Print raw JSON instead of a summary.')
    return parser


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    args = build_parser().parse_args()
    exit_code = 0
    for i, url in enumerate(args.urls):
        if i:
            print()
        try:
            song = fetch_suno_song(url)
        except SunoFetchError as exc:
            print(f'Error fetching {url}: {exc}', file=sys.stderr)
            exit_code = 1
            continue
        if args.json:
            song = dict(song)
            song['created_at'] = song['created_at'].isoformat() if song['created_at'] else None
            print(json.dumps(song, ensure_ascii=False, indent=2))
        else:
            print(format_summary(song))
    sys.exit(exit_code)
