#!/usr/bin/env python3
"""Collega i testi delle lezioni alla funzione tr().

Percorre il blocco const LESSONS = [...] e avvolge ogni frammento di prosa in
tr('b.<hash>', <testo originale>). La chiave è l'hash del testo italiano: se il
testo cambia, cambia la chiave e la traduzione vecchia risulta "non più usata".

Uso:
  collega-lezioni.py            mostra cosa verrebbe modificato (prova a vuoto)
  collega-lezioni.py --scrivi   applica le modifiche al file
"""
import hashlib, io, os, re, sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
HTML = os.path.join(BASE, 'Guida-AI-5-Pilastri.html')

# un frammento è "prosa" se ha uno spazio e almeno quattro lettere di fila
PROSA = re.compile(r'[A-Za-zÀ-ÿ]{4}')


def chiave(testo):
    return 'b.' + hashlib.sha1(testo.encode('utf-8')).hexdigest()[:10]


def e_prosa(testo):
    t = testo.strip()
    if len(t) < 6 or ' ' not in t:
        return False
    # frammento di tag o di attributo spezzato da un'interpolazione: non è testo
    if t.count('<') != t.count('>') or t.count('"') % 2:
        return False
    if t.startswith('"') or t.endswith('"'):
        return False
    # deve restare del testo leggibile una volta tolti i marcatori
    visibile = re.sub(r'<[^>]*>', ' ', t).strip()
    return len(visibile) >= 8 and ' ' in visibile and bool(PROSA.search(visibile))


class Collegatore:
    def __init__(self, s):
        self.s = s
        self.out = []
        self.trovati = []

    def emit(self, t):
        self.out.append(t)

    def avvolgi(self, testo_sorgente, apri, chiudi):
        """Restituisce tr('b.x', <letterale>) se è prosa, altrimenti il letterale."""
        if not e_prosa(testo_sorgente):
            return apri + testo_sorgente + chiudi
        k = chiave(testo_sorgente)
        self.trovati.append((k, testo_sorgente))
        return "tr('%s',%s%s%s)" % (k, apri, testo_sorgente, chiudi)

    def stringa(self, i):
        """Legge il letterale che inizia a i. Restituisce (codice_nuovo, indice_dopo)."""
        s, q = self.s, self.s[i]
        if q != '`':
            j, buf = i + 1, []
            while j < len(s):
                if s[j] == '\\':
                    buf.append(s[j:j + 2]); j += 2; continue
                if s[j] == q:
                    break
                buf.append(s[j]); j += 1
            return self.avvolgi(''.join(buf), q, q), j + 1
        # template literal: alterna testo e ${ espressione }
        j, pezzi, testo = i + 1, [], []
        while j < len(s):
            if s[j] == '\\':
                testo.append(s[j:j + 2]); j += 2; continue
            if s[j] == '`':
                break
            if s.startswith('${', j):
                pezzi.append(('t', ''.join(testo))); testo = []
                espr, j = self.espressione(j + 2)
                pezzi.append(('e', espr))
                continue
            testo.append(s[j]); j += 1
        pezzi.append(('t', ''.join(testo)))
        if all(k == 't' for k, _ in pezzi):
            return self.avvolgi(pezzi[0][1], '`', '`'), j + 1
        fuori = ['`']
        for k, v in pezzi:
            if k == 't':
                if e_prosa(v):
                    fuori.append('${' + self.avvolgi(v, '`', '`') + '}')
                else:
                    fuori.append(v)
            else:
                fuori.append('${' + v + '}')
        fuori.append('`')
        return ''.join(fuori), j + 1

    def espressione(self, i):
        """Legge il contenuto di ${ ... } fino alla graffa di chiusura. Restituisce (codice, indice_dopo_})."""
        s, liv, out = self.s, 1, []
        j = i
        while j < len(s):
            c = s[j]
            if c in "'\"`":
                codice, j = self.stringa(j)
                out.append(codice); continue
            if s.startswith('tr(', j) and (j == 0 or not re.match(r'[\w$.]', s[j - 1])):
                codice, j = self.salta_tr(j)
                out.append(codice); continue
            if c == '{':
                liv += 1
            elif c == '}':
                liv -= 1
                if liv == 0:
                    return ''.join(out), j + 1
            out.append(c); j += 1
        raise ValueError('interpolazione non chiusa')

    def salta_tr(self, i):
        """Copia una chiamata tr(...) già esistente senza toccarla."""
        s, j, liv = self.s, i + 3, 1
        out = ['tr(']
        while j < len(s):
            c = s[j]
            if c in "'\"`":
                q = c; k = j + 1; buf = [c]
                while k < len(s):
                    if s[k] == '\\':
                        buf.append(s[k:k + 2]); k += 2; continue
                    if s[k] == q and q != '`':
                        break
                    if q == '`' and s[k] == '`':
                        break
                    buf.append(s[k]); k += 1
                buf.append(q)
                out.append(''.join(buf)); j = k + 1; continue
            if c == '(':
                liv += 1
            elif c == ')':
                liv -= 1
                if liv == 0:
                    out.append(')'); return ''.join(out), j + 1
            out.append(c); j += 1
        raise ValueError('tr( non chiusa')

    def esegui(self):
        s = self.s
        j = 0
        while j < len(s):
            c = s[j]
            if c in "'\"`":
                codice, j = self.stringa(j)
                self.emit(codice); continue
            if s.startswith('tr(', j) and (j == 0 or not re.match(r'[\w$.]', s[j - 1])):
                codice, j = self.salta_tr(j)
                self.emit(codice); continue
            if s.startswith('//', j):
                k = s.find('\n', j)
                k = len(s) if k < 0 else k
                self.emit(s[j:k]); j = k; continue
            self.emit(c); j += 1
        return ''.join(self.out), self.trovati


def fine_corpo(s, i):
    """Restituisce l'indice dopo il corpo della funzione che inizia a s[i] (` oppure {)."""
    c = Collegatore(s)
    if s[i] == '`':
        _, j = c.stringa(i)
        return j
    liv, j = 0, i
    while j < len(s):
        ch = s[j]
        if ch in "'\"`":
            _, j = c.stringa(j); continue
        if ch == '{':
            liv += 1
        elif ch == '}':
            liv -= 1
            if liv == 0:
                return j + 1
        j += 1
    raise ValueError('corpo della lezione non chiuso')


def main():
    s = io.open(HTML, encoding='utf-8').read()

    pezzi, trovati, pos = [], [], 0
    for m in re.finditer(r'body:\(\)=>', s):
        if m.start() < pos:
            continue
        i = m.end()
        j = fine_corpo(s, i)
        nuovo_corpo, t = Collegatore(s[i:j]).esegui()
        pezzi.append(s[pos:i]); pezzi.append(nuovo_corpo)
        trovati += t
        pos = j
    pezzi.append(s[pos:])
    nuovo = ''.join(pezzi)

    doppie = {}
    for k, t in trovati:
        doppie[k] = doppie.get(k, 0) + 1
    ripetute = sum(1 for v in doppie.values() if v > 1)

    print('frammenti collegati: %d (chiavi uniche %d, ripetute %d)' % (len(trovati), len(doppie), ripetute))
    print('caratteri di testo: %d' % sum(len(t) for t in {k: t for k, t in trovati}.values()))

    if '--scrivi' not in sys.argv:
        print('\nEsempi:')
        for k, t in trovati[:6]:
            print('  %s  %s' % (k, t.strip()[:90].replace('\n', ' ')))
        print('\nProva a vuoto: nessuna modifica scritta. Usa --scrivi per applicare.')
        return

    io.open(HTML, 'w', encoding='utf-8').write(nuovo)
    print('\nFile aggiornato.')


if __name__ == '__main__':
    main()
