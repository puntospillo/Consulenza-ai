# Cartella della Guida AI · I 5 Pilastri

Qui vive `Guida-AI-5-Pilastri.html`: la guida AI per utenti non tecnici, in un unico file HTML (niente librerie, niente build), multilingua (it · en · es · fr).

## Prima di lavorarci

Leggi la skill `.claude/skills/guida-5-pilastri/SKILL.md`: contiene mappa del file, convenzioni, stato verificato degli strumenti AI, regole di traduzione, verifica e pubblicazione.

## Regole sempre valide

- **Non leggere tutto l'HTML**: è ~400 KB. Cerca con `grep -n`, leggi solo le righe che servono, modifica con sostituzioni verificate (`assert s.count(a)==1`).
- **Verifica prima di consegnare**: `python3 .claude/skills/guida-5-pilastri/scripts/verifica.py` e, per le modifiche visibili, la procedura nel browser (`references/verifica-browser.md`).
- **Aggiorna `const REV`** a ogni modifica e dì all'utente quale versione è stata salvata. Niente date né registro delle revisioni nella pagina.
- **Traduzioni**: si modificano i file in `traduzioni/` e si esegue `scripts/costruisci.py`. L'italiano resta nel codice come rete di sicurezza.
- **Pubblicazione solo su richiesta**: `bash .claude/skills/guida-5-pilastri/scripts/pubblica.sh "messaggio"`. Va online solo questo file; mai la cartella `AI 5 pilastri/` del consulente.
- **Istruzioni sugli strumenti AI**: ricontrollale sul web prima di scriverle, cambiano ogni poche settimane.

## File della cartella

- `Guida-AI-5-Pilastri.html` — l'app
- `RICREARE-QUESTA-APP.md` — documento per ricostruirla da zero in una chat nuova
- `traduzioni/` — `en.json`, `es.json`, `fr.json`
- `.claude/skills/guida-5-pilastri/` — skill di lavoro, riferimenti e script
