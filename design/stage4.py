import stage21
"""Business flows: static content remains useful without JavaScript."""
from html import escape
import json
from pathlib import Path
import stage5

FLOWS = [
 {'id':'auto','label':'Автосервис','title':'От записи до выдачи автомобиля','intro':'Связать клиента, загрузку мастерской и выполнение работ.','service':'automation','visibility':['Записи и загрузка постов','Статус каждого заказ-наряда','Ответственный и следующий шаг','История работ по автомобилю'],'steps':[
  ['Запись','Новая','Клиент выбирает время или оставляет обращение.','Администратор','Согласовать время и описание задачи.','calendar'],
  ['Приёмка','Согласование','Фиксируются автомобиль, задача и согласованные работы.','Мастер-приёмщик','Согласовать состав работ с клиентом.','clipboard'],
  ['Работы','В работе','Заказ-наряд передан исполнителю, отмечается ход работ.','Механик','Выполнить работы и отметить результат.','wrench'],
  ['Проверка','Готов к проверке','Результат проверяется по согласованному перечню.','Мастер-приёмщик','Проверить выполнение и подготовить выдачу.','check'],
  ['Выдача','Завершён','Автомобиль передан клиенту, история заказа сохранена.','Администратор','Закрыть заказ и сохранить историю.','car']]},
 {'id':'property','label':'Управляющая компания','title':'От обращения жителя до результата','intro':'Понятный маршрут заявки и ответственность на каждом этапе.','service':'automation','visibility':['Обращения по адресам и темам','Назначенные исполнители','Открытые и завершённые задачи','История решений по заявке'],'steps':[
  ['Обращение','Новая','Житель сообщает о проблеме и указывает адрес.','Диспетчер','Уточнить адрес и содержание обращения.','message'],
  ['Разбор','На рассмотрении','Определяются вид работ и приоритет по правилам компании.','Диспетчер','Проверить заявку и назначить исполнителя.','clipboard'],
  ['Назначение','Назначена','Исполнитель получает задачу и согласованный срок.','Ответственный сотрудник','Принять задачу в работу.','person'],
  ['Выполнение','В работе','Исполнитель фиксирует выполненные действия и результат.','Исполнитель','Отметить выполнение и передать на проверку.','wrench'],
  ['Закрытие','Завершена','Результат проверен и отражён в истории обращения.','Диспетчер','Закрыть заявку по принятому порядку.','check']]},
 {'id':'commerce','label':'Торговля','title':'От выбора товара до обработки заказа','intro':'Заказ, наличие и исполнение связаны согласованными правилами.','service':'integrations','visibility':['Заказы и текущие статусы','Согласование наличия','Этап комплектации и передачи','Исключения, требующие решения'],'steps':[
  ['Заказ','Новый','Покупатель выбирает товары и оформляет заказ.','Менеджер','Проверить состав и контакт для согласования.','cart'],
  ['Подтверждение','Согласование','Проверяются наличие и условия получения.','Менеджер','Подтвердить согласованный заказ.','clipboard'],
  ['Комплектация','Собирается','Товары подготавливаются по составу заказа.','Склад','Собрать и проверить комплект.','box'],
  ['Передача','Передан','Заказ передан для получения или доставки.','Менеджер / доставка','Зафиксировать передачу заказа.','truck'],
  ['Завершение','Завершён','Результат отражён в истории заказа.','Менеджер','Закрыть заказ по согласованным правилам.','check']]},
]
PATHS={
 'calendar':'M7 4v5m10-5v5M4 9h16M5 6h14a1 1 0 0 1 1 1v13H4V7a1 1 0 0 1 1-1Zm3 7h3m3 0h3m-9 4h3',
 'clipboard':'M8 5H5v16h14V5h-3M8 3h8v5H8V3Zm0 10h8m-8 4h5',
 'wrench':'m14 5 3 3 3-3a6 6 0 0 1-7 8l-6 7-3-3 7-6a6 6 0 0 1 3-6Z',
 'check':'M20 12a8 8 0 1 1-5-7M8 11l4 4 8-9',
 'car':'m5 9 2-5h10l2 5M3 10h18v8H3v-8Zm2 8v3m14-3v3M6 13h2m8 0h2',
 'message':'M3 4h18v13H9l-6 4V4Zm4 5h10M7 13h6',
 'person':'M16 7a4 4 0 1 1-8 0 4 4 0 0 1 8 0Zm-12 14v-3a8 8 0 0 1 16 0v3',
 'cart':'M2 4h3l3 12h11l3-9H6m4 14h.1m8-.1h.1',
 'box':'m12 3 9 5v9l-9 5-9-5V8l9-5Zm0 9v10M3 8l9 4 9-4M7 5l10 5',
 'truck':'M3 5h11v12H3V5Zm11 5h4l3 4v3h-7M8 18a2 2 0 1 1-4 0 2 2 0 0 1 4 0Zm12 0a2 2 0 1 1-4 0 2 2 0 0 1 4 0Z',
}
content=json.loads((Path(__file__).parent/'flow-content.json').read_text(encoding='utf-8'))
for flow in FLOWS:
    for i,row in enumerate(content[flow['id']]):
        role={'auto':['calendar','car','wrench','message','check'],'property':['message','person','wrench','check','clipboard'],'commerce':['cart','clipboard','box','truck','check']}[flow['id']][i]
        flow['steps'][i]=[row['title'],row['status'],row['event'],row['owner'],row['benefit'],role]
FLOWS[0]['visibility']=['Загрузка мастеров','Статусы заказов','Просроченные задачи','Заказы, ожидающие согласования']
FLOWS[0]['intro']='Администратор ведёт заказ, мастер выполняет работы, руководитель видит загрузку и задержки.'
FLOWS[1]['title']='От обращения жителя до подтверждения выполнения'
FLOWS[1]['visibility']=['Открытые обращения','Назначенные ответственные','Просроченные задачи','Повторные проверки и возвраты']
FLOWS[2]['title']='От заказа до статуса доставки'
FLOWS[2]['visibility']=['Заказы по этапам','Неподтверждённое наличие','Задержки сборки','Состояние доставки']
FLOWS=stage5.add_flows(FLOWS)
def icon(role):
 return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{PATHS[role]}"/></svg>'

def flow_section(compact=False):
 body='<section class="business-flows" id="business-processes"><div class="wrap section"><div class="section-heading"><div><span class="eyebrow">ОТ ЗАДАЧИ — К ПРОЦЕССУ</span><h2>Каждый знает следующий шаг.<br>Руководитель видит весь процесс.</h2></div><p>Связываем роли, задачи и статусы в понятный маршрут. Пример решения · Не готовый продукт.</p></div><div class="flow-tabs" aria-label="Выбрать бизнес-процесс">'+''.join(f'<a href="#flow-{f["id"]}" data-flow-tab="{f["id"]}">{f["label"]}</a>' for f in FLOWS)+'</div><div data-flows>'
 for f in FLOWS:
  body+=f'<section class="flow-panel" id="flow-{f["id"]}" data-flow-panel="{f["id"]}" aria-labelledby="flow-title-{f["id"]}"><div class="flow-title"><h3 id="flow-title-{f["id"]}">{f["title"]}</h3><p>{f["intro"]}</p></div><div class="flow-layout"><div class="flow-main"><ol class="flow-path">'
  for i,(title,status,event,owner,action,role) in enumerate(f['steps']):
   body+=f'<li><span class="flow-connector" aria-hidden="true"><svg viewBox="0 0 100 16" preserveAspectRatio="none"><path d="M0 8H96m-7-5 7 5-7 5" fill="none" stroke="currentColor" stroke-width="1.5" vector-effect="non-scaling-stroke"/></svg></span><button class="flow-step" data-flow-step="{i}" type="button" disabled><span class="flow-node">{icon(role)}</span><span class="flow-number">0{i+1}</span><strong>{title}</strong><span class="flow-state">{status}</span></button><div class="flow-static"><p>{event}</p><small>Ответственный: {owner}</small></div></li>'
  body+='</ol><div class="flow-event" hidden aria-live="polite"><span class="eyebrow">ДЕЙСТВИЕ И ОТВЕТСТВЕННОСТЬ</span><h4 data-event-title></h4><p data-event-text></p><dl><div><dt>Роль</dt><dd data-event-owner></dd></div><div><dt>Результат шага</dt><dd data-event-action></dd></div></dl><div class="flow-browse"><span data-flow-index>Шаг 1 из 5</span><button type="button" data-flow-back>Назад</button><button type="button" data-flow-next>Следующий шаг</button><button type="button" data-flow-start>К началу</button></div></div></div><aside class="flow-control"><span class="control-symbol" aria-hidden="true">◉</span><span class="eyebrow">ПАНЕЛЬ КОНТРОЛЯ</span><h4>Руководителю<br>видно</h4><ul>'+''.join('<li>'+escape(v)+'</li>' for v in f['visibility'])+'</ul><p>Команда видит статус и ответственного. Исключения можно разбирать по истории процесса.</p></aside></div>'+f'<div class="flow-bottom"><p>Можно начать с одного участка работы и проверить его на согласованных сценариях.</p><a class="btn primary" href="contacts.html?service={f["service"]}">Обсудить этот процесс <span aria-hidden="true">↗</span></a></div></section>'
 body+='</div><noscript><p class="fineprint">Показаны пять статических примеров. Ссылки выше ведут к каждому сценарию; интерактивный выбор шагов доступен при включённом JavaScript.</p></noscript></div><script type="application/json" id="flow-data">'+json.dumps(FLOWS,ensure_ascii=False).replace('<','\\u003c')+'</script></section>'
 if compact:
  body=body.replace('class="business-flows"','class="business-flows flow-showcase"',1)
  start=body.index('<div class="section-heading">')
  end=body.index('<div class="flow-tabs"',start)
  body=body[:start]+'''<div class="showcase-heading"><span class="eyebrow">АВТОМАТИЗАЦИЯ В ДЕЙСТВИИ</span><h2>От заявки до результата.<br>Без потерянных задач.</h2><p>Выберите ваш бизнес и пройдите путь заказа: кто отвечает, что происходит и что видит руководитель.</p><span class="showcase-disclaimer">Примеры сценариев для индивидуальной разработки</span></div>'''+body[end:]
  for f in FLOWS:
   start=body.index('<aside class="flow-control">')
   end=body.index('</aside>',start)+len('</aside>')
   preview=stage21.dashboard(f)
   # Replace each original aside; previews have a distinct class so the next lookup skips them.
   body=body[:start]+preview+body[end:]
  body=body.replace('ДЕЙСТВИЕ И ОТВЕТСТВЕННОСТЬ','ЧТО ПРОИСХОДИТ НА ЭТОМ ШАГЕ')
  body=body.replace('Можно начать с одного участка работы и проверить его на согласованных сценариях.','Начнём с вашего процесса. Подберём роли, этапы и интеграции под работу команды.')
  body=body.replace('Обсудить этот процесс <span aria-hidden="true">↗</span>','Обсудить автоматизацию')
 return body
