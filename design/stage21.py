"""Illustrative, stateful manager workspace; all records are fictional examples."""
from html import escape

EXAMPLES = {
 'sales': ('Запрос на обслуживание', 'Менеджер по продажам', ['Сайт', 'Телефон', 'Мессенджер'], ['Задача клиента', 'Сроки и ограничения', 'Бюджет и условия']),
 'commerce': ('Заказ из интернет-магазина', 'Менеджер магазина', ['Каталог', 'Корзина', 'Заказ'], ['Состав заказа', 'Наличие на складе', 'Адрес и способ доставки']),
 'auto': ('Техническое обслуживание', 'Мастер сервиса', ['Запись', 'Приёмка', 'Заказ-наряд'], ['Перечень работ', 'Запчасти', 'Согласование с клиентом']),
 'property': ('Обращение жителя', 'Диспетчер', ['Обращение', 'Адрес', 'Исполнитель'], ['Описание неисправности', 'Время визита', 'Результат работ']),
 'content': ('Материал для публикации', 'Редактор', ['Идея', 'План', 'Автор'], ['Тема и формат', 'Материалы', 'Согласование выпуска']),
}

def dashboard(f):
 key=f['id']; subject, role, sources, checks=EXAMPLES[key]
 h='<aside class="flow-control process-preview manager-workspace"><div class="preview-heading"><span class="preview-indicator" aria-hidden="true"></span><span>Вид руководителя</span><span class="preview-demo">Демо</span></div><figure class="manager-art"><img src="assets/process-route-v1.jpg" width="960" height="640" loading="lazy" decoding="async" alt="Фирменная иллюстрация: обращение, ответственный и выполненная задача"></figure><div class="manager-context"><span>Пример процесса</span><strong>'+escape(subject)+'</strong></div>'
 for i,(title,status,event,owner,benefit,icon) in enumerate(f['steps']):
  h+=f'<section class="manager-screen manager-screen-{i}" data-manager-screen="{i}"'+(' hidden' if i else '')+'><span class="manager-kicker">'+escape(title)+'</span><h4>'+escape(status)+'</h4>'
  if i==0:
   h+='<div class="manager-sources">'+''.join('<span>'+escape(s)+'</span>' for s in sources)+'</div><div class="manager-record"><span class="record-mark">01</span><div><strong>'+escape(subject)+'</strong><small>Обращение сохранено в системе</small></div><span class="record-dot" aria-hidden="true"></span></div><p class="manager-insight">Все каналы сходятся в одной карточке. Можно увидеть обращения, которые ещё ждут ответа.</p>'
  elif i==1:
   h+='<div class="manager-assignment"><span class="manager-avatar" aria-hidden="true">'+escape(role[:1])+'</span><div><strong>'+escape(owner)+'</strong><small>Ответственный за этот этап</small></div></div><div class="manager-notification"><span aria-hidden="true">✓</span><p>Задача назначена. Сотрудник видит, что нужно сделать дальше.</p></div><p class="manager-insight">Руководитель проверяет назначение и загрузку команды, вместо того чтобы искать исполнителя в чатах.</p>'
  elif i==2:
   h+='<ul class="manager-checklist">'+''.join('<li><span aria-hidden="true">✓</span>'+escape(s)+'</li>' for s in checks)+'</ul><p class="manager-insight">Условия и детали остаются рядом с задачей. При передаче между сотрудниками контекст сохраняется.</p>'
  elif i==3:
   h+='<div class="manager-document"><span class="document-fold" aria-hidden="true"></span><strong>'+escape(title)+'</strong><small>'+escape(event)+'</small><div class="document-lines" aria-hidden="true"><i></i><i></i><i></i></div></div><p class="manager-insight">Договорённости и действия записаны в истории. Видно, на чьей стороне следующий шаг.</p>'
  else:
   h+='<div class="manager-finish"><span aria-hidden="true">✓</span><strong>Есть зафиксированный итог</strong><small>'+escape(benefit)+'</small></div>'
   if key=='sales':
    h+='<div class="manager-outcomes" role="group" aria-label="Пример результата обращения"><button type="button" data-outcome="Сделка согласована. Следующая задача — передать заказ в работу." aria-pressed="true">Сделка</button><button type="button" data-outcome="Клиент пока думает. Сохранены дата следующего контакта и ответственный." aria-pressed="false">Позже</button><button type="button" data-outcome="Причина отказа сохранена. Её можно учесть при разборе обращений." aria-pressed="false">Отказ</button></div><p data-outcome-text aria-live="polite" class="manager-insight">Сделка согласована. Следующая задача — передать заказ в работу.</p>'
   else: h+='<p class="manager-insight">Можно проверить историю действий и понять, где нужна помощь, а не собирать отчёты вручную.</p>'
  h+='</section>'
 h+='<div class="manager-progress" aria-label="Прогресс примера">'+''.join('<span data-manager-progress="'+str(i)+'"></span>' for i in range(5))+'</div><p class="manager-footnote">Иллюстрация возможностей · Не данные клиентов</p></aside>'
 return h
