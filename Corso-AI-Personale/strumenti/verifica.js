/* Verifica di Guida AI Personal.
   Apre ogni lezione nei 3 livelli e nei 4 stati di strumento, senza browser.
   Uso:  node strumenti/verifica.js        (dalla cartella Corso-AI-Personale) */
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path');
const FILE = path.join(__dirname, '..', 'Corso-AI-Personale.html');
const html = fs.readFileSync(FILE, 'utf8');
const js = html.split("<script>\n'use strict';", 2)[1].split('</script>')[0];

/* ---- DOM minimo: basta a far girare il codice della pagina ---- */
const store = {};
function mkEl(id){
  return {
    id, _html:'', _text:'', style:{ setProperty(){}, width:'' }, dataset:{}, title:'',
    classList:{ add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    children: [],
    set innerHTML(v){ this._html = String(v); }, get innerHTML(){ return this._html; },
    set textContent(v){ this._text = String(v); }, get textContent(){ return this._text; },
    getBoundingClientRect(){ return {top:0}; },
    appendChild(){}, remove(){}, click(){}, select(){}, focus(){},
    closest(){ return null; }, querySelectorAll(){ return []; }
  };
}
const els = {};
const get = id => els[id] || (els[id] = mkEl(id));
['page','side','toolsel','lvchip','prog-l','prog-r','prog-i','toast'].forEach(get);
const sandbox = {
  document:{
    getElementById: id => els[id] || null,
    querySelector: s => get(s.replace(/^#/,'')),
    querySelectorAll: () => [],
    createElement: () => mkEl('tmp'),
    addEventListener(){}, body:{ appendChild(){} }
  },
  window:{ scrollTo(){}, scrollBy(){}, location:{hash:''} },
  location:{ hash:'' }, history:{ replaceState(){} },
  localStorage:{ getItem:k=>store[k]??null, setItem:(k,v)=>{store[k]=String(v);}, removeItem:k=>{delete store[k];} },
  navigator:{ clipboard:{ writeText:async()=>{} } },
  URL:{ createObjectURL:()=>'blob:', revokeObjectURL(){} }, Blob: class {},
  setTimeout, clearTimeout, console, Math, Date, JSON, confirm:()=>false
};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
const esporta = `
globalThis.__api = { get S(){return S}, LESSONS, LV, TEST, MAP_EXAMPLE, QZ, QZ_ARG, HOW, WHERE, RICETTE,
  qzAvail, qzPick, qzQuestion, qzEnd, ricVisible, testLevel, toolIntro, set curId(v){curId=v} };`;
try { vm.runInContext("'use strict';\n" + js + esporta, sandbox, {filename:'guida.js'}); }
catch(e){ console.log('ERRORE ALL’AVVIO:', e.message); process.exit(1); }

const A = sandbox.__api, S = A.S, LESSONS = A.LESSONS, LV = A.LV;
const problemi = [];
const STRUMENTI = ['', 'chatgpt', 'claude', 'gemini'];

console.log('File:', path.basename(FILE), '·', html.length.toLocaleString('it-IT'), 'caratteri');
console.log('Revisione:', (js.match(/const REV = '([^']+)'/)||[])[1], '· verificato il', (js.match(/const AGG = '([^']+)'/)||[])[1]);
console.log('Lezioni totali:', LESSONS.length);
[1,2,3].forEach(n=>{
  S.lv = n; S.ric = {f:'tutti', l:'tutti'};
  console.log(`  livello ${n} (${LV[n].l}): ${LESSONS.filter(l=>l.lv<=n).length} lezioni · ${A.qzAvail().length} domande di quiz · ${A.ricVisible().length} ricette`);
});

/* ---- 1. ogni lezione, in ogni livello, con ogni strumento ---- */
let render = 0;
for(const lv of [1,2,3]){
  for(const tool of STRUMENTI){
    S.lv = lv; S.tool = tool;
    S.test = lv === 1 ? {} : Object.fromEntries(A.TEST.map(q=>[q.id, 1]));
    S.map.rows = A.MAP_EXAMPLE.map((r,i)=>Object.assign({id:'r'+i}, r));
    S.quiz = {q1:'prompt', q6:'skill'};
    for(const l of LESSONS.filter(x=>x.lv <= lv)){
      render++;
      const dove = `${l.id} [liv.${lv}/${tool||'nessuno strumento'}]`;
      let out;
      try { out = l.body(); }
      catch(e){ problemi.push(`ERRORE  ${dove} body(): ${e.message}`); continue; }
      try { A.curId = l.id; if(l.update) l.update(); }
      catch(e){ problemi.push(`ERRORE  ${dove} update(): ${e.message}`); }
      const tutto = out + ' ' + Object.values(els).map(e=>e._html + ' ' + e._text).join(' ');
      ['undefined','[object Object]','NaN'].forEach(w=>{
        if(tutto.includes(w)) problemi.push(`ATTENZIONE  ${dove} contiene "${w}"`);
      });
    }
  }
}
console.log(`\nRender eseguiti: ${render}`);

/* ---- 2. due giri di quiz per livello ---- */
for(const lv of [1,2,3]){
  S.lv = lv;
  for(let giro = 0; giro < 2; giro++){
    const set = A.qzPick();
    if(set.length !== Math.min(10, A.qzAvail().length)) problemi.push(`ATTENZIONE  quiz liv.${lv}: giro da ${set.length} domande`);
    S.qz = {fase:'domanda', set, i:0, risposte:[], ordine:set.map(()=>[0,1,2,3])};
    for(let i = 0; i < set.length; i++){
      S.qz.i = i; S.qz.risposte[i] = {scelta:0, ok:true};
      try { A.qzQuestion(); } catch(e){ problemi.push('ERRORE  qzQuestion(): ' + e.message); }
    }
    S.qz.fase = 'fine';
    try { A.qzEnd(); } catch(e){ problemi.push('ERRORE  qzEnd(): ' + e.message); }
    set.forEach(qi=>{
      const q = A.QZ[qi];
      if(q.lv > lv) problemi.push(`ATTENZIONE  quiz liv.${lv}: e uscita una domanda di livello ${q.lv}`);
      const dest = LESSONS.find(x=>x.id === q.go);
      if(!dest) problemi.push(`ATTENZIONE  quiz: rimanda alla lezione inesistente "${q.go}"`);
      else if(dest.lv > lv) problemi.push(`ATTENZIONE  quiz liv.${lv}: rimanda a "${q.go}", che e di livello ${dest.lv}`);
    });
  }
}

/* ---- 3. coerenza delle strutture ---- */
Object.entries(A.QZ_ARG).forEach(([k,x])=>{
  if(!LESSONS.some(l=>l.id === x.go)) problemi.push(`ATTENZIONE  argomento quiz "${k}": lezione "${x.go}" inesistente`);
});
Object.entries(A.HOW).forEach(([k,v])=>{
  ['chatgpt','claude','gemini'].forEach(t=>{ if(!v[t]) problemi.push(`ATTENZIONE  istruzioni "${k}": manca ${t}`); });
});
A.RICETTE.forEach((r,i)=>{
  if(!A.WHERE[r.w]) problemi.push(`ATTENZIONE  ricetta ${i} "${r.t}": chiave "${r.w}" inesistente`);
});

/* ---- 4. il test di livello assegna i livelli giusti ---- */
const esiti = {};
for(const p of [0,1,2,3]){
  S.test = Object.fromEntries(A.TEST.map(q=>[q.id, p]));
  esiti['tutte ' + 'ABCD'[p]] = A.testLevel();
}
console.log('Test di livello, rispondendo sempre uguale →', JSON.stringify(esiti));
if(JSON.stringify(esiti) !== JSON.stringify({'tutte A':1,'tutte B':1,'tutte C':2,'tutte D':3}))
  problemi.push('ATTENZIONE  il test di livello non assegna piu i livelli attesi (A/B=1, C=2, D=3)');

const unici = [...new Set(problemi)];
if(unici.length){ console.log('\n--- PROBLEMI ---'); unici.forEach(p=>console.log(p)); console.log(`\nTotale: ${unici.length}`); process.exit(1); }
console.log('\nNessun problema rilevato.');
