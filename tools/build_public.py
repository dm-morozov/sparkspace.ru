"""Build a public static release without the local lead API or draft consent."""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
from urllib.parse import urlsplit, unquote
import json, re, runpy, shutil, sys, zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'design'
TARGET = ROOT / 'dist' / 'public'
DOMAIN = 'https://sparkspace.ru'
sys.path.insert(0, str(SOURCE))
runpy.run_path(str(SOURCE / 'build.py'), run_name='__main__')
import stage6
import stage29_company
import stage33_metadata

manifest = json.loads((ROOT / 'backend/docker/static-manifest.json').read_text(encoding='utf-8'))
names = [n for n in manifest if n not in {'consent-draft.html', 'lead-form.js'}]
TARGET.mkdir(parents=True, exist_ok=True)
# Only overwrite release allowlist files; do not touch other local directories.
for name in names:
    src, dst = SOURCE / name, TARGET / name
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not name.endswith('.html'):
        shutil.copyfile(src, dst)
        continue
    html = src.read_text(encoding='utf-8')
    html = html.replace('<meta name="robots" content="noindex,nofollow">', '<meta name="robots" content="index,follow">')
    html = re.sub(r'<script src="lead-form\.js[^\"]*"></script>', '', html)
    if name == 'contacts.html':
        contact = '<main id="main">' + stage29_company.contacts() + '</main>'
        html = re.sub(r'<main id="main">.*?</main>', lambda _: contact, html, flags=re.S)
    url = DOMAIN + ('/' if name == 'index.html' else '/' + name)
    title = re.search(r'<title>(.*?)</title>', html).group(1)
    description = escape(stage33_metadata.DESCRIPTIONS[name], quote=True)
    meta = f'<meta property="og:description" content="{description}"><link rel="canonical" href="{url}"><meta property="og:type" content="website"><meta property="og:locale" content="ru_RU"><meta property="og:site_name" content="SparkSpace"><meta property="og:title" content="{title}"><meta property="og:url" content="{url}"><meta property="og:image" content="{DOMAIN}/assets/app-product-concept-v1.jpg"><link rel="icon" href="assets/sparkspace-mark.png">'
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

pages={n:Page((TARGET/n).read_text(encoding='utf-8')) for n in names if n.endswith('.html')}
for n,page in pages.items():
    assert page.h1 == 1, n
    assert page.forms == 0, n
    text=(TARGET/n).read_text(encoding='utf-8')
    assert 'noindex' not in text and '/api/v1/leads' not in text and 'consent-draft.html' not in text, n
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
