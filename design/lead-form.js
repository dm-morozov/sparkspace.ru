/* No storage/analytics: payload and idempotency key live only in this form's memory. */
const leadForm = document.querySelector('#lead-form');
if (leadForm) {
  const statusBox = leadForm.querySelector('.lead-status');
  const submitButton = leadForm.querySelector('[type=submit]');
  submitButton.disabled=false;
  const conflictButton = leadForm.querySelector('.conflict-retry');
  const fields = ['name','contact','service','message','project_url','consent'];
  let pending = null;
  let sending = false;
  let conflict = false;
  const serviceField = leadForm.elements.service;
  const wanted = new URLSearchParams(location.search).get('service');
  if ([...serviceField.options].some(o=>o.value===wanted)) serviceField.value=wanted;
  const localFile = location.protocol==='file:';
  if (localFile) document.querySelector('#form-mode').textContent='Файл открыт без сервера. Отправка недоступна; введённый текст останется в форме. Для проверки нужен локальный HTTP-сервер с API.';

  function clearErrors() {
    leadForm.querySelectorAll('.field-error').forEach(e=>e.textContent='');
    leadForm.querySelectorAll('[aria-invalid]').forEach(e=>e.removeAttribute('aria-invalid'));
  }
  function showErrors(errors) {
    let first;
    for (const e of errors) {
      if (!fields.includes(e.field)) continue;
      const input = leadForm.elements[e.field];
      const label = document.querySelector('#error-'+e.field);
      if (input && label) {input.setAttribute('aria-invalid','true'); label.textContent=e.message; first ||= input;}
    }
    if (first) first.focus(); else statusBox.focus();
  }
  function readPayload() {
    const data = new FormData(leadForm);
    return {name:String(data.get('name')||'').trim(),contact:String(data.get('contact')||'').trim(),service:String(data.get('service')||'unsure'),message:String(data.get('message')||'').trim(),budget:String(data.get('budget')||'estimate'),project_url:String(data.get('project_url')||'').trim()||null,source_path:'/contacts.html',website:String(data.get('website')||'').trim(),consent:data.get('consent')==='on'};
  }
  function validate(p) {
    const errors=[];
    const length = s=>Array.from(s).length;
    const add=(field,message)=>errors.push({field,message});
    if (length(p.name)<2||length(p.name)>100) add('name','Укажите имя: от 2 до 100 символов.');
    const email=/^[^\s@]+@[^\s@.]+(?:\.[^\s@.]+)+$/;
    const telegram=/^(?:@|https:\/\/t\.me\/)[a-zA-Z][a-zA-Z0-9_]{4,31}$/;
    const phone=/^\+?[0-9 ()-]+$/;
    if (length(p.contact)<5||length(p.contact)>200||!(email.test(p.contact)||telegram.test(p.contact)||(phone.test(p.contact)&&p.contact.replace(/\D/g,'').length>=10&&p.contact.replace(/\D/g,'').length<=15))) add('contact','Укажите телефон, email или Telegram (@username).');
    if (length(p.message)<10||length(p.message)>3000) add('message','Опишите задачу: от 10 до 3000 символов.');
    if (p.project_url) {
      try {const url=new URL(p.project_url);if(!['http:','https:'].includes(url.protocol)||!url.hostname||url.username||url.password||length(p.project_url)>2048) throw new Error();}
      catch {add('project_url','Укажите публичный адрес http:// или https:// без пароля.');}
    }
    for (const field of ['name','contact','project_url']) if (p[field]&&/[\x00-\x1f\x7f]/.test(p[field])) add(field,'Удалите управляющие символы.');
    if (/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(p.message)) add('message','Удалите управляющие символы из описания.');
    if (!p.consent) add('consent','Подтвердите согласие на обработку заявки.');
    return errors;
  }
  leadForm.addEventListener('input',()=>{
    if(sending) return;
    pending=null;conflict=false;conflictButton.hidden=true;statusBox.textContent='';statusBox.className='lead-status';clearErrors();
  });
  conflictButton.addEventListener('click',()=>{pending=null;conflict=false;conflictButton.hidden=true;leadForm.requestSubmit();});
  leadForm.addEventListener('submit',async event=>{
    event.preventDefault();if(sending) return;
    clearErrors();statusBox.className='lead-status';
    if(localFile){statusBox.textContent='Отправка недоступна в режиме файла. Откройте локальную HTTP-версию с API. Ввод сохранён в форме.';return;}
    if(conflict){statusBox.textContent='Ключ занят другой заявкой. Выберите «Отправить как новую заявку» или измените данные.';return;}
    const payload=readPayload();
    const errors=validate(payload);
    if(errors.length){statusBox.textContent='Проверьте отмеченные поля.';statusBox.classList.add('error');showErrors(errors);return;}
    const body=JSON.stringify(payload);
    if(new TextEncoder().encode(body).length>16384){statusBox.textContent='Заявка слишком большая. Сократите описание.';statusBox.classList.add('error');return;}
    if(!pending||pending.body!==body) pending={body,key:crypto.randomUUID()};
    const request=pending;
    sending=true;submitButton.disabled=true;submitButton.textContent='Сохраняем…';statusBox.textContent='';
    const controls=[...leadForm.querySelectorAll('input,select,textarea')];controls.forEach(e=>e.disabled=true);
    const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),15000);
    let responseErrors=[];
    try {
      const response=await fetch('/api/v1/leads',{method:'POST',signal:controller.signal,headers:{'Content-Type':'application/json','Idempotency-Key':request.key},body:request.body});
      const data=await response.json().catch(()=>null);
      if((response.status===200||response.status===201)&&data?.ok===true&&typeof data.id==='string'&&/^[0-9a-f]{8}-[0-9a-f-]{27}$/i.test(data.id)) {
        statusBox.textContent='Заявка сохранена. Внешняя доставка отключена.';statusBox.classList.add('success');leadForm.reset();pending=null;
      } else {
        statusBox.classList.add('error');
        if(response.status===422){statusBox.textContent=typeof data?.detail==='string'?data.detail:'Проверьте поля заявки.';responseErrors=Array.isArray(data?.errors)?data.errors.filter(e=>typeof e.field==='string'&&typeof e.message==='string'):[];}
        else if(response.status===409){conflict=true;conflictButton.hidden=false;statusBox.textContent='Эта попытка связана с другим содержимым. Данные сохранены в форме. Можно осознанно отправить новую заявку.';}
        else if(response.status===429){const retry=Number(response.headers.get('Retry-After'));statusBox.textContent='Слишком много попыток. '+(Number.isInteger(retry)&&retry>0?`Попробуйте через ${retry} с.`:'Попробуйте позже.')+' Данные сохранены в форме.';}
        else if(response.status===503){statusBox.textContent='Не удалось сохранить заявку. Попробуйте позже. Ввод и ключ повтора сохранены в этой форме.';}
        else statusBox.textContent='Сервер не подтвердил сохранение заявки. Попробуйте позже. Ввод сохранён в форме.';
      }
    } catch(e) {
      statusBox.classList.add('error');statusBox.textContent=(e.name==='AbortError'?'Сервер не ответил вовремя.':'Не удалось связаться с сервером.')+' Результат неизвестен. Повторите отправку: в этой форме сохранён тот же ключ попытки.';
    } finally {
      clearTimeout(timer);sending=false;submitButton.disabled=false;submitButton.innerHTML='Сохранить заявку <span aria-hidden="true">↗</span>';controls.forEach(e=>e.disabled=false);
      if(responseErrors.length)showErrors(responseErrors);
    }
  });
}

const processDemo=document.querySelector('[data-demo]');
if(processDemo){
  const states=[['','Не назначен','Заявка ещё не создана. Начните демонстрацию.','Создать демо-заявку'],['Новая','Не назначен','Заявка поступила. Нужен ответственный.','Назначить исполнителя'],['В работе','Специалист А','Ответственный видит задачу и может отметить результат.','Отметить выполнение'],['Выполнена','Специалист А','Расчёт подготовлен — демонстрационный результат. Осталось показать уведомление.','Показать демо-уведомление'],['Выполнена','Специалист А','Все шаги пройдены. В реальном процессе правила, роли и каналы согласуются под вашу работу.','']];
  let index=0;
  const next=processDemo.querySelector('[data-demo-next]');
  const reset=processDemo.querySelector('[data-demo-reset]');reset.hidden=false;
  function render(){const [status,person,explanation,label]=states[index];processDemo.querySelector('.demo-ticket').hidden=index===0;processDemo.querySelector('[data-demo-status]').textContent=status;processDemo.querySelector('[data-demo-person]').textContent=person;processDemo.querySelector('[data-demo-explanation]').textContent=explanation;next.textContent=label;next.hidden=index===4;processDemo.querySelectorAll('[data-step]').forEach((e,i)=>{e.classList.toggle('active',i===index&&index<4);e.classList.toggle('done',i<index);if(i===index&&index<4)e.setAttribute('aria-current','step');else e.removeAttribute('aria-current');});const log=processDemo.querySelector('.demo-log');log.replaceChildren();['Демо-заявка создана','Исполнитель назначен','Выполнение отмечено','Показан пример уведомления'].slice(0,index).forEach(text=>{const item=document.createElement('li');item.textContent=text;log.append(item);});const notification=processDemo.querySelector('.demo-notification');notification.hidden=index!==4;notification.textContent=index===4?'Пример уведомления: заявка ДЕМО-104 выполнена. Ответственный — Специалист А. Это демо, сообщение не отправлено.':'';}
  next.addEventListener('click',()=>{if(index<4)index++;render();if(index===4)reset.focus();});reset.addEventListener('click',()=>{index=0;render();next.focus();});render();
}
