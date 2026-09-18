const b=document.querySelector('.menu'),n=document.querySelector('.links');
if(b&&n)b.onclick=()=>{const o=n.classList.toggle('open');b.setAttribute('aria-expanded',o)};
document.querySelectorAll('[data-year]').forEach(e=>e.textContent=new Date().getFullYear());
const target=new Date('2026-10-18T08:00:00-04:00');
document.querySelectorAll('[data-countdown]').forEach(c=>{const ms=Math.max(0,target-new Date());if(!ms){c.textContent='The Odyssey is underway';return}const days=Math.floor(ms/864e5),hours=Math.floor(ms%864e5/36e5);c.textContent=`${days} days ${hours} hours to departure`});
const io='IntersectionObserver'in window?new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');io.unobserve(e.target)}}),{threshold:.1}):null;
document.querySelectorAll('.reveal').forEach(e=>io?io.observe(e):e.classList.add('visible'));
document.querySelectorAll('[data-form]').forEach(f=>f.onsubmit=e=>{e.preventDefault();f.querySelector('small').textContent='Email signup is being connected before launch. No address was submitted.'});
