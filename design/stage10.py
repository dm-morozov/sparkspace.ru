"""Three visual directions, with all eight existing service destinations."""

def directions(services, icon):
    lookup = {s[0]: s[1] for s in services}
    scenes = [
        ('sites', 'Сайты и приложения', 'Клиент понимает предложение и легко делает следующий шаг.', ['websites','applications','redesign'],
         'Схематичный пример сайта с предложением и кнопкой обращения',
         '''<div class="scene-site"><div class="scene-browser"><i></i><i></i><i></i></div><div class="scene-site-nav"><b>Ваш бренд<span>✦</span></b><span>Услуги&nbsp;&nbsp; О нас</span></div><div class="scene-site-body"><div><strong>Ваше дело.<br>В лучшем свете.</strong><span class="scene-line"></span><span class="scene-line short"></span><span class="scene-cta">Обсудить задачу</span></div><div class="scene-site-image"><span class="scene-spark">✦</span><span class="scene-orbit"></span></div></div></div><div class="scene-mobile"><span class="scene-mobile-notch"></span><b>✦</b><i></i><i></i><span></span></div>'''),
        ('systems', 'Автоматизация и интеграции', 'Заявки, сотрудники и сервисы работают в одном процессе.', ['automation','integrations'],
         'Схематичный пример передачи заявки от администратора мастеру и контроля выполнения',
         '''<div class="scene-system"><div class="scene-system-head"><span class="scene-system-mark">✦</span><b>Рабочий процесс</b><span class="scene-live">●</span></div><div class="scene-ticket"><span class="scene-ticket-icon"><svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M7 3h7l4 4v14H6V3h1Z"/><path d="M14 3v5h4M9 12h6M9 16h4"/></svg></span><div><b>Новая заявка</b><small>Администратор принял обращение</small></div><span class="scene-status">Принята</span></div><div class="scene-transfer"><span>Назначить ответственного</span><b>↓</b></div><div class="scene-ticket assigned"><span class="scene-ticket-icon">✓</span><div><b>Задача мастеру</b><small>Детали и статус — в одной карточке</small></div></div><div class="scene-system-foot"><span>Сайт</span><b>↔</b><span>CRM</span><b>↔</b><span>Уведомления</span></div></div>'''),
        ('growth', 'Развитие и сопровождение', 'Находим слабые места, улучшаем сайт и поддерживаем его после запуска.', ['seo','audit','support'],
         'Схематичный пример проверки сайта, исправления ошибок и поисковой подготовки',
         '''<div class="scene-review"><div class="scene-search"><span>⌕</span> Ваши услуги в поиске</div><div class="scene-result"><small>ваш-сайт.ru / услуги</small><b>Ваш бизнес. Нужная услуга.</b><span class="scene-line"></span><span class="scene-line short"></span></div><div class="scene-check"><span>✓</span><b>Мобильная версия</b><small>Проверка</small></div><div class="scene-check"><span>✓</span><b>Форма обращения</b><small>Проверка</small></div><div class="scene-review-foot"><i></i> Проверить → Улучшить → Развивать</div></div>''')
    ]
    body = '<div class="visual-directions">'
    for i, (key,title,desc,slugs,label,art) in enumerate(scenes):
        body += f'<article class="visual-direction direction-{key}"><figure class="direction-scene" role="img" aria-label="{label}"><div class="scene-kicker" aria-hidden="true"><span>0{i+1}</span><span>ПРИМЕР РЕШЕНИЯ</span></div><div class="scene-art" aria-hidden="true">{art}</div></figure><div class="direction-info"><h3>{title}</h3><p>{desc}</p><ul>'
        for slug in slugs:
            body += f'<li><a href="{slug}.html"><span>{lookup[slug]}</span></a></li>'
        body += '</ul></div></article>'
    return body+'</div>'
