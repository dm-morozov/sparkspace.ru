"""Build a public static release without the local lead API or draft consent."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, runpy, shutil, sys, zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'design'
TARGET = ROOT / 'dist' / 'public'
DOMAIN = 'https://sparkspace.ru'
sys.path.insert(0, str(SOURCE))
runpy.run_path(str(SOURCE / 'build.py'), run_name='__main__')
import stage6

manifest = json.loads((ROOT / 'backend/docker/static-manifest.json').read_text(encoding='utf-8'))
responsive = json.loads((ROOT / 'tools/responsive_images.json').read_text(encoding='utf-8')) if (ROOT / 'tools/responsive_images.json').exists() else {}

def responsive_image(match):
    tag = match.group(0)
    source = re.search(r' src="([^"]+)"', tag)
    if not source or source[1] not in responsive:
        return tag
    variants = responsive[source[1]]
    tag = tag.replace(source[0], f' src="{variants[-1][0]}"')
    sizes = '(max-width: 650px) calc(100vw - 40px), (max-width: 900px) 560px, 50vw'
    if source[1].endswith('stage27-hero-v1.png'):
        sizes = '(max-width: 900px) calc(100vw - 40px), 50vw'
    attributes = ' srcset="' + ', '.join(f'{path} {width}w' for path,width in variants) + f'" sizes="{sizes}"'
    return tag.replace('<img', '<img' + attributes, 1)
names = [n for n in manifest if n not in {'consent-draft.html', 'lead-form.js'}]
TARGET.mkdir(parents=True, exist_ok=True)
# Only overwrite release allowlist files; do not touch other local directories.
for name in names:
    src, dst = SOURCE / name, TARGET / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not name.endswith('.html'):
        shutil.copyfile(src, dst)
        if name == 'style.css':
            css = src.read_text(encoding='utf-8').replace("@import url('service-pages.css');", '')
            dst.write_text(css + '\n' + (SOURCE/'service-pages.css').read_text(encoding='utf-8'), encoding='utf-8')
        continue
    html = src.read_text(encoding='utf-8')
    html = html.replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow">')
    html = re.sub(r'<script src="lead-form\.js[^\"]*"></script>', '', html)
    if name == 'contacts.html':
        contact = '<main id="main"><section class="wrap inner-intro"><div class="breadcrumb"><a href="index.html">Главная</a><span>/</span>Контакты</div><h1>Обсудим ваш проект</h1><p>Расскажите о задаче, пришлите ссылку на сайт или примеры. Обсудим подходящее решение, этапы и стоимость.</p></section><section class="wrap public-enquiry"><div><h2>Выберите удобный способ связи</h2>' + stage6.links() + '</div><aside><h2>С чего начать</h2><p>Чем занимается ваш бизнес? Что хотите сделать или улучшить? Если сайт уже есть, приложите его адрес.</p><p>Готовое техническое задание не обязательно. Состав работ и бюджет согласуем до начала проекта.</p></aside></section></main>'
        html = re.sub(r'<main id="main">.*?</main>', lambda _: contact, html, flags=re.S)
        starter = '<section class="wrap contact-context" data-contact-context hidden><h2>Ваше направление: <span data-service-name></span></h2><label for="message-starter">Начало сообщения. Можно дополнить и скопировать.</label><textarea id="message-starter" rows="5"></textarea><button class="btn primary" type="button">Скопировать текст</button><p role="status" aria-live="polite"></p></section>'
        html = html.replace('<section class="wrap public-enquiry">', starter + '<section class="wrap public-enquiry">')
        html = html.replace('</body>', '<script src="contact-context.js"></script></body>')
    # Render an SVG instead of relying on a font containing diagonal-arrow glyphs.
    arrow = '<svg class="external-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M7 17 17 7M7 7h10v10"/></svg>'
    html = html.replace('↗', arrow)
    html = re.sub(r'<img\b[^>]*>', responsive_image, html)
    url = DOMAIN + ('/' if name == 'index.html' else '/' + name)
    title = re.search(r'<title>(.*?)</title>', html).group(1)
    meta = f'<link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="SparkSpace"><meta property="og:title" content="{title}"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMAIN}/assets/app-product-concept-v1.jpg"><link rel="icon" href="assets/sparkspace-mark.png">'
    html = html.replace('</head>', meta + '</head>')
    dst.write_text(html, encoding='utf-8')

with (TARGET / 'style.css').open('a', encoding='utf-8') as f:
    f.write('\n.public-enquiry{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1fr);gap:70px;padding-bottom:70px}.public-enquiry h2{font-size:28px}.public-enquiry aside p{color:var(--muted);font-size:16px;line-height:1.8;margin-top:20px}@media(max-width:700px){.public-enquiry{grid-template-columns:minmax(0,1fr);gap:40px;padding-bottom:45px}.public-enquiry h2{font-size:25px}}\n')
(TARGET / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n', encoding='utf-8')
urls = [DOMAIN + ('/' if n == 'index.html' else '/' + n) for n in names if n.endswith('.html')]
(TARGET / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{u}</loc></url>' for u in urls) + '</urlset>', encoding='utf-8')

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.refs=[]; self.ids=set(); self.h1=0; self.forms=0; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        self.h1 += tag == 'h1'; self.forms += tag == 'form'
        if 'id' in a: self.ids.add(a['id'])
        self.refs.extend(a[k] for k in ('href','src') if k in a)
        if 'srcset' in a:
            self.refs.extend(item.strip().split()[0] for item in a['srcset'].split(','))

pages={n:Page((TARGET/n).read_text(encoding='utf-8')) for n in names if n.endswith('.html')}
for n,page in pages.items():
    assert page.h1 == 1, n
    assert page.forms == 0, n
    text=(TARGET/n).read_text(encoding='utf-8')
    assert 'noindex' not in text and '/api/v1/leads' not in text and 'consent-draft.html' not in text, n
    assert '↗' not in text, n
    for ref in page.refs:
        u=urlsplit(ref)
        if u.scheme or u.netloc: continue
        path=unquote(u.path) or n
        assert (TARGET/path).is_file(), (n,ref)
        if u.fragment and path in pages: assert unquote(u.fragment) in pages[path].ids, (n,ref)
release_names=names+['robots.txt','sitemap.xml']
with zipfile.ZipFile(ROOT/'dist/sparkspace-static.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
    for n in release_names: archive.write(TARGET/n,n)
print(f'Public release: {len(pages)} pages, {len(release_names)} files; no forms or local API. ZIP: dist/sparkspace-static.zip')
