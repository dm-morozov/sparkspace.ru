"""Browser acceptance for the static release. Requires Playwright and Chrome.

Run after build_public.py: python tools/check_browser.py --output .qa/browser
No external contact links are activated and no messages are sent.
"""
from pathlib import Path
import argparse,json,threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright

root=Path(__file__).resolve().parents[1]
args=argparse.ArgumentParser()
args.add_argument('--output',default='.qa/browser')
args.add_argument('--executable')
args=args.parse_args()
output=root/args.output;output.mkdir(parents=True,exist_ok=True)
class QuietHandler(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(QuietHandler,directory=str(root/'dist/public')))
threading.Thread(target=server.serve_forever,daemon=True).start()
base=f'http://127.0.0.1:{server.server_port}'
services=['integrations','seo','redesign','audit','support']
results=[];errors=[]
with sync_playwright() as pw:
 launch={'executable_path':args.executable} if args.executable else {'channel':'chrome'}
 browser=pw.chromium.launch(headless=True,**launch)
 context=browser.new_context(permissions=['clipboard-read','clipboard-write'])
 page=context.new_page()
 page.on('pageerror',lambda error:errors.append(str(error)))
 for slug in services+['contacts']:
  for width in [1440,1180,390,320]:
   page.set_viewport_size({'width':width,'height':900})
   page.goto(f'{base}/{slug}.html'+('?service=integrations' if slug=='contacts' else ''))
   page.evaluate('async()=>{document.documentElement.style.scrollBehavior="auto";for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,70))}scrollTo(0,0)}')
   page.wait_for_timeout(700)
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(slug,width,'horizontal overflow')
   assert page.locator('img').evaluate_all('(imgs)=>imgs.every(i=>i.complete&&i.naturalWidth>0)'),(slug,width,'image failed')
   assert page.locator('h1').count()==1
   assert page.locator('form').count()==0
   page.screenshot(path=str(output/f'{slug}-{width}.png'),full_page=True)
   results.append({'page':slug,'width':width,'overflow':False,'allImagesLoaded':True})
 # Repeated keyboard navigation and menu closure, including 1180px breakpoint.
 for width in [1440,1180,390,320]:
  page.set_viewport_size({'width':width,'height':900})
  page.goto(f'{base}/integrations.html')
  for repeat in range(2):
   if width<=1180:
    button=page.locator('.menu-button');button.focus();page.keyboard.press('Enter')
    assert button.get_attribute('aria-expanded')=='true'
   summary=page.locator('.mega summary');summary.focus();page.keyboard.press('Enter')
   assert page.locator('.mega').get_attribute('open') is not None
   scrolls=page.locator('#navigation,.mega-panel').evaluate_all('(xs)=>xs.filter(x=>getComputedStyle(x).overflowY==="auto"&&x.scrollHeight>x.clientHeight).length')
   assert scrolls<=1,(width,'nested scrolling')
   broken_words=page.locator('.menu-group>a>span:not(.menu-arrow)').evaluate_all('''(labels)=>labels.flatMap(label=>Array.from(label.childNodes).filter(n=>n.nodeType===3).flatMap(n=>Array.from(n.textContent.matchAll(/\\S+/g)).filter(m=>{const r=document.createRange();r.setStart(n,m.index);r.setEnd(n,m.index+m[0].length);return r.getClientRects().length>1}).map(m=>m[0])))''')
   assert not broken_words,(width,'menu words split',broken_words)
   page.wait_for_timeout(700)
   page.screenshot(path=str(output/f'menu-{width}.png'))
   page.keyboard.press('Escape')
   assert page.locator('.mega').get_attribute('open') is None
   assert summary.evaluate('(x)=>x===document.activeElement')
   if width<=1180:
    page.keyboard.press('Escape')
    assert button.get_attribute('aria-expanded')=='false'
  for _ in range(16):
   page.keyboard.press('Tab')
   assert page.evaluate('document.activeElement===document.body||Boolean(document.activeElement.getClientRects().length)'),(width,'hidden keyboard focus')
 # FAQ toggles support repeated activation.
 page.goto(f'{base}/integrations.html')
 question=page.locator('.website-faq summary').first
 question.focus();page.keyboard.press('Enter')
 assert question.locator('..').get_attribute('open') is not None
 page.keyboard.press('Enter');assert question.locator('..').get_attribute('open') is None
 # Each service CTA reaches the correct local contact context.
 for slug in services:
  page.goto(f'{base}/{slug}.html')
  page.locator('.service29-hero .btn').click()
  assert f'service={slug}' in page.url
  starter=page.locator('#message-starter')
  assert 'Здравствуйте!' in starter.input_value()
  assert 'body=' in page.locator('.public-contact-list a[href^="mailto:"]').get_attribute('href')
  starter.fill('Тестовый локальный черновик')
  for _ in range(2):page.locator('[data-contact-context] button').click()
  assert page.evaluate('navigator.clipboard.readText()')=='Тестовый локальный черновик'
 page.goto(f'{base}/contacts.html?service=%3Cscript%3E')
 assert not page.locator('[data-contact-context]').is_visible()
 assert '?' not in page.locator('.public-contact-list a[href^="mailto:"]').get_attribute('href')
 # Reduced motion stays visible and does not activate scroll reveals.
 page.emulate_media(reduced_motion='reduce')
 for slug in services:
  page.goto(f'{base}/{slug}.html')
  assert page.locator('.app-will-reveal').count()==0
  assert page.locator('[data-app-reveal]').evaluate_all('(xs)=>xs.every(x=>getComputedStyle(x).opacity==="1")')
 # Main and existing specialized pages still load at wide and narrow sizes.
 for slug in ['index','websites','applications','automation']:
  for width in [1440,390,320]:
   page.set_viewport_size({'width':width,'height':900});page.goto(f'{base}/{slug}.html')
   assert not page.evaluate('document.documentElement.scrollWidth>innerWidth'),(slug,width)
 assert not errors,errors
 browser.close()
server.shutdown()
report={'screens':results,'javascriptErrors':errors,'menuKeyboardRepeated':True,'faqRepeated':True,'contactContextAndClipboard':True,'unknownServiceSafe':True,'reducedMotion':True,'existingPagesResponsive':True}
(output/'report.json').write_text(json.dumps(report,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=True))
