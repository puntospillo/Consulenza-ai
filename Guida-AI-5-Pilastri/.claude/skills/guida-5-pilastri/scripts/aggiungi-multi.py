#!/usr/bin/env python3
"""Unisce in un colpo solo le traduzioni delle tre lingue.

Uso:  aggiungi-multi.py < frammento.json
dove frammento.json è {"en": {chiave: testo, ...}, "es": {...}, "fr": {...}}
"""
import json, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
TRAD = os.path.join(BASE, 'traduzioni')


def main():
    nuovo = json.load(sys.stdin)
    for lang in ('en', 'es', 'fr'):
        voci = nuovo.get(lang)
        if not voci:
            print('%s: nessuna voce' % lang); continue
        p = os.path.join(TRAD, lang + '.json')
        d = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
        prima = len(d)
        d.update(voci)
        json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
        print('%s: +%d voci, totale %d' % (lang, len(d) - prima, len(d)))


if __name__ == '__main__':
    main()
