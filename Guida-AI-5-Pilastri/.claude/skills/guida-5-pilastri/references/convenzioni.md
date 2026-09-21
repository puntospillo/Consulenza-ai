# Convenzioni di contenuto e di codice

## Contenuto

- **Destinatari**: persone non tecniche. Ogni termine inglese va spiegato la prima volta.
- **Mai "il cliente"** come soggetto esterno: chi legge è l'utente. Esempi dal suo lavoro: ufficio acquisti, fornitori, fatture, contratti, verbali, colleghi.
- **Un esempio concreto per ogni concetto**, scelto tra i casi più frequenti in ufficio.
- **Istruzioni per un solo strumento alla volta**: `howBox('chiave')` mostra solo quello scelto; `byTool({chatgpt,claude,gemini,any})` per le frasi brevi; `where('chat'|'local'|'app'|…)` per le etichette.
- **Installazioni sempre dichiarate**: `needTag`/`whereLine` producono "⬇ da installare" oppure "Nessuna installazione".
- **Regole anti-invenzione** dove servono: usa solo i file dati, indica pagina e frase esatta, scrivi NON TROVATO, calcoli con il codice, l'ultima verifica è dell'utente.
- **Privacy**: account aziendale, dati anonimizzati, mai password in chat, agenti su copie dei file.
- **Riquadro `aiMake(...)`** in ogni lezione dove si crea qualcosa (prompt, istruzioni, skill, .md, app, agente).
- **`keys([...])`** ("Da ricordare") chiude quasi ogni lezione.
- Apostrofo tipografico `’` e virgolette `“ ”`.

## Codice

- Tutto in un file: niente librerie, niente richieste di rete, niente `fetch`.
- `localStorage` solo dentro `try/catch`; si salvano avanzamento, strumento, lingua e risultati del quiz. **Mai** i testi degli esercizi.
- Nessun `innerHTML` con testo scritto dall'utente senza `esc()`.
- Gli schemi sono SVG inline: niente immagini esterne.
- Un solo `id` per elemento interattivo nella pagina corrente (gli `outBox` usano id parlanti: `p-skill`, `ric-12`, `caso-3`).
- Responsive obbligatorio: nessuno scorrimento orizzontale a 400px. Tabelle dentro `.tbl-wrap`, schemi dentro `.tree`/`.diagram`.

## Mattoncini disponibili

`card`, `analogy`, `keys`, `warn`, `note`, `ex`, `tryBox`, `outBox`, `tbl`, `fld`, `cb`, `aiMake`, `howBox`, `whereLine`, `stepsL`, `mp` (percorso di menu), `cmd` (comando), `rule`, `badge`.

## Stato dell'app

`S` (in `initState`) contiene: `tool`, `lang`, `done`, `prompt`, `dec`, `file`, `proj`, `asst`, `md`, `skill`, `quiz`, `map`, `app`, `prd`, `agente`, `cmd`, `ric`, `pers`, `tok`, `qz`.
`render()` ridisegna tutta la lezione corrente; `update()` aggiorna solo le parti interattive mentre l'utente scrive.
