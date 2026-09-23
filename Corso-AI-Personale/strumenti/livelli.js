/* Controllo dei livelli di Guida AI Personal.
   Cerca, nel testo che l'utente vede davvero, le parole che a quel livello
   non sono ancora state spiegate (agente, skill, token, Codex, Cowork...).
   Uso:  node strumenti/livelli.js        (dalla cartella Corso-AI-Personale) */
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path');
const FILE = path.join(__dirname, '..', 'Corso-AI-Personale.html');
const js = fs.readFileSync(FILE, 'utf8').split("<script>\n'use strict';", 2)[1].split('</script>')[0];

const store = {};
function mkEl(id){
  return { id, _html:'', _text:'', style:{ setProperty(){}, width:'' }, dataset:{}, title:'',
    classList:{ add(){}, remove(){}, toggle(){}, contains(){ return false; } }, children: [],
    set innerHTML(v){ this._html = String(v); }, get innerHTML(){ return this._html; },
    set textContent(v){ this._text = String(v); }, get textContent(){ return this._text; },
    getBoundingClientRect(){ return {top:0}; }, appendChild(){}, remove(){}, click(){}, select(){}, focus(){},
    closest(){ return null; }, querySelectorAll(){ return []; } };
}
const els = {}; const get = id => els[id] || (els[id] = mkEl(id));
['page','side','toolsel','lvchip','prog-l','prog-r','prog-i','toast'].forEach(get);
const sandbox = {
  document:{ getElementById: id => els[id] || null, querySelector: s => get(s.replace(/^#/,'')),
    querySelectorAll: () => [], createElement: () => mkEl('t'), addEventListener(){}, body:{ appendChild(){} } },
  window:{ scrollTo(){}, scrollBy(){}, location:{hash:''} }, location:{ hash:'' }, history:{ replaceState(){} },
  localStorage:{ getItem:k=>store[k]??null, setItem:(k,v)=>{store[k]=String(v);}, removeItem:k=>{delete store[k];} },
  navigator:{ clipboard:{ writeText:async()=>{} } },
  URL:{ createObjectURL:()=>'b', revokeObjectURL(){} }, Blob: class {},
  setTimeout, clearTimeout, console, Math, Date, JSON, confirm:()=>false
};
sandbox.globalThis = sandbox; vm.createContext(sandbox);
vm.runInContext("'use strict';\n" + js +
  "\nglobalThis.__api={get S(){return S}, LESSONS, TEST, MAP_EXAMPLE, toolIntro};", sandbox, {filename:'guida.js'});
const A = sandbox.__api, S = A.S, LESSONS = A.LESSONS;

/* Parole che a quel livello non sono ancora state spiegate. */
const VIETATE = {
  1: [['agent','agente/agenti'], ['\\bskill','skill'], ['SKILL\\.md','SKILL.md'], ['Codex','Codex'],
      ['\\bWork\\b','Work'], ['Cowork','Cowork'], ['Antigravity','Antigravity'], ['Claude Code','Claude Code'],
      ['AI Studio','AI Studio'], ['\\bSites\\b','Sites'], ['token','token'], ['markdown','markdown'],
      ['\\.md\\b','.md'], ['mini-app','mini-app'], ['terminale','terminale'],
      ['da installare','etichetta "da installare"'], ['app per computer','app per computer']],
  2: [['agent','agente/agenti'], ['\\bskill','skill'], ['SKILL\\.md','SKILL.md'], ['Codex','Codex'],
      ['Cowork','Cowork'], ['Antigravity','Antigravity'], ['Claude Code','Claude Code'], ['AI Studio','AI Studio'],
      ['mini-app','mini-app'], ['terminale','terminale'], ['\\bWork\\b','Work']]
};
/* Queste due lezioni descrivono apposta cosa c'e nei livelli successivi. */
const AMMESSE = ['livello', 'fine-piano'];

const testo = h => String(h).replace(/<[^>]+>/g,' ').replace(/\s+/g,' ');
let totale = 0;
for(const lv of [1,2]){
  const trovati = {};
  for(const tool of ['', 'chatgpt', 'claude', 'gemini']){
    S.lv = lv; S.tool = tool; S.test = {};
    S.map.rows = A.MAP_EXAMPLE.map((r,i)=>Object.assign({id:'r'+i}, r));
    S.quiz = {};
    for(const l of LESSONS.filter(x=>x.lv <= lv)){
      if(AMMESSE.includes(l.id)) continue;
      const t = testo(l.body());
      for(const [re, nome] of VIETATE[lv]){
        const m = t.match(new RegExp(re, 'gi'));
        if(m){ const k = `${l.id} → ${nome}`; trovati[k] = (trovati[k] || 0) + m.length; }
      }
    }
    if(tool){
      const t = testo(A.toolIntro(tool));
      for(const [re, nome] of VIETATE[lv])
        if(new RegExp(re, 'i').test(t)) trovati[`presentazione di ${tool} → ${nome}`] = 1;
    }
  }
  const n = Object.keys(trovati).length; totale += n;
  console.log(`\n=== LIVELLO ${lv}: ${n === 0 ? 'pulito' : n + ' punti da sistemare'} ===`);
  Object.entries(trovati).sort().forEach(([k,c])=>console.log(`  ${k}  (${c}x)`));
}

/* Il quiz non deve usare parole non spiegate, in nessuna delle sue parti. */
console.log('\n=== QUIZ ===');
let quiz = 0;
sandbox.QZ === undefined && vm.runInContext('globalThis.__qz = QZ;', sandbox);
(sandbox.__qz || []).forEach((q, i)=>{
  const t = [q.q, ...q.o, q.e].join(' ');
  (VIETATE[q.lv] || []).forEach(([re, nome])=>{
    if(new RegExp(re, 'i').test(t)){ quiz++; console.log(`  domanda ${i} (liv.${q.lv}) → ${nome}: ${testo(q.q).slice(0,60)}...`); }
  });
});
if(quiz === 0) console.log('  pulito');
totale += quiz;

console.log(totale === 0
  ? '\nTutto in regola: nessuna parola fuori livello.'
  : `\nDa sistemare: ${totale} punti.`);
process.exit(totale === 0 ? 0 : 1);
