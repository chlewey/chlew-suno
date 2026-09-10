# Makefile for the suno songbook collection.
#
# Requires GNU Make and latexmk (latexmk ships with MiKTeX). Engine choice
# and pass/index handling live in .latexmkrc -- see that file for why
# LuaLaTeX is forced instead of XeLaTeX.
#
# No `make` binary was available on the machine this was written on
# (Windows without WSL/msys/choco make); build.ps1 is the equivalent that
# runs there today. Keep the two in sync if you add or rename a book.
#
# IMPORTANT: songs.idx/songs.ind/tags.idx/tags.ind are SHARED filenames
# across every book below -- never run this with `make -j`.

LATEXMK := latexmk

# target name -> (source .tex, desired job/PDF name)
# job names match the old `%& -job-name=...` lines the sources carry;
# lualatex does not honor that comment, so it's passed explicitly instead.
.PHONY: all clean distclean \
        chlewrics electronica pop rockola generos internal stories entourage ricochets original

all: chlewrics electronica pop rockola generos internal stories entourage ricochets original

chlewrics:
	$(LATEXMK) -jobname=Chlewrics chlewrics.tex

electronica:
	$(LATEXMK) -jobname=Electronica_lyrics electronica.tex

pop:
	$(LATEXMK) -jobname=Pop_lyrics pop.tex

rockola:
	$(LATEXMK) -jobname=Rockola_lyrics rockola.tex

generos:
	$(LATEXMK) -jobname=Genres_lyrics generos.tex

internal:
	$(LATEXMK) -jobname=Internal internal.tex

stories:
	$(LATEXMK) -jobname=Storytelling_lyrics stories.tex

entourage:
	$(LATEXMK) -jobname=Entourage_Lyrics entourage-eco.tex

ricochets:
	$(LATEXMK) -jobname=Ricochets_lyrics ricochets.tex

original:
	$(LATEXMK) -jobname=Original_lyrics original.tex

clean:
	-$(LATEXMK) -c -jobname=Chlewrics chlewrics.tex
	-$(LATEXMK) -c -jobname=Electronica_lyrics electronica.tex
	-$(LATEXMK) -c -jobname=Pop_lyrics pop.tex
	-$(LATEXMK) -c -jobname=Rockola_lyrics rockola.tex
	-$(LATEXMK) -c -jobname=Genres_lyrics generos.tex
	-$(LATEXMK) -c -jobname=Internal internal.tex
	-$(LATEXMK) -c -jobname=Storytelling_lyrics stories.tex
	-$(LATEXMK) -c -jobname=Entourage_Lyrics entourage-eco.tex
	-$(LATEXMK) -c -jobname=Ricochets_lyrics ricochets.tex
	-$(LATEXMK) -c -jobname=Original_lyrics original.tex
	-rm -f songs.idx songs.ind songs.ilg tags.idx tags.ind tags.ilg

distclean: clean
	-rm -f Chlewrics.pdf Electronica_lyrics.pdf Pop_lyrics.pdf Rockola_lyrics.pdf \
	       Genres_lyrics.pdf Internal.pdf Storytelling_lyrics.pdf Entourage_Lyrics.pdf \
	       Ricochets_lyrics.pdf Original_lyrics.pdf
