<#
.SYNOPSIS
    Build script for the suno songbook collection (PowerShell equivalent of
    the Makefile -- no `make` binary was available on this machine, so this
    is the one that actually runs here today).

.DESCRIPTION
    Engine choice and pass/index handling live in .latexmkrc: builds always
    use LuaLaTeX, never XeLaTeX, because XeLaTeX has been unreliable on this
    machine for the Arabic/CJK content used across these songbooks. Keep
    this file and the Makefile in sync if you add or rename a book.

    Each book writes its intermediate files (.aux, .toc, .log, .fls,
    .fdb_latexmk and the songs/tags indexes) to its own directory,
    build/<JobName>/ (latexmk -auxdir); only the PDF and its .synctex.gz stay
    in the root. imakeidx names its indexes songs.* and tags.* in every book,
    so a shared directory made latexmk rerun a book whenever another book had
    been built in between. With one aux directory per book, an unchanged book
    is up to date on the second build.

.PARAMETER Target
    One of: all, chlewrics, electronica, pop, rockola, generos, americana, internal,
    stories, entourage, ricochets, original, personal, bable, clean, distclean.
    Default: all.

.EXAMPLE
    .\build.ps1
    .\build.ps1 -Target ricochets
    .\build.ps1 -Target clean
#>
param(
    [ValidateSet('all','chlewrics','electronica','pop','rockola','generos','americana',
                 'internal','stories','entourage','ricochets','original',
                 'personal','bable','clean','distclean')]
    [string]$Target = 'all'
)

# Deliberately NOT setting $ErrorActionPreference = 'Stop': in PowerShell
# 5.1, that turns every stderr line a native exe writes (e.g. makeindex's
# own banner) into a terminating exception, even on success. Real failures
# are caught via $LASTEXITCODE below instead.

# latexmk is a Perl script; MiKTeX does not bundle Perl, and this machine's
# PowerShell PATH has none either. Git for Windows does ship one, just not
# on PATH by default -- add it for this process only (no permanent/system
# PATH change) if `perl` isn't already reachable.
if (-not (Get-Command perl -ErrorAction SilentlyContinue)) {
    $gitPerl = 'C:\Program Files\Git\usr\bin'
    if (Test-Path (Join-Path $gitPerl 'perl.exe')) {
        $env:PATH = "$gitPerl;$env:PATH"
    } else {
        Write-Warning "No 'perl' found on PATH and Git's bundled perl.exe isn't at '$gitPerl' either -- latexmk will fail. Install Strawberry Perl or Git for Windows."
    }
}

# target name -> (source .tex, desired job/PDF name)
# job names match the old `%& -job-name=...` lines the sources carry;
# lualatex does not honor that comment, so it's passed explicitly instead.
$books = [ordered]@{
    electronica = @{ Src = 'electronica.tex';   Job = 'Electronica_lyrics' }
    pop         = @{ Src = 'pop.tex';           Job = 'Pop_lyrics' }
    rockola     = @{ Src = 'rockola.tex';       Job = 'Rockola_lyrics' }
    generos     = @{ Src = 'generos.tex';       Job = 'Genres_lyrics' }
    americana   = @{ Src = 'americana.tex';     Job = 'Americana_lyrics' }
    internal    = @{ Src = 'internal.tex';      Job = 'Internal' }
    stories     = @{ Src = 'stories.tex';       Job = 'Storytelling_lyrics' }
    entourage   = @{ Src = 'entourage-eco.tex'; Job = 'Entourage_Lyrics' }
    ricochets   = @{ Src = 'ricochets.tex';     Job = 'Ricochets_lyrics' }
    original    = @{ Src = 'original.tex';      Job = 'Original_lyrics' }
    personal    = @{ Src = 'personal.tex';      Job = 'Personal_lyrics' }
    bable       = @{ Src = 'bable.tex';         Job = 'Bable_lyrics' }
    chlewrics   = @{ Src = 'chlewrics.tex';     Job = 'Chlewrics' }
}

function Invoke-Book([string]$Name, [hashtable]$Info) {
    Write-Host "==> $Name -> $($Info.Job).pdf (lualatex via latexmk)" -ForegroundColor Cyan
    # Splat an explicit args array -- passing "-jobname=$($Info.Job)" and
    # "$($Info.Src)" inline on the call line makes latexmk ignore the
    # filename and fall back to its own (ambiguous) default-file detection.
    $latexmkArgs = @("-jobname=$($Info.Job)", "-auxdir=$(Get-AuxDir $Info)", $Info.Src)
    & latexmk @latexmkArgs
    if ($LASTEXITCODE -ne 0) {
        throw "latexmk failed for $($Info.Src) (jobname $($Info.Job)); see $(Get-AuxDir $Info)/$($Info.Job).log"
    }
}

function Get-AuxDir([hashtable]$Info) {
    return "build/$($Info.Job)"
}

function Clear-Book([hashtable]$Info) {
    $latexmkArgs = @('-c', "-jobname=$($Info.Job)", "-auxdir=$(Get-AuxDir $Info)", $Info.Src)
    & latexmk @latexmkArgs 2>$null | Out-Null
}

function Remove-SharedIndexFiles {
    # Leftovers from before the per-book aux directories (songs.*/tags.* used
    # to be written to the root by every book). Harmless if absent.
    Remove-Item -ErrorAction SilentlyContinue songs.idx, songs.ind, songs.ilg, tags.idx, tags.ind, tags.ilg
}

switch ($Target) {
    'all' {
        foreach ($name in $books.Keys) { Invoke-Book $name $books[$name] }
    }
    'clean' {
        foreach ($name in $books.Keys) { Clear-Book $books[$name] }
        Remove-SharedIndexFiles
    }
    'distclean' {
        foreach ($name in $books.Keys) { Clear-Book $books[$name] }
        Remove-SharedIndexFiles
        foreach ($name in $books.Keys) { Remove-Item -ErrorAction SilentlyContinue "$($books[$name].Job).pdf" }
    }
    default {
        Invoke-Book $Target $books[$Target]
    }
}
