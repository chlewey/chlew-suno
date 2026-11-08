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
# Each book writes its intermediate files (including the songs/tags
# indexes, which imakeidx names identically in every book) to its own
# build/<JobName>/ directory via -auxdir, so books no longer overwrite each
# other's indexes and an unchanged book is up to date on the next build.

LATEXMK := latexmk

# target name -> (source .tex, desired job/PDF name)
# job names match the old `%& -job-name=...` lines the sources carry;
# lualatex does not honor that comment, so it's passed explicitly instead.
.PHONY: all clean distclean \
        chlewrics electronica pop rockola generos americana internal stories entourage ricochets original personal bable

all: chlewrics electronica pop rockola generos americana internal stories entourage ricochets original personal bable

chlewrics:
	$(LATEXMK) -jobname=Chlewrics -auxdir=build/Chlewrics chlewrics.tex

electronica:
	$(LATEXMK) -jobname=Electronica_lyrics -auxdir=build/Electronica_lyrics electronica.tex

pop:
	$(LATEXMK) -jobname=Pop_lyrics -auxdir=build/Pop_lyrics pop.tex

rockola:
	$(LATEXMK) -jobname=Rockola_lyrics -auxdir=build/Rockola_lyrics rockola.tex

generos:
	$(LATEXMK) -jobname=Genres_lyrics -auxdir=build/Genres_lyrics generos.tex

americana:
	$(LATEXMK) -jobname=Americana_lyrics -auxdir=build/Americana_lyrics americana.tex

internal:
	$(LATEXMK) -jobname=Internal -auxdir=build/Internal internal.tex

stories:
	$(LATEXMK) -jobname=Storytelling_lyrics -auxdir=build/Storytelling_lyrics stories.tex

entourage:
	$(LATEXMK) -jobname=Entourage_Lyrics -auxdir=build/Entourage_Lyrics entourage-eco.tex

ricochets:
	$(LATEXMK) -jobname=Ricochets_lyrics -auxdir=build/Ricochets_lyrics ricochets.tex

original:
	$(LATEXMK) -jobname=Original_lyrics -auxdir=build/Original_lyrics original.tex

personal:
	$(LATEXMK) -jobname=Personal_lyrics -auxdir=build/Personal_lyrics personal.tex

bable:
	$(LATEXMK) -jobname=Bable_lyrics -auxdir=build/Bable_lyrics bable.tex

clean:
	-$(LATEXMK) -c -jobname=Chlewrics -auxdir=build/Chlewrics chlewrics.tex
	-$(LATEXMK) -c -jobname=Electronica_lyrics -auxdir=build/Electronica_lyrics electronica.tex
	-$(LATEXMK) -c -jobname=Pop_lyrics -auxdir=build/Pop_lyrics pop.tex
	-$(LATEXMK) -c -jobname=Rockola_lyrics -auxdir=build/Rockola_lyrics rockola.tex
	-$(LATEXMK) -c -jobname=Genres_lyrics -auxdir=build/Genres_lyrics generos.tex
	-$(LATEXMK) -c -jobname=Americana_lyrics -auxdir=build/Americana_lyrics americana.tex
	-$(LATEXMK) -c -jobname=Internal -auxdir=build/Internal internal.tex
	-$(LATEXMK) -c -jobname=Storytelling_lyrics -auxdir=build/Storytelling_lyrics stories.tex
	-$(LATEXMK) -c -jobname=Entourage_Lyrics -auxdir=build/Entourage_Lyrics entourage-eco.tex
	-$(LATEXMK) -c -jobname=Ricochets_lyrics -auxdir=build/Ricochets_lyrics ricochets.tex
	-$(LATEXMK) -c -jobname=Original_lyrics -auxdir=build/Original_lyrics original.tex
	-$(LATEXMK) -c -jobname=Personal_lyrics -auxdir=build/Personal_lyrics personal.tex
	-$(LATEXMK) -c -jobname=Bable_lyrics -auxdir=build/Bable_lyrics bable.tex
	-rm -f songs.idx songs.ind songs.ilg tags.idx tags.ind tags.ilg

distclean: clean
	-rm -f Chlewrics.pdf Electronica_lyrics.pdf Pop_lyrics.pdf Rockola_lyrics.pdf \
	       Genres_lyrics.pdf Americana_lyrics.pdf Internal.pdf Storytelling_lyrics.pdf Entourage_Lyrics.pdf \
	       Ricochets_lyrics.pdf Original_lyrics.pdf Personal_lyrics.pdf Bable_lyrics.pdf
