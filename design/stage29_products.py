"""Scoped product-service pages; prices come exclusively from the shared service record."""
from html import escape

import stage4
import stage25_delivery
import stage25_enquiry


def _hero(s, title, intro, image, alt, anchor, secondary):
    slug = escape(s[0], quote=True)
    return f'''<section class="product29-intro"><div class="wrap">
<nav class="breadcrumb" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span aria-hidden="true">/</span><a href="services.html">Услуги</a><span aria-hidden="true">/</span><span aria-current="page">{escape(s[1])}</span></nav>
<div class="product29-hero"><div class="product29-copy"><h1>{title}</h1><p>{intro}</p>
<div class="product29-actions"><a class="btn primary" href="contacts.html?service={slug}">Обсудить задачу</a><a class="product29-link" href="#{anchor}">{secondary}</a></div>
<p class="product29-start">{escape(s[4])}<span>Состав и этапы согласуем до начала работы</span></p></div>
<figure class="product29-art"><img src="assets/{image}" width="960" height="640" fetchpriority="high" decoding="async" alt="{alt}"></figure></div></div></section>'''


def _finish(s, faq):
    body = f'''<section class="wrap product29-budget" id="product29-budget"><div><span class="eyebrow">ПОНЯТНЫЙ ПЕРВЫЙ ШАГ</span><h2>Начнём с нужного объёма</h2><p>Обсудим задачу, выберем первый этап и определим результат, который вы сможете принять.</p></div><div class="product29-budget-detail"><strong>{escape(s[4])}</strong><p>{escape(s[7])}</p><a class="product29-link" href="contacts.html?service={escape(s[0], quote=True)}">Получить оценку своей задачи</a><small>Хостинг, лицензии и платные сервисы оплачиваются отдельно.</small></div></section>'''
    body += stage25_delivery.delivery()
    body += '<section class="wrap website-faq product29-faq"><h2>Перед началом работы</h2><div>'
    for q, a in faq:
        body += f'<details><summary>{escape(q)}<span aria-hidden="true">+</span></summary><p>{escape(a)}</p></details>'
    body += '</div></section>'
    body += stage25_enquiry.enquiry()
    return body


def applications(s, faq):
    body = '<div class="product29 product29-applications">'
    body += _hero(
        s, 'Приложения<br>для клиентов и команды',
        'Записаться на услугу, пройти обучение, проверить заказ. Превращаем ваш сценарий в понятный продукт для клиентов или команды.',
        'stage27-hero-v1.png',
        'Приложение на компьютере и телефоне в единой композиции с элементами рабочего процесса',
        'product29-scenarios', 'Выбрать сценарий',
    )
    body += '''<section class="wrap product29-scenarios" id="product29-scenarios"><div class="product29-section-title"><span class="eyebrow">СНАЧАЛА — ПОЛЕЗНОЕ ДЕЙСТВИЕ</span><h2>Что человек сможет<br>сделать в вашем приложении?</h2></div>
<div class="product29-scenario-layout"><article class="product29-scenario-feature">
<div class="product29-appointment" aria-hidden="true"><span class="product29-demo-label">Пример интерфейса записи</span><div class="product29-appointment-card"><span>Запись на услугу</span><strong>Удобное время<br>уже выбрано</strong><div class="product29-time"><i>10:00</i><i>11:30</i><i class="is-selected">14:00</i></div><div class="product29-confirmation"><span>✓</span> Подтверждение в личном кабинете</div></div></div>
<span class="eyebrow">ДЛЯ ВАШИХ КЛИЕНТОВ</span><h3>Выбрать услугу.<br>Записаться. Вернуться.</h3><p>Услуги, свободное время и история обращений в одном месте. Сотрудник получает данные для работы, клиент видит следующий шаг.</p></article>
<div class="product29-scenario-notes"><article><span class="product29-step-label">Обучение</span><h3>Потренироваться<br>и разобрать ошибки</h3><p>Темы, задания и сохранённый результат. Путь, к которому удобно возвращаться.</p><a class="product29-link" href="#product29-pilot">Посмотреть реальный пример</a></article><article><span class="product29-step-label">Внутренний сервис</span><h3>Получить задачу<br>и довести до результата</h3><p>Личный рабочий список, ответственные и история. Команда работает по согласованным правилам.</p><a class="product29-link" href="automation.html">Автоматизация для команды</a></article></div></div></section>
<section class="product29-case" id="product29-pilot"><div class="wrap product29-case-layout"><div class="product29-case-copy"><span class="eyebrow">РЕАЛЬНЫЙ ПРОЕКТ · PILOTSPACE</span><h2>Из документов —<br>в удобную тренировку</h2><p>Пилоты из Узбекистана попросили сделать подготовку удобнее. В PilotSpace вопросы собраны по темам, есть избранное и работа над ошибками.</p><ul><li>Тренировка в своём темпе</li><li>Возврат к сложным вопросам</li><li>Понятный путь без поиска по документам</li></ul><a class="product29-link" href="case-pilotspace.html">Как устроен PilotSpace</a></div><a class="product29-real-screen" href="case-pilotspace.html" aria-label="Открыть кейс PilotSpace"><img src="assets/pilotspace-quiz-desktop.jpg" width="1265" height="712" loading="lazy" decoding="async" alt="Реальный экран PilotSpace: тренировочный вопрос и варианты ответа"><span>Настоящий экран проекта</span></a></div></section>
<section class="wrap product29-platform"><div class="product29-section-title"><span class="eyebrow">ПЛАТФОРМА ПОД ЗАДАЧУ</span><h2>По ссылке.<br>Или в телефоне.</h2><p>Выбираем по тому, как продуктом будут пользоваться.</p></div><div class="product29-platform-options"><article><span class="product29-device product29-device-browser" aria-hidden="true"></span><h3>Веб-приложение</h3><p>Открывается в браузере. Подходит для кабинетов, внутренних инструментов и запуска первой версии.</p></article><article><span class="product29-device product29-device-phone" aria-hidden="true"></span><h3>Мобильное приложение</h3><p>Когда нужен отдельный мобильный сценарий и возможности устройства. Требования площадок и публикацию согласуем заранее.</p></article></div></section>'''
    return body + _finish(s, faq) + '</div>'


def automation(s, faq):
    body = '<div class="product29 product29-automation">'
    body += _hero(
        s, 'Работа движется.<br>Вы видите весь процесс.',
        'Связываем заявки, сотрудников и этапы работы. Создаём внутренние инструменты под правила вашей компании.',
        'stage27-process-cutout.png',
        'Заявка, ответственный сотрудник и выполненная задача, соединённые в единый процесс',
        'business-processes', 'Пройти путь заказа',
    )
    body += '''<section class="wrap product29-change"><div class="product29-section-title"><span class="eyebrow">МЕНЬШЕ РУЧНОГО СОГЛАСОВАНИЯ</span><h2>У каждого заказа<br>есть следующий шаг</h2><p>Не нужно собирать картину по сообщениям и звонкам. Нужные данные остаются рядом с задачей.</p></div><div class="product29-change-list"><article><span class="product29-change-mark" aria-hidden="true">01</span><div><h3>Понятно, кто отвечает</h3><p>Заявка назначена сотруднику. При передаче сохраняются детали и договорённости.</p></div></article><article><span class="product29-change-mark" aria-hidden="true">02</span><div><h3>Видно, что задерживается</h3><p>Статусы и согласованные сроки показывают, где требуется решение или помощь.</p></div></article><article><span class="product29-change-mark" aria-hidden="true">03</span><div><h3>Есть история результата</h3><p>Выполненные действия и проверка остаются в заказе. К ним можно вернуться.</p></div></article></div></section>'''
    body += stage4.flow_section(compact=True)
    body += '''<section class="wrap product29-choice"><div><span class="eyebrow">СНАЧАЛА РАЗБИРАЕМ ПРОЦЕСС</span><h2>Настроить готовое<br>или разработать своё?</h2><p>Проверим, можно ли решить задачу существующей системой. Собственный инструмент нужен, когда важные правила работы не укладываются в её возможности.</p></div><div class="product29-choice-panel"><span>Первый участок работы</span><h3>Один процесс.<br>Понятные правила.<br>Проверяемый результат.</h3><p>Зафиксируем роли, этапы, исключения и нужные данные. После проверки с командой определим следующий шаг развития.</p><a class="product29-link" href="integrations.html">Если нужно связать готовые сервисы</a></div></section>'''
    return body + _finish(s, faq) + '</div>'
