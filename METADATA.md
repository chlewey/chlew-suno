# Song notes and tags

Individual song `.tex` files are the source of truth. `notes_index.md` is a generated view; regenerate it with `python extract_notes.py` after editing notes.

Run `python audit_metadata.py` to generate `metadata_audit.json`: a completion queue and tag vocabulary with song counts. Audit findings are review prompts, not instructions to guess missing facts. Existing tags outside the preferred spelling may be intentional; review their uses before renaming them.

## Notes

Use one nonempty `notes` environment. Keep the following order, omitting fields that are unknown or irrelevant:

1. Source: original poem, prompt, story, image, adaptation or narrative universe, with its title and creator when known.
2. Attribution: who wrote the lyrics, who adapted them, and any documented AI contribution. Distinguish lyrics from musical production.
3. Narrative: principal character, narrator, situation and relevant setting. Keep the description short and specific.
4. Version context: translation, rewrite, alternate perspective or relationship to another song.

Preserve established attribution wording unless evidence supports a correction. Do not infer authorship from the folder, production tool, style or fictional universe. Track unresolved provenance in the review queue rather than inserting invented credit or generic filler into printed notes.

## Tags

Use existing vocabulary where it expresses the same concept. Prefer lowercase words separated by hyphens. Keep one occurrence of each tag per song.

- `\tag*{2026}` records the documented composition year and is not indexed.
- `\tag{thomas-entourage}` identifies the narrative universe.
- Character tags identify a principal subject or narrator; a passing mention alone does not require a tag.
- Genre tags describe the actual style block. Reuse a specific existing genre rather than creating near synonyms.
- Add setting or theme tags when they support useful retrieval across songs, with evidence in the lyrics or notes.

Keep the order year, universe, principal characters, genre, then other retrieval tags. This is a presentation convention; the audit does not reorder source files.

`\setin{2025-06}` records an in-story date, independently of composition year. Preserve the precision supported by the source. `\tagexclude` controls a collection's presentation; it does not remove metadata from individual songs.

## Completion workflow

Review missing or empty notes first, then missing year and indexed tags, then vocabulary inconsistencies. Work through one collection or folder at a time. Resolve provenance using drafts and documented sources, add only supported metadata, rerun the audit, and regenerate the notes index. Review the diff before accepting broad vocabulary changes.
