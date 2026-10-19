"""One-time authoring helper: Pillow is only needed to refresh image variants.

The normal public build stays Python-standard-library only.
"""
from pathlib import Path
import json
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
assets=ROOT/'design/assets'
originals=[
 'stage27-hero-v1.png','stage28-websites-v1.png','stage27-process-cutout.png',
 'stage26-enquiry-cutout-v1.png','mu56-home-desktop.jpg','pilotspace-home-desktop.jpg',
 'akudinov-home-desktop.jpg','prommashina-home-desktop.jpg',
]
mapping={}
for name in originals:
 im=Image.open(assets/name)
 variants=[]
 for width in [480,960]:
  height=round(im.height*width/im.width)
  target=f'{Path(name).stem}-{width}.webp'
  im.resize((width,height),Image.Resampling.LANCZOS).save(assets/target,quality=90,method=6)
  variants.append([f'assets/{target}',width])
 mapping[f'assets/{name}']=variants
for slug in ['integrations','seo','redesign','audit','support']:
 mapping[f'assets/service-{slug}-v1.webp']=[
  [f'assets/service-{slug}-v1-480.webp',480],
  [f'assets/service-{slug}-v1.webp',960],
 ]
(ROOT/'tools/responsive_images.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf8')
manifest_path=ROOT/'backend/docker/static-manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf8'))
for variants in mapping.values():
 for path,_ in variants:
  if path not in manifest:manifest.append(path)
# Original PNG sources remain available locally; release only optimized variants.
manifest=[n for n in manifest if n not in {f'assets/{n}' for n in originals if n.endswith('.png')}]
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf8')
for source,variants in mapping.items():
 if (assets/Path(source).name).exists():
  print(source, (assets/Path(source).name).stat().st_size, '->', [(w,(ROOT/'design'/p).stat().st_size) for p,w in variants])
