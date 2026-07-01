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

**Flag "Stampa per cliente" (aggiunto 23/06/2026, in `Hle` e `ble`)**: checkbox `printClient`/`setPrintClient`, default `!0` (preimpostato ON). Quando ON nasconde SOLO in stampa (classe `print:hidden` applicata condizionalmente, mai sul video) i riferimenti a costo tecnico/margine: in `Hle` colonna "Costo tecnico" (header+celle+subtotale) e il segmento "Costo tecnici" nel TOTALE GENERALE; in `ble` colonne Costo/Margine/Margine% della tabella, i segmenti "costo"/"margine" nell'intestazione per-cliente, e l'intera riga di card riepilogo in alto (`grid ... mb-5`, nascosta per intero in stampa). Pattern: `className:printClient?\`...classi normali... print:hidden\`:\`...classi normali...\`` — mai una classe fissa, sempre condizionale sullo stato. Se si aggiunge un nuovo riferimento a costo/margine in questi due report, va wrappato con lo stesso pattern.

**Stampa Contratto (`lle(contratto,usage,interventi,clientName,tecnici)`)**: genera un HTML standalone in una nuova finestra (`window.open` + `print()`), NON è JSX/React — è un template a stringa con `<style>` inline. Colonne tabella: N°/Data/Tecnico/Tipo/Onsite/Stato/Ore/**Richiesta intervento**(`motivoRichiesta`, aggiunta 23/06/2026)/Descrizione. Il `colspan` della riga "Nessun intervento" deve sempre combaciare col numero di `<th>` (va aggiornato ogni volta che si aggiunge una colonna).

**Tutti i `<title>` dei popup di stampa hanno il prefisso "NPS "** (aggiunto 23/06/2026, regola: "quando salvi il pdf chiamalo NPS + nome stampa" — Chrome usa `document.title`/`<title>` come nome file predefinito per "Salva come PDF"): `lle` → `NPS Contratto ${numero}`, `O9` (Rapportino intervento) → `NPS Rapportino ${numero}`, `k9` (stampa generica, usata da Fornitori "Elenco interventi" e Statistiche Assistenza) → `NPS ${titolo}`. Se si aggiunge un nuovo template di stampa, dargli sempre questo prefisso.

**Report Consulenza (`Hle`) e Report Assistenza (`ble`) NON usano più `window.print()` sulla pagina live** (cambiato 23/06/2026, richiesta: "togli da tutti i report l'URL https://puntospillo.github.io/Consulenza-ai/"): stampare la SPA in-place mostra nel footer del browser l'URL della pagina (GitHub Pages), cosa che non si può disattivare via CSS — l'unico modo per eliminarlo è, come già faceva `lle`, generare l'HTML in una finestra popup separata (`window.open('','_blank')`+`document.write`, location `about:blank`) e stampare quella. Entrambi i Report ora hanno una funzione `printNow` (closure locale dentro il componente, usa le stesse variabili già calcolate per la vista a schermo — `x`/`S`/`C`/`T`/`printClient`/`tecArr` in `Hle`, `o`/`a`/`ctr`/`printClient`/`t`/`e`/`n` in `ble`) che ricostruisce la tabella come stringa HTML e apre il popup; il bottone "Stampa/PDF" chiama `printNow` invece di `window.print()`. **Se si modifica la vista a schermo di questi due report, ricordarsi di replicare la modifica anche nella corrispondente `printNow`** (sono due implementazioni parallele dello stesso contenuto, una JSX e una stringa HTML — non c'è componente condiviso). Titoli: `NPS ${T}` per Hle, `NPS Report Assistenza` per ble. Rispettano il flag `printClient` esattamente come la vista a schermo (stesse colonne nascoste).

**Verifica funzionale senza login Microsoft**: aprire l'app in locale (anche su `localhost`) reindirizza sempre al login MSAL reale (redirect URI registrato solo per `https://puntospillo.github.io/Consulenza-ai/`), quindi non si può testare a mano in locale. Per verificare che una modifica JSX non causi un crash silenzioso (es. variabile residua non più definita, bug reale capitato il 23/06/2026 in `Hle` dopo il refactor dei filtri condivisi — `f` non più esistente usato in `B9[f].toUpperCase()`), il modo più veloce è: estrarre lo script, iniettare `window.__T={NomeComponente,v,X,y}` subito prima della riga finale `(0,y.createRoot)...render(...)`, togliere `type="module"` dal tag `<script>` (jsdom non esegue gli script ESM anche con `runScripts:"dangerously"`), caricare il tutto in `jsdom` (`npm install jsdom` con `--cache` su una dir scrivibile se la cache npm di sistema è root-owned), e poi chiamare `T.y.createRoot(div).render(T.v.createElement(T.NomeComponente,{...props finti minimi}))` dentro un try/catch — qualunque eccezione runtime (variabile non definita, proprietà di `undefined`, ecc.) emerge subito nello stack trace, cosa che il solo controllo di sintassi (`new Function(...)`) non rileva.

**Quando fare anche il test jsdom (non solo `new Function`), deciso il 24/06/2026:** il controllo di sintassi basta per modifiche di basso rischio (testo, classi CSS, una colonna/campo in più, copy). Va aggiunto il test jsdom (mount reale del componente, eventualmente con click sul bottone rilevante per attivare una closure come `printNow`) quando la modifica tocca: refactor di stato/filtri condivisi tra più componenti (es. introduzione/cambio di un hook come `Vle2`), nuove funzioni di generazione HTML/print, o qualunque modifica che lasci variabili "orfane" da un pattern precedente (rinominare uno stato locale, sostituire una struttura dati). In quei casi il rischio di una variabile residua non più in scope è concreto e il solo parser JS non lo vede.

**Regola margine Consulenza (fissata il 20/06/2026)**: SOLO in Consulenza, `margine = imponibile - (costo tecnico + spese)`. `HI(progetto, tecnici=[])` ora accetta un secondo parametro tecnici e sottrae `cL(progetto,tecnici)` dal margine in tutti e 3 i rami (internal/fixed/hourly); espone anche `costoTec` nel suo oggetto di ritorno. **Ogni chiamata a `HI()` deve passare l'array tecnici** — i 4 punti che la chiamano sono `Mle` (dashboard, 2 volte), `Nle` (Clienti), `Ple` (dettaglio progetto). Se in futuro si aggiunge una nuova chiamata a `HI()`, ricordarsi il secondo argomento, altrimenti il margine torna sbagliato silenziosamente (default `[]` → costoTec=0). Questa regola NON si applica ad Assistenza, che ha formule di margine proprie e separate.

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
- `Zle` = vista Progetti (Consulenza, pagina full-size con la stessa logica di raggruppamento cliente→gruppo→progetto che prima viveva solo nella sidebar; rimossa dalla sidebar il 20/06/2026, ora è una voce di menu propria subito sotto Dashboard). Ha filtri cliente/gruppo/progetto; i gruppi sono evidenziati con riga verde e badge "N da fare" se contengono progetti con todos aperti (somma di `HI(progetto).openTodos`).
- `WI(ore)` = converte ore in ticket (`Math.round(ore*4)`). Da mostrare sempre accanto a qualunque cifra di ore-da-contratto (residue/usate/contrattate) in Contratti (`D9`, card KPI in `ple`) e nel form Intervento (`cle`).
- `Vle2` = hook di filtro CONDIVISO tra `Zle` (Progetti) e `Hle` (Report Consulenza), aggiunto 22/06/2026 su richiesta esplicita di avere "filtri uguali" nelle due sezioni. Espone `{client,group,project,billing,pstatus,tipo,tecnico,model,from,to,interno,controls,reset,active}` — `controls` è la barra filtri JSX pronta da inserire, `active` indica se almeno un filtro è impostato. `billing`=stato fatturazione (`B9`), `pstatus`=stato progetto (`z9`: lead/in_progress/pending_payment/completed/archived), `model`=modello AI (`wI`), `interno`=``/`si`/`no`. **Chi lo usa deve adattare i propri filtri ai dati che possiede**: `Zle` filtra `projects` direttamente (i filtri a livello voce — tipo/tecnico/model/billing/periodo — si traducono in `project.timeEntries.some(...)`), `Hle` filtra le time-entries dentro ogni progetto. Se serve aggiungere un filtro a una terza vista Consulenza, riusare `Vle2` invece di duplicare lo stato.
- `Yle2` = pagina "Impostazioni" CONDIVISA, aggiunta 24/06/2026 su richiesta esplicita di unire i due menu "OneDrive" (Consulenza) e "Import" (Assistenza) in un'unica voce di menu identica nei due contesti. È un semplice wrapper che renderizza in sequenza `Wle` (login/sync/backup OneDrive, h1 "OneDrive & Backup") e `Tle` (import Excel + configurazione assistenza, h1 "Import Excel & Configurazione") con un divider in mezzo — `Wle` e `Tle` NON sono stati toccati/fusi, restano due componenti distinti con la loro logica originale, `Yle2` li mostra solo uno sotto l'altro. Usata sia per la voce menu Consulenza (key `sync`, label cambiata da "OneDrive" a "Impostazioni") sia per la voce menu Assistenza (key `a_import`, label cambiata da "Import" a "Impostazioni"); entrambe passano `{state,setState,globalAccount:C}` (anche dal lato Assistenza, dove `globalAccount` prima non veniva passato — `C` è uno state radice di `jle`, accessibile da entrambi i branch). Se in futuro serve aggiungere un'altra sezione di "impostazioni" condivisa, aggiungerla dentro `Yle2`, non duplicarla nei due menu.
- `Jle2` = vista "Statistiche progetti interni" (Consulenza), raggiungibile con un toggle dentro `Vle` (Statistiche & BI) — stesso menu, vista separata. Ha propri filtri (cliente, periodo dal/al — NON condivisi con `Vle`/vista esterni). Mostra ore/spese/costo tecnico totali, il riquadro "Ore progetti interni" (spostato qui da `Vle` il 20/06/2026, prima viveva — per errore — nella vista esterni), grafico ore per progetto interno, grafico utilizzo modelli AI (`aiModel` delle time-entries) e tabella dettaglio con nome progetto NON troncato (il nome troncato si usa solo nei grafici). `Vle` di default mostra ancora la vista "esterni" originale.
- **Attenzione filtri**: in `Vle` (vista esterni) la card "Costo tecnici" deve sempre derivare da `y` (le time-entries già filtrate da cliente/progetto/tipo/stato/periodo), mai da `e` (l'array progetti non filtrato) — errore reale fatto e corretto il 20/06/2026: usare `cL(progetto,tecnici)` su tutti i progetti include anche quelli interni e ignora i filtri, gonfiando il numero rispetto al resto della pagina. Usare invece `y.reduce((s,t)=>s+sL(t,tecnici),0)`.
- **"Da contratto"** ha sostituito la card "IVA" in `Ple` (dettaglio progetto) e in `Vle` (Statistiche & BI, vista esterni): mostra l'imponibile delle time-entries con `billingStatus==='contratto'`. Non toccato: le colonne/celle IVA dentro `Hle` (Report Consulenza) e `Rle` (tabella ore) — lasciate invariate il 20/06/2026 per restare nello scope richiesto.

**"Sospeso" NON è più uno stato ma un flag booleano** (cambiato 01/07/2026 su richiesta esplicita: "metti un bottone di fianco allo stato invece di metterlo nello stato"): campo `sospeso` sull'intervento, ortogonale a `stato` (che ora è solo da_assegnare/aperto/in_lavorazione/chiuso — `AI` non contiene più `sospeso`). `II()` migra i vecchi record `stato==='sospeso'` → `stato:'aperto', sospeso:true` (idem l'import Excel). UI: in `cle` un bottone toggle "Sospeso" di fianco al select Stato; in `mle` badge violet "Sospeso" accanto al badge stato e il filtro rapido `sospeso` filtra sul flag; in `F9` (Report/Statistiche) campo `sosp` + bottone "Solo sospesi"; in dashboard `ule` la casella "In sospeso" = `e.sospeso&&e.stato!=='chiuso'`; `O9` (rapportino) stampa " · SOSPESO". Se si aggiunge una nuova vista con filtro stato, ricordarsi che sospeso va gestito a parte.

**Tecnici interni MAI in Fatture Fornitori** (01/07/2026): `vL()` filtra i tecnici con `tipologia!=='interno'&&(tipologia==='fornitore'||fornitoreId)`; stesso guard in `I()` di `mle` (avviso "in attesa di fattura fornitore") e `isForn` di `F9`. Un tecnico interno con `fornitoreId` sporco resta comunque escluso.

**Allegati: icona con conteggio nelle righe Interventi** (01/07/2026): in `mle`, nella cella azioni (stampa/modifica/elimina), sotto le icone c'è un div rosso `text-red-600` con icona `ke` + numero allegati, visibile solo se `t.allegati?.length>0`.

**Regola di business "interventi da assegnare"** (vedi anche memoria `consulenza-ai-interventi-da-assegnare`): SEMPRE `stato==='da_assegnare'` OPPURE `!tecnicoId` (nessun tecnico assegnato), non solo lo stato. Variabile `daAss` in `mle` implementa questa unione.

**Sync automatico Consulenza→Intervento**: in `Rle` (tabella ore progetto), la funzione `syncInt(entry, project)` crea/aggiorna/rimuove un Intervento collegato (campo `entry.linkedInterventoId`) ogni volta che una time-entry ha `billingStatus==='contratto'` e `contractId` impostato, così le ore scalano davvero il contratto (tramite la stessa logica di `KI`/`JI` usata in Assistenza). Richiede che `appState`/`setAppState` (lo stato globale e il suo setter da `jle`) siano passati come prop fino a `Rle`, attraverso `Ple`. Se la time-entry non ha un tecnico assegnato, **alla prima sincronizzazione** chiede il nome con `prompt()` (solo una volta: i sync successivi su una entry già collegata non richiedono più input).

**IMPORTANTE — niente doppio conteggio**: `KI()` calcola il consumo di un contratto **solo** dai record in `e.interventi` (incluso il tipo `consulenza`, popolato dal sync sopra). NON deve più leggere direttamente `qI()` (le time-entries Consulenza) per evitare di contare due volte le stesse ore — è già successo una volta (bug corretto il 19/06/2026). `qI()` esiste ancora come funzione ma non va più usato per il calcolo di `KI`.

**Backfill storico**: in `Tle` (Import & Impostazioni) c'è un bottone "Sincronizza ore Consulenza su contratti" che crea retroattivamente gli Interventi collegati per le time-entries `billingStatus==='contratto'` già esistenti ma senza `linkedInterventoId` (caso tipico: dati registrati prima che il sync automatico esistesse).

**`qle` (modal Registra/Modifica ore Consulenza)**: ora supporta sia creazione che modifica tramite il prop opzionale `initial` (se presente, precompila i campi, mostra "Modifica voce ore" come titolo, e preserva `id`/`linkedInterventoId` al salvataggio). In `Rle` l'editing delle righe non è più inline: la matita apre `qle` in modalità edit; solo Ore/Tariffa/Stato restano modificabili al volo direttamente nella tabella.

**Convenzioni Assistenza consolidate (19-20/06/2026, sort invertito il 22/06/2026):**
- **Ordinamento interventi**: ovunque si elenchino interventi singoli (mle, ple, vL/Ele, gruppi cliente in ble) si ordina per **data intervento** (`dataIntervento`) decrescente — pattern: `.sort((e,t)=>t.dataIntervento.localeCompare(e.dataIntervento))`. ATTENZIONE: prima (19-20/06) la regola era "data di inserimento" (`createdAt`); l'utente ha cambiato idea il 22/06/2026 e ha chiesto esplicitamente di tornare a data intervento ovunque — se in futuro emerge ambiguità su quale criterio usare, questa è la regola attualmente valida (verificare comunque con l'utente se sembra di nuovo sbagliata, potrebbe cambiare ancora).
- **Filtri Interventi (`mle`)**: il range data ha SEMPRE bisogno di due input (`Da` e `A`) — esisteva un bug reale (22/06/2026) in cui lo stato/filtro "a data" (`O`/`k`) era nella logica di filtro ma il relativo `<input>` non era renderizzato, quindi il filtro pareva "non funzionare". C'è anche un filtro Onsite (select sì/no/tutti) e un bottone "Reset filtri" che deve azzerare TUTTI gli stati filtro inclusi i toggle booleani degli avvisi rapidi (contratto senza contratto, da fatturare cliente, in attesa fattura fornitore).
- **Campo `noteInterne`** sull'intervento (aggiunto 22/06/2026): note libere visibili solo nell'app, mai incluse nei template di stampa (`lle`, `O9`) perché quei template referenziano i campi singolarmente — basta non aggiungerlo lì, non serve un filtro esplicito di esclusione.
- **`vL(state, fornitoreId, from, to, fattFilter)`** (Fatture Fornitori): `fornitoreId` è opzionale dal 22/06/2026 — se vuoto/falsy, mostra gli interventi di TUTTI i fornitori. `fattFilter` (5° parametro) dal 22/06/2026 NON è più un booleano ma una stringa: `` ``=tutte, `` `no` ``=da fatturare, `` `si` ``=fatturate. `Ele` deve sempre chiamare `vL` direttamente (mai `a?vL(...):[]`), e mostra una colonna "Fornitore" per distinguere le righe quando non ne è selezionato uno specifico. **Bug reale ricorrente in `Ele` (corretto il 22/06/2026, due volte)**: oltre a `vL` stesso, anche il blocco JSX che renderizza la tabella era gated dietro `a?(...)::(0,X.jsx)("Seleziona un fornitore...")` — quindi anche dopo aver "sistemato" `vL` per accettare fornitore vuoto, l'utente vedeva comunque il messaggio placeholder finché non sceglieva un fornitore. Quando si rende una sezione "funzionante senza filtro X", controllare TUTTI i punti che condizionano il rendering su quel filtro, non solo la funzione dati.
- **Ordinamento Report Assistenza (`ble`)**: dentro ogni gruppo cliente, le righe sono ordinate per `numFatturaFornitore` (vuoto=ultimo) e poi per `dataIntervento` decrescente — non solo per data. La tabella mostra anche la colonna "N° Fattura"; la descrizione dell'intervento è una riga sotto (colSpan pieno, NON una colonna), per poterla leggere per intero invece di un line-clamp-1 cramped.
- **"Segna come fatturati" in `Ele` scrive anche `costoTecnicoOrario`** (22/06/2026): oltre a `costoFatturatoFornitore`/`oreImpiegate`/`numFatturaFornitore`, calcola `importo/ore` e lo scrive come override del costo orario sull'intervento. Questo è importante perché `ZI()` (usata OVUNQUE per costo/margine: `mle`, `ble`, `xle`, `_le`, `ple`) legge `costoTecnicoOrario` se presente, altrimenti il costo standard del tecnico — senza questo writeback i margini calcolati a valle restavano basati sulla tariffa stimata, non su quella effettivamente fatturata dal fornitore.
- **Allegati** (aggiunto 22/06/2026, campo `allegati:[{id,name,webUrl,size}]` su intervento E su progetto Consulenza): caricati su OneDrive via Graph API con `uploadAllegato(cloudCfg, id, file)` / rimossi con `deleteAllegato(cloudCfg, fileId)` (vicino a `YJ`/`XJ`/`ZJ`/`QJ` nel bundle) — sono generiche, riusabili per qualunque entità con un id, basta passare l'id giusto. **Lo stato globale ha già tutto il necessario per chiamare Graph da qualsiasi componente**: `state.cloud` = `{clientId,tenantId,filePath}` (inizializzato da `NI`, salvato nello stesso JSON dell'app) — un componente che riceve `state:e` (o `appState`/`gS` come `Ple`) può fare `KJ(e.cloud)` per ottenere un token senza prop-drilling aggiuntivo. Cartella: `<cartella del filePath>/Allegati/<id>/`, sorella della cartella che contiene `consulenza-ai-stato.json`. Upload semplice via `PUT .../content` (limite Graph ~4MB, niente upload-session a chunk).
  - **`cle`** (intervento): UI dedicata inline nel form, accetta solo `application/pdf`, disponibile solo se l'intervento è già stato salvato una volta (l'id viene generato solo al salvataggio).
  - **`Wle3`** (progetto Consulenza, componente separato, usato come tab "Allegati" in `Ple`): accetta PDF + altri file M365 (Word/Excel/PowerPoint/immagini), sempre disponibile perché `Ple` è raggiungibile solo per un progetto già esistente (ha sempre un id).
- **Il filtro/badge "Fatturato" lato cliente in Assistenza NON esiste come stato reale tracciato**: il campo `daFatturare` è solo un booleano (pending/listino), non c'è uno stato "già fatturato al cliente" sull'intervento. L'opzione del filtro `fatt` in `F9` che corrispondeva a `!daFatturare` è stata rietichettata da "Fatturato" a **"Listino"** il 22/06/2026 per coerenza col badge già usato in `mle` (che diceva "Listino", non "Fatturato", per lo stesso caso) — evita la falsa impressione che esista un vero tracciamento di fatturazione cliente. NON confondere con `fatturatoFornitore` (booleano reale, fatturazione del fornitore) o col campo `billingStatus`/`B9` di Consulenza (concetto completamente separato).
- **Costo/Ricavi/Margine/Margine%**: ovunque si mostra il costo di un intervento (`ZI(intervento,tecnici)`) si mostra anche il ricavo figurativo (`uL(intervento,contratti)`), il margine (`ricavi-costo`) e la margine% (`ricavi>0?margine/ricavi*100:0`). Componenti coinvolti: `mle` (lista interventi), `ble` (Report Assistenza: cards in alto, riepilogo per cliente, righe tabella), `xle` (Statistiche Assistenza: cards in alto e tabelle per categoria via `h()`), `_le` (Fornitori, via `QI()` estesa con ticket/ricavi), `Ele` (Fatture Fornitori).
- **`uL(intervento,contratti)`** ha sempre un `return 0` finale esplicito per il caso `gratuito` — NON rimuoverlo, altrimenti torna `undefined` e qualsiasi somma con `+=` diventa `NaN` (bug reale corretto il 19/06/2026).
- **N° Ticket vicino al N° intervento**: quando una tabella elenca interventi singoli e non ha già una colonna Ticket, va aggiunta subito dopo la colonna N°.
- **Attenzione ai colSpan**: ogni volta che si aggiunge una colonna a una tabella, va aggiornato anche il `colSpan` della riga "nessun risultato" — è facile sbagliare il conteggio (succedeva il 20/06/2026 sia in `_le` che in `Ele`).
- **`F9(state)`** è l'hook condiviso di filtro Interventi usato da `ble` e `xle`: include client/tecnico/fornitore/tipo/modalità/stato/fatturazione cliente (`fatt`)/**fatturazione fornitore (`fattForn`, aggiunto 22/06/2026)**/periodo/ricerca testuale (`q`, include numero/ticket/**N° fattura fornitore**/descrizione). Se manca un filtro in un report Assistenza, controllare prima se è già incluso qui prima di aggiungerlo di nuovo. `Ele` (Fatture Fornitori) ha la propria ricerca separata (non usa F9) — se si estende la ricerca in uno dei due, ricordarsi di estendere anche l'altro per coerenza.

**ATTENZIONE — due cose diverse si chiamano "ticket", non confonderle (chiarito il 20/06/2026):**
- **`t.numeroTicket`** = il numero ticket dell'helpdesk inserito manualmente sull'intervento (campo testo libero). È QUESTO il campo "Ticket" che va sempre mostrato di fianco al N° intervento in ogni vista, ed è già incluso nella ricerca testuale di `mle`.
- **`lL(intervento)`** = ticket CALCOLATI dal consumo ore (1 ora tecnica onsite/remoto → N ticket, è una metrica derivata, non un campo dati). Quando si mostra questo valore (somme aggregate di "ticket consumati" in Statistiche/Report/Fornitori), l'etichetta deve essere **"Ticket cons."**, mai solo "Ticket" — altrimenti si confonde con `numeroTicket`. Errore reale fatto e poi corretto il 20/06/2026 in `_le`, `xle`, `ble`, `mle` (card riepilogo).

**Aiuto contestuale (`HLP`)**: oggetto globale `var HLP={chiave_pagina:[titolo,testo],...}` definito subito prima di `function jle(){`. Contiene un testo di aiuto per ogni chiave di pagina (sia Assistenza `a_*` sia Consulenza). Un bottone fisso "?" in basso a destra (sempre visibile, dentro `jle`, stato `showHelp/setShowHelp`) apre un modal (`X9`) con `HLP[o===\`assistance\`?c:n]`. Per aggiungere/aggiornare un testo di aiuto, basta modificare la voce corrispondente in `HLP` — non serve toccare il bottone né il modal. Tenere `HLP` in sync col contenuto di `MANUALE-UTENTE.md`.

**Per ritrovare una funzione dopo un redeploy/rebuild**: cerca per testo visibile nell'interfaccia (es. `grep -oE '.{0,30}children:\`Statistiche Assistenza\`.{0,30}' index.html`), non fidarti dei nomi minificati salvati qui — possono cambiare se il progetto viene rigenerato.

## ATTENZIONE CRITICA — il CSS è pre-compilato, non generato al volo

Il CSS di Tailwind è in un `<style rel="stylesheet" crossorigin>` (dopo il `<script>` principale, non prima) ed è stato **compilato una volta in fase di build**, includendo solo le classi usate nel codice sorgente originale. **Non c'è nessun motore Tailwind a runtime nel browser**: se nel JSX scrivo una classe che non esisteva già da qualche parte nel bundle originale, quella classe non avrà NESSUNA regola CSS — l'elemento risulta invisibile/non stilizzato, senza alcun errore in console (bug successo realmente il 20-21/06/2026 con `bg-violet-600`/`hover:bg-violet-700` sul bottone "Guida": sfondo trasparente, testo bianco invisibile).

**Prima di usare una classe Tailwind "nuova" (colore, opacità frazionaria, valore arbitrario `[...]`, ecc.), verificarne l'esistenza nel CSS compilato:**
```bash
python3 -c "
data=open('index.html',encoding='utf-8').read()
i=data.find('<style rel=\"stylesheet\"');s=data.find('>',i)+1;e=data.find('</style>',s)
open('/tmp/realapp.css','w').write(data[s:e])
"
grep -oE '\.NOME-CLASSE-ESCAPED\{[^}]*\}' /tmp/realapp.css
```
(NB: NON usare il tag `<style:...>` di LibreOffice/OpenDocument che appare altrove nel file per i template di stampa — è XML estraneo dentro stringhe JS, non il CSS dell'app.)

**Conseguenze pratiche:**
- Sfondi pieni "-600/-700" sicuramente compilati e verificati: `blue`, `emerald`, `rose`, `indigo` (solo `-600`, niente hover `-700` per indigo). `violet`/`amber`/`teal`/`purple`/`pink`/`cyan`/`orange` ecc. esistono solo come testo o sfondi chiari (-50/-100), **non** come sfondo pieno per bottoni.
- z-index disponibili: solo `z-10`, `z-40`, `z-50` (niente valori arbitrari `z-[60]` ecc.). I modali (`X9`, `b9`) sono tutti `z-50`: un elemento fixed che deve restare sopra un modale aperto deve essere anch'esso `z-50` **e** renderizzato più in basso nell'albero JSX (l'ordine nel DOM decide chi vince a parità di z-index).
- `whitespace-pre-line` e `leading-relaxed` NON esistono; usare `whitespace-pre-wrap` e `leading-snug` per testo multi-riga.
- `bg-white/25`, `bg-white/20`, `bg-white/30` non esistono; `bg-white/70` sì.
- **Posizionamento `fixed`** (bug reale ripetuto il 21/06/2026 col bottone Guida): `bottom-5`, `left-5`, `right-5` NON esistono — senza inset valido un elemento `fixed` torna alla sua posizione statica nel flusso del DOM (es. appare vicino al logo invece che nell'angolo). Valori di inset compilati e verificati: `top-0/1/2/3/4/full`, `right-0/1/2/3/4`, `left-0/2`, `bottom-0` (NIENTE altri bottom-N). Per scostarsi dal bordo usare margini, non altri valori di inset: `mb-1/2/3/4/5/6`, `ml-1/2/3`, `mr-1/2` esistono; **`m-*` generico (m-3, m-4…) NON esiste**, usare sempre il margine direzionale (`mb-`, `ml-`, ecc.). La scala dei margini è corta (max `mb-6`=1.5rem, niente `mb-8/10/12`): per uno scostamento preciso/maggiore su un elemento `fixed` (es. per non sovrapporsi a un altro elemento fisso, come il bottone Guida sopra la riga di stato sync), usare **`style={{bottom:'4.5rem'}}` inline** invece di cercare una classe Tailwind — lo stile inline funziona sempre, indipendentemente dal CSS pre-compilato.
- Quando in dubbio, riusare una combinazione di classi già presente altrove nel bundle (copiare da un bottone esistente) invece di comporne una nuova a mano.

## Attenzione

- I parametri a singola lettera vengono **shadowati** di continuo in closure annidate (es. `e`, `t`, `n`, `r` cambiano significato dentro ogni `.map()`/`.reduce()` annidato). Prima di riusare una variabile "esterna" dentro una closure profonda, verifica che non sia già stata ridichiarata con `let`/destructuring nello stesso scope — altrimenti referenzi il valore sbagliato.
- Non rifattorizzare/rinominare in chiaro il codice minificato: il rischio di rompere riferimenti incrociati è alto e il guadagno di leggibilità è minimo dato che resta comunque un file generato.
- Se una modifica richiede di toccare più di ~10 punti diversi del file, valuta con l'utente se non sia più sensato chiedere il progetto sorgente (se esiste) invece di continuare a patchare il bundle.
