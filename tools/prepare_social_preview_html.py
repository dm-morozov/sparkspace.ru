"""Create native HTML share-card layouts for browser capture, not generated UI."""
from pathlib import Path
from html import escape
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'design'))
from stage35_social import SOCIAL_CARDS

CSS = '''
body{margin:0;background:#fff;font-family:'Golos Text','Segoe UI',sans-serif}
.card35{width:1200px;height:630px;overflow:hidden;position:relative;background:#f8f9fd;color:#182039;isolation:isolate}
.card35:after{content:"";position:absolute;right:-100px;top:-80px;width:700px;height:700px;background:radial-gradient(ellipse,#ece8ff99,transparent 68%);z-index:-1}
.brand35{position:absolute;left:60px;top:44px;display:flex;align-items:center;gap:13px;font-size:32px;letter-spacing:-1.5px;font-weight:700}
.brand35 img{width:32px;height:47px;object-fit:contain}
.kind35{position:absolute;left:60px;top:153px;font-size:13px;font-weight:600;letter-spacing:1.8px;color:#5e43ed;text-transform:uppercase}
.copy35{position:absolute;left:60px;top:207px;width:545px;z-index:2}
.copy35 h1{font-size:62px;font-weight:600;line-height:1.08;letter-spacing:-2.8px;margin:0}
.copy35 p{font-size:23px;line-height:1.5;color:#687085;margin:26px 0 0;max-width:485px;letter-spacing:-.25px}
.art35{position:absolute;left:610px;top:159px;width:590px;height:393px;object-fit:contain}
.case35 .copy35{top:228px;width:510px}.case35 .copy35 h1{font-size:70px}
.case35 .copy35 p{font-size:23px;max-width:450px}
.screen35{position:absolute;left:628px;top:174px;width:512px;margin:0;border:1px solid #deddeb;border-radius:16px;overflow:hidden;background:white;box-shadow:0 24px 55px #25204d0c}
.screen35-bar{height:34px;background:#f3f2fa;display:flex;align-items:center;padding:0 16px;font-size:12px;color:#687085;gap:6px}
.screen35-bar i{width:5px;height:5px;background:#c4bfdc;border-radius:50%;display:block}.screen35-bar span{margin-left:12px}
.screen35 img{display:block;width:100%;height:auto}
.caption35{position:absolute;left:628px;top:515px;width:512px;text-align:center;font-size:12px;color:#737b8d}
.footer35{position:absolute;left:60px;right:60px;bottom:43px;border-top:1px solid #e3e3ef;padding-top:20px;display:flex;align-items:center;justify-content:space-between}
.footer35 strong{font-size:18px;color:#5e43ed;font-weight:500}.footer35 span{font-size:10px;letter-spacing:1.3px;color:#737b8d}
'''


def main():
    folder = ROOT / 'design' / 'qa-stage35'
    folder.mkdir(exist_ok=True)
    for key, card in SOCIAL_CARDS.items():
        is_case = bool(card['caption'])
        art = (f'<figure class="screen35"><div class="screen35-bar"><i></i><i></i><i></i>'
               f'<span>{"mu56.ru" if key == "mu56" else "pilotspace.ru"}</span></div>'
               f'<img src="{escape(card["art"], quote=True)}" alt=""></figure>'
               f'<div class="caption35">{escape(card["caption"])}</div>') if is_case else (
               f'<img class="art35" src="{escape(card["art"], quote=True)}" alt="">')
        kind = 'Реальный проект' if is_case else 'Цифровые решения для бизнеса'
        html = (f'<!doctype html><html lang="ru"><head><meta charset="utf-8">'
                f'<meta name="robots" content="noindex,nofollow"><base href="../">'
                f'<link rel="stylesheet" href="style.css"><style>{CSS}</style></head><body>'
                f'<article class="card35 {"case35" if is_case else ""}" aria-label="{escape(card["alt"], quote=True)}">'
                '<div class="brand35"><img src="assets/sparkspace-mark.png" alt="">SparkSpace</div>'
                f'<div class="kind35">{kind}</div><div class="copy35"><h1>{escape(card["title"])}</h1>'
                f'<p>{escape(card["subtitle"])}</p></div>{art}'
                '<div class="footer35"><strong>sparkspace.ru</strong><span>РАЗРАБОТКА · ПРОДВИЖЕНИЕ · АВТОМАТИЗАЦИЯ</span></div>'
                '</article></body></html>')
        (folder / f'social-{key}.html').write_text(html, encoding='utf-8')
    print('Prepared six 1200x630 native HTML share-card layouts')


if __name__ == '__main__':
    main()
