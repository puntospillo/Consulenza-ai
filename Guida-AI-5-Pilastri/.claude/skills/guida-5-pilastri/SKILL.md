---
name: guida-5-pilastri
description: Usa questa skill quando lavori su Guida-AI-5-Pilastri.html (la guida AI in un solo file HTML, multilingua it/en/es/fr): aggiungere o modificare lezioni, ricette, skill della libreria, domande del quiz, istruzioni per ChatGPT/Claude/Gemini, traduzioni, verifica e pubblicazione. Serve a lavorare senza rileggere tutto il file.
---

# Guida AI · I 5 Pilastri — come lavorarci

App: un unico file `Guida-AI-5-Pilastri.html` (niente librerie, niente build, si apre con doppio clic). Multilingua: it · en · es · fr, selettore in alto nella pagina.
Pubblicata su GitHub Pages dal repo `puntospillo/Consulenza-ai`, alla URL `https://puntospillo.github.io/Consulenza-ai/Guida-AI-5-Pilastri/Guida-AI-5-Pilastri.html`.

## Regola d'oro: non rileggere tutto il file

`Guida-AI-5-Pilastri.html` è oltre 1,4 MB (il grosso sono le traduzioni iniettate in `const TXT`, tutte su una riga): leggerlo per intero costa moltissimo. Invece:

1. Trova il punto con `grep -n` (vedi `references/mappa-file.md` per i nomi dei blocchi).
2. Leggi solo quelle righe (`sed -n 'A,Bp'` o Read con offset/limit).
3. Modifica con uno script Python che fa `assert s.count(a)==1` prima di sostituire (vedi sotto).
4. Verifica con `scripts/verifica.py`.

## Modifica sicura (schema da riusare)

```bash
python3 - <<'EOF'
f='Guida-AI-5-Pilastri.html'; s=open(f).read()
def rep(a,b):
    global s
    c=s.count(a); assert c==1,(a[:80],c); s=s.replace(a,b)
rep("testo esatto da sostituire", "nuovo testo")
open(f,'w').write(s)
EOF
python3 .claude/skills/guida-5-pilastri/scripts/verifica.py
```

Se `assert` fallisce non è stato scritto nulla: il file resta integro.

## Dove intervenire (dettagli in `references/mappa-file.md`)

| Devi… | Vai a |
|---|---|
| Aggiungere/modificare una lezione | array `LESSONS`, chiamate `L({id, p, t, sub, min, body, update})` |
| Istruzioni per uno strumento | oggetto `HOW` (chiavi: modes, setup, personal, verify, file, project, assistant, skillUse, md, install, appChat, appLocal, appFull, agent, agentMd, tokens) |
| Etichette "dove farlo" | `WHERE`, `NEED`, `TOOL_INTRO`, `TOOL_MODELS`, `AGENT_MD` |
| Ricette | `RICETTE` (categorie `RIC_CAT`, livelli `RIC_LVL`) |
| Skill pronte | `SKILL_LIB` |
| Casi di agenti | `CASI` |
| Quiz | `QZ` (+ `QZ_ARG`; campo `t:'claude'` = domanda che compare solo con quello strumento) |
| Testi tradotti | `TXT` e file in `traduzioni/` (vedi `references/traduzioni.md`) |
| Versione mostrata | `const REV` |

**Attenzione con gli array/oggetti di primo livello** (`PRESETS`, `SKILL_PRESETS`, `APP_PRESETS`, `AGENT_PRESETS`, `MAP_EXAMPLE`, `FILE_TIPI`, `USCITE`, `QUIZ`, `DEC_Q`, le funzioni `*SVG()`): sono valutati una volta sola al caricamento, **fuori** da un `body:()=>`, quindi non li tocca il codemod che ha tradotto le lezioni. Se aggiungi testo italiano lì dentro, wrappalo a mano con `tr('b.<hash>', 'Italiano')` (per i campi di un preset, aggiungi anche `campoK:'b.<hash>'` e leggi con `tr(obj.campoK, obj.campo)`, come già fanno `applyPreset`/`presetLabel`) — altrimenti resta in italiano anche cambiando lingua, e `verifica.py` non se ne accorge. Dettagli in `references/traduzioni.md`.

## Convenzioni di contenuto

Sintesi in `references/convenzioni.md`. Le tre irrinunciabili:

- Chi legge è l'utente finale: mai parlare "del cliente" come soggetto esterno.
- Ogni istruzione operativa vale **solo per lo strumento scelto** (`howBox`, `byTool`, `where`): mai schede con tutti e tre.
- Dove si crea qualcosa serve il riquadro `aiMake(...)` "Fattelo creare dall'AI".

## Stato degli strumenti AI

`references/strumenti-2026.md`: cosa è stato verificato e quando. **Prima di scrivere istruzioni operative, ricontrolla sul web**: ChatGPT, Claude e Gemini cambiano ogni poche settimane.

### Aggiornare i modelli (checklist, per non rileggere tutto il file)

Quando esce un nuovo modello (GPT, Claude, Gemini), i punti da toccare sono sempre questi — tutti con chiavi di traduzione **fisse** (non content-addressed), quindi cambiare il testo italiano non rompe il lookup nelle altre lingue, ma le traduzioni esistenti restano vecchie finché non le aggiorni a mano:

| Punto nell'HTML | grep | Chiave in `traduzioni/*.json` |
|---|---|---|
| Riquadro modelli nella scelta strumento | `const TOOL_MODELS` | `tool.chatgpt.mod`, `tool.claude.mod`, `tool.gemini.mod` |
| Lezione token/consumo | `how.tokens.chatgpt.1` / `how.tokens.claude.2` (grep su `HOW =` → `tokens:`) | stessa chiave |
| Data di verifica mostrata in Benvenuto | `const AGG_DATA` | `ui.dataVerifica` (il valore di AGG_DATA stesso è la chiave italiana da tradurre) |
| Due domande del quiz (indice dinamico: conta le righe da `const QZ = [` incluso, parti da 0) | cerca il testo del modello dentro `const QZ = [` | `qz.<indice>.q`, `.o0..o3`, `.e` — oggi sono gli indici **63** (ChatGPT) e **66** (Claude); se aggiungi/togli domande gli indici cambiano, riconta |

Procedura:
1. Ricontrolla sul web i modelli attuali (nomi, date, piani).
2. Modifica l'HTML nei 4 punti sopra (schema `rep()` di `SKILL.md`).
3. Modifica le stesse chiavi in `traduzioni/en.json`, `es.json`, `fr.json` (lo script di costruzione non traduce da solo: va fatto a mano o con `scripts/aggiungi-multi.py`).
4. `python3 scripts/costruisci.py` poi `scripts/verifica.py`.
5. Aggiorna `references/strumenti-2026.md` (data in testa + la riga del produttore cambiato).
6. Bump `const REV`, verifica nel browser (sweep + residui italiano, `references/verifica-browser.md`), poi pubblica solo su richiesta.

## Verifica (obbligatoria prima di consegnare)

```bash
python3 .claude/skills/guida-5-pilastri/scripts/verifica.py
```

Controlla: sintassi dello script, link interni, id duplicati, testi non tradotti, funzioni non usate, peso del file.
In più, nel browser: aprire tutte le lezioni con i 4 stati strumento e a 400px di larghezza (procedura in `references/verifica-browser.md`).

## Pubblicazione

```bash
bash .claude/skills/guida-5-pilastri/scripts/pubblica.sh "messaggio del commit"
```

Pubblica **solo** `Guida-AI-5-Pilastri/Guida-AI-5-Pilastri.html`. Mai la cartella `AI 5 pilastri/`.
Aggiorna `const REV` prima di pubblicare e dì all'utente quale versione è stata salvata.
