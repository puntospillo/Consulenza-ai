#!/usr/bin/env python3
"""Unisce un frammento JSON a una lingua. Uso: aggiungi.py en < frammento.json"""
import json, os, sys
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
lang = sys.argv[1]
p = os.path.join(BASE, 'traduzioni', lang + '.json')
d = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
nuovo = json.load(sys.stdin)
d.update(nuovo)
json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1, sort_keys=True)
print('%s: +%d voci, totale %d' % (lang, len(nuovo), len(d)))
