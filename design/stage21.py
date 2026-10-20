"""Illustrative, stateful manager workspace; all records are fictional examples."""
from html import escape
from stage30_flow_views import SUBJECTS, VIEWS, render_view


def dashboard(f):
 key=f['id']
 titles=[step[0] for step in f['steps']]
 if titles != list(VIEWS[key]):
  raise ValueError('Manager views must match the scenario steps: '+key)
 h='<aside class="flow-control process-preview manager-workspace"><div class="preview-heading"><span class="preview-indicator" aria-hidden="true"></span><span>Вид руководителя</span><span class="preview-demo">Демо</span></div><figure class="manager-art"><img src="assets/stage27-process-cutout.png" width="960" height="640" loading="lazy" decoding="async" alt="Фирменная иллюстрация: обращение, ответственный и выполненная задача"></figure><div class="manager-context"><span>Пример процесса</span><strong>'+escape(SUBJECTS[key])+'</strong></div>'
 for i,(title,status,event,owner,benefit,icon) in enumerate(f['steps']):
  h+=f'<section class="manager-screen manager-screen-{i}" data-manager-screen="{i}"'+(' hidden' if i else '')+'><span class="manager-kicker">'+escape(title)+'</span><h4>'+escape(status)+'</h4>'
  h+=render_view(key,title)
  if key=='sales' and title=='Итог':
   h+='<div class="manager-outcomes" role="group" aria-label="Пример результата обращения"><button type="button" data-outcome="Сделка согласована. Следующая задача — передать заказ в работу." aria-pressed="true">Сделка</button><button type="button" data-outcome="Клиент пока думает. Сохранены дата следующего контакта и ответственный." aria-pressed="false">Позже</button><button type="button" data-outcome="Причина отказа сохранена. Её можно учесть при разборе обращений." aria-pressed="false">Отказ</button></div><p data-outcome-text aria-live="polite" class="manager-insight">Сделка согласована. Следующая задача — передать заказ в работу.</p>'
  h+='</section>'
 h+='<div class="manager-progress" aria-label="Прогресс примера">'+''.join('<span data-manager-progress="'+str(i)+'"></span>' for i in range(len(f['steps'])))+'</div><p class="manager-footnote">Иллюстрация возможностей · Не данные клиентов</p></aside>'
 return h
