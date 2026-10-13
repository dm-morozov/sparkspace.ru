const toggle=document.querySelector('.menu-button'),nav=document.querySelector('#navigation'),mega=document.querySelector('.mega');
function closeNavigation(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Открыть меню');mega.open=false}
toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню');nav.classList.toggle('open',open);if(!open)mega.open=false});
document.addEventListener('click',e=>{if(!mega.contains(e.target))mega.open=false;if(!nav.contains(e.target)&&!toggle.contains(e.target))closeNavigation()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(mega.open){mega.open=false;mega.querySelector('summary').focus()}else if(nav.classList.contains('open')){closeNavigation();toggle.focus()}}});
mega.addEventListener('focusout',e=>{if(e.relatedTarget&&!mega.contains(e.relatedTarget))mega.open=false});
nav.addEventListener('focusout',e=>{if(e.relatedTarget&&!nav.contains(e.relatedTarget)&&e.relatedTarget!==toggle)closeNavigation()});
const mobileNavigation=window.matchMedia('(max-width:1100px)');
mobileNavigation.addEventListener('change',()=>closeNavigation());
const current=location.pathname.split('/').pop()||'index.html';
nav.querySelectorAll('a[href]').forEach(a=>{if(a.getAttribute('href')===current){a.setAttribute('aria-current','page');if(mega.contains(a))mega.classList.add('is-current')}});

// Application page: reveal once, with visible no-JS and reduced-motion fallbacks.
const appRevealNodes=[...document.querySelectorAll('[data-app-reveal]')];
if(appRevealNodes.length && 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches){
 const appRevealObserver=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('app-is-visible');appRevealObserver.unobserve(entry.target);}});},{threshold:.12});
 appRevealNodes.forEach(node=>{node.classList.add('app-will-reveal');appRevealObserver.observe(node);});
}
