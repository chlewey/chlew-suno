import re
import argparse
import os
import shutil
import sys

def maketag(title):
    tag = re.sub(r'[-\'’:\\\(\)¿\?,¡!/]', '', title.lower())
    tag = re.sub('[ñ&]', 'n', tag)
    tag = re.sub('[áäâà]', 'a', tag)
    tag = re.sub('[éèêë]', 'e', tag)
    tag = re.sub('[íìîï]', 'i', tag)
    tag = re.sub('[óöòô]', 'o', tag)
    tag = re.sub('[úü]', 'u', tag)
    tag = re.sub('[æ]', 'ae', tag)
    tag = re.sub('[øœ]', 'oe', tag)
    tag = re.sub('[å]', 'aa', tag)
    tag = re.sub('[þð]', 'th', tag)
    tag = re.sub(' ', '_', tag)
    tag = re.sub('_+', '_', tag)
    return tag


def build_parser():
    parser = argparse.ArgumentParser(
        description='Split a LaTeX song collection into individual files.'
    )
    parser.add_argument('input', nargs='?', help='Input file. If omitted, read stdin.')
    parser.add_argument('output', nargs='?', help='Combined output file.')
    parser.add_argument('-d', '--dir', dest='directory', help='Default target directory.')
    parser.add_argument(
        '-m', '--modify', action='store_true',
        help='Write the combined output back to the input file.'
    )
    parser.add_argument(
        '-b', '--backup', nargs='?', const='bak',
        help='Back up the input before modifying it, optionally using this extension.'
    )
    parser.add_argument(
        '-r', '--regex-fix', action='store_true',
        help='Apply regex fixes to generated song files.'
    )
    return parser


def parse_directive(line):
    match = re.match(
        r'^\s*%!\s*dir\s*=\s*(.*?)\s*(?:;\s*scope\s*=\s*(next|keep)\s*)?$',
        line,
    )
    if not match:
        return None
    return match.group(1), match.group(2)


def regex_fix(text):
    text = re.sub(
        r'\[((Vers|(Pre-|Final )?Chorus|Bridge|Breakdown|Intro|Outro|Movement|Chapter|Contra|Counter)[^\]\[]*)\]',
        r'\\songpart{\1}',
        text,
    )
    text = re.sub(r'([^\s\\\}%])( *\n[¿¡“\w])', r'\1\\\\\2', text)
    return re.sub(r'\[([^\]\[]*)\]', r'\\annotation{\1}', text)


def split_songs(text, default_directory):
    bang_line_re = re.compile(r'(?m)^\s*%![^\r\n]*(?:\r?\n|$)')
    directory = default_directory
    next_directory = None
    scope = 'keep'
    regex_enabled = bool(re.search(r'(?mi)^\s*%!\s*regex-fix\s*=\s*true\s*$', text))
    songs = []
    cursor = 0

    title_re = re.compile(r'\\songtitle\{([^{}]*)\}\s*')
    matches = list(title_re.finditer(text))
    if not matches:
        return bang_line_re.sub('', text), []
    preamble = ''

    for index, title_match in enumerate(matches):
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        between = text[cursor:title_match.start()]
        directives = [parse_directive(line) for line in bang_line_re.findall(between)]
        for directive in directives:
            if directive:
                target, explicit_scope = directive
                if explicit_scope:
                    scope = explicit_scope
                if scope == 'next':
                    next_directory = target
                else:
                    directory = target

        body = text[title_match.end():body_end]
        body = bang_line_re.sub('', body)
        target_directory = next_directory or directory
        songs.append((title_match.group(1), body, target_directory))
        next_directory = None
        cursor = title_match.end()

        if index == 0:
            preamble = bang_line_re.sub('', text[:title_match.start()])

    return preamble, songs, regex_enabled


if __name__ == '__main__':
    args = build_parser().parse_args()
    ifilename = args.input
    if (args.modify or args.backup is not None) and not ifilename:
        build_parser().error('--modify and --backup require an input file')
    if (args.modify or args.backup is not None) and args.output:
        build_parser().error('an output file cannot be used with --modify or --backup')
    ofilename = ifilename if args.modify or args.backup is not None else args.output
    if ifilename:
        with open(ifilename, 'r', encoding='utf-8-sig') as f:
            text = f.read()
        input_path, ext = os.path.splitext(ifilename)
        default_directory = args.directory or input_path
    else:
        text = sys.stdin.read()
        ext = '.tex'
        default_directory = args.directory or '.'

    if args.backup is not None:
        backup_ext = args.backup.lstrip('.') or 'bak'
        shutil.copy2(ifilename, f'{ifilename}.{backup_ext}')

    ofile = open(ofilename, 'w', encoding='utf-8') if ofilename else sys.stdout

    preamble, songs, directive_regex_fix = split_songs(text, default_directory)
    regex_enabled = args.regex_fix or directive_regex_fix
    ofile.write(preamble)
    for title, body, path in songs:
        os.makedirs(path, exist_ok=True)
        base = maketag(title)
        fnb, fn = f'{path}/{base}', f'{path}/{base}{ext}'
        j = 0
        while os.path.exists(fn):
            j += 1
            fnb, fn = f'{path}/{base}_{j}', f'{path}/{base}_{j}{ext}'

        ofile.write(f'\\input{{{fnb}}}\n')
        with open(fn, 'w', encoding='utf-8') as f:
            song_text = f'\\songtitle{{{title}}}\n\n{body}'
            f.write(regex_fix(song_text) if regex_enabled else song_text)
    if ofilename:
        ofile.close()
