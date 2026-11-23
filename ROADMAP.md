# Roadmap — Suno songbooks

An ongoing collection: songs keep arriving, so there is no "finished" state. The roadmap instead defines what a clean, releasable round of the twelve songbooks looks like, and the order to get there. Concrete items are in [TODO.md](TODO.md); conventions in `CLAUDE.md`, `METADATA.md` and `MANUAL.md`.

Updated: 2026-11-22. About 1 090 song files: `chlewey` 158, `rataflechera` 168, `wyomee` 173, `gabisson` 168, `dvigitt` 101, and 322 still in `temp/`.

## Milestones

### 1. Credits and sources verified
Every song's notes say where the lyrics came from and who wrote them, and that is checked rather than recalled.

- Sources checked against chlewey.net and blog.chlewey.net, now back online.
- The LLM credited for each song checked against chat histories, prompts and Suno pages.
- Empty or generic notes rewritten (`audit_metadata.py`).
- No `% TODO: lyricist unverified` lines left, or each remaining one explained.

### 2. `temp/` emptied
The 322 songs in `temp/` moved to the author directory of their Suno account, or kept in `temp/` with a reason recorded.

### 3. Songbook structure settled
- Crossover exceptions decided (*Se Acabó la Discusión*, *Every Step, Every Stripe*, *Call Me Xumi*).
- Rockola coherence pass, including a new name for *Operatic Portals*.
- Loose ends from CLAUDE.md "Open items": Pautina in `personal.tex`, *Five Reasons to Celebrate* in Xumi's profile chapter.
- `docs/songbook-index.csv` regenerated from the `.tex` sources.

### 4. Narrative songbooks complete
- *Ricochets*: the 11 vignettes still missing from `lyric_drafts/ricochets-vignettes.md` written and fetched from Suno.
- *Entourage*: songs aligned with the `thomas-entourage` canon and its song catalog (see that repo's ROADMAP, milestone 4).

### 5. Covers
Every `\albumcover` has an image file; the proposals files in `covers/` list every album the `.tex` files reference.

### 6. Release build
All twelve books (`make all` or `build.ps1`) compile with LuaLaTeX with no errors, and the PDFs are reviewed. The cloud environment has no LaTeX engine, so this step runs on the author's machine.

## Order
1 is the priority, since the sites are back online now. 2 and 3 go together, because placing a song from `temp/` means choosing its albums. 4 and 5 can run at any time. 6 closes each round.
