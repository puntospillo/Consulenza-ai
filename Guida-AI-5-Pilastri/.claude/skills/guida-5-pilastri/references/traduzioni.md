# Multilingua: come funziona e come si aggiunge una traduzione

Lingue: **it** (originale), **en**, **es**, **fr**. Selettore a bandierine nella barra in alto.

## Principio

L'italiano resta **scritto nel codice** e fa da rete di sicurezza. Le altre lingue sono *sovrascritture* per chiave:

```js
tr('p1-craft.titolo', 'La formula CRAFT')
```

- Se la lingua scelta ha la chiave, mostra la traduzione.
- Se non ce l'ha, mostra l'italiano passato come secondo argomento.

Così la guida funziona sempre, anche con traduzioni incomplete, e si può tradurre a blocchi.

## Variabili dentro i testi

Le parti dinamiche non si scrivono con `${}` dentro le traduzioni: si usano segnaposto tra graffe.

```js
tr('x.y', 'Come si fa in {tool}', {tool: toolName()})
```

## Dove stanno le traduzioni

- Sorgente: `traduzioni/en.json`, `traduzioni/es.json`, `traduzioni/fr.json` (chiave → testo).
- Nel file HTML vengono iniettate dallo script di costruzione, dentro il blocco delimitato da:

```js
/* === TRADUZIONI: generato da scripts/costruisci.py, non modificare a mano === */
const TXT = { … };
/* === FINE TRADUZIONI === */
```

Comando:

```bash
python3 .claude/skills/guida-5-pilastri/scripts/costruisci.py
```

## Come tradurre un blocco senza consumare troppo

1. `python3 .claude/skills/guida-5-pilastri/scripts/estrai.py p1-craft` → elenca le chiavi di quel blocco con il testo italiano.
2. Scrivi le tre traduzioni nei rispettivi JSON (solo le chiavi nuove).
3. Ricostruisci e verifica.

Non rileggere l'intero HTML per tradurre: lavora sulle chiavi.

## Regole di traduzione

- **Esempi invariati**: fatture, IVA, bandi, nomi italiani restano come sono, tradotti alla lettera. Non si adattano ai contesti locali.
- **Nomi dei menu nella lingua vera dell'interfaccia**: es. *Impostazioni › Controlli dati* → EN *Settings › Data controls*, ES *Configuración › Controles de datos*, FR *Paramètres › Contrôles des données*. Se un nome non è certo, lasciare l'inglese tra parentesi.
- **Nomi dei prodotti non si traducono**: Work, Codex, Cowork, Claude Code, Artifact, Gem, Notebook, Antigravity, Sites, Canvas, Deep Research, skill, prompt, token.
- Tono: semplice e diretto come in italiano; dare del "lei" solo negli esempi di testi formali.
- Tutte e quattro le lingue devono avere lo **stesso numero di lezioni, ricette, skill e domande del quiz**: si traduce, non si riscrive.

## Stato: traduzione completa (Rev. 2.1)

Tutti i testi delle 42 lezioni, il ricettario (52 casi), il glossario, il quiz e
**tutti gli strumenti interattivi** (costruttore CRAFT, generatori di prompt per
mini-app/PRD/agenti/file di istruzioni/skill, mappa delle attività da delegare,
con i relativi preset di esempio) sono tradotti al 100% in en/es/fr.

Se in futuro si aggiunge testo italiano nel codice, per riprendere il lavoro:

```
python3 .claude/skills/guida-5-pilastri/scripts/estrai.py b --manca en
```

Restituisce le chiavi `b.<hash>` non ancora tradotte (create da
`scripts/collega-lezioni.py` per i corpi delle lezioni; le stesse chiavi si
riusano per qualsiasi nuovo testo aggiunto a mano con `tr('b.<hash>', 'Italiano')`).
Si lavora a lotti di circa 6.500 caratteri, si traduce in en/es/fr in un unico
file JSON `{"en":{…},"es":{…},"fr":{…}}` e si unisce con:

```
python3 .claude/skills/guida-5-pilastri/scripts/aggiungi-multi.py < lotto.json
python3 .claude/skills/guida-5-pilastri/scripts/costruisci.py
python3 .claude/skills/guida-5-pilastri/scripts/verifica.py
```

Regole di traduzione già applicate: registro informale ("tu") in tutte le lingue,
markup HTML e nomi dei file invariati, esempi italiani tradotti ma non localizzati.

### Attenzione: `estrai.py`/`verifica.py` non vedono tutto

Gli array di primo livello valutati una sola volta al caricamento (es. `PRESETS`,
`SKILL_PRESETS`, `APP_PRESETS`, `AGENT_PRESETS`, `MAP_EXAMPLE`, `FILE_TIPI`,
`USCITE`) non sono dentro un `body:()=>`, quindi il codemod originale non li ha
mai toccati. Sono stati tradotti a mano in questa sessione con lo stesso schema
`campo` + `campoK:'b.<hash>'`, letto a runtime con `tr(obj.campoK, obj.campo)`
(vedi `applyPreset`/`presetLabel` in cima al file). Se si aggiungono nuove voci a
questi array, vanno wrappate allo stesso modo — altrimenti restano in italiano
senza che `verifica.py` se ne accorga (conta solo le chiamate `tr('b.…', …)`
scritte come stringa letterale). Per lo stesso motivo `verifica.py` segnala come
"chiavi non più usate" quelle referenziate via variabile (es. `tr(val[k+'K'], …)`
o `tr('ric.'+i+'.p', …)`): sono falsi positivi, non vanno rimosse dai file
`traduzioni/*.json`.
