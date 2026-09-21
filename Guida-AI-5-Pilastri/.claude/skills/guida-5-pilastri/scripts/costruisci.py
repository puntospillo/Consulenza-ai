#!/usr/bin/env python3
"""Inietta traduzioni/*.json dentro Guida-AI-5-Pilastri.html, nel blocco TRADUZIONI."""
import json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
HTML = os.path.join(BASE, 'Guida-AI-5-Pilastri.html')
TRAD = os.path.join(BASE, 'traduzioni')
INIZIO = '/* === TRADUZIONI: generato da scripts/costruisci.py, non modificare a mano === */'
FINE = '/* === FINE TRADUZIONI === */'

def main():
    s = open(HTML, encoding='utf-8').read()
    if INIZIO not in s or FINE not in s:
        sys.exit('Blocco TRADUZIONI non trovato nel file HTML.')
    dati = {}
    for lang in ('en', 'es', 'fr'):
        p = os.path.join(TRAD, lang + '.json')
        dati[lang] = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    blocco = INIZIO + '\nconst TXT = ' + json.dumps(dati, ensure_ascii=False, separators=(',', ':')) + ';\n' + FINE
    i, j = s.index(INIZIO), s.index(FINE) + len(FINE)
    open(HTML, 'w', encoding='utf-8').write(s[:i] + blocco + s[j:])
    print('Traduzioni iniettate: ' + ' · '.join('%s %d' % (l, len(d)) for l, d in dati.items()))
    print('Dimensione file: %d KB' % (os.path.getsize(HTML) // 1024))

if __name__ == '__main__':
    main()
