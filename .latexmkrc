# latexmk config for the suno songbook collection.
#
# Always build with LuaLaTeX (LuaHBTeX). XeLaTeX has been unreliable on this
# machine for the Arabic/CJK content used across these songbooks (Noto Naskh
# Arabic, Yu Gothic, Malgun Gothic via polyglossia/fontspec) -- LuaTeX's
# luaotfload resolves the same fonts correctly, so do not switch engines.
$pdf_mode = 4;                                             # 4 = lualatex -> pdf
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';

# songs.idx/songs.ind/tags.idx/tags.ind (imakeidx, packages `songs` and
# `tags`) are SHARED, fixed filenames across every songbook in this
# directory -- each build overwrites them from scratch. Never build more
# than one songbook at a time: no `latexmk -jobs=N`, no `make -j`.
$max_repeat = 5;

# what `latexmk -c` removes (keeps the PDF; use -C / distclean for that too)
$clean_ext = 'ilg ind idx synctex.gz fls fdb_latexmk xdv';
