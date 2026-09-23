---
name: aggiorna-guide-ai
description: Aggiorna Guida AI Personal con le novità verificate di ChatGPT, Claude e Gemini: descrizioni degli strumenti, istruzioni operative, quiz, ricette e glossario. Lavora solo su Corso-AI-Personale.html e non tocca le altre app del repository.
argument-hint: "[opzionale: data da cui cercare, es. 2026-09-20]"
disable-model-invocation: true
allowed-tools: WebSearch, WebFetch, Read, Edit, Write, Grep, Glob, Bash(git status:*), Bash(git diff:*), Bash(git add:*), Bash(git commit:*), Bash(git checkout:*), Bash(git log:*), Bash(node:*)
---

# Aggiornamento di Guida AI Personal

## Perimetro: solo questa app

Modifichi **un solo file**: `Corso-AI-Personale/Corso-AI-Personale.html`.

Il repository `Consulenza-ai` contiene anche altre app — `Guida-AI-5-Pilastri/`,
`Guida AI Pro Ita/`, `Kit-Consulenza-AI/` e il gestionale `index.html` nella radice.
**Non aprirle e non modificarle**, nemmeno se contengono le stesse informazioni
da aggiornare. Hanno una loro vita e una loro skill.

Aggiorni le informazioni su tre soli prodotti: **ChatGPT / OpenAI**, **Claude (Anthropic)**
e **Google Gemini**. Ogni altro prodotto AI è fuori perimetro.

## Regole non negoziabili

- Ogni modifica ai contenuti deve avere una fonte **primaria** con URL e data: blog e news
  ufficiali, release notes, changelog, documentazione e pagine dei modelli di OpenAI,
  Anthropic e Google. Le testate tech servono solo a scoprire le novità, non a confermarle.
- Se una novità non è confermata da una fonte primaria, **non la inserisci**: la elenchi nel
  report come "non verificata".
- Distingui sempre: rilasciato, in prova/beta, annunciato ma non disponibile. Scrivilo nei testi.
- Non inventare prezzi, limiti, date o numeri. Se la fonte non lo dice, non lo scrivi.
- Non cambiare grafica, struttura o logica. Solo contenuti.
- L'HTML è l'unica copia: non esistono sorgenti separati da ricompilare. Si modifica direttamente.

## Procedura

### 0. Preparazione

1. `git status --short -- Corso-AI-Personale/`. Se **questa cartella** ha modifiche non
   committate, fermati e chiedi come procedere. Le modifiche nelle altre cartelle non ti
   riguardano: non sono un motivo per fermarti.
2. Crea il branch: `git checkout -b aggiornamento-ai-AAAA-MM-GG`.
3. Data di partenza della ricerca, in quest'ordine: la data dell'ultimo controllo scritta in
   `Corso-AI-Personale/AI_UPDATES_LOG.md`; oppure l'argomento $ARGUMENTS; oppure gli ultimi 90 giorni.

### 1. Mappa dei contenuti, prima di cercare sul web

Con Grep, individua nell'HTML tutti i punti che parlano dei tre strumenti. Ecco dove stanno:

| Cosa | Come trovarlo |
|---|---|
| Descrizione dei tre strumenti, una per livello | `const TOOL_INTRO_LV` |
| Istruzioni operative per ogni strumento | `const HOW = {` — sezioni `modes`, `setup`, `personal`, `verify`, `file`, `immagini`, `mobile`, `progetti`, `assistenti`, `skill`, `md`, `computer`, `miniapp`, `agenti`, `agentmd`, `tokens` |
| Riga "dove si fa" sotto le spiegazioni | `const WHERE` e `const NEED` |
| Domande del quiz | `const QZ = [` |
| Ricettario | `const RICETTE = [` |
| Glossario | dentro la lezione `fine-glossario` |
| Data dell'ultimo controllo | `const AGG` |
| Numero di revisione | `const REV` |

Scrivi l'inventario in una tabella: punto del file → cosa afferma oggi.

### 2. Ricerca delle novità

Una ricerca separata per fornitore. Per ciascuno: nuovi prodotti e funzioni delle app di uso
comune, funzioni rinominate o chiuse, cambi nei piani gratuiti e a pagamento. Apri le pagine
ufficiali con WebFetch e verifica ogni punto, annotando URL e data.

Questa app parla a persone che usano l'AI nella vita privata: interessano le funzioni che si
vedono nell'app e sul telefono. I dettagli per sviluppatori e le API sono fuori perimetro.

### 3. Analisi dello scostamento

Incrocia l'inventario con le novità e classifica ogni punto: **obsoleto** (afferma qualcosa che
non è più vero), **incompleto** (manca una novità rilevante), **a posto**.

Priorità assoluta: una risposta del quiz che era giusta e oggi è sbagliata.

Mostra la tabella degli scostamenti e **aspetta conferma** prima di modificare il file.

### 4. Modifiche, rispettando i tre livelli

L'app si adatta al livello dell'utente e questo vincola cosa puoi scrivere e dove.

- Ogni lezione ha un campo `lv` (1, 2 o 3) e si vede solo da quel livello in su. Lo stesso vale
  per le domande del quiz (campo `lv`) e per le ricette (campo `l`: base, intermedio, avanzato).
- **Dentro le istruzioni**, le righe si marcano per livello e vengono tolte al momento giusto da
  `lvFilter()`: un passo diventa `[3, 'testo']` in `stepsL()`, una riga di tabella prende il
  livello come primo elemento in `modeTbl()`, e una regola si scrive `rule(testo, minimo, massimo)`.
- Quindi: **le funzioni che richiedono di installare qualcosa, le skill e gli agenti vanno
  marcate livello 3**. Al livello Base e Intermedio non devono comparire né loro né le parole
  che li nominano.
- Nel quiz, controlla anche le risposte sbagliate: non devono citare parole che a quel livello
  non sono state spiegate.

Aggiorna i testi, poi aggiorna `const AGG` con la data di oggi e alza `const REV`.

### 5. Verifica

Dalla cartella `Corso-AI-Personale/`:

    node strumenti/verifica.js
    node strumenti/livelli.js

- `verifica.js` apre ogni lezione nei 3 livelli e nei 4 stati di strumento (nessuno scelto,
  ChatGPT, Claude, Gemini), fa due giri di quiz per livello e controlla che il test di livello
  assegni ancora i livelli giusti. Deve finire con "Nessun problema rilevato".
- `livelli.js` cerca le parole fuori livello nel testo che l'utente vede davvero.
  Deve finire con "Tutto in regola".

Se uno dei due segnala qualcosa, correggi e rilancia. Non proseguire con i test rossi.

### 6. Chiusura

1. Rileggi `git diff` per intero: deve toccare **solo** `Corso-AI-Personale/`.
2. Aggiorna `Corso-AI-Personale/AI_UPDATES_LOG.md` aggiungendo una sezione in cima con: data del
   controllo, novità applicate con l'URL della fonte, novità scartate perché non verificate,
   punti del file modificati.
3. `git add Corso-AI-Personale/` e commit con messaggio `Guida AI Personal Rev. X.Y: <cosa è cambiato>`.
4. **Non fare push.** La pubblicazione su GitHub Pages è una decisione di Maurizio: l'app è online
   a https://puntospillo.github.io/Consulenza-ai/Corso-AI-Personale/Corso-AI-Personale.html
   e il push la aggiorna per tutti.

## Report finale, in italiano e breve

- novità applicate, divise per fornitore, con la fonte
- quiz corretti, se ce ne sono
- esito dei due controlli automatici
- novità scartate perché non verificate
- punti dubbi da valutare a mano
- nome del branch da revisionare
