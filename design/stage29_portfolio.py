"""Presentation wrappers around existing projects and factual case content."""
import re
import stage25_enquiry


def projects(projects_html):
    return '''<div class="portfolio29"><section class="wrap portfolio29-intro">
<nav class="breadcrumb" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span aria-hidden="true">/</span><span aria-current="page">Проекты</span></nav>
<div class="portfolio29-intro-grid"><div><span class="eyebrow">ПРОЕКТЫ SPARKSPACE</span><h1>Идеи становятся<br>рабочими инструментами</h1></div><p>Сайты услуг, каталоги и веб-приложения. Посмотрите реальные интерфейсы и задачи, которые они помогают решать.</p></div>
</section><section class="wrap portfolio29-projects" aria-label="Примеры проектов">''' + projects_html + '''</section>''' + stage25_enquiry.enquiry() + '</div>'


def solutions(flow_html):
    return '''<div class="solutions29"><section class="wrap portfolio29-intro">
<nav class="breadcrumb" aria-label="Хлебные крошки"><a href="index.html">Главная</a><span aria-hidden="true">/</span><span aria-current="page">Решения для бизнеса</span></nav>
<div class="portfolio29-intro-grid"><div><span class="eyebrow">РЕШЕНИЯ ДЛЯ БИЗНЕСА</span><h1>Работа движется.<br>Вы видите главное.</h1></div><div><p>Обращения, задачи и ответственность — в одном процессе. Посмотрите примеры и выберите сценарий, близкий вашему бизнесу.</p><a class="text-link" href="#business-processes">Посмотреть сценарии</a></div></div>
</section>''' + flow_html + '''<section class="wrap solutions29-next"><div><span class="eyebrow">ОТ ПРИМЕРА К ВАШЕЙ ЗАДАЧЕ</span><h2>Начнём с одного процесса</h2><p>Разберём, как он устроен сейчас, где возникают задержки и что стоит изменить в первую очередь.</p></div><div class="solutions29-links"><a href="automation.html"><strong>Автоматизация</strong><span>Роли, задачи, статусы и контроль выполнения</span></a><a href="integrations.html"><strong>Интеграции</strong><span>Обмен данными между вашими сервисами</span></a><a href="applications.html"><strong>Веб-приложения</strong><span>Инструмент под особенности вашей работы</span></a></div></section>''' + stage25_enquiry.enquiry() + '</div>'


def case(body, kind):
    """Keep every factual paragraph/caption; move one real screen closer to the intro."""
    if kind not in ('mu56', 'pilotspace'):
        raise ValueError('Unknown case kind')
    screens = re.search(r'<section\b[^>]*\bid="screens"[^>]*>.*?</section>', body, re.S)
    if screens:
        figure = re.search(r'<figure class="case-screen">.*?</figure>', screens.group(), re.S)
        if figure:
            remaining = screens.group().replace(figure.group(), '', 1)
            has_more = '<figure' in remaining
            body = body.replace(screens.group(), remaining if has_more else '', 1)
            preview_id = '' if has_more else ' id="screens"'
            preview = f'<section class="wrap case29-preview"{preview_id}>' + figure.group() + '</section>'
            body = body.replace('</section>', '</section>' + preview, 1)
    # The existing related service links remain; the full enquiry replaces their old button.
    body = re.sub(r'<a class="btn [^"]*"[^>]*>.*?</a>', '', body, flags=re.S)
    other_href, other_name = ('case-pilotspace.html', 'PilotSpace — веб-тренажёр') if kind == 'mu56' else ('case-mu56.html', 'Мир Улыбок — сайт услуг')
    navigation = f'<nav class="wrap case29-navigation" aria-label="Другие проекты"><a href="projects.html">Все проекты</a><a href="{other_href}">{other_name}</a></nav>'
    return f'<div class="case29 case29--{kind}">' + body + navigation + stage25_enquiry.enquiry() + '</div>'
