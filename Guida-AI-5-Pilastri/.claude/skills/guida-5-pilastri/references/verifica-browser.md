# Verifica nel browser (prima di pubblicare)

Apri il file nel browser interno e incolla questo nella console (o eseguilo con lo strumento JavaScript).

## 1. Tutte le lezioni, tutti gli strumenti, tutte le lingue

```js
const errs=[];
for (const lang of Object.keys(LANGS)) { setLang(lang);
  for (const t of ['','chatgpt','claude','gemini']) { S.tool=t;
    for (let i=0;i<LESSONS.length;i++){
      try{ goTo(i);
        const m=document.getElementById('page').innerText.match(/.{0,40}(undefined|\[object Object\]|NaN).{0,40}/);
        if(m) errs.push([lang,t,LESSONS[i].id,m[0]]);
      }catch(e){ errs.push([lang,t,LESSONS[i].id,e.message]); }
    } } }
errs
```

Risultato atteso: array vuoto.

## 2. Nessuno scorrimento orizzontale a 400px

Imposta la finestra a 400×850, poi:

```js
const over=[]; for (let i=0;i<LESSONS.length;i++){ goTo(i);
  if(document.documentElement.scrollWidth > document.documentElement.clientWidth+2) over.push(LESSONS[i].id); }
over
```

## 3. Quiz

```js
document.querySelector('[data-act="qz-start"]').click();
for(let k=0;k<10;k++){ document.querySelector('[data-act="qz-ans"]').click(); document.querySelector('[data-act="qz-next"]').click(); }
```

Deve arrivare al voto senza errori. Con uno strumento scelto devono comparire anche le domande con `t:` di quello strumento.

## 4. Salvataggio

Cambia lingua e strumento, completa una lezione, ricarica la pagina: devono restare lingua, strumento, avanzamento e voti.

## 5. Residui di italiano nelle lingue tradotte

Il controllo 1 trova `undefined`/`NaN`, ma non un testo rimasto in italiano (che è comunque una stringa valida). Serve una scansione euristica separata, dopo ogni giro di traduzione:

```js
const italianTells = /\b(perché|però|questo|questa|questi|queste|sempre|ecco|allora|proprio|già|invece|soprattutto|così|quale|quali|senza|tramite|oppure|inoltre|infatti|cioè|nonché|purché|affinché|benché|dell'AI|dell’AI|all'AI|all’AI|sull'AI|sull’AI)\b/;
const hits=new Set();
for (const lang of ['en','es','fr']) { setLang(lang);
  for (const t of ['chatgpt','claude','gemini']) { S.tool=t;
    for (let i=0;i<LESSONS.length;i++){ goTo(i);
      document.getElementById('page').innerText.split('\n').forEach(line=>{
        if (italianTells.test(line)) hits.add(`${lang}|${LESSONS[i].id}|${line.slice(0,160)}`);
      });
    } } }
[...hits]
```

Risultato atteso: array vuoto. Le parole nella lista sono scelte apposta perché **non esistono** in inglese/spagnolo/francese (a differenza di "poco", "dopo", "dentro", "tutto" ecc. che sono anche parole spagnole/italiane comuni e darebbero falsi positivi). Se emergono righe, cerca il testo esatto nel sorgente: quasi sempre è dentro una funzione o un array **fuori da un `body:()=>`** (vedi il paragrafo "Attenzione con gli array/oggetti di primo livello" in `SKILL.md`), quindi mai passato dal codemod di traduzione e da wrappare a mano.
