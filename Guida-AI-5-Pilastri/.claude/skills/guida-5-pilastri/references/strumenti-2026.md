# Stato degli strumenti — verificato il 20 settembre 2026

Da ricontrollare sul web prima di scrivere istruzioni operative: cambia ogni poche settimane.
Nel file la data è in `const AGG_DATA` (mostrata nella pagina Benvenuto).

## ChatGPT (OpenAI)

- App per computer unica: **Chat**, **Work** (lavori lunghi su documenti, fogli, presentazioni e **cartelle locali**), **Codex** (app e programmi). La vecchia "modalità agente" non esiste più.
- Avvio di Work sul computer: apri una cartella o un progetto collegato, poi scegli **Work** dal selettore. Permessi sotto la casella: lasciare **Chiedi approvazione**; le modalità più libere si attivano in *Impostazioni › Generale › Permessi*.
- **Skill**: *barra laterale › Plugin › scheda Skill*, solo piani aziendali (Business, Enterprise, Edu). Piani personali: Progetto dedicato o Codex. Richiamo con `@` in chat, `$` in Codex. Skill di Codex in `.agents/skills/`.
- **GPT personalizzati** in dismissione. **Sites** pubblica siti e web app.
- Comandi Codex: `/status` nell'app, `/compact` nella versione a riga di comando.
- Modelli: **GPT-6 Astra** (3 settembre 2026, il più potente, piani a pagamento) e **GPT-5.6** nelle versioni Sol, Terra, Luna.

## Claude (Anthropic)

- **16 settembre 2026: Cowork è entrato nella chat.** Restano due modalità: **Chat** (domande, file, cartelle, artifact) e **Claude Code** (app e programmi). Rollout graduale: prima Pro e Max, poi Team e Free. Nelle versioni non ancora aggiornate c'è ancora la scheda **Cowork**: funziona allo stesso modo.
- Novità dello stesso annuncio: **Docs** e **Slides** (documenti e presentazioni scritti insieme), Design dentro le conversazioni.
- Cartella di lavoro: nella casella, **Lavora in un progetto o cartella**. Approvazioni: **Manuale** (predefinita) o **Automatica**. Istruzioni per cartella quando la scegli; istruzioni generali in *Impostazioni › Cowork › Istruzioni globali* (dove presente).
- **Skill**: *Personalizza › Skill* → `+` → Crea skill → Carica una skill (.zip). Condivisione su Team ed Enterprise dal menu ⋯.
- Altre voci: *Impostazioni › Funzionalità* (Esecuzione codice e creazione file, memoria), *Impostazioni › Profilo* (preferenze), *Impostazioni › Utilizzo* (limite di 5 ore e settimanale), *Impostazioni › Privacy*, chat in incognito.
- Claude Code: `/init`, `/clear`, `/compact`, `/context`. Componenti aggiuntivi per Excel, Word, PowerPoint; Claude in Chrome.
- Modelli: **Fable 5.1** (il più potente, in Claude Code), **Opus 5** (lavori difficili), **Sonnet 5** (predefinito), **Haiku 4.5** (rapido).

## Gemini (Google)

- App Gemini: **Gem**, **Notebook** (spazio per tema), Canvas, Deep Research, e Gemini dentro Gmail, Drive, Documenti, Fogli, Presentazioni.
- **Gemini Notebook** = l'ex NotebookLM (rinominato a luglio 2026): risposte citate sui documenti caricati.
- **Antigravity** (app per computer, `antigravity.google/download`) ha sostituito Gemini CLI per gli account personali dal 18 giugno 2026. Progetti con cartelle, regole in `GEMINI.md` o `AGENTS.md`, skill in `.agents/skills/`. Livello gratuito con limiti che si ricaricano.
- **Gemini Spark non è disponibile in Italia e nell'UE**.
- **Google AI Studio › Build** per app complete online.
- Voci utili: *Impostazioni › Contesto personale*, *Mantieni attività*, *Altro › Ricontrolla la risposta*, *Condividi ed esporta › Esporta in Documenti*, *Esporta in Fogli*.
- Modelli nel selettore dell'app: **Flash-Lite**, **Flash** (Gemini 3.8 con AI Pro e Ultra), **Pro** (Gemini 3.1 Pro), **Deep Think** (solo Ultra).

## Skill: formato standard

`SKILL.md` con `name` e `description` nel blocco iniziale, sotto le 500 righe; cartelle `assets/` (modelli), `references/` (dettagli letti solo se richiamati), `scripts/` (calcoli e controlli).
File di istruzioni degli agenti: `AGENTS.md` (Codex), `CLAUDE.md` (Claude Code), `GEMINI.md` (Antigravity).
