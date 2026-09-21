# Mappa del file

Ordine dei blocchi in `Guida-AI-5-Pilastri.html` (i numeri di riga cambiano: cerca con `grep -n`).

| Blocco | Come trovarlo |
|---|---|
| CSS | `<style>` … `</style>` in testa |
| Struttura pagina | `<div class="app">` (indice `#side`, barra `.topbar`, `#page`) |
| Lingue e traduzioni | `const LANGS`, `const TXT`, `function t(` |
| Strumenti | `const TOOLS = {`, `TOOL_INTRO`, `TOOL_MODELS`, `AGG_DATA` |
| Stato | `function initState()` |
| Helper testo/HTML | `const esc =`, `function fld(`, `const card =`, `const aiMake =` |
| Schemi SVG | `function pillarsSVG(`, `hierSVG`, `chainSVG`, `chatVsAgentSVG`, `loopSVG`, `flowSVG`, `mapBars` |
| Istruzioni per strumento | `const HOW = {` (le chiavi sono commentate: `/* ---- … ---- */`) |
| Etichette dove/installazioni | `const WHERE = {`, `const NEED = {`, `const AGENT_MD` |
| Aiuto alla scelta | `const DEC_Q`, `function decide(` |
| Lezioni | `/* ============ LEZIONI ============ */` poi le `L({id:'…'})` in ordine |
| Generatori di testo | `function buildPrompt(`, `fileText`, `persText`, `projText`, `asstText`, `skillText`, `appText`, `prdText`, `agentText`, `cmdText` |
| Esempi precaricati | `const PRESETS`, `SKILL_PRESETS`, `APP_PRESETS`, `AGENT_PRESETS`, `MAP_EXAMPLE` (funzioni tradotte a runtime: ognuna è `() => [...]`, non un array statico — vedi nota in `SKILL.md`) |
| Mini-quiz "cosa ti serve?" (lezione p2-differenze) | `const QUIZ = () => [`, `const QOPT = () => [` |
| Libreria skill | `const SKILL_LIB = [` |
| Casi di agenti | `const CASI = [` |
| Ricettario | `const RIC_CAT`, `const RIC_LVL`, `const RICETTE = [` |
| Quiz | `const QZ_ARG`, `const QZ = [`, `qzPool`, `qzPick`, `qzHome`, `qzQuestion`, `qzEnd` |
| Versione | `const REV =` |
| Motore | `/* ============ MOTORE DELLA GUIDA ============ */`: `GROUPS`, `renderSide`, `renderToolSel`, `progress`, `render`, `goTo`, gestore dei click (`data-act`) |
| Avvio | in fondo: `initState()`, ripristino da `localStorage`, `render()` |

## Azioni dei pulsanti (`data-act`)

`goi` (vai a lezione per indice) · `go` (vai per id) · `next` · `menu` · `copy` · `download` · `set-tool` · `set-lang` · `reset` · `ric` · `ric-l` · `quiz` · `preset` · `preset-skill` · `preset-app` · `preset-agent` · `add-row` · `del-row` · `example-map` · `qz-start` · `qz-ans` · `qz-next` · `qz-home` · `qz-reset`

## Chiavi di `localStorage`

- `guida-ai-5-pilastri` → `{lesson, done, tool, lang}`
- `guida-ai-5-pilastri-quiz` → `{storico:[{t, voto, arg}], viste:{}}`

Le due chiavi sono **condivise fra le lingue**: chi cambia lingua non perde avanzamento né voti.
