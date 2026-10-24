const flowRoot=document.querySelector('.business-flows');
if(flowRoot){
 const flowData=JSON.parse(document.querySelector('#flow-data').textContent);
 const tabs=[...flowRoot.querySelectorAll('[data-flow-tab]')];
 const panels=[...flowRoot.querySelectorAll('[data-flow-panel]')];
 function scenarioFromHash(){
  const id=location.hash.startsWith('#flow-')?location.hash.slice(6):'';
  return flowData.some(flow=>flow.id===id)?id:null;
 }
 let current=scenarioFromHash()||flowData[0].id;
 const mobileJumps=new Map();
 const selectedSteps=new Map();
 flowRoot.classList.add('flow-enhanced');
 flowRoot.querySelector('.flow-tabs').setAttribute('role','tablist');
 function step(panel,index){
  const flow=flowData.find(f=>f.id===panel.dataset.flowPanel);
  const [title,status,event,owner,action]=flow.steps[index];
  selectedSteps.set(flow.id,index);
  panel.querySelectorAll('[data-manager-screen]').forEach(view=>{view.hidden=Number(view.dataset.managerScreen)!==index;});
  panel.querySelectorAll('[data-manager-progress]').forEach(marker=>{marker.classList.toggle('is-complete',Number(marker.dataset.managerProgress)<=index);});
  panel.querySelectorAll('[data-flow-step]').forEach((button,i)=>button.classList.toggle('is-complete',i<index));
  const preview=panel.querySelector('[data-preview-stage]');
  if(preview){preview.textContent=status;panel.querySelector('[data-preview-owner]').textContent=owner;panel.querySelector('[data-preview-next]').textContent=index<flow.steps.length-1?flow.steps[index+1][0]:'Процесс завершён';}

  panel.querySelector('[data-event-title]').textContent=(preview||panel.querySelector('.manager-workspace'))?title:title+' \u00b7 '+status;
  panel.querySelector('[data-event-text]').textContent=event;
  panel.querySelector('[data-event-owner]').textContent=owner;
  panel.querySelector('[data-event-action]').textContent=action;
  panel.querySelector('[data-flow-index]').textContent='Шаг '+(index+1)+' из 5';
  panel.querySelector('[data-flow-back]').disabled=index===0;
  panel.querySelector('[data-flow-next]').disabled=index===4;
  panel.querySelector('.flow-event').hidden=false;
  panel.querySelectorAll('[data-flow-step]').forEach((button,i)=>{button.setAttribute('aria-pressed',String(i===index));if(i===index)button.setAttribute('aria-current','step');else button.removeAttribute('aria-current');});
  const jump=mobileJumps.get(flow.id);
  if(jump){
   const selectedButton=panel.querySelectorAll('[data-flow-step]')[index];
   const screen=panel.querySelector('[data-manager-screen="'+index+'"]');
   selectedButton.parentElement.append(jump.toManager);
   screen.prepend(jump.toStep);
   jump.toManager.setAttribute('aria-label','Показать вид руководителя: '+title);
   jump.toManager.setAttribute('aria-controls',screen.id);
   jump.toStep.setAttribute('aria-label','Вернуться к шагу: '+title);
   jump.selectedButton=selectedButton;jump.screen=screen;
  }
 }
 function select(id,focus=false,syncUrl=true){
  if(!flowData.some(flow=>flow.id===id))return;
  current=id;if(!selectedSteps.has(id))selectedSteps.set(id,0);
  if(syncUrl&&location.hash!=='#flow-'+id){
   // Keep query/context and history state; selecting a tab must not scroll the page.
   const url=new URL(location.href);url.hash='flow-'+id;
   try{history.replaceState(history.state,'',url.href)}catch{/* Restricted previews may not allow history writes. */}
  }
  tabs.forEach(tab=>{const active=tab.dataset.flowTab===id;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;if(active&&focus)tab.focus();});
  panels.forEach(panel=>{panel.hidden=panel.dataset.flowPanel!==id;if(!panel.hidden)step(panel,selectedSteps.get(id)||0);});
 }
 tabs.forEach((tab,index)=>{
  tab.id='tab-'+tab.dataset.flowTab;tab.setAttribute('role','tab');tab.setAttribute('aria-controls','flow-'+tab.dataset.flowTab);
  tab.addEventListener('click',event=>{event.preventDefault();select(tab.dataset.flowTab);});
  tab.addEventListener('keydown',event=>{let next;if(event.key==='ArrowRight')next=(index+1)%tabs.length;else if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else if(event.key===' '||event.key==='Enter'){event.preventDefault();select(tab.dataset.flowTab);return;}else return;event.preventDefault();select(tabs[next].dataset.flowTab,true);});
 });
 panels.forEach(panel=>{
  const screens=[...panel.querySelectorAll('[data-manager-screen]')];
  if(screens.length){
   const toManager=document.createElement('button'),toStep=document.createElement('button');
   toManager.type='button';toManager.className='flow32-jump';toManager.textContent='Вид руководителя';
   toStep.type='button';toStep.className='flow32-return';toStep.textContent='Вернуться к шагу';
   screens.forEach(screen=>{screen.id='manager-'+panel.dataset.flowPanel+'-'+screen.dataset.managerScreen;screen.tabIndex=-1;});
   const jump={toManager,toStep};mobileJumps.set(panel.dataset.flowPanel,jump);
   function reveal(target,block){target.focus({preventScroll:true});target.scrollIntoView({block,behavior:'auto'});}
   toManager.addEventListener('click',()=>reveal(jump.screen,'start'));
   toStep.addEventListener('click',()=>reveal(jump.selectedButton,'center'));
  }
  panel.querySelectorAll('[data-outcome]').forEach(button=>button.addEventListener('click',()=>{
   panel.querySelectorAll('[data-outcome]').forEach(item=>item.setAttribute('aria-pressed',String(item===button)));
   panel.querySelector('[data-outcome-text]').textContent=button.dataset.outcome;
  }));
  panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby','tab-'+panel.dataset.flowPanel);
  panel.querySelectorAll('[data-flow-step]').forEach(button=>{button.disabled=false;button.addEventListener('click',()=>step(panel,Number(button.dataset.flowStep)));});
  panel.querySelector('[data-flow-back]').addEventListener('click',()=>step(panel,Math.max(0,(selectedSteps.get(panel.dataset.flowPanel)||0)-1)));
  panel.querySelector('[data-flow-next]').addEventListener('click',()=>step(panel,Math.min(4,(selectedSteps.get(panel.dataset.flowPanel)||0)+1)));
  panel.querySelector('[data-flow-start]').addEventListener('click',()=>step(panel,0));
 });
 function followHash(){
  const id=scenarioFromHash();if(!id)return;
  const activePanel=panels.find(panel=>!panel.hidden);
  select(id,Boolean(activePanel&&activePanel.contains(document.activeElement)),false);
 }
 window.addEventListener('hashchange',followHash);
 window.addEventListener('popstate',followHash);
 select(current,false,false);
}
