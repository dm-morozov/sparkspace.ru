"""Extract the measured 1200x630 native card from browser screenshot canvases.

This only removes outside-canvas whitespace; content is not repainted/rescaled.
Run after browser capture of qa-stage35/social-*.html at document origin 0,0.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
KEYS = ('general', 'websites', 'systems', 'development', 'mu56', 'pilotspace')


def main():
    for key in KEYS:
        source = ROOT / 'design' / 'qa-stage35' / f'social-{key}-capture.jpg'
        target = ROOT / 'design' / 'assets' / f'stage35-social-{key}.jpg'
        with Image.open(source) as image:
            if image.width < 1200 or image.height < 630:
                raise ValueError('Capture does not contain the complete card: ' + str(source))
            image.crop((0, 0, 1200, 630)).convert('RGB').save(target, quality=94, optimize=True, progressive=True)
        print(f'{target.name}: 1200x630, {target.stat().st_size} bytes')


if __name__ == '__main__':
    main()
