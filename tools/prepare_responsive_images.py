"""Resize existing approved RGBA art without generating or repainting content.

Run with a Python environment containing Pillow and WebP support.
Original PNGs remain the fallback and are never modified.
"""
from pathlib import Path
from PIL import Image, features

ASSETS = Path(__file__).resolve().parents[1] / 'design' / 'assets'
SOURCES = {
    'stage27-hero-v1': (480, 720, 960),
    'stage28-websites-v1': (480, 720, 960),
    'stage27-process-cutout': (480, 720, 960),
    'stage26-enquiry-cutout-v1': (360, 540, 720),
}


def main():
    if not features.check('webp'):
        raise RuntimeError('Pillow must support WebP')
    for stem, widths in SOURCES.items():
        with Image.open(ASSETS / (stem + '.png')) as original:
            image = original.convert('RGBA')
            for width in widths:
                if width > image.width:
                    raise ValueError('Do not upscale approved art')
                height = round(image.height * width / image.width)
                variant = image.resize((width, height), Image.Resampling.LANCZOS)
                target = ASSETS / f'{stem}-stage34-{width}.webp'
                variant.save(target, 'WEBP', lossless=True, method=6, exact=True)
                with Image.open(target) as check:
                    assert check.size == (width, height)
                    assert check.convert('RGBA').getchannel('A').tobytes() == variant.getchannel('A').tobytes()
                    assert check.convert('RGBA').tobytes() == variant.tobytes()
                print(f'{target.name}: {width}x{height}, {target.stat().st_size} bytes; lossless RGBA verified')


if __name__ == '__main__':
    main()
