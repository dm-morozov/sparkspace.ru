"""Real mobile case evidence; decorative generated art never substitutes screenshots."""
from html import escape

CASES = {
    'mu56': {
        'name': 'Мир Улыбок',
        'title': 'Выбрать праздник<br>с телефона',
        'intro': 'Реальные фотографии, программы и цены помогают познакомиться с предложением до обращения.',
        'screen': 'mu56-mobile-stage32.png',
        'accent': 'stage32-mu56-accent.png',
        'alt': 'Реальный мобильный экран сайта детских праздников Мир Улыбок',
        'steps': [
            ('Познакомиться', 'Посмотреть фотографии и понять, какие праздники можно заказать.'),
            ('Выбрать формат', 'Сопоставить программы, персонажей и состав предложения.'),
            ('Обсудить праздник', 'Перейти от выбранного варианта к обращению.'),
        ],
        'note': 'Собственный бизнес-проект: от структуры и фотографий до кода и Telegram-бота.',
    },
    'pilotspace': {
        'name': 'PilotSpace',
        'title': 'Вернуться к практике<br>с телефона',
        'intro': 'Учебные вопросы собраны в браузерном тренажёре. Можно выбрать тему и сосредоточиться на нужном материале.',
        'screen': 'pilotspace-mobile-stage32.png',
        'accent': 'stage32-pilot-accent.png',
        'alt': 'Реальный мобильный экран веб-тренажёра PilotSpace',
        'steps': [
            ('Выбрать тему', 'Найти нужный раздел подготовки и перейти к вопросам.'),
            ('Потренироваться', 'Отвечать на вопросы выбранной темы в браузере.'),
            ('Повторить сложное', 'Вернуться к ошибкам и избранным вопросам.'),
        ],
        'note': 'Создан по запросу пилотов из Узбекистана. Самостоятельный тренажёр, не официальный экзамен.',
    },
}


def mobile_case(kind):
    """Embed once per case. Assets are captured/generated and verified by integrator."""
    if kind not in CASES:
        raise ValueError('Unknown mobile case: ' + kind)
    c = CASES[kind]
    title_id = 'case32-mobile-' + kind
    src = 'assets/' + c['screen']
    body = (
        f'<section class="wrap case32-mobile case32-mobile--{kind}" aria-labelledby="{title_id}">'
        '<div class="case32-mobile-copy"><span class="case32-label">Реальный мобильный интерфейс</span>'
        f'<h2 id="{title_id}">{c["title"]}</h2><p class="case32-intro">{escape(c["intro"])}</p>'
        '<ol class="case32-steps">'
    )
    for index, (title, text) in enumerate(c['steps'], 1):
        body += (
            '<li><span class="case32-step-number" aria-hidden="true">' + str(index) + '</span>'
            f'<div><h3>{escape(title)}</h3><p>{escape(text)}</p></div></li>'
        )
    body += (
        '</ol><div class="case32-context">'
        f'<img src="assets/{c["accent"]}" width="600" height="400" loading="lazy" decoding="async" alt="">'
        f'<p>{escape(c["note"])}</p></div></div>'
        '<figure class="case32-mobile-figure">'
        f'<a class="case32-screen-link" href="{src}" target="_blank" rel="noopener" '
        f'aria-label="Рассмотреть мобильный экран {escape(c["name"], quote=True)} в новой вкладке">'
        f'<img src="{src}" width="375" height="812" loading="lazy" decoding="async" alt="{escape(c["alt"], quote=True)}">'
        '</a><figcaption>'
        f'<a class="case32-zoom" href="{src}" target="_blank" rel="noopener">Рассмотреть экран <span>(новая вкладка)</span></a>'
        '<span class="case32-screen-note">Работающий проект · снимок 24.10.2026. Интерфейс не перерисован.</span>'
        '</figcaption></figure></section>'
    )
    return body
