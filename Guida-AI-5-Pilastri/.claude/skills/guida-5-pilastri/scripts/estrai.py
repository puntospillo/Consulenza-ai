#!/usr/bin/env python3
"""Estrae le chiavi di traduzione dalla guida.

Uso:
  estrai.py                      elenco dei gruppi di chiavi e stato delle traduzioni
  estrai.py p1-craft             chiavi di quel gruppo, con il testo italiano
  estrai.py p1-craft --manca en  solo le chiavi non ancora tradotte in inglese, in JSON
"""
import json, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
HTML = os.path.join(BASE, 'Guida-AI-5-Pilastri.html')
TRAD = os.path.join(BASE, 'traduzioni')


def leggi_stringa(s, i):
    """Legge la stringa JS che inizia a s[i] ('...', "..." o `...`). Restituisce (testo, indice dopo)."""
    q = s[i]
    if q not in "'\"`":
        return None, i
    out, i = [], i + 1
    while i < len(s):
        c = s[i]
        if c == '\\':
            nxt = s[i + 1]
            out.append({'n': '\n', 't': '\t'}.get(nxt, nxt)); i += 2; continue
        if c == q:
            return ''.join(out), i + 1
        out.append(c); i += 1
    raise ValueError('stringa non chiusa')


def chiavi():
    s = open(HTML, encoding='utf-8').read()
    fuori = []
    for m in re.finditer(r"\btr\(\s*'([^']+)'\s*,\s*", s):
        testo, _ = leggi_stringa(s, m.end())
        fuori.append((m.group(1), testo if testo is not None else ''))
    # chiavi costruite a runtime: lezioni, pilastri, gruppi
    for m in re.finditer(r"L\(\{id:'([^']+)', p:(?:null|'[^']*'),(?: lv:\d+,)? t:'([^']*)', sub:'([^']*)'", s):
        fuori.append((m.group(1) + '.t', m.group(2)))
        fuori.append((m.group(1) + '.sub', m.group(3)))
    for m in re.finditer(r"(p[1-5]):\{n:'[^']*',\s*t:'([^']*)',\s*short:'([^']*)',[^}]*?det:'([^']*)'", s):
        fuori.append(('pil.%s.t' % m.group(1), m.group(2)))
        fuori.append(('pil.%s.short' % m.group(1), m.group(3)))
        fuori.append(('pil.%s.det' % m.group(1), m.group(4)))
    for nome, suff in (('TOOL_INTRO', 'intro'), ('TOOL_MODELS', 'mod')):
        blocco = re.search(r"const %s = \{(.*?)\n\};" % nome, s, re.S)
        if blocco:
            for m in re.finditer(r"(chatgpt|claude|gemini)\s*:\s*", blocco.group(1)):
                testo, _ = leggi_stringa(blocco.group(1), m.end())
                if testo is not None:
                    fuori.append(('tool.%s.%s' % (m.group(1), suff), testo))
    for m in re.finditer(r"\['(?:null|[a-z0-9]+)','([^']+)','#[0-9a-f]+','[^']*','(gr\.[a-z0-9]+)'\]", s):
        fuori.append((m.group(2), m.group(1)))
    for m in re.finditer(r"\[null,'([^']+)','#[0-9a-f]+','','(gr\.[a-z0-9]+)'\]", s):
        fuori.append((m.group(2), m.group(1)))
    # dati strutturati: ricette, skill, casi, quiz, etichette
    def blocco(nome):
        m = re.search(r"const %s = \[(.*?)\n\];" % nome, s, re.S)
        return m.group(1) if m else ''

    def campi(testo, chiavi):
        """Scorre le voci di un array di oggetti e restituisce i campi richiesti."""
        voci, i, liv = [], 0, 0
        inizio = None
        while i < len(testo):
            c = testo[i]
            if c in "'\"`":
                _, i = leggi_stringa(testo, i); continue
            if c == '{':
                if liv == 0: inizio = i
                liv += 1
            elif c == '}':
                liv -= 1
                if liv == 0 and inizio is not None:
                    voci.append(testo[inizio:i + 1]); inizio = None
            i += 1
        out = []
        for v in voci:
            d = {}
            for k in chiavi:
                m = re.search(r"(?:^|[{,\s])%s\s*:\s*" % k, v)
                if m:
                    try:
                        val, _ = leggi_stringa(v, m.end())
                    except ValueError:
                        val = None
                    if val is not None: d[k] = val
            mid = re.search(r"id\s*:\s*'([^']+)'", v)
            if mid: d['__id'] = mid.group(1)
            mo = re.search(r"[{,\s]o\s*:\s*\[", v)
            if mo:
                j, opzioni = mo.end(), []
                try:
                    while len(opzioni) < 4 and j < len(v):
                        if v[j] == ']': break
                        if v[j] in "'\"`":
                            val, j = leggi_stringa(v, j); opzioni.append(val)
                        else: j += 1
                except ValueError:
                    opzioni = []
                if opzioni: d['__o'] = opzioni
            out.append(d)
        return out

    for i, r in enumerate(campi(blocco('RICETTE'), ('t', 'sit', 'ott', 'p', 'tip'))):
        for k in ('t', 'sit', 'ott', 'p', 'tip'):
            if k in r: fuori.append(('ric.%d.%s' % (i, k), r[k]))
    for k_ in campi(blocco('SKILL_LIB'), ('t', 'quando', 'cartella', 'md')):
        if '__id' in k_:
            for k in ('t', 'quando', 'cartella', 'md'):
                if k in k_: fuori.append(('lib.%s.%s' % (k_['__id'], k), k_[k]))
    for i, c in enumerate(campi(blocco('CASI'), ('t', 'sit', 'cart', 'check', 'prompt'))):
        for k in ('t', 'sit', 'cart', 'check', 'prompt'):
            if k in c: fuori.append(('caso.%d.%s' % (i, k), c[k]))
    for i, q in enumerate(campi(blocco('QZ'), ('q', 'e'))):
        if 'q' in q: fuori.append(('qz.%d.q' % i, q['q']))
        for n, o in enumerate(q.get('__o', [])): fuori.append(('qz.%d.o%d' % (i, n), o))
        if 'e' in q: fuori.append(('qz.%d.e' % i, q['e']))
    for nome, pref, sub in (('QZ_ARG', 'qzarg', 'l'), ('RIC_LVL', 'riclvl', 'l'), ('TIPI', 'tipo', None)):
        m = re.search(r"const %s = \{(.*?)\};" % nome, s, re.S)
        if not m: continue
        for mm in re.finditer(r"\n?\s*([a-z]+)\s*:\s*\{", m.group(1)):
            corpo = m.group(1)[mm.end():]
            if sub:
                q = re.search(r"\b%s\s*:\s*" % sub, corpo)
                if q:
                    val, _ = leggi_stringa(corpo, q.end())
                    if val: fuori.append(('%s.%s' % (pref, mm.group(1)), val))
            else:
                for k in ('l', 'sol'):
                    q = re.search(r"\b%s\s*:\s*" % k, corpo)
                    if q:
                        val, _ = leggi_stringa(corpo, q.end())
                        if val: fuori.append(('tipo.%s.%s' % (mm.group(1), k), val))
    m = re.search(r"const RIC_CAT = \{(.*?)\};", s, re.S)
    if m:
        for mm in re.finditer(r"(\w+)\s*:\s*'([^']*)'", m.group(1)):
            fuori.append(('riccat.%s' % mm.group(1), mm.group(2)))
    for nome, pref in (('WHERE', 'where'), ('NEED', 'need')):
        m = re.search(r"const %s = \{(.*?)\n\};" % nome, s, re.S)
        if not m: continue
        for riga in m.group(1).split('\n'):
            mk = re.match(r"\s*(\w+)\s*:\s*\{(.*)\}", riga)
            if not mk: continue
            for mm in re.finditer(r"(chatgpt|claude|gemini|any)\s*:\s*'([^']*)'", mk.group(2)):
                fuori.append(('%s.%s.%s' % (pref, mk.group(1), mm.group(1)), mm.group(2)))
    vis, out = set(), []
    for k, v in fuori:
        if k not in vis: vis.add(k); out.append((k, v))
    return out


def carica(lang):
    p = os.path.join(TRAD, lang + '.json')
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def main():
    argv = sys.argv[1:]
    manca = None
    if '--manca' in argv:
        i = argv.index('--manca'); manca = argv[i + 1] if len(argv) > i + 1 else 'en'; argv = argv[:i] + argv[i + 2:]
    args = [a for a in argv if not a.startswith('--')]
    voci = chiavi()
    if not args and not manca:
        gruppi = {}
        for k, _ in voci:
            gruppi[k.split('.')[0]] = gruppi.get(k.split('.')[0], 0) + 1
        trad = {l: carica(l) for l in ('en', 'es', 'fr')}
        print('%-26s %6s %6s %6s %6s' % ('gruppo', 'chiavi', 'en', 'es', 'fr'))
        for g, n in sorted(gruppi.items()):
            ks = [k for k, _ in voci if k.split('.')[0] == g]
            print('%-26s %6d %6d %6d %6d' % (g, n, *[sum(1 for k in ks if k in trad[l]) for l in ('en', 'es', 'fr')]))
        print('\ntotale chiavi: %d' % len(voci))
        return
    sel = [(k, v) for k, v in voci if not args or any(k.split('.')[0] == a or k.startswith(a) for a in args)]
    if manca:
        d = carica(manca)
        sel = [(k, v) for k, v in sel if k not in d]
        print(json.dumps(dict(sel), ensure_ascii=False, indent=1))
        return
    for k, v in sel:
        print('%s\n  %s\n' % (k, v.replace('\n', '\n  ')))


if __name__ == '__main__':
    main()
