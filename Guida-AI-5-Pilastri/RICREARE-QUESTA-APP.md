# Come ricreare da zero la "Guida AI · I 5 Pilastri"

Questo documento serve per **aprire una chat nuova** (Claude Code, Codex, Antigravity o simili) e far ricostruire la stessa app.
Copia tutto il contenuto e incollalo come primo messaggio, aggiungendo in fondo eventuali variazioni che vuoi.

App di riferimento online: https://puntospillo.github.io/Consulenza-ai/Guida-AI-5-Pilastri/Guida-AI-5-Pilastri.html

---

## 1. Cosa devi costruire

Un **corso interattivo in un unico file HTML** chiamato `Guida-AI-5-Pilastri.html`, in italiano, che insegna a usare l'AI a chi oggi la usa solo per fare domande in chat.

Vincoli tecnici obbligatori:

- **Un solo file HTML**, senza librerie esterne, senza connessione a internet, senza servizi esterni. Si apre con doppio clic.
- HTML, CSS e JavaScript scritti a mano nello stesso file (niente framework, niente build).
- Nel browser si salvano **solo** avanzamento, strumento scelto e risultati del quiz (`localStorage`, dentro `try/catch`). I testi scritti negli esercizi **non** si salvano, e l'app lo dice.
- Tutti i contenuti in italiano, con apostrofi tipografici (’) e virgolette « “ ” ».
- Deve funzionare bene anche a **400px di larghezza** (telefono): nessuno scorrimento orizzontale della pagina.
- Dimensione attuale di riferimento: circa 3.900 righe, 370 KB.

Destinatari: impiegati, responsabili, professionisti **non tecnici**, che non hanno mai creato skill, agenti o app. Tono: semplice, concreto, mai gergale; ogni termine inglese va spiegato.

---

## 2. Struttura dell'interfaccia

- **Colonna sinistra (indice)**: intestazione con logo "AI", titolo **Guida AI**, sotto una riga con "App by Pippo" e l'etichetta "Rev. 1.0" (da `const REV = '1.0'`). Poi l'elenco delle lezioni raggruppate per pilastro, con pallino di completamento, e in fondo il pulsante "↺ Ricomincia da capo".
- **Barra in alto**: pulsante "☰ Indice" (solo su schermi stretti), barra di avanzamento con "Lezione X di Y · N completate · %", e il **selettore dello strumento**: ChatGPT · Claude · Gemini.
- **Corpo**: una lezione alla volta, con intestazione colorata per pilastro (occhiello, titolo, sottotitolo, "Lezione n di m", minuti stimati, "Completata") e in fondo i pulsanti "← lezione precedente" e "Ho capito, avanti →".
- Ogni lezione ha un `id` usato anche come ancora nell'indirizzo (`#p1-craft`).

## 3. La scelta dello strumento (parte centrale del progetto)

Nella prima lezione l'utente sceglie **ChatGPT, Claude o Gemini**. Da quel momento:

- Tutte le istruzioni operative mostrano **solo** lo strumento scelto (funzione `howBox(argomento)` che pesca da un oggetto `HOW`), mai schede con tutti e tre.
- Testi, tabelle e consigli si adattano con funzioni tipo `byTool({chatgpt:…, claude:…, gemini:…, any:…})` e `where('chat'|'local'|'app'|…)`.
- Se nessuno strumento è scelto, al posto delle istruzioni compaiono tre pulsanti per sceglierlo.
- Dove serve installare qualcosa compare l'etichetta arancione "⬇ da installare"; dove basta il browser è scritto "Nessuna installazione".

Argomenti coperti dall'oggetto `HOW` (uno per strumento): quando usare cosa, prima configurazione, personalizzazione, strumenti anti-errore, lavorare con i file, progetti, assistenti, installare e usare le skill, file .md, portare l'AI sul computer, mini-app in chat, mini-app sul computer, app complete, agenti, file di istruzioni dell'agente, consumi e limiti.

## 4. Le 42 lezioni

**Inizia (4)**
1. `benvenuto` · Benvenuto · 4 min
2. `parole` · Le parole che incontrerai · 5
3. `strumenti` · La mappa del tuo strumento · 8
4. `dati` · I tuoi file: online o sul computer? · 7

**Pilastro I · Competenze prima degli strumenti (9)**
5. `p1-brief` · Il prompt è un brief, non un incantesimo · 5
6. `p1-craft` · La formula CRAFT · 6
7. `p1-prova` · Scrivi il tuo primo prompt CRAFT · 8
8. `p1-migliorare` · Migliorare il risultato · 6
9. `p1-allucinazioni` · Risultati affidabili, senza allucinazioni · 9
10. `p1-contesto` · Il contesto: cosa dare all'AI · 5
11. `p1-token` · Usare meno token (e non finire i limiti) · 13
12. `p1-file` · Lavorare sui file: Excel, Word, PDF, PowerPoint · 12
13. `p1-chaining` · Lavori complessi: un passo alla volta · 6

**Pilastro II · Elimina la frizione (9)**
14. `p2-attrito` · Smetti di rispiegare tutto ogni volta · 4
15. `p2-personalizza` · Personalizza la tua AI · 10
16. `p2-progetti` · I Progetti · 8
17. `p2-assistenti` · Gli Assistenti personalizzati · 8
18. `p2-markdown` · Cos'è un file .md (Markdown) · 7
19. `p2-skill` · Le Skill · 9
20. `p2-skill-prova` · Crea la tua prima skill · 12
21. `p2-skill-libreria` · Libreria: 10 skill pronte · 10
22. `p2-differenze` · Differenze e come combinarli · 6

**Pilastro III · Progetta prima di costruire (2)**
23. `p3-perche` · Prima progetta, poi automatizza · 5
24. `p3-mappa` · Mappa le tue attività · 12

**Pilastro IV · Costruisci il tuo Kit AI (6)**
25. `p4-app` · Piccole app su misura, senza programmare · 6
26. `p4-regole` · Le 5 regole per non sbagliare · 6
27. `p4-computer` · Portare l'AI sul tuo computer · 10
28. `p4-crea` · Creare una mini-app, passo passo · 10
29. `p4-prova` · Descrivi la tua app · 8
30. `p4-app-complete` · Creare app complete e pubblicarle · 14

**Pilastro V · Dal supporto alla delega (7)**
31. `p5-chatbot` · Chatbot o agente? · 6
32. `p5-loop` · Il loop: come lavora un agente · 5
33. `p5-controlli` · Controlli, stop e intervento umano · 7
34. `p5-primo` · Il tuo primo agente, passo passo · 12
35. `p5-prova` · Scrivi il prompt del tuo agente · 10
36. `p5-casi` · Agenti al lavoro: 8 casi concreti · 12
37. `p5-istruzioni` · Il file di istruzioni dell'agente · 7

**Conclusione (5)**
38. `fine-ricettario` · Ricettario: 52 casi pronti · 15
39. `fine-problemi` · Quando qualcosa non va · 6
40. `fine-piano` · Il tuo piano in 4 settimane · 4
41. `fine-quiz` · Quiz finale · 5
42. `fine-glossario` · Glossario completo · 5

## 5. Come è fatta ogni lezione

Ogni lezione è un oggetto `L({id, p, t, sub, min, body, update})` dentro un array `LESSONS`; `body()` restituisce HTML e `update()` aggiorna le parti interattive quando l'utente scrive.

Mattoncini riutilizzabili (funzioni che restituiscono HTML):

- `card(titolo, corpo, occhiello)` · riquadro bianco
- `analogy(emoji, titolo, testo)` · analogia tratta dalla vita quotidiana
- `keys([...])` · riquadro verde "✅ Da ricordare" (in fondo a quasi ogni lezione)
- `warn(titolo, testo)` e `note(titolo, testo)` · avvisi giallo e azzurro
- `ex(sbagliato, giusto, perchéNo, perchéSì, etichette…)` · confronto "✗ Così no / ✓ Così sì"
- `tryBox(titolo, corpo)` · esercizio "PROVA TU"
- `outBox(id, titolo, testo, nomeFileDaScaricare)` · riquadro scuro con i pulsanti Copia e ⬇ Scarica
- `tbl(intestazioni, righe)` · tabella con scorrimento su schermi stretti
- `fld(percorsoStato, etichetta, opzioni)` e `cb(...)` · campi che scrivono nello stato
- `aiMake(id, titolo, prompt, consiglio)` · riquadro viola "✨ FATTELO CREARE DALL'AI"
- `howBox(argomento)` · istruzioni dello strumento scelto
- `whereLine(dove, alternativa)` · riga "Dove farlo con …" con etichetta di installazione
- `stepsL(colore, passi)` · elenco numerato con pallini colorati

Schemi disegnati in SVG dentro il codice (nessuna immagine esterna): i 5 pilastri, progetti e skill, catena di prompt, chatbot contro agente, loop dell'agente, tre modi di elaborare i file, grafico a barre della mappa attività, anello del voto del quiz.

## 6. Esercizi interattivi

Tutti generano un testo pronto da copiare (o un file da scaricare) mentre l'utente compila i campi:

| Lezione | Esercizio | Risultato |
|---|---|---|
| `p1-prova` | Prompt CRAFT con 5 esempi precaricati | prompt + indicatore di completezza |
| `p1-token` | Simulatore dei consumi di una chat lunga | confronto a barre e risparmio stimato |
| `p1-file` | Richiesta per un file (Excel, Word, PDF, PowerPoint) | prompt con controlli |
| `strumenti` | "Quale uso per il mio lavoro?" (5 domande) | consiglio per lo strumento scelto |
| `p2-personalizza` | Istruzioni personali | testo con conteggio caratteri |
| `p2-progetti` | Istruzioni di un progetto | testo da incollare |
| `p2-assistenti` | Istruzioni di un assistente | system prompt |
| `p2-markdown` | Editor Markdown con anteprima dal vivo | — |
| `p2-skill-prova` | Generatore di `SKILL.md` con 3 esempi | file `SKILL.md` |
| `p3-mappa` | Tabella delle attività (frequenza, minuti, necessità umana) | grafico, ore recuperabili, strumento consigliato |
| `p4-prova` | Descrizione di una mini-app (livello 1 o 2) con 4 esempi | richiesta per l'agente |
| `p4-app-complete` | Requisiti di un'app | file `PRD.md` |
| `p5-prova` | Prompt di un agente con 3 esempi | prompt + verifica dei controlli troppo vaghi |
| `p5-istruzioni` | File di istruzioni dell'agente | `AGENTS.md`, `CLAUDE.md` o `GEMINI.md` secondo lo strumento |
| `p2-differenze` | Quiz breve di 6 casi | risposta commentata |

Raccolte di contenuti pronti:

- **Ricettario**: 52 casi con situazione, cosa ottieni, dove farlo, prompt e consiglio; filtri per argomento (Excel, Word e PDF, presentazioni, email, ricerca, app, agenti, organizzazione) e per livello (base, intermedio, avanzato).
- **Libreria skill**: 10 file `SKILL.md` completi e scaricabili (report mensile, verbale, presentazione, confronto offerte, estrazione fatture, risposte frequenti, revisione documenti, analisi contratto, pulizia dati, requisiti app), con struttura `assets/`, `references/`, `scripts/`.
- **Casi di agenti**: 8 casi completi con prompt (unire Excel, note spese, contratti, presentazione, lettere, riordino cartelle, confronto preventivi, verbale).

## 7. Quiz finale

- **62 domande** a scelta multipla su 10 argomenti (prompt, allucinazioni, token, file, dati, personalizzazione, skill, workflow, app, agenti).
- Giri da **10 domande**: si scelgono argomenti diversi e si dà la precedenza alle domande mai viste; le 4 risposte vengono mescolate.
- Una domanda per volta: risposta giusta in verde, sbagliata in rossa, spiegazione e pulsante "Rivedi la lezione".
- A fine giro: voto su 10 in un anello animato, giudizio (🏆 🎉 👍 📚 💪), pallini delle risposte ed elenco delle domande sbagliate.
- Pagina risultati: giri completati, voto migliore, media, domande viste, grafico degli ultimi giri, percentuale per argomento con l'argomento da ripassare per primo, pulsante per azzerare.

## 8. Contenuti: regole ferree

- Non parlare mai "del cliente" come soggetto esterno: chi legge è l'utente. Gli esempi riguardano il suo lavoro (ufficio acquisti, fornitori, fatture, contratti, verbali, colleghi).
- Ogni concetto arriva con un esempio concreto e frequente, non teorico.
- In ogni lezione dove si crea qualcosa (prompt, istruzioni, skill, .md, app, agente) ci deve essere il riquadro "Fattelo creare dall'AI".
- Le regole contro le informazioni inventate vanno ripetute dove servono: usa solo i file dati, indica pagina e frase esatta, scrivi NON TROVATO, calcoli con il codice, l'ultima verifica è dell'utente.
- Privacy: account aziendale, dati personali anonimizzati, mai password in chat, agenti sempre su copie dei file.
- Ogni istruzione operativa deve dire **dove** si fa e **se serve installare** qualcosa.

## 9. Stato delle app (verificato a settembre 2026)

Queste informazioni cambiano spesso: **falle verificare sul web** prima di scrivere le istruzioni.

- **ChatGPT**: app per computer unica con **Chat**, **Work** (agente per documenti, fogli, presentazioni e cartelle locali) e **Codex** (app e programmi). La vecchia "modalità agente" non esiste più. I GPT personalizzati sono in dismissione: le **Skill** stanno in *barra laterale › Plugin › Skill*, ma solo nei piani aziendali; con i piani personali si usano Progetti o Codex. **Sites** pubblica siti e web app. Permessi: sotto la casella, "Chiedi approvazione". Comandi: `/status` (nell'app), `/compact` (riga di comando).
- **Claude**: chat, Progetti, **Skill** (*Personalizza › Skill*, caricamento .zip), **Artifact**, **Cowork** (agente su cartelle, modalità Manuale o Automatica, istruzioni globali e per cartella), **Claude Code** (scheda Code), componenti aggiuntivi per Excel, Word e PowerPoint, Claude in Chrome. Impostazioni utili: *Funzionalità › Esecuzione codice e creazione file*, *Profilo*, *Utilizzo* (finestra di 5 ore e settimanale). Comandi: `/init`, `/clear`, `/compact`, `/context`.
- **Gemini**: app Gemini, **Gem**, **Notebook** nell'app, **Gemini Notebook** (prima NotebookLM), Canvas, Deep Research, Gemini dentro Gmail, Drive, Documenti, Fogli, Presentazioni; **Google AI Studio › Build** per le app online; **Antigravity** (ha sostituito Gemini CLI per gli account personali) per le cartelle del computer, con livello gratuito a consumo limitato. **Gemini Spark non è disponibile in Italia e nell'UE**. Impostazioni: *Contesto personale*, *Mantieni attività*; verifica delle risposte con *Altro › Ricontrolla la risposta*.
- Skill in formato `SKILL.md` con `name` e `description` nel blocco iniziale; cartelle `assets/`, `references/`, `scripts/`; SKILL.md sotto le 500 righe. File di istruzioni degli agenti: `AGENTS.md` (Codex), `CLAUDE.md` (Claude Code), `GEMINI.md` (Antigravity).

## 10. Controlli prima di considerarla finita

1. Controllo della sintassi dello script (per esempio `node --check`).
2. Aprire **tutte** le lezioni nei 4 stati (nessuno strumento, ChatGPT, Claude, Gemini) e verificare che non compaiano `undefined`, `[object Object]` o `NaN` e che non ci siano errori.
3. Verificare a 400px che nessuna lezione faccia scorrere la pagina in orizzontale.
4. Provare: esempi precaricati, filtri del ricettario, scaricamento di `SKILL.md`, cambio di strumento (la pagina deve restare al punto in cui eri), due giri completi di quiz, chiusura e riapertura del file (avanzamento e voti devono restare).

## 11. Pubblicazione (facoltativa)

L'originale è pubblicato su GitHub Pages dal repository pubblico `puntospillo/Consulenza-ai`, caricando solo il file `Guida-AI-5-Pilastri/Guida-AI-5-Pilastri.html`.

---

## Prompt da usare nella chat nuova

> Costruisci l'app descritta nel documento qui sopra, in un unico file HTML chiamato `Guida-AI-5-Pilastri.html`.
> Prima di scrivere codice: fammi le domande necessarie, una alla volta, poi propormi un piano a tappe (struttura e motore, poi i contenuti pilastro per pilastro, poi ricettario, libreria skill e quiz).
> Verifica sul web lo stato attuale di ChatGPT, Claude e Gemini prima di scrivere le istruzioni operative, e segnalami le differenze rispetto al capitolo 9.
> Alla fine esegui i controlli del capitolo 10 e dimmi cosa non hai potuto verificare.
