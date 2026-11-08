# CLAUDE.md — project memory for the Suno songbooks

Versioned memory for Claude Code sessions in this repository. It records how the
project works, the conventions agreed with the owner, and what is still open.
It is a snapshot of 2026-11-06: the `.tex` files are authoritative whenever they
disagree with this file. Keep it updated (and committed) when conventions change.

## What this is

A collection of LaTeX songbooks for songs produced with Suno from lyrics by Carlos
Eŭgenĭo Thompson Pinzón ("Chlewey"), written by him, by AI collaborators (Suno,
Claude, ChatGPT, Gemini, Grok, DeepSeek) or both. Credits and sources matter and are
recorded per song.

- Each song is one `.tex` file under an author directory: `chlewey/`, `rataflechera/`,
  `wyomee/`, `gabisson/`, `dvigitt/` (one per Suno account) and `temp/`.
- Each songbook is a top-level `.tex` file (memoir class, landscape A4) that `\input`s
  songs into `\part` → `\chapter` ("Album") groups. The same song may appear in several
  songbooks.
- Build: LuaLaTeX through latexmk (`.latexmkrc`), `make <book>` or `build.ps1`.
  Targets: chlewrics electronica pop rockola generos americana internal stories
  entourage ricochets original personal bable. The `.idx/.ind` files are shared:
  never `make -j`. The cloud container has no LaTeX engine, so Claude cannot build;
  say so and ask the owner to run `make` instead of claiming a layout was checked.
- `MANUAL.md` documents `suno_fetch.py` and `desong.py`; read it before touching the
  import workflow.

### Songbooks

| File | Organizing principle |
|---|---|
| `stories.tex` | Fiction, alternate histories, portraits, self/family, thematic albums |
| `internal.tex` | Internal and non-fiction: chronicle, soul, faith and argument, places, craft |
| `personal.tex` | Strictly personal/self songs (Biographical I/II, Soul and craves, The self) |
| `original.tex` | Original lyrics only, first appearance of each song (no re-genres/adaptations) |
| `entourage-eco.tex` | The *Thomas' Entourage* universe: characters, stories, arcs |
| `ricochets.tex` | The *Ricochets* novel |
| `generos.tex`, `pop.tex`, `rockola.tex`, `electronica.tex` | Genre songbooks |

Regenerate a part/chapter outline with a short script that scans
`\part{}`/`\chapter{}`/`\input{}` (do not trust old outlines, albums move often).
Current shape of the restructured books (names only, no counts):

- **stories**: Named Fictional Works · Early Life · Encounters Universe · Portraits ·
  Self (*Life progression*, *Life arcs*) · Thematic Cycles (Summery, Death Sea and
  hospitality, Ilva and Khamid, Fatherhood) · Thematic Albums (Cats, Fleeting intimacy and
  power dynamics, Waiting nostalgia and melancholy, Pursuit surveillance and betrayal,
  Children's songs and small creatures, Uncomplicated life) · Form and Craft.
- **internal**: Personal Chronicle · Soul and Turmoil · Faith and Argument (Pray,
  Brother I/II, *Essays*, *Dilemmas and arguments*) · Places · Social Commentary ·
  Nation and Ritual · Form and Craft (Meta, Acrostics, Instrumental I Tropical groove /
  II Other colors, Fragments, Adaptations I re-genres / II adapted lyrics / III
  cross-language). The old catch-all "More" no longer exists.
- **personal**: Biographical I (20th century) / II (21st century, plus whole-life songs),
  Soul and craves, The self, Extra stuff.
- **rockola**: Entourage albums (Gabi's Industrial, Thomas albums, Crew Cabin & Flight,
  Operatic Portals = single-character spotlights, Ensembles & Offices, …), Ricochets,
  Other narrative, Essays, Lyrical (incl. *Life Stories in Rock*).
- **entourage-eco**: Characters, one "Character profile: X" chapter per main character
  (Xumi has her own), story arcs, extras.

## Song file format

```
\songtitle{Title}
\tag*{2026}\tag{genre}\tag{original-lyrics}...\label{sec:slug}   % label only when other notes \pageref it
\begin{notes} ... \end{notes}
\begin{style} Suno style prompt, verbatim \end{style}
\begin{lyrics} \songpart{Verse 1} lines ending in \\ ... \end{lyrics}
```

### Tags

- The starred tag `\tag*{YYYY}` is the year of the *lyrics' origin*, not of the render:
  a re-genre or adaptation keeps the source year (Siento 1996, A Someone or a Someone
  2023). `\tag*` also marks language tags such as `\tag*{english-lyrics}` in some files.
- Authorship: `original-lyrics` (written by Carlos Thompson, even if LLMs helped the
  process), `original-source` (Suno/LLM lyrics based on a text of his), `partial-lyrics`
  (stanzas split between him and an AI), `social-media-seed`, `ai-based`, `ai-portrait`,
  `autobiographical`. Do not guess: if the source or lyricist is unknown write
  `% TODO: lyricist unverified (...)` inside the notes block and leave the tag out.
- Language: `spanish-lyrics`, `swedish-lyrics`, `german-lyrics`, `conlang-lyrics`, ...
  (English is the default and often untagged).
- Universe/character tags: `thomas-entourage`, `thomas-garcia` (the Entourage's Thomas;
  `thomas-bauer` belongs to another universe), `gabriele-wiater`, `xumi` +
  `camila-alexander`, `pilar-venegas`, `sylvia-lai`, `claire-jones`, `zahra-moradi`, ...;
  `african-empire`, `monukae`, `mombuto`, `abulon`, `gladiel`; `tallinn`. Check the
  existing tag before inventing one. Only tag a character when the song is about them
  (a passing mention is not enough).
- Versions of one song: a cross-reference tag named after the parent's slug
  (`two-years-in-sodermalm`, `siento`, `my-quiet-genius`).

### Notes

- Typical forms: "Lyrics by Suno based on <source>…", "Original lyrics by Carlos
  Thompson.", "Adaptation by Claude/Gemini/Grok of <song> (page \pageref{sec:...})",
  "Re-genre of <song>, same lyrics". End imported songs with
  "Retrieved from <Creator>'s Suno page (<model>, <d Month yyyy>)." taken from the JSON.
- Use `\emph{}` for titles; only use `\pageref` when the target has a `\label`.
- All *Tallinn* vignettes are narrated in Thomas's voice; Carroll Gardens is voiced by
  Gabi and Mariain; Xumi's memoir songs are Suno lyrics from Xumi's memoir.
- Avoid pronouns for characters whose pronouns are not established in the repo.

## Import workflow (staging)

1. `python suno_fetch.py <url> --json > .json/<slug>.json` (owner or tool run).
2. Stage entries in `temp.tex` (or `temp2.tex`): `%! regex-fix=true`, then
   `%! dir=<author dir>` before each group, then raw Suno text (bracket section labels
   such as `[Verse 1]`; `desong` converts them). Creator → directory: Carlos Th →
   `chlewey`, rataflechera → `rataflechera`, Wyomee Dank → `wyomee`, Gabriel →
   `gabisson`, Dvigitt → `dvigitt`.
3. **The owner runs** `python desong.py temp.tex -m -b`. Claude must never create or
   overwrite the per-song files that `desong.py` generates.
4. File names are `maketag(title)` (see `desong.py`), with `_1`, `_2`, … when the name
   already exists in that directory. Predict them before adding `\input` lines, and say
   the books will not compile until the owner has run `desong` and pushed the files.
5. Optional `% -> songbook.tex (Chapter)` comment lines in staged entries record intended
   placements.
6. Check afterwards that every `\input` resolves and none is duplicated inside a book.

## Placement rules (agreed with the owner)

- **Genre songbooks** (`generos`, `pop`, `rockola`, `electronica`): one genre album per
  song by default. A second genre album only for a real crossover, case by case. Each
  re-genre goes to the album of *its* genre. Genre books use inline comments
  `\input{dir/file} % genre, year`; `entourage-eco` uses `% Character`.
- **original.tex**: only the first appearance of each original-lyrics song; never
  adaptations, re-genres, or songs with other people's lyrics (partial authorship has its
  own chapter).
- **personal.tex**: only genuinely personal/self songs.
- **Thematic books** (`stories`, `internal`, `entourage-eco`, `ricochets`): by theme.
- Size: around 20 songs per chapter is the ceiling. Do not move songs just because a
  chapter is near it; leave a `%` comment naming split candidates (see the Monukae note
  in `original.tex`, Other Narratives).
- Split by source, not by medium: *Essays* = originated as an essay/article/blog post/
  unpublished essay; *Dilemmas and arguments* = originated in a discussion (Quora,
  Google+, comment threads); short social-media posts about inner states belong to
  Later Thoughts. AI conversations are not a criterion by themselves.
- Stories *Life progression* = short single-episode stories in chronological order;
  *Life arcs* = multi-year stories ordered by focus year. Personal *Biographical* is
  split by century instead; whole-life songs go with the later volume.
- Albums need a clear identity. A "More"/miscellaneous album is a smell: dissolve it by
  placing its songs, or name what they share.
- Proposals are discussed with the owner first. Apply a restructuring only when told to.

## Covers

- Files: `covers/<songbook>/<slug>.png|.jpg|.jpeg`; chapters use
  `\albumcover{covers/<book>/<slug>}` and fall back to a gray square when the image is
  missing.
- Prompts live in `covers/<book>/<book>-cover-proposals.md`: `## Album title`, then the
  backticked path, then the prompt (everything until the next `#`/`##`). `gen_covers.py`
  turns them into images (needs `GEMINI_API_KEY`) and ignores lines starting with `>`,
  which are human notes.
- Rules: **never delete an image**; keep the old prompt when an album is retired or split
  and add a `> Note:` saying it was recycled; reuse the existing slug when the new album
  is not a stretch, and rename the file only when the slug would become meaningless.
- Prompts must be self-contained for an image generator: never write "matching the
  first volume"; describe the graphic identity explicitly.
- House styles: stories = long photographic paragraphs; internal = short one-liners;
  rockola = triangle still life (guitar lower-left, two objects); personal = two flat
  fields (matte black and white) split by a jagged gold-leaf seam, objects in full color;
  entourage-eco = comic-book illustration (clear-line characters, gouache backgrounds,
  one place and one moment, Thomas never face-on; the house-style paragraph and
  character looks are in the proposals file and `covers/entourage-eco/characters.yaml`).
  The old photorealistic prompts live in `entourage-eco-cover-proposals-photorealistic.md`,
  which `gen_covers.py` does not read. Headings that are not albums must use `###`, or
  `gen_covers.py` merges them into the next album's title.

## Owner preferences (carry into every session)

- Answer in the language of the thread's first message (English or Spanish) and switch
  when the owner switches. Spanish: "tú" or "usted", never "vos"; central Colombian
  vocabulary, formal register. English: American spelling.
- No praise, no apologies: name the error and continue. Be factual and say when the owner
  is wrong.
- Do not launch tools to fix or create things unless asked. If the owner asks a question,
  answer it without fixing. Discussion/planning turns stay read-only.
- The owner's typing is often noisy (typos); interpret generously, but confirm
  ambiguous song-to-album decisions before applying them.
- Commit and push work to `main` (a stop hook insists on a clean tree).

## Git and GitHub

- Work only on `main`: commit there and `git push origin main`. Do not create, switch to
  or keep any other branch (`claude/...` or otherwise), locally or on GitHub, and do not
  open pull requests. The owner confirmed this on 2026-11-08 after a stale
  `claude/vigilant-thompson-wxmkim` branch caused confusion; it has been deleted.
- If a session starts on another branch, stop and tell the owner instead of committing
  there.
- On Windows, a file open in Excel, a browser or an editor is locked: `git checkout`/
  `merge` can half-apply ("unable to unlink ... Invalid argument"). Check that each git
  step succeeded before the next one; never chain destructive steps with `;`.
- GitHub work goes through the `mcp__github__*` tools when available (no `gh` CLI).
- Commit messages end with the attribution lines the harness gives for the session.

## Open items (as of 2026-11-06)

- Cover images still to generate for several new albums (find them with a script that
  lists `\albumcover` paths without an image file). The tex references
  `covers/entourage-eco/meta-and-adjacent` has no entry in the proposals file.
- Crossover exceptions not yet decided: Se Acabó la Discusión (rockola Confessions too?),
  Every Step, Every Stripe (generos Country & Outlaw too?), Call Me Xumi (pop Misc too?).
- Rockola: *Operatic Portals* now holds single-character spotlights; the name no longer
  fits well. Rockola still needs a coherence pass.
- Pautina (`temp/pautina_andreya`) is in `stories.tex` but not in `personal.tex`.
- *Five Reasons to Celebrate* is tagged `xumi` but is not in Xumi's profile chapter.
- Lines marked `% TODO: lyricist unverified` await the owner (Extension of Friendship,
  Catching Up, Paolo's Text, Quiet Cracked Routine, Carroll Gardens, …).
- Nothing in this environment has been compiled; run `make` for the touched books.
