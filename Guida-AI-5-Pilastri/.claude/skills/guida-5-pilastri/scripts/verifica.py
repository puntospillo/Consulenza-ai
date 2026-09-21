#!/usr/bin/env python3
"""Controlli statici sulla guida. Uso: python3 .claude/skills/guida-5-pilastri/scripts/verifica.py"""
import json, os, re, subprocess, sys, tempfile

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
HTML = os.path.join(BASE, 'Guida-AI-5-Pilastri.html')
TRAD = os.path.join(BASE, 'traduzioni')

def main():
    s = open(HTML, encoding='utf-8').read()
    js = s[s.index('<script>') + 8:s.rindex('</script>')]
    problemi, note = [], []

    # 1. sintassi
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(js); tmp = f.name
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    os.unlink(tmp)
    if r.returncode: problemi.append('sintassi JS:\n' + r.stderr.strip())

    # 2. link interni
    ids = set(re.findall(r"L\(\{id:'([^']+)'", js))
    tos = set(re.findall(r"data-to=\\?\"([a-z0-9-]+)\\?\"", js)) | set(re.findall(r"go:'([a-z0-9-]+)'", js)) | set(re.findall(r"step:'([a-z0-9-]+)'", js))
    rotti = sorted(t for t in tos if t not in ids)
    if rotti: problemi.append('link a lezioni inesistenti: ' + ', '.join(rotti))

    # 3. id duplicati fra le lezioni
    out = re.findall(r"outBox\('([^']+)'", js)
    dup = sorted({x for x in out if out.count(x) > 1})
    if dup: note.append('id di outBox ripetuti (ok solo se in lezioni diverse): ' + ', '.join(dup))

    # 4. codice non usato
    nomi = re.findall(r"\bfunction (\w+)\(", js) + re.findall(r"\bconst (\w+) = (?:\(|\w+ =>|async)", js)
    inutil = sorted({n for n in nomi if len(re.findall(r'\b%s\b' % re.escape(n), js)) < 2})
    if inutil: note.append('definizioni mai usate: ' + ', '.join(inutil))

    # 5. traduzioni
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import estrai
    chiavi = set(k for k, _ in estrai.chiavi())
    if os.path.isdir(TRAD):
        for lang in ('en', 'es', 'fr'):
            p = os.path.join(TRAD, lang + '.json')
            if not os.path.exists(p):
                note.append('manca traduzioni/%s.json' % lang); continue
            d = json.load(open(p, encoding='utf-8'))
            manca = sorted(chiavi - set(d))
            extra = sorted(set(d) - chiavi)
            note.append('%s: %d/%d tradotte%s' % (lang, len(chiavi) - len(manca), len(chiavi),
                        (', %d chiavi non più usate' % len(extra)) if extra else ''))
            if extra: note.append('  chiavi da togliere da %s.json: %s' % (lang, ', '.join(extra[:8])))
    # 6. peso
    kb = len(s.encode('utf-8')) // 1024
    note.append('lezioni: %d · dimensione: %d KB · chiavi di traduzione: %d' % (len(ids), kb, len(chiavi)))
    if kb > 2048: problemi.append('file troppo grande: %d KB' % kb)

    for n in note: print('·', n)
    if problemi:
        print('\nPROBLEMI:')
        for p in problemi: print('✗', p)
        sys.exit(1)
    print('\n✓ Controlli statici superati. Ora la verifica nel browser (references/verifica-browser.md).')

if __name__ == '__main__':
    main()
