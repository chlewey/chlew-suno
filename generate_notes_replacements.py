#!/usr/bin/env python3
"""Generate all Notes replacements for wyomee.tex"""

from pathlib import Path
import re
import json

text = Path('wyomee.tex').read_text(encoding='utf-8')

notes_map = {
    'Melgar Table': "From the \\emph{Thomas' Entourage} universe by Carlos Thompson.\\\n" + 
                    "Character: Gabriele Wiater.\\\n" + 
                    "A New Year's Eve family gathering celebration among characters from the narrative.",
    
    'The Pirate\'s Ledger': "Original work.\\\n" + 
                           "Musical theater-style narrative song drawn from historical maritime themes.",
    
    'Guided Hands': r"Original work.\\
Theme: Mental health, accountability, and the need for structured support systems.",
    
    'Vaina que crece': r"Original work by Carlos Thompson.\\
Artistic electronic composition exploring metamorphosis and creative growth.",
    
    'Monoestable': r"Original work in Spanish.\\
Explores state dynamics and internal oscillation; themed around instability and emotional transformation.",
    
    'E Numa Lah': r"Original work.\\
Experimental composition with stylized, non-semantic vocals and abstract sound design.",
    
    'Mirá': r"Original work from 1996.\\
Musical theater piece using conversational narrative framing.",
    
    'Si pienso': r"Original work by Carlos Thompson.\\
In Spanish. Trance meditation on memory and obsessive thought patterns.",
    
    'Iros de risk': r"Original work.\\
Experimental trance composition with fragmented narrative structure.",
    
    'Uneekwa En Urbo': r"Original work.\\
Esperanto folk duet, a portrait of an urban figure presented through dual vocal perspectives.",
    
    'Potsdam Leeres Büro': r"From the \emph{Thomas' Entourage} universe.\\
Character: Gabriele Wiater, SVA student in New York.\\
Inner monologue and emotional landscape.",
    
    'Sunlit Gem Music': r"Original work.\\
A meditation on romantic idealization drawn from a classical-style love poem.",
    
    'Soap Line Logic': r"Original work from 2026.\\
Abstract electronic reflection on mundane ritual and meditative routine.",
    
    'Equals': r"From the \emph{Thomas' Entourage} universe.\\
Characters: Mariain Schumer and Gabriele Wiater.\\
Co-written with ChatGPT. High interaction.\\
Explores emotional recalibration and mutual growth in relationship transformation.",
    
    'East Rock / The VIllage': r"From the \emph{Thomas' Entourage} universe.\\
Character: Mariain Schumer.\\
Co-written with ChatGPT. High interaction.\\
Portrait of a woman navigating two cities and life trajectories.",
    
    'Lilac-eyed Demon': r"From the \emph{Thomas' Entourage} universe.\\
Character: Mariain Schumer.\\
Dubstep accusation and introspective reckoning with impact and culpability.",
    
    'Fast Neunzehn (Zwei Welten Bluten)': r"From the \emph{Ricochets} universe.\\
Character: Carolina Müller.\\
Co-written by Carlos Thompson, Claude, and Gemini. High interaction.\\
Narcocorrido-influenced industrial track exploring dual identity and moral complexity.",
    
    'Su peccadu meu': r"From the \emph{Thomas' Entourage} universe.\\
Character: Sylvia Lai.\\
Campidanese lyrics with techno production. Reflection on desire and transgression.",
    
    'Almost Enough': r"Original work from 1992.\\
Introspective pop ballad on performance anxiety and self-doubt.",
    
    'Library to Longing': r"Original work.\\
Placeholder title; structure pending.",
    
    'Swedish Pages': r"Original work.\\
Placeholder title; structure pending.",
    
    'Clumsy Hearts': r"Original work.\\
Placeholder title; structure pending.",
    
    'Ciudad Prestada': r"Original work.\\
Latin alternative meditation on belonging and the provisional nature of home.",
    
    'Still Unfinished': r"Original work.\\
Co-written with Grok.\\
Based on character Damon from the short story \emph{Drift} by Carlos Thompson and ChatGPT.",
    
    'Ghost Cheek Kiss': r"Original work.\\
Co-written with Grok.\\
Based on character Fran from the short story \emph{Drift} by Carlos Thompson and ChatGPT.",
    
    'Southern Static': r"Original work.\\
Co-written with Grok.\\
Based on character Raoul from the short story \emph{Drift} by Carlos Thompson and ChatGPT.",
    
    'Pared fría': r"Original work in Spanish.\\
Trance-dubstep exploration of silence and emotional stasis.",
    
    'Extension of Friendship': r"Original work.\\
Folk-chamber piece on emotional boundaries and clandestine connection.",
    
    'Catching Up': r"Original work.\\
Musical theater cabaret scenario of reunion and temptation.",
    
    'Landscape': r"Original work.\\
Synthwave composition reflecting on external beauty and interior complexity.",
    
    'Bucket List': r"Original work.\\
House music meditation on aspirations and spiritual geography.",
    
    'Diamond Depth August': r"Original work.\\
Salsa composition with historical narrative framing.",
    
    'Miladi in the Dark': r"Original work.\\
Medieval folk ballad exploring grief, ritual, and medieval emotional landscape.",
    
    'Destinies Overlap': r"Original work.\\
Alternative rock narrative of parallel lives and unforeseen convergence.",
    
    'Best Available Lens': r"Original work.\\
Dubstep hymn on epistemology and practical philosophy.",
    
    'Not In The Creed': r"Original work.\\
Gospel-soul reflection on religious childhood and eventual departure.",
    
    'Which God Stands Still': r"Original work.\\
Gospel composition on faith and the search for immovable truth.",
    
    'Ashes in the Pews': r"Original work.\\
Dubstep-gospel exploration of ritual transmission and inherited belief.",
    
    'Neon Shutter // Only Herself': r"Original work, AI-generated portrait from 2026.",
    
    'Copper In The Pines': r"Original work, AI-generated portrait from 2026.",
    
    'Peeling Paint Girl': r"Original work, AI-generated portrait from 2026.",
    
    'Ulla In The Hall': r"From the \emph{Encounters} universe.\\
Character: Ulla.\\
AI-generated portrait from 2026.",
}

# Generate replacements
replacements = []
pattern = re.compile(r'(\\section\{([^}]*)\}.*?\\subsection\{Notes\})\n\n(\\subsection)', re.S)

for m in pattern.finditer(text):
    full_match = m.group(0)
    section_title = m.group(2)
    
    if section_title in notes_map:
        old_str = full_match
        new_str = m.group(1) + '\n' + notes_map[section_title] + '\n\n' + m.group(3)
        replacements.append({
            'title': section_title,
            'oldString': old_str,
            'newString': new_str
        })

print(f"Generated {len(replacements)} replacements")
print("\nReplacements ready for application:")
for r in replacements[:3]:
    print(f"  - {r['title']}")

# Save for later inspection if needed
Path('replacements.json').write_text(json.dumps(replacements[:2], indent=2))
print(f"\nFirst 2 replacements saved to replacements.json")
print(f"Total to apply: {len(replacements)}")
