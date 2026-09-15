const b=document.querySelector('.menu'),n=document.querySelector('.links');
if(b&&n)b.onclick=()=>{const o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)};

document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());

const c=document.querySelector('[data-countdown]');
if(c){const d=Math.max(0,Math.ceil((new Date('2026-10-02T09:00:00-04:00')-new Date())/864e5));c.textContent=d?`${d} days to departure`:'The Odyssey is underway'}

const io='IntersectionObserver'in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.1}):null;
document.querySelectorAll('.reveal').forEach(e=>io?io.observe(e):e.classList.add('visible'));

document.querySelectorAll('[data-form]').forEach(f=>f.onsubmit=e=>{e.preventDefault();f.querySelector('small').textContent='Email signup is being connected before launch. No address was submitted.'});

// Keep every page aligned with the canonical PourHouse Life identity.
const logo=location.pathname.includes('/field-notes/')?'../assets/pourhouse-life-logo.webp':'assets/pourhouse-life-logo.webp';
document.querySelectorAll('a.brand').forEach(a=>a.innerHTML=`<img class="brand-logo" src="${logo}" alt="">PourHouse Life`);
document.querySelectorAll('.footer h2').forEach(e=>{if(/^(?:PourHouse|Cissy & Bud)$/.test(e.textContent.trim()))e.textContent='PourHouse Life'});
document.querySelectorAll('.bottom span').forEach(e=>{if(e.childNodes.length===1)e.textContent=e.textContent.replace(/(?:Cissy & Bud|PourHouse)$/,'PourHouse Life')});
document.title=document.title.replace(/\| PourHouse$/,'| PourHouse Life').replace(/Cissy & Bud/g,'PourHouse Life');
const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
for(let node;node=walker.nextNode();){
  const parent=node.parentElement?.tagName;
  if(parent!=='SCRIPT'&&parent!=='STYLE')node.nodeValue=node.nodeValue
    .replace(/Cissy\s*&\s*Bud|Cissy and Bud/g,'PourHouse Life')
    .replace(/77-day PCH-Ex/g,'77-night PCH-Ex');
}

if(location.pathname.endsWith('/prius-utah-2019.html')){
  document.title='Mighty V Passage | PourHouse Life';
  const h1=document.querySelector('h1');if(h1)h1.textContent='Mighty V Passage';
  const intro=document.querySelector('.feature-copy>p:last-child');if(intro)intro.textContent=intro.textContent.replace('five national parks','four Utah national parks');
}
