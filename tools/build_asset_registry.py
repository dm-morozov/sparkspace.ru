"""Inventory shipped raster images. Run after public build; --check never writes.

Uses Pillow already supplied by the workspace runtime. Provenance is curated in
asset-sources.json; filesystem timestamps are deliberately not capture dates.
"""
import argparse
import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.avif', '.ico'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []
        self.groups = []
        self.picture = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'picture':
            self.picture = []
        values = []
        if tag in ('img', 'source'):
            if a.get('src'):
                values.append((a['src'], tag))
            if a.get('srcset'):
                values.extend((part.strip().split()[0], 'srcset') for part in a['srcset'].split(',') if part.strip())
        if tag == 'meta' and a.get('property', a.get('name')) in ('og:image', 'twitter:image'):
            values.append((a.get('content', ''), 'social'))
        if tag == 'a' and a.get('href'):
            values.append((a['href'], 'original-link'))
        if tag == 'link' and 'icon' in a.get('rel', ''):
            values.append((a.get('href', ''), 'icon'))
        self.refs.extend(values)
        if self.picture is not None and tag in ('img', 'source'):
            self.picture.extend(url for url, _ in values)

    def handle_endtag(self, tag):
        if tag == 'picture' and self.picture is not None:
            self.groups.append(self.picture)
            self.picture = None


def local_image(url):
    parsed = urlsplit(url)
    if parsed.netloc and parsed.netloc not in ('sparkspace.ru', 'www.sparkspace.ru'):
        return None
    path = unquote(parsed.path).lstrip('/')
    if Path(path).suffix.lower() not in EXTENSIONS:
        return None
    if '..' in Path(path).parts:
        raise ValueError('Unsafe image reference: ' + url)
    return path


def collect(public, manifest, sources):
    paths = json.loads(manifest.read_text(encoding='utf-8-sig'))
    names = sorted(p for p in paths if Path(p).suffix.lower() in EXTENSIONS)
    usage = {name: {} for name in names}
    groups = {name: set() for name in names}
    page_hashes = {}
    # Matches the explicit draft exclusion in tools/build_public.py.
    for page in sorted(p for p in paths if p.endswith('.html') and p != 'consent-draft.html'):
        page_hashes[page] = digest(public / page)
        parser = References()
        parser.feed((public / page).read_text(encoding='utf-8'))
        for url, role in parser.refs:
            name = local_image(url)
            if name:
                if name not in usage:
                    raise ValueError(f'{page}: image absent from public manifest: {name}')
                usage[name].setdefault(page, set()).add(role)
        for picture in parser.groups:
            members = {local_image(url) for url in picture} - {None}
            for name in members:
                groups[name].update(members - {name})
    curated = json.loads(sources.read_text(encoding='utf-8-sig'))['assets']
    records = []
    for name in names:
        file = public / name
        sha = digest(file)
        info = curated.get(name, {'kind': 'unknown', 'source': 'unknown', 'date': 'unknown', 'purpose': 'unknown'})
        if info.get('reviewed_sha256') and info['reviewed_sha256'] != sha:
            raise ValueError(f'{name}: provenance hash stale; recheck source/date/captions before updating sidecar')
        with Image.open(file) as image:
            alpha = image.convert('RGBA').getchannel('A').getextrema()
            records.append({'path': name, 'sha256': sha, 'bytes': file.stat().st_size,
                            'width': image.width, 'height': image.height, 'format': image.format,
                            'has_alpha_channel': 'A' in image.getbands() or 'transparency' in image.info,
                            'has_transparency': alpha[0] < 255,
                            'pages': [{'path': page, 'roles': sorted(roles)} for page, roles in sorted(usage[name].items())],
                            'responsive_variants': sorted(groups[name]), 'provenance': info})
    return {'schema_version': 1, 'manifest_sha256': digest(manifest), 'sources_sha256': digest(sources),
            'page_sha256': page_hashes,
            'scope': 'Public manifest raster images; HTML img/source/picture/social/icon/original links. CSS backgrounds and inline SVG are outside this inventory.',
            'assets': records}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--public-dir', type=Path, default=ROOT / 'dist/public')
    ap.add_argument('--manifest', type=Path, default=ROOT / 'backend/docker/static-manifest.json')
    ap.add_argument('--sources', type=Path, default=ROOT / 'design/asset-sources.json')
    ap.add_argument('--output', type=Path, default=ROOT / 'design/asset-registry.json')
    ap.add_argument('--check', action='store_true')
    args = ap.parse_args()
    try:
        result = collect(args.public_dir, args.manifest, args.sources)
        if args.check:
            previous = json.loads(args.output.read_text(encoding='utf-8'))
            if previous != result:
                raise ValueError('Registry stale: rebuild after reviewing source/date/caption changes')
            print(f'PASS: {len(result["assets"])} public images match registry, sources and current HTML usage')
        else:
            args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            print(f'Wrote {len(result["assets"])} public images: {args.output}')
    except (OSError, ValueError, KeyError) as exc:
        ap.exit(1, f'Asset registry error: {exc}\n')


if __name__ == '__main__':
    main()
