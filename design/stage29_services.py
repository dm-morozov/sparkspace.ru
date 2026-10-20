"""Service directory using the approved homepage identity and supplied prices."""
from html import escape

import stage25_enquiry


def services(S):
    lookup = {item[0]: item for item in S}
    summaries = {
        "websites": "Лендинг, сайт компании или магазин с понятным путём к заказу.",
        "applications": "Кабинет, обучение или сервис для клиентов и сотрудников.",
        "redesign": "Новый интерфейс с сохранением нужных функций и контента.",
        "automation": "Заявки, ответственные и этапы в одном рабочем процессе.",
        "integrations": "Передача данных между сайтом, CRM и другими сервисами.",
        "seo": "Структура и содержание, которые помогают находить ваши услуги.",
        "audit": "Проблемы сайта, их приоритет и конкретный план исправлений.",
        "support": "Исправления, новые страницы и функции по согласованному списку.",
    }

    def links(slugs):
        items = []
        for slug in slugs:
            service = lookup[slug]
            items.append(
                f'<li><a class="services29-link" href="{slug}.html">'
                f'<span class="services29-link-copy"><strong>{escape(service[1])}</strong>'
                f'<span>{escape(summaries[slug])}</span></span>'
                f'<span class="services29-link-price">{escape(service[4])}</span>'
                '</a></li>'
            )
        return '<ul class="services29-links">' + ''.join(items) + '</ul>'

    groups = [
        ("launch", "Запустить или обновить",
         "Сайт и приложение, с которыми удобно вашим клиентам.",
         "stage28-websites-v1.png",
         "Объёмные макеты сайта услуги, компании и интернет-магазина",
         ["websites", "applications", "redesign"]),
        ("process", "Связать работу команды",
         "Меньше ручных передач. Больше ясности в каждом заказе.",
         "stage27-process-cutout.png",
         "Обращение, ответственный и результат соединены в один процесс",
         ["automation", "integrations"]),
        ("growth", "Развивать то, что есть",
         "Найти слабые места и последовательно улучшать проект.",
         "stage27-hero-v1.png",
         "Интерфейсы сайта и приложения с инструментами развития",
         ["seo", "audit", "support"]),
    ]
    body = (
        '<div class="services29">'
        '<section class="wrap services29-intro">'
        '<nav class="breadcrumb" aria-label="Хлебные крошки">'
        '<a href="index.html">Главная</a><span aria-hidden="true">/</span>'
        '<span aria-current="page">Услуги</span></nav>'
        '<h1>Что нужно<br>вашему бизнесу?</h1>'
        '<p>Запустить сайт, связать процессы или улучшить работающий проект. '
        'Выберите задачу, чтобы посмотреть варианты и состав работ.</p>'
        '</section><section class="wrap services29-directory" aria-label="Направления работы">'
    )
    for key, title, text, image, alt, slugs in groups:
        body += (
            f'<article class="services29-group services29-{key}">'
            '<div class="services29-group-intro">'
            f'<div><h2>{title}</h2><p>{text}</p></div>'
            f'<img src="assets/{image}" width="960" height="640" '
            f'loading="lazy" decoding="async" alt="{alt}"></div>'
            + links(slugs) + '</article>'
        )
    body += (
        '</section><div class="wrap services29-note">'
        '<p>Стартовая цена относится к ограниченному составу работ. '
        'На странице каждой услуги описано, что входит в этот объём.</p>'
        '<a href="prices.html">Сравнить стоимость и условия</a>'
        '</div></div>'
    )
    return body + stage25_enquiry.enquiry()
