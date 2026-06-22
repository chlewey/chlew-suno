import re

def maketag(title):
    tag = re.sub(r'[-\'’:\\\(\)¿\?,¡!/]', '', title.lower())
    tag = re.sub('[ñ&]', 'n', tag)
    tag = re.sub('[áäâà]', 'a', tag)
    tag = re.sub('[éèêë]', 'e', tag)
    tag = re.sub('[íìîï]', 'i', tag)
    tag = re.sub('[óöòô]', 'o', tag)
    tag = re.sub('[úü]', 'u', tag)
    tag = re.sub(' ', '_', tag)
    tag = re.sub('_+', '_', tag)
    return tag
    
if __name__ == '__main__':
    import sys, os

    ofilename = sys.argv[2] if len(sys.argv)>2 else None
    ifilename = sys.argv[1] if len(sys.argv)>1 else None
    if ifilename:
        with open(ifilename, 'r', encoding='utf-8') as f:
            text = f.read()
        path, ext = os.path.splitext(ifilename)
    else:
        text = sys.stdin.read()
        path, ext = '.', '.tex'
    os.makedirs(path, exist_ok=True)

    ofile = open(ofilename, 'w', encoding='utf-8') if ofilename else sys.stdout
    
    parts = re.split(r'\\songtitle\{([^{}]*)\}\s*', text)
    ofile.write(parts[0])
    for i in range(1, len(parts), 2):
        base = maketag(parts[i])
        fnb, fn = f'{path}/{base}', f'{path}/{base}{ext}'
        j = 0
        while os.path.exists(fn):
            j += 1
            fnb, fn = f'{path}/{base}_{j}', f'{path}/{base}_{j}{ext}'

        ofile.write(f'\\input{{{fnb}}}\n')
        with open(fn, 'w', encoding='utf-8') as f:
            f.write(f'\\songtitle{{{parts[i]}}}\n\n')
            f.write(parts[i+1])
    ofile.close()
