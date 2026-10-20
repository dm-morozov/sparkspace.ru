const toggle=document.querySelector('.menu-button'),nav=document.querySelector('#navigation'),mega=document.querySelector('.mega');
const megaSummary=mega.querySelector('summary'),megaPanel=mega.querySelector('.mega-panel');
const mobileNavigation=window.matchMedia('(max-width:1180px)');
const hoverNavigation=window.matchMedia('(hover:hover) and (pointer:fine)');
let megaCloseTimer;
function cancelMegaClose(){window.clearTimeout(megaCloseTimer)}
function setMegaOpen(open){cancelMegaClose();mega.open=open;megaSummary.setAttribute('aria-expanded',String(open))}
megaPanel.id=megaPanel.id||'services-navigation';
megaSummary.setAttribute('aria-controls',megaPanel.id);
megaSummary.setAttribute('aria-expanded',String(mega.open));
// Keep native details/summary activation for keyboard, touch and no-JS navigation.
mega.addEventListener('toggle',()=>megaSummary.setAttribute('aria-expanded',String(mega.open)));
function closeNavigation(){nav.classList.remove('open');toggle.setAttribute('aria-expanded','false');toggle.setAttribute('aria-label','Открыть меню');setMegaOpen(false)}
toggle.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));toggle.setAttribute('aria-label',open?'Закрыть меню':'Открыть меню');nav.classList.toggle('open',open);if(!open)setMegaOpen(false)});
mega.addEventListener('pointerenter',event=>{if(event.pointerType==='mouse'&&hoverNavigation.matches&&!mobileNavigation.matches)setMegaOpen(true)});
mega.addEventListener('pointerleave',event=>{
 if(event.pointerType!=='mouse'||!hoverNavigation.matches||mobileNavigation.matches)return;
 cancelMegaClose();
 // Allow travel across the small visual gap, and never hide a focused service link.
 megaCloseTimer=window.setTimeout(()=>{if(!megaPanel.contains(document.activeElement))setMegaOpen(false)},180);
});
mega.addEventListener('focusin',cancelMegaClose);
document.addEventListener('click',e=>{if(!mega.contains(e.target))setMegaOpen(false);if(!nav.contains(e.target)&&!toggle.contains(e.target))closeNavigation()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(mega.open){setMegaOpen(false);megaSummary.focus()}else if(nav.classList.contains('open')){closeNavigation();toggle.focus()}}});
mega.addEventListener('focusout',e=>{if(!e.relatedTarget||!mega.contains(e.relatedTarget))setMegaOpen(false)});
nav.addEventListener('focusout',e=>{if(e.relatedTarget&&!nav.contains(e.relatedTarget)&&e.relatedTarget!==toggle)closeNavigation()});
mobileNavigation.addEventListener('change',closeNavigation);
hoverNavigation.addEventListener('change',()=>setMegaOpen(false));
const current=location.pathname.split('/').pop()||'index.html';
nav.querySelectorAll('a[href]').forEach(a=>{if(a.getAttribute('href')===current){a.setAttribute('aria-current','page');if(mega.contains(a))mega.classList.add('is-current')}});

// Application page: reveal once, with visible no-JS and reduced-motion fallbacks.
const appRevealNodes=[...document.querySelectorAll('[data-app-reveal]')];
if(appRevealNodes.length && 'IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches){
 const appRevealObserver=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('app-is-visible');appRevealObserver.unobserve(entry.target);}});},{threshold:.12});
 appRevealNodes.forEach(node=>{node.classList.add('app-will-reveal');appRevealObserver.observe(node);});
}
