"""Home composition and grouped navigation; preserve the accepted sources."""
def directions(services,icon):
 groups=[('Сайты и приложения','Публичный сайт или продукт для ваших пользователей.',['websites','applications','redesign']),('Автоматизация и интеграции','Процессы команды и обмен между системами.',['automation','integrations']),('Развитие и сопровождение','Проверка, улучшения и работа после запуска.',['seo','audit','support'])]
 lookup={s[0]:s for s in services}
 body='<div class="direction-groups">'
 for i,(title,desc,slugs) in enumerate(groups):
  body+=f'<article class="direction-group"><div class="direction-art" aria-hidden="true">{icon([0,2,3][i])}<span>0{i+1}</span></div><h3>{title}</h3><p>{desc}</p><ul>'
  for slug in slugs:body+=f'<li><a href="{slug}.html"><span>{lookup[slug][1]}</span><b aria-hidden="true">↗</b></a></li>'
  body+='</ul></article>'
 return body+'</div>'

def projects():
 return '''<div class="project-composition"><a class="project-feature" href="case-mu56.html"><div class="project-caption"><span class="eyebrow">01 / САЙТ УСЛУГ</span><h3>Мир Улыбок</h3><p>Реальные фотографии, выбор программы и путь к обращению.</p><span class="text-link">Посмотреть проект <b aria-hidden="true">↗</b></span></div><div class="project-stage"><svg class="project-orbit" viewBox="0 0 600 420" fill="none" aria-hidden="true"><circle cx="300" cy="210" r="190"/><ellipse cx="300" cy="210" rx="285" ry="125" transform="rotate(-24 300 210)"/></svg><img src="assets/mu56-home-desktop.jpg" alt="Реальная публичная страница сайта Мир Улыбок" width="1265" height="712" loading="lazy"></div></a><a class="project-feature" href="case-pilotspace.html"><div class="project-stage"><svg class="project-orbit" viewBox="0 0 600 420" fill="none" aria-hidden="true"><path d="M30 350 170 190 280 270 430 70 560 130"/><circle cx="430" cy="70" r="18"/><path d="M20 390h560"/></svg><img src="assets/pilotspace-home-desktop.jpg" alt="Реальная публичная страница тренажёра PilotSpace" width="1265" height="712" loading="lazy"></div><div class="project-caption"><span class="eyebrow">02 / ВЕБ-ПРИЛОЖЕНИЕ</span><h3>PilotSpace</h3><p>Темы, тренировки и работа над ошибками.</p><span class="text-link">Как устроен тренажёр <b aria-hidden="true">↗</b></span></div></a></div>'''
