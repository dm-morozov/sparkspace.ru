const flowRoot=document.querySelector('.business-flows');
if(flowRoot){
 const flowData=JSON.parse(document.querySelector('#flow-data').textContent);
 const tabs=[...flowRoot.querySelectorAll('[data-flow-tab]')];
 const panels=[...flowRoot.querySelectorAll('[data-flow-panel]')];
 const validHash=location.hash.replace('#flow-','');
 let current=flowData.some(f=>f.id===validHash)?validHash:flowData[0].id;
 const selectedSteps=new Map();
 flowRoot.classList.add('flow-enhanced');
 flowRoot.querySelector('.flow-tabs').setAttribute('role','tablist');
 function step(panel,index){
  const flow=flowData.find(f=>f.id===panel.dataset.flowPanel);
  const [title,status,event,owner,action]=flow.steps[index];
  selectedSteps.set(flow.id,index);
  const preview=panel.querySelector('[data-preview-stage]');
  if(preview){preview.textContent=status;panel.querySelector('[data-preview-owner]').textContent=owner;panel.querySelector('[data-preview-next]').textContent=index<flow.steps.length-1?flow.steps[index+1][0]:'Процесс завершён';}

  panel.querySelector('[data-event-title]').textContent=preview?title:title+' · '+status;
  panel.querySelector('[data-event-text]').textContent=event;
  panel.querySelector('[data-event-owner]').textContent=owner;
  panel.querySelector('[data-event-action]').textContent=action;
  panel.querySelector('[data-flow-index]').textContent='Шаг '+(index+1)+' из 5';
  panel.querySelector('[data-flow-back]').disabled=index===0;
  panel.querySelector('[data-flow-next]').disabled=index===4;
  panel.querySelector('.flow-event').hidden=false;
  panel.querySelectorAll('[data-flow-step]').forEach((button,i)=>{button.setAttribute('aria-pressed',String(i===index));if(i===index)button.setAttribute('aria-current','step');else button.removeAttribute('aria-current');});
 }
 function select(id,focus=false){
  current=id;selectedSteps.set(id,0);
  tabs.forEach(tab=>{const active=tab.dataset.flowTab===id;tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;if(active&&focus)tab.focus();});
  panels.forEach(panel=>{panel.hidden=panel.dataset.flowPanel!==id;if(!panel.hidden)step(panel,selectedSteps.get(id)||0);});
 }
 tabs.forEach((tab,index)=>{
  tab.id='tab-'+tab.dataset.flowTab;tab.setAttribute('role','tab');tab.setAttribute('aria-controls','flow-'+tab.dataset.flowTab);
  tab.addEventListener('click',event=>{event.preventDefault();select(tab.dataset.flowTab);});
  tab.addEventListener('keydown',event=>{let next;if(event.key==='ArrowRight')next=(index+1)%tabs.length;else if(event.key==='ArrowLeft')next=(index+tabs.length-1)%tabs.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=tabs.length-1;else if(event.key===' '||event.key==='Enter'){event.preventDefault();select(tab.dataset.flowTab);return;}else return;event.preventDefault();select(tabs[next].dataset.flowTab,true);});
 });
 panels.forEach(panel=>{
  panel.setAttribute('role','tabpanel');panel.setAttribute('aria-labelledby','tab-'+panel.dataset.flowPanel);
  panel.querySelectorAll('[data-flow-step]').forEach(button=>{button.disabled=false;button.addEventListener('click',()=>step(panel,Number(button.dataset.flowStep)));});
  panel.querySelector('[data-flow-back]').addEventListener('click',()=>step(panel,Math.max(0,(selectedSteps.get(panel.dataset.flowPanel)||0)-1)));
  panel.querySelector('[data-flow-next]').addEventListener('click',()=>step(panel,Math.min(4,(selectedSteps.get(panel.dataset.flowPanel)||0)+1)));
  panel.querySelector('[data-flow-start]').addEventListener('click',()=>step(panel,0));
 });
 select(current);
}
