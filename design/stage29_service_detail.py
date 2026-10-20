"""Scoped service pages: existing commercial scope, visual explanation, shared enquiry."""
from html import escape as e
import stage25_enquiry

CONFIG = {
    'seo': ('Чтобы вас находили по делу', 'От запроса клиента — к подходящей странице', 'Разбираем спрос, выбираем приоритетные страницы и последовательно улучшаем их. Результат работы показываем в отчёте.', 'stage28-websites-v1.png', ['Запрос клиента', 'Страница услуги', 'Обращение'], 'Сайт отвечает на вопрос клиента', [('Спрос', 'Что ищут перед обращением'), ('Структура', 'Где найти нужную услугу'), ('Содержание', 'Что поможет принять решение')]),
    'audit': ('Сначала понять. Затем улучшать.', 'План исправлений с понятным приоритетом', 'Проверка помогает выбрать, чем заняться сначала. Отделяем проблемы, мешающие обращению, от улучшений, которые могут подождать.', 'stage26-enquiry-cutout-v1.png', ['Проверка', 'Приоритеты', 'План исправлений'], 'Каждая находка — с объяснением', [('Наблюдение', 'Где возникает затруднение'), ('Влияние', 'Какой сценарий затронут'), ('Действие', 'Что и в каком порядке исправить')]),
    'support': ('Сайт развивается вместе с вами', 'Изменения, за которыми легко следить', 'Собираем задачи, согласуем объём, показываем сделанное. Перед существенными изменениями готовим резервную копию и проверяем затронутые сценарии.', 'stage27-process-cutout.png', ['Задача', 'Проверка', 'Готовое изменение'], 'Понятно, что происходит с задачей', [('Согласовано', 'Объём и условия работы'), ('В работе', 'Изменения и проверка'), ('Передано', 'Результат и пояснения')]),
    'redesign': ('Новый вид. Продуманный переход.', 'Обновляем опыт, сохраняем важные сценарии', 'Сначала фиксируем функции и материалы, которые нужны бизнесу. Затем проектируем новую версию и проверяем её отдельно от действующего сайта.', 'stage28-websites-v1.png', ['Текущий сайт', 'Новая версия', 'Проверенный запуск'], 'Перед переходом сверяем главное', [('Функции', 'Формы, каталог, кабинеты'), ('Контент', 'Материалы и адреса страниц'), ('Подключения', 'Обмен данными и оплата')]),
    'integrations': ('Сервисы работают вместе', 'Одно действие запускает следующий шаг', 'Согласуем, какие данные и куда передавать. Учитываем статусы, ошибки и повторные запросы, чтобы обмен можно было контролировать.', 'stage27-process-cutout.png', ['Сайт', 'CRM / учёт', 'Уведомление'], 'Обмен по понятным правилам', [('Данные', 'Какие поля передаём'), ('Статус', 'Как подтверждаем обработку'), ('Ошибка', 'Что делаем при сбое')]),
}


def visual(slug, config):
    _, _, _, image, steps, title, rows = config
    # A labelled schematic, never presented as client data or a measured result.
    body = f'<div class="detail29-visual detail29-visual--{slug}"><img src="assets/{image}" width="960" height="640" alt="" decoding="async"><div class="detail29-board"><span class="detail29-demo">Пример подхода</span><h2>{e(title)}</h2><ol class="detail29-route">'
    for label in steps:
        body += f'<li>{e(label)}</li>'
    body += '</ol><div class="detail29-signals">'
    for label, text in rows:
        body += f'<div><b>{e(label)}</b><span>{e(text)}</span></div>'
    return body + '</div></div></div>'


def service(s, faq):
    slug, name, heading, desc, price, formats, deliver, scope, _ = s
    config = CONFIG[slug]
    eyebrow, section_title, section_desc, *_ = config
    body = f'''<div class="detail29 detail29--{slug}">
<section class="detail29-intro"><div class="wrap">
<nav class="breadcrumb" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span aria-hidden="true">/</span><a href="services.html">Услуги</a><span aria-hidden="true">/</span><span aria-current="page">{e(name)}</span></nav>
<div class="detail29-hero"><div class="detail29-copy"><span class="eyebrow">{e(name)}</span><h1>{e(heading)}</h1><p>{e(desc)}</p><div class="detail29-actions"><a class="btn primary" href="contacts.html?service={slug}">Обсудить задачу</a><a href="#service-scope">Состав и стоимость</a></div><div class="detail29-start"><span>С чего можно начать</span><strong>{e(price)}</strong><a href="#service-scope">Посмотреть условия</a></div></div>{visual(slug, config)}</div>
</div></section>
<section class="wrap detail29-formats"><div class="detail29-heading"><div><span class="eyebrow">{e(eyebrow)}</span><h2>{e(section_title)}</h2></div><p>{e(section_desc)}</p></div><div class="detail29-options">'''
    for i, (title, text) in enumerate(formats):
        body += f'<article><span class="detail29-number" aria-hidden="true">0{i+1}</span><div><h3>{e(title)}</h3><p>{e(text)}</p></div></article>'
    body += '</div></section>'
    if slug == 'integrations':
        body += '''<section class="wrap service31-proof" aria-labelledby="service31-proof-title"><a class="service31-proof-image" href="case-mu56.html" aria-label="Посмотреть кейс Мир Улыбок"><img src="assets/mu56-home-desktop.jpg" width="1265" height="712" loading="lazy" decoding="async" alt="Реальная главная страница сайта детских праздников Мир Улыбок"></a><div><span class="eyebrow">ПРИМЕР ИЗ СОБСТВЕННОГО БИЗНЕСА</span><h2 id="service31-proof-title">Сайт и Telegram-бот<br>в одном проекте</h2><p>Для «Мира Улыбок» мы создали сайт с нуля и работающего Telegram-бота. Это собственный бизнес: интерфейс и инструменты развиваем вместе с его задачами.</p><a class="service31-proof-link" href="case-mu56.html">Посмотреть проект «Мир Улыбок»</a><small>На изображении — сайт проекта. Подключения для вашего бизнеса согласуем отдельно.</small></div></section>'''
    body += '''<section class="detail29-scope" id="service-scope"><div class="wrap detail29-scope-grid"><div><span class="eyebrow">СОСТАВ РАБОТ</span><h2>Что можем включить<br>в ваш проект</h2><p>Выберем нужные работы из списка и согласуем смету. Состав стартового пакета указан в блоке «Бюджет и границы».</p><ol class="detail29-deliver">'''
    for item in deliver:
        body += f'<li>{e(item)}</li>'
    body += f'''</ol></div><aside class="detail29-budget"><span class="eyebrow">БЮДЖЕТ И ГРАНИЦЫ</span><h3>{e(price)}</h3><p>{e(scope)}</p><a class="btn primary" href="contacts.html?service={slug}">Оценить мою задачу</a><span class="detail29-budget-note">Стоимость дополнительных работ согласуем отдельно.</span></aside></div></section>
<section class="wrap detail29-faq"><div><span class="eyebrow">ПЕРЕД НАЧАЛОМ</span><h2>Важные детали</h2></div><div>'''
    for question, answer in faq:
        body += f'<details><summary>{e(question)}<span aria-hidden="true">+</span></summary><p>{e(answer)}</p></details>'
    return body + '</div></section>' + stage25_enquiry.enquiry() + '</div>'
