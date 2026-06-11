#!/usr/bin/env python3
"""Generate all Notes replacements for wyomee.tex"""

from pathlib import Path
import re
import json

text = Path('wyomee.tex').read_text(encoding='utf-8')

notes_map = {
    'Melgar Table': "From the \\emph{Thomas' Entourage} universe by Carlos Thompson.\\\nCharacter: Gabriele Wiater.\\\nA New Year's Eve family gathering celebration among characters from the narrative.",
    'The Pirate\'s Ledger': "Original work.\\\nMusical theater-style narrative song drawn from historical maritime themes.",
    'Guided Hands': "Original work.\\\nTheme: Mental health, accountability, and the need for structured support systems.",
    'Vaina que crece': "Original work by Carlos Thompson.\\\nArtistic electronic composition exploring metamorphosis and creative growth.",
    'Monoestable': "Original work in Spanish.\\\nExplores state dynamics and internal oscillation; themed around instability and emotional transformation.",
    'E Numa Lah': "Original work.\\\nExperimental composition with stylized, non-semantic vocals and abstract sound design.",
    'Mira': "Original work from 1996.\\\nMusical theater piece using conversational narrative framing.",
    'Si pienso': "Original work by Carlos Thompson.\\\nIn Spanish. Trance meditation on memory and obsessive thought patterns.",
    'Iros de risk': "Original work.\\\nExperimental trance composition with fragmented narrative structure.",
    'Uneekwa En Urbo': "Original work.\\\nEsperanto folk duet, a portrait of an urban figure presented through dual vocal perspectives.",
    'Potsdam Leeres Büro': "From the \\emph{Thomas' Entourage} universe.\\\nCharacter: Gabriele Wiater, SVA student in New York.\\\nInner monologue and emotional landscape.",
    'Sunlit Gem Music': "Original work.\\\nA meditation on romantic idealization drawn from a classical-style love poem.",
    'Soap Line Logic': "Original work from 2026.\\\nAbstract electronic reflection on mundane ritual and meditative routine.",
    'Equals': "From the \\emph{Thomas' Entourage} universe.\\\nCharacters: Mariain Schumer and Gabriele Wiater.\\\nCo-written with ChatGPT. High interaction.\\\nExplores emotional recalibration and mutual growth in relationship transformation.",
    'East Rock / The VIllage': "From the \\emph{Thomas' Entourage} universe.\\\nCharacter: Mariain Schumer.\\\nCo-written with ChatGPT. High interaction.\\\nPortrait of a woman navigating two cities and life trajectories.",
    'Lilac-eyed Demon': "From the \\emph{Thomas' Entourage} universe.\\\nCharacter: Mariain Schumer.\\\nDubstep accusation and introspective reckoning with impact and culpability.",
    'Fast Neunzehn (Zwei Welten Bluten)': "From the \\emph{Ricochets} universe.\\\nCharacter: Carolina Müller.\\\nCo-written by Carlos Thompson, Claude, and Gemini. High interaction.\\\nNarcocorrido-influenced industrial track exploring dual identity and moral complexity.",
    'Su peccadu meu': "From the \\emph{Thomas' Entourage} universe.\\\nCharacter: Sylvia Lai.\\\nCampidanese lyrics with techno production. Reflection on desire and transgression.",
    'Almost Enough': "Original work from 1992.\\\nIntrospective pop ballad on performance anxiety and self-doubt.",
    'Library to Longing': "Original work.\\\nPlaceholder title; structure pending.",
    'Swedish Pages': "Original work.\\\nPlaceholder title; structure pending.",
    'Clumsy Hearts': "Original work.\\\nPlaceholder title; structure pending.",
    'Ciudad Prestada': "Original work.\\\nLatin alternative meditation on belonging and the provisional nature of home.",
    'Still Unfinished': "Original work.\\\nCo-written with Grok.\\\nBased on character Damon from the short story \\emph{Drift} by Carlos Thompson and ChatGPT.",
    'Ghost Cheek Kiss': "Original work.\\\nCo-written with Grok.\\\nBased on character Fran from the short story \\emph{Drift} by Carlos Thompson and ChatGPT.",
    'Southern Static': "Original work.\\\nCo-written with Grok.\\\nBased on character Raoul from the short story \\emph{Drift} by Carlos Thompson and ChatGPT.",
    'Pared fria': "Original work in Spanish.\\\nTrance-dubstep exploration of silence and emotional stasis.",
    'Extension of Friendship': "Original work.\\\nFolk-chamber piece on emotional boundaries and clandestine connection.",
    'Catching Up': "Original work.\\\nMusical theater cabaret scenario of reunion and temptation.",
    'Landscape': "Original work.\\\nSynthwave composition reflecting on external beauty and interior complexity.",
    'Bucket List': "Original work.\\\nHouse music meditation on aspirations and spiritual geography.",
    'Diamond Depth August': "Original work.\\\nSalsa composition with historical narrative framing.",
    'Miladi in the Dark': "Original work.\\\nMedieval folk ballad exploring grief, ritual, and medieval emotional landscape.",
    'Destinies Overlap': "Original work.\\\nAlternative rock narrative of parallel lives and unforeseen convergence.",
    'Best Available Lens': "Original work.\\\nDubstep hymn on epistemology and practical philosophy.",
    'Not In The Creed': "Original work.\\\nGospel-soul reflection on religious childhood and eventual departure.",
    'Which God Stands Still': "Original work.\\\nGospel composition on faith and the search for immovable truth.",
    'Ashes in the Pews': "Original work.\\\nDubstep-gospel exploration of ritual transmission and inherited belief.",
    'Neon Shutter // Only Herself': "Original work, AI-generated portrait from 2026.",
    'Copper In The Pines': "Original work, AI-generated portrait from 2026.",
    'Peeling Paint Girl': "Original work, AI-generated portrait from 2026.",
    'Ulla In The Hall': "From the \\emph{Encounters} universe.\\\nCharacter: Ulla.\\\nAI-generated portrait from 2026.",
}

# Generate replacements by finding each empty Notes section
pattern = re.compile(r'(\\section\{([^}]*)\}.*?\\subsection\{Notes\})\n\n(\\subsection)', re.S)

count = 0
for m in pattern.finditer(text):
    full_match = m.group(0)
    section_title = m.group(2)
    
    if section_title in notes_map:
        old_str = full_match
        new_str = m.group(1) + '\n' + notes_map[section_title] + '\n\n' + m.group(3)
        
        print(f"{count+1}. {section_title}")
        count += 1

print(f"\nTotal replacements found: {count}")
