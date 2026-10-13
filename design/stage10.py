"""Three visual directions, with all eight existing service destinations."""

def directions(services, icon):
    lookup = {s[0]: s[1] for s in services}
    scenes = [
        ('sites','Сайты и приложения','Клиент понимает предложение и легко делает следующий шаг.',['websites','applications','redesign'],'Иллюстрация сайта на компьютере и телефоне'),
        ('systems','Автоматизация и интеграции','Заявки, сотрудники и сервисы работают в одном процессе.',['automation','integrations'],'Иллюстрация процесса: заявка, сотрудник и выполненная задача'),
        ('growth','Развитие и сопровождение','Находим слабые места, улучшаем сайт и поддерживаем его после запуска.',['seo','audit','support'],'Иллюстрация проверки и улучшения сайта'),
    ]
    body = '<div class="visual-directions">'
    for i, (key,title,desc,slugs,label) in enumerate(scenes):
        body += f'<article class="visual-direction direction-{key}"><figure class="direction-scene direction-illustration"><img src="assets/direction-{key}-v1.jpg" width="960" height="640" loading="lazy" decoding="async" alt="{label}"></figure><div class="direction-info"><h3>{title}</h3><p>{desc}</p><ul>'
        for slug in slugs:
            body += f'<li><a href="{slug}.html"><span>{lookup[slug]}</span></a></li>'
        body += '</ul></div></article>'
    return body+'</div>'
