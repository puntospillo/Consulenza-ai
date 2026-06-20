---
name: edit-bundle
description: Modificare index.html di Consulenza-ai (gestionale NPS Computer Assistenza & Consulenza). Usare SEMPRE questa skill prima di toccare index.html in questo progetto - spiega come editare in sicurezza un bundle React minificato a riga unica senza sorgenti, dove sono le funzioni principali, e il workflow di verifica/pubblicazione.
---

# Modificare index.html (Consulenza-ai)

## Cos'è questo progetto
`index.html` è un **bundle React già compilato e minificato in un'unica riga** (~1.6MB), output di un tool tipo `vite-plugin-singlefile`. **Non esistono file sorgente** (niente `src/`, niente componenti separati). È l'unico artefatto: leggerlo per intero con `Read` o `cat` è costosissimo in token e va evitato.

L'app è il gestionale "Assistenza & Consulenza" di NPS Computer:
- **Consulenza**: progetti, ore/time-entry, fatturazione, statistiche, report
- **Assistenza**: clienti, contratti, interventi, tecnici, fornitori, import Excel
- Login Microsoft (MSAL/Azure AD), dati su OneDrive/Excel via Microsoft Graph
- Pubblicato anche su GitHub Pages: `https://puntospillo.github.io/Consulenza-ai/`
- Repo: `github.com/puntospillo/Consulenza-ai`, branch `main`

## Workflow per ogni modifica

1. **Non leggere mai il file intero.** Usa `grep -oE` o script `python3` con `data.find(...)` per individuare la porzione di codice rilevante, stampando solo un intorno (es. `data[idx-500:idx+2000]`).

2. **Trova la funzione/JSX rilevante** partendo da una stringa di testo visibile nell'UI (es. `"Contratti"`, `"Statistiche Assistenza"`) o da un nome di funzione noto (vedi mappa sotto).

3. **Applica la modifica con un mini-script Python**, mai con `sed` su una riga di 1.6MB:
   ```python
   import re
   with open('index.html', encoding='utf-8') as f:
       data = f.read()

   def replace_unique(data, old, new, label):
       n = data.count(old)
       if n != 1:
           print(f"FAIL [{label}]: found {n} occurrences")
           return data, False
       return data.replace(old, new, 1), True

   data, ok = replace_unique(data, "STRINGA_ESATTA_DA_TROVARE", "STRINGA_NUOVA", "etichetta")
   if ok:
       with open('index.html', 'w', encoding='utf-8') as f:
           f.write(data)
   ```
   Usa sempre `replace_unique` (count deve essere esattamente 1) per evitare di colpire occorrenze multiple per errore.

4. **Verifica subito la sintassi JS** dopo ogni batch di modifiche:
   ```bash
   node -e "
   const fs = require('fs');
   const data = fs.readFileSync('index.html','utf8');
   const m = data.match(/<script type=\"module\" crossorigin>([\s\S]*?)<\/script>/);
   try { new Function(m[1]); console.log('SYNTAX OK'); } catch(e) { console.log('SYNTAX ERROR:', e.message); }
   "
   ```

5. **Testa in locale** prima di pubblicare:
   ```bash
   cd "/Users/mauriziopagani/Desktop/Claude_Code/Consulenza-ai" && python3 -m http.server 8765 &
   ```
   poi apri `http://localhost:8765/index.html`.

6. **Commit e push** (chiedi sempre conferma prima del push):
   ```bash
   git add index.html && git commit -m "..." && git push origin main
   ```
   Le credenziali sono già salvate nel Keychain dell'utente (Personal Access Token), il push funziona senza richiedere username/password.

## Mappa delle funzioni/variabili chiave (nomi minificati, possono cambiare a ogni build)

Variabili a singola lettera sono riusate ovunque nel bundle con significati diversi per scope — **non assumere il significato da altri punti del file**, verifica sempre nel contesto locale.

**Stato app principale** (`function jle()`):
- `o` / `s` = modalità app: `consulting` (Consulenza) o `assistance` (Assistenza) — bottoni nel menu, default impostato su `assistance`
- `n` / `r` = pagina attiva lato Consulenza (`dashboard`, `clients`, `tecnici`, `stats`, `report`, `registers`, `sync`)
- `c` / `l` = pagina attiva lato Assistenza (`a_dashboard`, `a_anagrafica`, `a_contracts`, `a_interventi`, `a_tecnici`, `a_fornitori`, `a_fatture`, `a_report`, `a_stats`, `a_import`)

**Funzioni di calcolo riutilizzabili:**
- `KI(e,t,n,r)` — calcolo uso/residuo ore di un contratto Assistenza (per tipo: tecnica/sistemistico/specialistico/consulenza). Ritorna `{perType, totaleContratto, totaleUsate, totaleResiduo, pctResiduo, inScadenza, esaurito}`. `esaurito` è vero se `(contrattate>0 || usate>0) && residuo<=0` (fixato per coprire anche contratti a 0 ore con interventi scalati)
- `JI(e,t)` — wrapper di `KI` per un contratto: `JI(state, contract)`
- `ZI(entry, tecnici)` — costo tecnico per un **intervento Assistenza** (campo `oreImpiegate`)
- `sL(entry, tecnici)` — costo tecnico per una **time-entry Consulenza** (campo `hours`)
- `cL(project, tecnici)` — somma `sL` su tutte le timeEntries di un progetto
- `wle(state, workbook, force)` — parser import Excel Assistenza (Fornitori/Tecnici/Clienti/Contratti/Interventi); `force=true` sovrascrive i duplicati invece di saltarli
- `nrm(str)` — normalizza nomi (minuscole, accenti, punteggiatura, rimuove forme societarie Srl/SpA/Snc/Sas) per il matching fuzzy nell'import

**Componenti principali (nomi minificati — cercali per testo UI, non per nome):**
- `fle` = vista Contratti (Assistenza, lista card)
- `ple` = vista dettaglio singolo Contratto
- `xle` = Statistiche Assistenza
- `Tle` = Import & Impostazioni
- `Vle` = Statistiche & BI Consulenza
- `Hle` = Report Consulenza (tabulati, con export CSV)
- `Ple` = vista dettaglio Progetto Consulenza
- `Rle` = tabella ore/time-entries dentro un Progetto
- `mle` = vista Interventi (Assistenza, lista/tabella + filtri)
- `cle` = form Nuovo/Modifica Intervento (modal aperto da `mle`)

**Regola di business "interventi da assegnare"** (vedi anche memoria `consulenza-ai-interventi-da-assegnare`): SEMPRE `stato==='da_assegnare'` OPPURE `!tecnicoId` (nessun tecnico assegnato), non solo lo stato. Variabile `daAss` in `mle` implementa questa unione.

**Sync automatico Consulenza→Intervento**: in `Rle` (tabella ore progetto), la funzione `syncInt(entry, project)` crea/aggiorna/rimuove un Intervento collegato (campo `entry.linkedInterventoId`) ogni volta che una time-entry ha `billingStatus==='contratto'` e `contractId` impostato, così le ore scalano davvero il contratto (tramite la stessa logica di `KI`/`JI` usata in Assistenza). Richiede che `appState`/`setAppState` (lo stato globale e il suo setter da `jle`) siano passati come prop fino a `Rle`, attraverso `Ple`. Se la time-entry non ha un tecnico assegnato, **alla prima sincronizzazione** chiede il nome con `prompt()` (solo una volta: i sync successivi su una entry già collegata non richiedono più input).

**IMPORTANTE — niente doppio conteggio**: `KI()` calcola il consumo di un contratto **solo** dai record in `e.interventi` (incluso il tipo `consulenza`, popolato dal sync sopra). NON deve più leggere direttamente `qI()` (le time-entries Consulenza) per evitare di contare due volte le stesse ore — è già successo una volta (bug corretto il 19/06/2026). `qI()` esiste ancora come funzione ma non va più usato per il calcolo di `KI`.

**Backfill storico**: in `Tle` (Import & Impostazioni) c'è un bottone "Sincronizza ore Consulenza su contratti" che crea retroattivamente gli Interventi collegati per le time-entries `billingStatus==='contratto'` già esistenti ma senza `linkedInterventoId` (caso tipico: dati registrati prima che il sync automatico esistesse).

**`qle` (modal Registra/Modifica ore Consulenza)**: ora supporta sia creazione che modifica tramite il prop opzionale `initial` (se presente, precompila i campi, mostra "Modifica voce ore" come titolo, e preserva `id`/`linkedInterventoId` al salvataggio). In `Rle` l'editing delle righe non è più inline: la matita apre `qle` in modalità edit; solo Ore/Tariffa/Stato restano modificabili al volo direttamente nella tabella.

**Convenzioni Assistenza consolidate (19-20/06/2026):**
- **Ordinamento interventi**: ovunque si elenchino interventi singoli (mle, ple, vL/Ele) si ordina per **data di inserimento** (`createdAt`) decrescente, NON per data intervento. Pattern: `.sort((e,t)=>(t.createdAt??\`\`).localeCompare(e.createdAt??\`\`))`.
- **Costo/Ricavi/Margine/Margine%**: ovunque si mostra il costo di un intervento (`ZI(intervento,tecnici)`) si mostra anche il ricavo figurativo (`uL(intervento,contratti)`), il margine (`ricavi-costo`) e la margine% (`ricavi>0?margine/ricavi*100:0`). Componenti coinvolti: `mle` (lista interventi), `ble` (Report Assistenza: cards in alto, riepilogo per cliente, righe tabella), `xle` (Statistiche Assistenza: cards in alto e tabelle per categoria via `h()`), `_le` (Fornitori, via `QI()` estesa con ticket/ricavi), `Ele` (Fatture Fornitori).
- **`uL(intervento,contratti)`** ha sempre un `return 0` finale esplicito per il caso `gratuito` — NON rimuoverlo, altrimenti torna `undefined` e qualsiasi somma con `+=` diventa `NaN` (bug reale corretto il 19/06/2026).
- **N° Ticket vicino al N° intervento**: quando una tabella elenca interventi singoli e non ha già una colonna Ticket, va aggiunta subito dopo la colonna N°.
- **Attenzione ai colSpan**: ogni volta che si aggiunge una colonna a una tabella, va aggiornato anche il `colSpan` della riga "nessun risultato" — è facile sbagliare il conteggio (succedeva il 20/06/2026 sia in `_le` che in `Ele`).
- **`F9(state)`** è l'hook condiviso di filtro Interventi usato da `ble` e `xle`: include già client/tecnico/fornitore/tipo/modalità/stato/fatturazione/periodo. Se manca un filtro "per tipo" in un report Assistenza, controllare prima se è già incluso qui (probabilmente sì) prima di aggiungerlo di nuovo.

**ATTENZIONE — due cose diverse si chiamano "ticket", non confonderle (chiarito il 20/06/2026):**
- **`t.numeroTicket`** = il numero ticket dell'helpdesk inserito manualmente sull'intervento (campo testo libero). È QUESTO il campo "Ticket" che va sempre mostrato di fianco al N° intervento in ogni vista, ed è già incluso nella ricerca testuale di `mle`.
- **`lL(intervento)`** = ticket CALCOLATI dal consumo ore (1 ora tecnica onsite/remoto → N ticket, è una metrica derivata, non un campo dati). Quando si mostra questo valore (somme aggregate di "ticket consumati" in Statistiche/Report/Fornitori), l'etichetta deve essere **"Ticket cons."**, mai solo "Ticket" — altrimenti si confonde con `numeroTicket`. Errore reale fatto e poi corretto il 20/06/2026 in `_le`, `xle`, `ble`, `mle` (card riepilogo).

**Per ritrovare una funzione dopo un redeploy/rebuild**: cerca per testo visibile nell'interfaccia (es. `grep -oE '.{0,30}children:\`Statistiche Assistenza\`.{0,30}' index.html`), non fidarti dei nomi minificati salvati qui — possono cambiare se il progetto viene rigenerato.

## Attenzione

- I parametri a singola lettera vengono **shadowati** di continuo in closure annidate (es. `e`, `t`, `n`, `r` cambiano significato dentro ogni `.map()`/`.reduce()` annidato). Prima di riusare una variabile "esterna" dentro una closure profonda, verifica che non sia già stata ridichiarata con `let`/destructuring nello stesso scope — altrimenti referenzi il valore sbagliato.
- Non rifattorizzare/rinominare in chiaro il codice minificato: il rischio di rompere riferimenti incrociati è alto e il guadagno di leggibilità è minimo dato che resta comunque un file generato.
- Se una modifica richiede di toccare più di ~10 punti diversi del file, valuta con l'utente se non sia più sensato chiedere il progetto sorgente (se esiste) invece di continuare a patchare il bundle.
