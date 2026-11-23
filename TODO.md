# TODO

## Verify sources against chlewey.net and blog.chlewey.net

Both sites are back online (noted 2026-11-21), so the notes that cite them can be checked against the original texts:

- Songs whose notes cite a blog entry or post by Carlos Thompson: check the title, the date and that the lyrics follow the text (for example *No te pido una respuesta*, *The Quiet Tongue*).
- Songs that claim older original texts on chlewey.net: the 1991 poems and the *Despertar* songs (`chlewey.net/scripts/1991`), *Mobisarna* from *Mobis* (`chlewey.net/scripts/mobis`), and other `original-lyrics` or `original-source` songs with a dated source.
- Fix the notes where they disagree, and clear the `% TODO: lyricist unverified` lines the sites can settle.

## Correct empty or generic notes

Some songs have an empty `notes` block, or notes that are generic filler about the arrangement ("A distinctive arrangement that supports the song's storytelling…") instead of source, lyricist and narrative. Rewrite them following `METADATA.md` (source, attribution, narrative, version context); `python audit_metadata.py` lists the candidates in `metadata_audit.json`. Do not invent facts: where the source or lyricist is unknown, write `% TODO: lyricist unverified (...)` and ask.

## Verify the LLM credited in each song

The LLM named as lyricist or adapter (Claude, ChatGPT, Grok, Gemini, DeepSeek, Suno) was often recalled from memory, particularly for the early songs. Check it against the surviving records (chat histories, prompts, Suno pages and dates) and correct the notes and `.txt/dna.md` where they disagree. Open cases: *Mobisarna* and the three Ilva and Khamid songs (*Nyckelharpa under asfalt*, *Ökenskor av salt*, *Vinterfrostleende*).

## Complete the Ricochets vignettes

Write the songs still missing from `lyric_drafts/ricochets-vignettes.md` (status as of 2026-11-21: 9 NEW, 2 PARTIAL). A vignette becomes COVERED only when its song has been fetched from Suno.

- [ ] 20. After I Cross That Gate (ch12, PARTIAL: the taxi dialogue is not sung)
- [ ] 21. Line of Fire (ch13)
- [ ] 23. Didn't You Learn Your Lesson? (ch14)
- [ ] 24. C'est dommage (ch14)
- [ ] 25. I Needed Him to Be Guilty (ch15)
- [ ] 27. The Second Kind of Fool (ch16)
- [ ] 30. Seven-Sixteenths (ch18)
- [ ] 32. Matteo, and Still Not Fair (ch20, PARTIAL: the Perez half is not sung)
- [ ] 33. Sargento Michael Pierce (ch21)
- [ ] 34. For Keaton (ch22)
- [ ] 35. What the Other Is Supposed to Be (ch22)

## Empty `temp/`

322 songs are still in `temp/`. Move each to the author directory of its Suno account (`chlewey`, `rataflechera`, `wyomee`, `gabisson`, `dvigitt`), or leave it in `temp/` with the reason noted.

## Songbook structure (from CLAUDE.md "Open items")

- [ ] Decide the crossover exceptions: *Se Acabó la Discusión* (rockola Confessions too?), *Every Step, Every Stripe* (generos Country & Outlaw too?), *Call Me Xumi* (pop Misc too?)
- [ ] Rockola coherence pass; rename *Operatic Portals*, which now holds single-character spotlights
- [ ] Pautina (`temp/pautina_andreya`): add to `personal.tex` or record why not
- [ ] *Five Reasons to Celebrate* is tagged `xumi` but is not in Xumi's profile chapter
- [ ] Regenerate `docs/songbook-index.csv` from the `.tex` sources

## Covers

- [ ] List the `\albumcover` paths with no image file (short script) and generate the missing covers
- [ ] Add `covers/entourage-eco/meta-and-adjacent` to the entourage-eco proposals file

## Release build

- [ ] `make all` (or `build.ps1`) on the author's machine with no LaTeX errors, then review the PDFs
