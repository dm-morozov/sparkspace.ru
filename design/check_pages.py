"""Validate generated local pages, links, anchors and shared service navigation."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).parent
class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids, self.refs = set(), []
        self.h1 = 0
        self.noindex = False
        self.feed(path.read_text(encoding='utf-8'))
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag == 'h1': self.h1 += 1
        if tag == 'meta' and attrs.get('name') == 'robots':
            self.noindex = 'noindex' in attrs.get('content', '')
        for key in ('href', 'src'):
            if key in attrs: self.refs.append(attrs[key])

pages = {path: Page(path) for path in ROOT.glob('*.html')}
errors, checked = [], 0
for path, page in pages.items():
    if page.h1 != 1: errors.append(f'{path.name}: h1={page.h1}')
    if not page.noindex: errors.append(f'{path.name}: missing noindex')
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme or url.netloc: continue
        target = path.parent / unquote(url.path) if url.path else path
        if not target.exists(): errors.append(f'{path.name}: missing {ref}')
        elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
            errors.append(f'{path.name}: missing anchor {ref}')
        checked += 1
    for slug in ('websites','applications','redesign','automation','integrations','seo','audit','support'):
        if page.refs.count(slug+'.html') < 2:
            errors.append(f'{path.name}: service {slug} not in both shared menu/footer')
print(f'{len(pages)} pages, {checked} local references, {len(errors)} errors')
for error in errors: print(error)
raise SystemExit(bool(errors))
