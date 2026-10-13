"""Homepage delivery milestones and a concrete starting point for enquiries."""
import stage9

def delivery():
    items=[('План и смета','Согласованный состав работ, этапы и стоимость.'),('Прототип','Структура и ключевые экраны до начала разработки.'),('Рабочая версия','Результат, который можно проверить на ваших сценариях.'),('Запуск и доступы','Готовый проект, доступы и объяснение, как с ним работать.')]
    body='<section class="wrap delivery-section"><div class="delivery-heading"><h2>Вы принимаете результат<br>на каждом этапе</h2><p>От первого обсуждения до передачи проекта. Состав работ и условия фиксируем в договоре.</p></div><ol class="delivery-milestones">'
    for i,(title,desc) in enumerate(items):
        body+=f'<li><span class="milestone-number" aria-hidden="true">0{i+1}</span><h3>{title}</h3><p>{desc}</p></li>'
    return body+'</ol><div class="delivery-foot"><p>После запуска помогаем поддерживать и развивать проект.</p><a href="approach.html">Подробнее о работе над проектом</a></div></section>'

def enquiry():
    messengers=stage9.messengers().replace('class="header-messengers"','class="inquiry-messengers"').replace('</svg></a>','</svg><span>Telegram</span></a>',1).replace('</svg></a>','</svg><span>MAX</span></a>',1)
    return '''<section class="wrap enquiry-section"><div class="enquiry-surface"><div class="enquiry-copy"><h2>Начнём с задачи.<br>Определим решение.</h2><p>Расскажите, что хотите сделать, или пришлите ссылку на действующий сайт. Обсудим подходящий вариант, этапы и стоимость.</p><div class="enquiry-outcome"><span>Состав работ</span><span>Этапы проекта</span><span>Оценка бюджета</span></div></div><div class="enquiry-actions"><a class="btn" href="contacts.html">Обсудить проект</a><span class="enquiry-channel-label">Или напишите напрямую</span>'''+messengers+'</div></div></section>'
