"""Responsive alpha WebP sources around four existing PNG illustrations.

Only generated, trusted HTML is processed. Original img tags remain byte-for-byte
unchanged. Existing picture elements are skipped, making enhancement idempotent.
Asset creation and CSS integration are owned by the public build integrator.
"""
import re


# Width descriptors name actual exported pixels, never HTML width attributes.
ASSETS = {
    'assets/stage27-hero-v1.png': (480, 720, 960),
    'assets/stage27-process-cutout.png': (480, 720, 960),
    'assets/stage28-websites-v1.png': (480, 720, 960),
    'assets/stage26-enquiry-cutout-v1.png': (360, 540, 720),
}

# Quote-aware tokenization preserves > inside quoted attribute values.
_TAG = re.compile(r'''</?(?:figure|picture|img)\b(?:[^>"']|"[^"]*"|'[^']*')*>''', re.I)
_ATTRIBUTE = re.compile(r'''(?:^|\s)([\w:-]+)\s*=\s*(?:"([^"]*)"|'([^']*)')''')
_NAME = re.compile(r'</?([a-z]+)', re.I)


def _attributes(tag):
    return {match[1].lower(): match[2] if match[2] is not None else match[3]
            for match in _ATTRIBUTE.finditer(tag)}


def _sizes(image_classes, figure_classes):
    if 'enquiry25-art' in image_classes:
        return '260px'
    if 'hero27-art' in figure_classes:
        return ('(max-width: 540px) calc(100vw - 36px), '
                '(max-width: 800px) min(540px, calc(100vw - 56px)), '
                '(max-width: 1100px) calc((100vw - 80px) / 2.15), '
                'min(584.2px, calc((100vw - 120px) / 2.15))')
    if 'website28-art' in figure_classes:
        return ('(max-width: 540px) calc(100vw - 36px), '
                '(max-width: 900px) min(560px, calc(100vw - 56px)), '
                '(max-width: 1100px) calc((100vw - 98px) / 2.1), '
                'min(589.6px, calc((100vw - 138px) / 2.1))')
    if 'manager-art' in figure_classes:
        # A 3:2 source needs at least 300px of width to cover a 200px-high slot.
        return '(max-width: 700px) max(300px, calc(100vw - 56px)), 600px'
    return '(max-width: 700px) calc(100vw - 56px), 600px'


def enhance(body):
    """Return HTML with responsive sources; leave all fallback attrs untouched."""
    figure_stack = []
    picture_depth = 0

    def replace(match):
        nonlocal picture_depth
        tag = match.group()
        name = _NAME.match(tag)[1].lower()
        closing = tag.startswith('</')
        if name == 'picture':
            picture_depth = max(0, picture_depth + (-1 if closing else 1))
            return tag
        if name == 'figure':
            if closing:
                if figure_stack:
                    figure_stack.pop()
            else:
                figure_stack.append(set(_attributes(tag).get('class', '').split()))
            return tag
        if closing or picture_depth:
            return tag
        attrs = _attributes(tag)
        src = attrs.get('src')
        if src not in ASSETS:
            return tag
        srcset = ', '.join(f'{src[:-4]}-stage34-{width}.webp {width}w'
                           for width in ASSETS[src])
        sizes = _sizes(set(attrs.get('class', '').split()),
                       figure_stack[-1] if figure_stack else set())
        return (f'<picture class="media34"><source type="image/webp" '
                f'srcset="{srcset}" sizes="{sizes}">{tag}</picture>')

    return _TAG.sub(replace, body)
