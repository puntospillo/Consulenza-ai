# Manuale Utente — Assistenza & Consulenza (NPS Computer)

Gestionale per attività di assistenza tecnica e consulenza IT/AI. App web, dati sincronizzati su OneDrive tramite login Microsoft.

URL: https://puntospillo.github.io/Consulenza-ai/

---

## 1. Accesso e modalità

All'apertura, l'app richiede il login con account Microsoft (MSAL/Azure AD). I dati vengono letti e scritti su un file Excel nel proprio OneDrive — non serve un database esterno.

In alto a sinistra trovi due bottoni per passare da una modalità all'altra:

- **Assistenza** (preimpostata all'avvio) — clienti, contratti, interventi tecnici, tecnici, fornitori, fatture fornitori, report e statistiche.
- **Consulenza** — progetti, registrazione ore, fatturazione, report e statistiche.

Sono due aree distinte con menu separati, ma condividono l'anagrafica Tecnici e i Clienti.

---

## 2. Modulo Assistenza

### 2.1 Dashboard
Panoramica generale: interventi recenti, contratti in scadenza/esauriti, indicatori principali. In alto a destra il bottone verde **"Nuovo intervento"** apre direttamente il form di creazione (accanto, se presenti, l'avviso "contratti esauriti").

### 2.2 Clienti
Anagrafica clienti: ragione sociale, codice cliente, referente, P.IVA, indirizzo, contatti, note.

### 2.3 Contratti
Elenco contratti di assistenza per cliente. Ogni contratto definisce un monte ore per tipologia (Assistenza Tecnica, Sistemistico, Specialistico, Consulenza) e un costo totale.

- **Barra "Ore residue"**: un'unica barra per contratto, con segmento verde per le ore di assistenza usate e segmento blu per le ore di consulenza/contratto usate. A fianco delle ore è sempre indicato anche il numero di **ticket** corrispondente (1 ora = 4 ticket).
- Un contratto viene segnalato **"Esaurito"** (bordo/badge rosso) quando le ore residue totali sono ≤ 0, **"In scadenza"** (badge giallo) quando restano ≤15% delle ore.
- Cliccando su un contratto si apre il **dettaglio**: ore contrattate/usate/residue (con conversione in ticket), utilizzo per tipologia, elenco di tutti gli interventi collegati (con N°, N° Ticket, descrizione, costo, incasso, margine, margine%) e i bottoni Chiudi/Riapri/Modifica/Stampa.
- **Stampa contratto**: report HTML con N°/Data/Tecnico/Tipo/Onsite/Stato/Ore/**Richiesta intervento**/Descrizione per ogni intervento collegato.
- Solo i contratti **aperti** (non chiusi) compaiono nei menu di selezione quando si crea un nuovo intervento o una voce ore a contratto; un contratto già collegato resta visibile anche se chiuso, etichettato "(chiuso)".

### 2.4 Interventi
Elenco di tutti gli interventi tecnici, ordinati per **data di inserimento più recente in alto**.

- Filtri rapidi per stato, oltre a filtri estesi per cliente/tecnico/fornitore/tipo/modalità/periodo, filtro fatturazione cliente (Tutti / Da fatturare / Listino) e ricerca testuale per N°, N° ticket o descrizione.
- **Da verificare** (ex "Sospeso"): non è uno degli stati, ma un contrassegno indipendente. Nella scheda intervento c'è un bottone "Da verificare" di fianco allo Stato: un intervento può quindi essere ad es. "In lavorazione", o anche "Chiuso", e contemporaneamente da verificare. Nell'elenco compare un badge viola accanto allo stato; il filtro rapido e la casella "Da verificare" della Dashboard usano questo contrassegno (la casella mostra tutti i contrassegnati, anche i chiusi). Nei Report e nelle Statistiche c'è il bottone "Solo da verificare". I vecchi interventi con stato "In sospeso" vengono convertiti automaticamente (stato "Aperto" + contrassegno).
- **Allegati in elenco**: se un intervento ha allegati, sotto le icone di stampa/modifica/eliminazione compare un'icona rossa con il numero di allegati presenti.
- **"Da assegnare"**: il bottone lampeggia e mostra un contatore quando ci sono interventi con stato "da assegnare" **oppure senza tecnico assegnato** — questa è la definizione ufficiale di "da assegnare" in tutta l'app.
- Ogni riga mostra, oltre a N°/Ticket/Cliente/Data/Tecnico/Tipo/Ore: **Costo, Ricavi, Margine, Margine%**. Se l'intervento è a contratto, il numero del contratto compare sotto il N° intervento.
- **Nuovo Intervento / Nuova Richiesta**: form con dati cliente, tecnico, modalità (a contratto / fuori contratto / gratuito), tipo, ore, ecc. Se selezioni "a contratto", appare il riepilogo delle **ore residue totali** del contratto (con ticket equivalenti), per sapere subito quanta capacità resta.
- **Annulla intervento**: disponibile direttamente dentro la scheda di modifica (non serve tornare all'elenco).
- **Allegati PDF**: nella scheda di modifica di un intervento già salvato, puoi allegare file PDF (es. rapportini firmati, foto, documenti del cliente). Vengono caricati su OneDrive nella stessa cartella dei dati dell'app, in una sottocartella `Allegati/<numero intervento>`; ogni allegato è apribile/scaricabile dal link e può essere eliminato singolarmente. Non disponibile per un intervento non ancora salvato la prima volta.

### 2.5 Tecnici / Fornitori
Anagrafica tecnici (interni, esterni, da fornitore) con costo orario, e fornitori con relativo ambito (assistenza/consulenza/entrambi). La tabella Fornitori mostra anche: interventi, ticket consumati, ore, costo, ricavi, margine e margine%.

### 2.6 Fatture Fornitori
Per ogni fornitore, elenco degli interventi svolti dai suoi tecnici, con possibilità di inserire l'importo fatturato e passare la voce a "fatturato". Mostra N°, N° Ticket, costo stimato, ricavi, margine, margine%. È possibile cercare per N° intervento o N° ticket. Gli interventi svolti da **tecnici interni** non compaiono mai qui (né nell'avviso "in attesa di fattura del fornitore" della pagina Interventi): questa sezione riguarda solo i tecnici di fornitori esterni.

### 2.7 Report
Report dettagliato per cliente, con filtri estesi (incluso il tipo) e ricerca testuale. I blocchi cliente sono ordinati per attività più recente; all'interno di ciascun blocco gli interventi sono ordinati per data di inserimento più recente. In alto: interventi, ore, ticket, costo tecnici, **ricavi da contratto**, **ricavi totali**, margine, margine%. Esportabile in CSV e stampabile.

**Stampa per cliente** (flag attivo di default): quando spuntato, la versione stampata nasconde i riquadri riepilogativi in alto e ogni riferimento a costo tecnico/margine/margine% (sia nelle intestazioni per cliente che nella tabella) — restano visibili ore, ricavi, descrizioni. Disattivando il flag la stampa mostra tutto come sullo schermo. La stampa si apre in una finestra separata (niente URL dell'app nel PDF) e il file salvato si chiama "NPS Report Assistenza".

### 2.8 Statistiche
Analisi incrociate su interventi, con gli stessi filtri estesi del Report. Tabelle "per tecnico / per cliente / per tipo / per stato" con interventi, ore, ticket, costo, ricavi, margine, margine%. Grafici: ore per tecnico, ore per cliente. Riepilogo ore/importi sui contratti attivi.

### 2.9 Impostazioni
Voce di menu unica, identica sia in Assistenza che in Consulenza (stessa pagina, raggiungibile da entrambi i menu — vedi anche sezione 3.8). Contiene due blocchi:

- **OneDrive & Backup**: stato login Microsoft, Salva/Carica manuale su OneDrive, configurazione Entra/Graph (Client ID, percorso file), backup/ripristino manuale via file JSON.
- **Import Excel & Configurazione**: importazione massiva da Excel di fornitori/tecnici/clienti/contratti/interventi (con modello scaricabile). La casella **"Forza sovrascrittura"** aggiorna i record già esistenti invece di saltarli. Il bottone **"Sincronizza ore Consulenza su contratti"** crea gli Interventi mancanti per le ore di Consulenza già fatturate "a contratto" in passato, così il consumo dei contratti torna corretto. Qui si configurano anche numerazione interventi, soglia di scadenza contratti e SLA per tipo.

---

## 3. Modulo Consulenza

### 3.1 Dashboard
Panoramica progetti: ore fatturabili/interne, imponibile, da contratto, da fatturare, in sospeso, spese, costo tecnici, margine. Elenco progetti raggruppati per cliente, con scadenze e attività da fare in evidenza.

### 3.2 Progetti
Tutti i progetti raggruppati per Cliente → Gruppo → Progetto. **Filtri** (gli stessi del Report, sezione 3.5): cliente, gruppo, progetto, stato fatturazione, stato progetto (Lead/In corso/Attesa pagamento/Completato/Archiviato), tipo consulenza, tecnico, modello AI, periodo (dal/al), interno/esterno.

- I **gruppi** sono evidenziati con una riga verde; se contengono progetti con attività ("da fare") aperte, mostrano un badge col conteggio totale.
- Ogni riga progetto mostra contatori per **Prompt**, **Note** e **Da fare** (stesso stile del badge "da fare").
- Cliccando su un progetto si entra nel dettaglio: ore, costi, costo tecnico, da contratto, da fatturare, in sospeso, margine — con piena possibilità di vedere e modificare tutte le ore registrate.
- Tab **Allegati**: carica PDF, Word, Excel, PowerPoint, immagini e altri file (max ~4MB ciascuno), salvati su OneDrive nella stessa cartella dei dati dell'app; ogni allegato è apribile o eliminabile singolarmente.

### 3.3 Registra ore
All'interno di un progetto, sezione "Ore & Fatturazione" (o "Ore dedicate" per i progetti interni). Premendo la matita su una riga si apre una finestra dedicata con tutti i campi (data, tipo, descrizione, tecnico, modello AI, tariffa, stato fatturazione, contratto); Ore/Tariffa/Stato restano comunque modificabili al volo direttamente in tabella.

- Selezionando **"Contratto"** come stato fatturazione e poi un contratto specifico, la **Tariffa €/h si compila automaticamente** col valore orario del contratto (costo totale ÷ ore contrattate).
- Quando una voce ore viene fatturata "a Contratto", l'app crea/aggiorna automaticamente un **Intervento collegato** in Assistenza (visibile anche lì), così le ore scalano davvero il monte ore del contratto. Se manca il tecnico, viene richiesto una sola volta.
- Solo i contratti **aperti** del cliente compaiono nel menu di selezione (un contratto già collegato resta visibile anche se chiuso).

### 3.4 Clienti
Elenco clienti consulenza con, per ciascuno: ore lavorate, imponibile, da fatturare, spese, costo tecnico, margine, ed elenco progetti collegati.

### 3.5 Report
Report per cliente/progetto. **Filtri** (gli stessi della sezione Progetti, 3.2): cliente, gruppo, progetto, stato fatturazione, stato progetto, tipo consulenza, tecnico, modello AI, periodo (dal/al), interno/esterno. Ordinato per data di inserimento più recente in alto. Per ogni voce: data, tecnico, costo tecnico, ore, tariffa, imponibile, IVA, totale. Esportabile in CSV, stampabile.

**Escludi contratti**: bottone accanto a "Stampa per cliente" che toglie dal report (video, CSV e stampa) tutte le voci ore fatturate "a Contratto"; quando attivo compare il parametro "Contratti esclusi" nell'intestazione.

**Stampa per cliente** (flag attivo di default): quando spuntato, la versione stampata nasconde la colonna "Costo tecnico" e il totale "Costo tecnici" nel riepilogo generale — restano visibili ore, imponibile, IVA, totale. Disattivando il flag la stampa mostra tutto come sullo schermo. La stampa si apre in una finestra separata (niente URL dell'app nel PDF) e il file salvato si chiama "NPS " + il titolo del report.

### 3.6 Statistiche
Due viste, selezionabili con un bottone, nella stessa pagina:

- **Progetti esterni** (vista predefinita): analisi su ricavi, margine, distribuzione per cliente/progetto, utilizzo modelli AI, andamento mensile, efficienza ore/ricavo, costo tecnici. Card in alto: ore, costo tecnici, imponibile, **da contratto**, da fatturare, in sospeso, margine, margine%.
- **Progetti interni**: vista separata e con filtri propri (cliente, periodo) per i progetti senza fatturazione (studio, R&D, preparazione) — ore totali, spese, costo tecnico, grafico ore per progetto, grafico utilizzo modelli AI, tabella dettaglio con nome progetto completo.

### 3.7 Spese e Note
Registrazione spese extra per progetto e note libere.

### 3.8 Impostazioni
Stessa voce di menu e stessa pagina della sezione 2.9 (Assistenza) — login/sync/backup OneDrive + import Excel e configurazione. Da qui o da lì il contenuto è identico.

---

## 4. Concetti trasversali importanti

- **Margine (solo Consulenza)**: sempre calcolato come `imponibile − (costo tecnico + spese)`, in ogni punto dell'app (Dashboard, Clienti, Dettaglio progetto, Statistiche).
- **N° Ticket** = numero ticket dell'helpdesk inserito a mano sull'intervento — sempre visibile accanto al N° intervento. Diverso dai **"ticket consumati"**, che sono calcolati dalle ore (1 ora = 4 ticket): quest'ultimo è sempre etichettato "Ticket cons." per non confonderlo col primo.
- **"Da assegnare"** = stato `da_assegnare` OPPURE nessun tecnico assegnato — vale ovunque nell'app, non solo nel filtro omonimo.
- **Versione app**: visibile in basso nel menu laterale (es. "v4.9.1"); aumenta a ogni aggiornamento pubblicato.
