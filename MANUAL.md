# Manual: `desong.py` and `suno_fetch.py`

Two command-line tools used to get new songs from Suno into this songbook project.

- **`suno_fetch.py`** pulls a song's title, style, lyrics, and metadata straight from
  Suno's public API, given any `suno.com` song URL.
- **`desong.py`** splits a staging file (a `.tex` file containing one or more
  `\songtitle{...}` blocks, such as `temp.tex` or `temp2.tex`) into individual
  per-song `.tex` files under per-author directories (`chlewey/`, `rataflechera/`,
  `wyomee/`, `gabisson/`, `dvigitt/`, `temp/`, ...).

The normal workflow is: fetch with `suno_fetch.py` → hand-write a staging entry
(title, tags, notes, style, lyrics) into `temp.tex`/`temp2.tex` → run `desong.py`
to split it into its own file → `\input` it from the relevant songbook(s).

---

## `suno_fetch.py`

### What it does

Suno song pages are a JS-rendered SPA, so a plain page fetch only returns the
HTML shell. Instead of scraping the rendered page, `suno_fetch.py` calls Suno's
own public metadata endpoint directly:

```
https://studio-api.prod.suno.com/api/clip/<song-id>
```

No login or API key is required. Short share links (`https://suno.com/s/<code>`)
are resolved to their canonical song id with one lightweight `HEAD` request
that follows the redirect; canonical/share links
(`https://suno.com/song/<uuid>` or `.../song/<uuid>?sh=<code>`) skip that step.

### Command-line usage

```bash
python suno_fetch.py <url> [<url> ...] [-j | --json]
```

- One or more Suno song URLs (short or canonical, any mix).
- Without `-j`/`--json`: prints a human-readable summary (title, creator, model,
  created date, play count, duration, URL, style, lyrics).
- With `-j`/`--json`: prints the same data as JSON (one object per URL, in order).

Examples:

```bash
# Human-readable summary
python suno_fetch.py "https://suno.com/s/5IyBdLePtrqcuBq0"

# JSON, redirected to a file for archiving
python suno_fetch.py "https://suno.com/s/5IyBdLePtrqcuBq0" --json > .json/mouth_of_the_machine.json

# Several songs in one call
python suno_fetch.py "https://suno.com/s/AAA" "https://suno.com/s/BBB" --json
```

If a URL can't be resolved or the API call fails, the tool prints an error for
that URL to stderr and continues with the rest; the process exits non-zero if
any URL failed.

### Fields returned

Each song is a dict (or, in JSON mode, an object) with:

| Field                  | Meaning                                                             |
|-------------------------|----------------------------------------------------------------------|
| `id`                    | Suno's internal song UUID                                           |
| `title`                  | Song title                                                          |
| `creator_display_name`   | Display name shown on Suno (e.g. `"Wyomee Dank"`)                    |
| `creator_handle`         | Account handle (e.g. `"wyomee"`) — see the author-folder mapping below |
| `style`                  | Full style/prompt text (goes in `\begin{style}...\end{style}`)       |
| `lyrics`                 | Full lyrics with `[Section]` markers (goes in `\begin{lyrics}...\end{lyrics}`) |
| `genre_tags`             | Suno's own short comma-separated genre label, if any (informational only) |
| `model_version`          | e.g. `"v6"`                                                          |
| `model_display_name`     | e.g. `"V6"` or `"V6-MINI"`                                            |
| `duration_seconds`       | Track length in seconds                                              |
| `play_count`             | Play count at fetch time                                            |
| `created_at`             | `datetime` (CLI JSON mode: ISO-8601 string) of when the song was generated |
| `is_public`              | Whether the song is publicly listed on Suno                          |
| `source_url`             | Canonical `https://suno.com/song/<uuid>` URL                         |

### Using it as a library

```python
from suno_fetch import fetch_suno_song

song = fetch_suno_song("https://suno.com/s/5IyBdLePtrqcuBq0")
print(song["title"], song["creator_handle"])
```

### Author-folder mapping

`creator_handle` identifies which Suno account made the song, which in turn
decides the `%! dir=` directive to use when staging it:

| Suno account (display name) | handle          | `dir=`          |
|------------------------------|-----------------|-----------------|
| Carlos Th                    | `chlewey`       | `chlewey`       |
| Gabriel                      | `gabisson`      | `gabisson`      |
| rataflechera                 | `rataflechera`  | `rataflechera`  |
| Wyomee Dank                  | `wyomee`        | `wyomee`        |
| Dvigitt                      | `dvigitt`       | `dvigitt`       |

(Older pre-2026 pieces without a clear per-account owner, such as the 2010
Enwigh Peady acrostics, use `dir=temp` instead — match whatever directory its
existing siblings already use.)

### What it does *not* do

It only fetches metadata — it does not decide tags, write notes, detect
duplicate/re-genre songs, or touch `temp.tex`/`temp2.tex`. Staging a fetched
song still means writing (or asking for) a `\songtitle`/`\tag`/`\begin{notes}`
block by hand, since tagging is a judgment call (genre, narrative-universe
tags, character tags, `original-lyrics` vs. `original-source` vs. an
adaptation cross-reference, etc.) that the metadata alone doesn't settle.

---

## `desong.py`

### What it does

Given a staging file containing one or more `\songtitle{...}` blocks, it
writes each song out to its own `.tex` file in the right author directory, and
replaces the staging file's content with the corresponding `\input{...}` lines
(so the staging file can be `\input` directly, or its lines copied into a
songbook chapter).

### Directives

Inside the staging file, `%!` comment lines control where songs land:

- `%! dir=<path>` — set the target directory for subsequent songs.
  - `; scope=keep` (default) — stays in effect until changed again.
  - `; scope=next` — applies to the *next* song only, then reverts to
    whatever directory was in effect before.
- `%! regex-fix=true` — anywhere in the file, enables automatic lyric cleanup
  (see below) for every song in that run.

Example staging file:

```latex
%! dir=chlewey
%! regex-fix=true

\songtitle{Some Song}
\tag*{2026}\tag{synth-pop}
...
\begin{lyrics}
...
\end{lyrics}

%! dir=rataflechera; scope=next

\songtitle{A Different Author's Song}
...
```

Here, "Some Song" is written under `chlewey/`, and only "A Different Author's
Song" goes under `rataflechera/` — the directory then reverts to `chlewey`
for anything after it.

### Regex fix

When enabled (`-r`/`--regex-fix` on the command line, or `%! regex-fix=true`
in the file), each song body is transformed before being written out:

- `[Verse 1]`, `[Chorus]`, `[Pre-Chorus]`, `[Bridge]`, `[Breakdown]`, `[Intro]`,
  `[Outro]`, etc. become `\songpart{...}`.
- Any other `[...]` bracketed cue becomes `\annotation{...}`.
- Line breaks inside a stanza get `\\` inserted automatically.

This is exactly the format `suno_fetch.py`'s raw `lyrics` field is in (Suno
uses the same `[Section]` bracket convention), so a fetched song's lyrics can
be pasted into the staging file mostly as-is and cleaned up automatically by
`desong.py` — **do not hand-edit `\songpart`/`\annotation`/`\\` formatting
yourself; that's this flag's job.**

### Filename slugs

Each song's filename is derived from its title via `maketag()`: lowercased,
punctuation stripped, accented characters transliterated (á→a, ñ→n, ø→oe,
etc.), spaces become underscores. If the resulting filename already exists,
`desong.py` automatically appends `_1`, `_2`, ... rather than overwriting —
so staging two songs with the same title (e.g. a re-genre sharing its
original's exact title) is safe.

### Command-line usage

```bash
python desong.py [input] [output] [-d DIR] [-m] [-b [EXT]] [-r]
```

- `input` — staging file to read. Omit to read from stdin.
- `output` — where to write the resulting `\input{...}` lines. Omit to print
  to stdout.
- `-d DIR`, `--dir DIR` — default target directory (used when the file has no
  `%! dir=` directive yet). If omitted, defaults to the input filename without
  its extension (e.g. `temp2.tex` → default directory `temp2`) — so a
  `%! dir=` directive at the top of the staging file is effectively required.
- `-m`, `--modify` — write the `\input{...}` lines back into the input file
  itself (in place of the split-out song bodies), instead of printing them.
  Requires an input file; incompatible with specifying `output`.
- `-b [EXT]`, `--backup [EXT]` — back up the input file before modifying it
  (only meaningful with `-m`), as `<input>.<EXT>` (default extension `bak`).
- `-r`, `--regex-fix` — force regex-fix cleanup even if the file has no
  `%! regex-fix=true` directive.

### Typical usage in this project

```bash
python desong.py temp2.tex -m -b
```

This splits every song currently staged in `temp2.tex` into its own file
under the directories named by its `%! dir=` directives, backs up the
original as `temp2.tex.bak` first, and rewrites `temp2.tex` in place to
contain just the resulting `\input{...}` lines — ready to copy into the
relevant songbook chapter(s), or to leave as a running log of what's been
promoted out of staging.

**This tool is run by the project owner, not by an assistant editing the
staging file.** An assistant staging new songs should only ever add
`\songtitle`/`\tag`/`\begin{notes}`/`\begin{style}`/`\begin{lyrics}` blocks
(plus `%!` directives) to `temp.tex`/`temp2.tex` — never invent or
pre-populate the individual per-author output files `desong.py` would create,
and never overwrite a per-author file that already exists from a previous run.
