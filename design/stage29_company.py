"""Company, process, contact and pricing pages in the approved visual system."""
from html import escape

import stage6
import stage25_delivery
import stage25_enquiry


def intro(label, title, text, image, alt):
    return (
        '<div class="company29"><section class="company29-hero"><div class="wrap">'
        '<nav class="breadcrumb" aria-label="Хлебные крошки"><a href="index.html">Главная</a>'
        f'<span aria-hidden="true">/</span><span aria-current="page">{label}</span></nav>'
        f'<div class="company29-hero-grid"><div><h1>{title}</h1><p>{text}</p></div>'
        f'<img src="assets/{image}" width="960" height="640" alt="{alt}" '
        'decoding="async"></div></div></section>'
    )


def about():
    body = intro(
        'О SparkSpace', 'Вникаем в бизнес.<br>Создаём решение.',
        'SparkSpace разрабатывает сайты, приложения и инструменты автоматизации. '
        'Соединяем дизайн, программирование и продвижение вокруг вашей задачи.',
        'stage27-hero-v1.png', 'Сайт, приложение и связанные цифровые инструменты'
    )
    body += (
        '<section class="wrap company29-story"><h2>Команда, которая ведёт<br>проект до запуска</h2>'
        '<div><p>В команде есть разработчики с опытом около 15 лет. '
        'Собираем нужную экспертизу под проект и показываем промежуточные версии.</p>'
        '<p>Работаем из Оренбурга с заказчиками по всей России. '
        'Состав работ, этапы и критерии результата согласуем до разработки.</p></div></section>'
        '<section class="wrap company29-principles" aria-label="Принципы работы">'
    )
    for title, text in [
        ('Сначала задача', 'Выясняем, что нужно клиентам и сотрудникам. Под это выбираем функции и интерфейс.'),
        ('Результат по этапам', 'Вы видите рабочие версии, проверяете сценарии и принимаете согласованный объём.'),
        ('Развитие после запуска', 'Передаём доступы и объясняем работу. Следующие улучшения оцениваем отдельно.'),
    ]:
        body += f'<article><h3>{title}</h3><p>{text}</p></article>'
    body += (
        '</section><section class="wrap company29-evidence commercial31-evidence">'
        '<div><h2>Наш подход можно посмотреть в работе</h2>'
        '<p>Два разных проекта. Посмотрите, какую задачу решает каждый.</p></div>'
        '<div class="commercial31-case-grid">'
        '<a class="commercial31-case" href="case-mu56.html">'
        '<img src="assets/mu56-home-desktop.jpg" loading="lazy" width="1265" height="712" '
        'alt="Настоящая главная страница сайта Мир Улыбок">'
        '<span class="commercial31-case-copy"><strong>Мир Улыбок</strong>'
        '<span>Собственный бизнес: сайт с нуля, фотографии, оптимизация и Telegram-бот.</span>'
        '<span class="commercial31-case-action">Посмотреть кейс</span></span></a>'
        '<a class="commercial31-case" href="case-pilotspace.html">'
        '<img src="assets/pilotspace-quiz-desktop.jpg" loading="lazy" width="1265" height="712" '
        'alt="Настоящий экран тренировки PilotSpace с вопросом и вариантами ответа">'
        '<span class="commercial31-case-copy"><strong>PilotSpace</strong>'
        '<span>По запросу пилотов из Узбекистана: тренировки по темам и работа над ошибками.</span>'
        '<span class="commercial31-case-action">Посмотреть кейс</span></span></a>'
        '</div></section></div>'
    )
    return body + stage25_enquiry.enquiry()


def approach():
    body = intro(
        'Подход', 'Понятный план.<br>Проверяемый результат.',
        'До разработки согласуем объём и критерии приёмки. '
        'По ходу проекта показываем, что готово и какой шаг следующий.',
        'stage28-websites-v1.png', 'Макеты страниц как наглядный результат проектирования'
    )
    body += stage25_delivery.delivery()
    body += '<section class="wrap company29-terms"><h2>Что фиксируем заранее</h2><div>'
    for title, text in [
        ('Объём и ответственность', 'Согласуем бриф, функции, сроки и ответственного за обратную связь. '
         'Решения и изменения сохраняем в переписке и документах.'),
        ('Оплата по этапам', 'Например: 30% после договора, 40% после согласованной рабочей версии, '
         '30% перед передачей финальных материалов. Порядок оплаты фиксируем в договоре под состав услуги и этапы проекта.'),
        ('Проверка и передача', 'Проверяем формы, переходы, права и ключевые сценарии. '
         'Порядок передачи исходников, доступов и прав закрепляем в договоре.'),
        ('Поддержка после запуска', '30 календарных дней исправляем без доплаты ошибки согласованного функционала. '
         'Новые функции, контент и дальнейшее сопровождение оцениваем отдельно.'),
    ]:
        body += f'<article><h3>{title}</h3><p>{text}</p></article>'
    return body + '</div></section></div>' + stage25_enquiry.enquiry()


def contacts():
    body = intro(
        'Контакты', 'Обсудим<br>ваш проект',
        'Пришлите идею, ссылку на сайт или описание процесса. '
        'Поможем определить первый шаг, состав работ и бюджет.',
        'stage26-enquiry-cutout-v1.png', 'Открытый блокнот, ручка и прозрачный символ диалога'
    )
    body += (
        '<section class="wrap company29-contacts"><div><h2>Как вам удобнее?</h2>'
        + stage6.links() +
        '<section class="contact30-context" data-contact-context hidden aria-labelledby="contact30-title">'
        '<span class="eyebrow">ВАШЕ ОБРАЩЕНИЕ</span><h3 id="contact30-title">Подготовим короткое сообщение</h3>'
        '<p class="contact30-selection" data-contact-selection></p>'
        '<label for="contact30-message">Текст для мессенджера</label>'
        '<textarea id="contact30-message" data-contact-message rows="5" maxlength="2000" '
        'aria-describedby="contact30-help" spellcheck="true"></textarea>'
        '<p id="contact30-help">Дополните текст, скопируйте и вставьте в Telegram или MAX. '
        'Сообщение отправите сами в выбранном приложении.</p>'
        '<div class="contact30-copy-row"><button class="btn primary" type="button" data-contact-copy>'
        'Скопировать сообщение</button><span data-contact-status role="status" aria-live="polite" '
        'aria-atomic="true"></span></div></section>'
        '</div><aside><h2>Чтобы начать разговор</h2>'
        '<ol><li>Чем занимается ваш бизнес?</li><li>Что хотите запустить или улучшить?</li>'
        '<li>Как сейчас решается эта задача?</li></ol>'
        '<p>Можно написать своими словами. Готовое техническое задание не обязательно.</p>'
        '<div class="company29-location"><strong>Оренбург</strong>'
        '<span>Работаем дистанционно. Время разговора согласуем.</span></div>'
        '</aside></section></div>'
    )
    return body


def prices(S):
    lookup = {item[0]: item for item in S}
    # A starting price names its deliverable, not an entire product it cannot buy.
    results = {
        'applications': 'Результат: сценарий и план разработки',
        'automation': 'Результат: рабочая версия одного процесса',
        'integrations': 'Результат: один сценарий передачи данных',
        'redesign': 'Объём и стоимость после разбора сайта',
        'seo': 'Результат: согласованные работы за месяц',
        'audit': 'Результат: найденные проблемы и приоритеты',
        'support': 'Результат: согласованный пакет доработок',
    }
    body = intro(
        'Стоимость', 'Начните с нужного.<br>Развивайте поэтапно.',
        'Выберите первый результат. Состав работ и стоимость фиксируем до начала этапа, '
        'а дополнительные задачи оцениваем отдельно.',
        'stage26-enquiry-cutout-v1.png', 'Блокнот для плана и оценки проекта с символом обсуждения'
    )
    body += (
        '<section class="wrap company29-prices"><h2>Ориентиры по направлениям</h2>'
        '<p class="company29-price-lead">У каждой стартовой цены есть границы. '
        'Раскройте состав работ, чтобы сравнить подходящие варианты.</p>'
        '<div class="company29-price-grid commercial31-prices">'
    )
    for slug in ['websites', 'applications', 'automation', 'integrations', 'redesign', 'seo', 'audit', 'support']:
        item = lookup[slug]
        price = (
            '<dl class="commercial31-site-formats">'
            f'<div><dt>Лендинг</dt><dd>{escape(item[4])}</dd></div>'
            '<div><dt>Сайт компании</dt><dd>от 50 000 ₽</dd></div>'
            '<div><dt>Интернет-магазин</dt><dd>По смете</dd></div>'
            '</dl>'
        ) if slug == 'websites' else (
            f'<strong class="company29-price">{escape(item[4])}</strong>'
            f'<span class="commercial31-result">{escape(results[slug])}</span>'
        )
        body += (
            f'<article><h3>{escape(item[1])}</h3>{price}'
            f'<p>{escape(item[2])}</p><details><summary>Что входит в стоимость</summary>'
            f'<p>{escape(item[7])}</p></details><div class="contact30-price-actions">'
            f'<a class="btn primary" href="contacts.html?service={slug}">Обсудить этот вариант</a>'
            f'<a href="{slug}.html">Подробнее об услуге</a></div></article>'
        )
    body += (
        '</div><div class="company29-price-conditions">'
        '<h2>Без неожиданных дополнений к смете</h2>'
        '<p>Домен, хостинг, лицензии и сторонние сервисы оплачиваются отдельно. '
        'Дизайн, тексты, перенос данных и интеграции входят только в согласованный объём.</p>'
        '<p>Разработку можно оплачивать по этапам, например 30/40/30. '
        'Порядок оплаты фиксируем в договоре под состав услуги и этапы проекта. '
        '30 дней после запуска исправляем ошибки согласованного функционала без доплаты.</p>'
        '<a href="approach.html">Как проходят работа и приёмка</a></div></section></div>'
    )
    return body + stage25_enquiry.enquiry()
