"""Deterministic, partially extracted stylesheet bundle. No glob or implicit EOL conversion."""
from pathlib import Path, PureWindowsPath
import argparse
import json
import re

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / 'style-bundle.json'


def literal_bytes(text):
    if not isinstance(text, str) or not re.fullmatch(r'(?:[ \t\r\n\f]|/\*(?:[^*]|\*(?!/))*\*/)*', text):
        raise ValueError('CSS literal may contain only comments and whitespace')
    return text.encode('utf-8')


def safe_css_path(name):
    if not isinstance(name, str) or not name or '\\' in name:
        raise ValueError('Expected a relative forward-slash CSS path')
    parts = name.split('/')
    if any(p in ('', '.', '..') for p in parts) or PureWindowsPath(name).drive or name.startswith('/'):
        raise ValueError('Absolute or traversing CSS path rejected: ' + name)
    if Path(name).suffix != '.css' or ':' in name:
        raise ValueError('Only CSS paths without stream names are allowed')
    path = ROOT
    for part in parts:
        path = path / part
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise ValueError('Symlink/junction CSS paths are forbidden')
    if not path.resolve().is_relative_to(ROOT.resolve()):
        raise ValueError('CSS path escapes design root')
    return path


def compose():
    """Return final bytes from the explicit ordered manifest; do not write."""
    if MANIFEST.is_symlink():
        raise ValueError('Manifest symlinks are forbidden')
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if manifest.get('schema_version') != 1 or not isinstance(manifest.get('entries'), list):
        raise ValueError('Unsupported style bundle manifest')
    pieces = []
    seen = set()
    for entry in manifest['entries']:
        if not isinstance(entry, dict):
            raise ValueError('Invalid CSS entry')
        if 'literal' in entry:
            if set(entry) != {'literal'}:
                raise ValueError('Literal entry cannot contain source or transform')
            pieces.append(literal_bytes(entry['literal']))
            continue
        if set(entry) != {'source', 'eol'}:
            raise ValueError('Source entry requires exactly source and eol')
        path = safe_css_path(entry['source'])
        if path in seen:
            raise ValueError('Duplicate CSS input: ' + entry['source'])
        seen.add(path)
        data = path.read_bytes()
        eol = entry.get('eol')
        if eol == 'lf':
            data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
        elif eol == 'crlf':
            data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n').replace(b'\n', b'\r\n')
        elif eol != 'preserve':
            raise ValueError('Explicit EOL transform required: ' + entry['source'])
        pieces.append(data)
    return b''.join(pieces)


def check(output='style.css'):
    """Compare the current output with composed bytes; never write."""
    return safe_css_path(output).read_bytes() == compose()


def build(output='style.css'):
    """Write only when bytes differ; return True if changed, False for no-op."""
    target = safe_css_path(output)
    entries = json.loads(MANIFEST.read_text(encoding='utf-8'))['entries']
    if target in {safe_css_path(entry['source']) for entry in entries if 'source' in entry}:
        raise ValueError('Output cannot overwrite a source')
    data = compose()
    if target.exists() and target.read_bytes() == data:
        return False
    target.write_bytes(data)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--output', default='style.css', help='Relative CSS output inside design')
    args = parser.parse_args()
    try:
        if args.check:
            if not check(args.output):
                parser.exit(1, 'Stylesheet differs from ordered bundle\n')
            print('PASS: byte-identical stylesheet')
        else:
            print('Written' if build(args.output) else 'Unchanged (no write)')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        parser.exit(1, f'Style bundle error: {exc}\n')


if __name__ == '__main__':
    main()
