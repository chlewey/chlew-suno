import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# file -> list of (chapter title exactly as in \chapter{...}, [lines to add])
PLAN = {
    'entourage-eco.tex': [
        ('Character profile: Natalia', [r'\input{dvigitt/when_i_say_yes}']),
        ('Character profile: Claire', [r'\input{gabisson/worthy}']),
        ('Character profile: Erika', [r'\input{chlewey/the_same_colombia}']),
        ('Characters', [r'\input{dvigitt/i_chose_this_life}']),
        ('Orbits', [r'\input{wyomee/the_fixed_point}',
                    r'\input{wyomee/public_knowledge}',
                    r'\input{wyomee/somewhere_between_flights}']),
    ],
    'original.tex': [
        ("Thomas' Entourage", [r'\input{dvigitt/when_i_say_yes}', r'\input{gabisson/worthy}']),
        ('Essays and Reckonings', [r'\input{chlewey/leading_the_jump}']),
        ('Restless Mind', [r'\input{chlewey/easy_love}']),
        ('Other Narratives', [r'\input{rataflechera/mueca_pantera}']),
    ],
    'personal.tex': [
        ('Biographical', [r'\input{chlewey/leading_the_jump}', r'\input{gabisson/tvaa_aar_paa_soder}']),
        ('Soul and craves', [r'\input{chlewey/easy_love}']),
    ],
    'stories.tex': [
        ('Self', [r'\input{chlewey/leading_the_jump}', r'\input{gabisson/tvaa_aar_paa_soder}']),
        ('African Empire -- Monukae', [r'\input{wyomee/under_aachen_sky}']),
        ('Cats', [r'\input{rataflechera/mueca_pantera}']),
        ('More', [r'\input{dvigitt/dvigitt_at_the_table}', r'\input{dvigitt/top_of_the_curve}']),
    ],
    'internal.tex': [
        ('Essays', [r'\input{rataflechera/draw_the_line}']),
        ('Soul', [r'\input{chlewey/easy_love}']),
    ],
    'ricochets.tex': [
        ('Canonical', [r'\input{wyomee/every_fact_in_its_own_time}',
                       r'\input{wyomee/her_leaving_never_left}',
                       r'\input{rataflechera/margot}']),
        ('Fragments and Summaries', [r'\input{rataflechera/a_narrow_way}',
                                     r'\input{rataflechera/the_lens_cannot_know}']),
    ],
    'pop.tex': [
        ("Thomas' Entourage in Rhythm and Blues", [r'\input{dvigitt/when_i_say_yes} % r-and-b, 2026']),
        ('Sophisti-Pop', [r'\input{gabisson/worthy} % sophisti-pop, 2026']),
        ("Thomas' Entourage through Ballads", [r'\input{wyomee/the_fixed_point} % soft-rock-ballad, 2026']),
        ('Vispop', [r'\input{gabisson/tvaa_aar_paa_soder} % vispop, 2026']),
        ('Misc', [r'\input{chlewey/easy_love} % soft-rock, 2026',
                  r'\input{dvigitt/top_of_the_curve} % electro-pop, 2026',
                  r'\input{dvigitt/i_chose_this_life} % adult-contemporary, 2025']),
        (r'Symphonic \& Chamber Pop', [r'\input{rataflechera/a_narrow_way} % chamber-pop-rock, 2026']),
        ('Telling Stories in Hip-Hop', [r'\input{wyomee/every_fact_in_its_own_time} % hip-hop-pop, 2026']),
    ],
    'rockola.tex': [
        (r'Pilots, Routes \& Foundations', [r'\input{wyomee/public_knowledge} % soft-rock, 2026',
                                           r'\input{wyomee/somewhere_between_flights} % pop-rock, 2026']),
        (r'Confessions \& Small Defeats', [r'\input{chlewey/leading_the_jump} % blues-rock, 2026']),
        ('The Colombian Trap (Ricochets)', [r'\input{rataflechera/the_lens_cannot_know} % alternative-rock, 2026']),
        (r'Debates, Satires \& Systems', [r'\input{rataflechera/draw_the_line} % rock-n-roll, 2026']),
    ],
    'generos.tex': [
        ('European Threads — French \\& Nordic', [r'\input{chlewey/the_same_colombia} % folk-rock, 2026']),
        (r'Ballads \& Bare Folk', [r'\input{dvigitt/dvigitt_at_the_table} % folk, 2026',
                                  r'\input{gabisson/a_ground_i_choose} % folk-pop, 2026',
                                  r'\input{gabisson/leave_the_door_unlatched} % folk-pop, 2026']),
        (r'Country \& Outlaw', [r'\input{wyomee/her_leaving_never_left} % country-folk, 2026']),
        (r'Chant \& Bardcore', [r'\input{wyomee/under_aachen_sky} % medieval-epic, 2026']),
    ],
    'electronica.tex': [
        ('Obsidian Shutter (Gothic Lights)', [r'\input{rataflechera/mueca_pantera} % ambient-dubstep, 2026']),
        ('The Crossfire Beats (Ricochets)', [r'\input{rataflechera/margot} % synth-pop, 2026']),
    ],
}

NEW_CHAPTER = r'''\chapter{Meta and adjacent}
\albumcover{covers/entourage-eco/meta-and-adjacent}
Not canon: songs about the making of the universe and its near neighbours -- the creative process behind \emph{Thomas' Entourage}, and Gabi's reasons for never marrying Thomas for a visa.
\clearpage\begin{multicols*}{4}
\input{dvigitt/into_the_digital_night}
\input{dvigitt/a_little_universe}
\input{gabisson/a_ground_i_choose}
\input{gabisson/leave_the_door_unlatched}
\end{multicols*}
'''

MOVE_OUT = [r'\input{dvigitt/into_the_digital_night}', r'\input{dvigitt/a_little_universe}']

for fname, edits in PLAN.items():
    p = Path(fname)
    text = p.read_bytes().decode('utf-8')
    eol = '\r\n' if '\r\n' in text else '\n'
    lines = text.split(eol)

    if fname == 'entourage-eco.tex':
        before = len(lines)
        lines = [l for l in lines if l.strip() not in MOVE_OUT]
        print(f'{fname}: removed {before - len(lines)} line(s) to move into new chapter')

    for title, new_lines in edits:
        target = '\\chapter{' + title + '}'
        starts = [i for i, l in enumerate(lines) if l.strip() == target]
        if len(starts) != 1:
            print(f'!! {fname}: chapter {title!r} matched {len(starts)} times, skipping')
            continue
        end = next(i for i in range(starts[0], len(lines)) if lines[i].strip() == '\\end{multicols*}')
        lines[end:end] = new_lines
        print(f'{fname}: +{len(new_lines)} in {title}')

    if fname == 'entourage-eco.tex':
        drafts = [i for i, l in enumerate(lines) if l.strip() == '\\chapter{Drafts}']
        assert len(drafts) == 1
        lines[drafts[0]:drafts[0]] = NEW_CHAPTER.split('\n')[:-1] + ['']
        print(f'{fname}: new chapter Meta and adjacent inserted before Drafts')

    p.write_bytes(eol.join(lines).encode('utf-8'))
