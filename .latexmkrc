# latexmk config for the suno songbook collection.
#
# Always build with LuaLaTeX (LuaHBTeX). XeLaTeX has been unreliable on this
# machine for the Arabic/CJK content used across these songbooks (Noto Naskh
# Arabic, Yu Gothic, Malgun Gothic via polyglossia/fontspec) -- LuaTeX's
# luaotfload resolves the same fonts correctly, so do not switch engines.
$pdf_mode = 4;                                             # 4 = lualatex -> pdf
$lualatex = 'lualatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';

# imakeidx names its indexes songs.* and tags.* in every songbook. build.ps1
# and the Makefile pass -auxdir=build/<JobName>, so each book keeps its own
# copies (and its .aux/.toc/.log/.fls/.fdb_latexmk) in its own directory and
# an unchanged book is not rerun just because another book was built.
# Building without -auxdir writes them to the root again and brings back
# the shared-file reruns.
$max_repeat = 5;

# what `latexmk -c` removes (keeps the PDF; use -C / distclean for that too)
$clean_ext = 'ilg ind idx synctex.gz fls fdb_latexmk xdv';
