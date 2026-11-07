"""In-memory rendering checks for restricted build sandboxes.
These do NOT validate HTTP, actual persistent storage, service workers, Safari, or native iOS.
"""
from pathlib import Path
import json
import shutil
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'playwright-artifacts'; OUT.mkdir(exist_ok=True)
html=(ROOT/'dist/index.html').read_text()
results=[]
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=shutil.which('chromium') or None,headless=True,args=['--no-sandbox'])
    for width,height,label in [(1440,1000,'desktop'),(390,844,'phone'),(320,720,'small-phone'),(768,1024,'tablet')]:
        context=browser.new_context(viewport={'width':width,'height':height},reduced_motion='reduce')
        page=context.new_page(); errors=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.evaluate('''() => {const values={};Object.defineProperty(window,'localStorage',{value:{getItem:k=>values[k]??null,setItem:(k,v)=>{values[k]=v;},removeItem:k=>{delete values[k];}}});window.exportedImages=[];HTMLAnchorElement.prototype.click=function(){if(this.download)window.exportedImages.push(this.href);};}''')
        page.set_content(html,wait_until='load')
        page.screenshot(path=str(OUT/f'{label}-home.png'),full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Home overflow {width}'
        page.get_by_role('button',name='Find my wonder ticket').click()
        assert page.get_by_role('button',name='Carry on').is_disabled()
        page.locator('[data-choice="begin"]').click();page.get_by_role('button',name='Carry on').click()
        page.locator('[data-choice="curious"]').click();page.get_by_role('button',name='Carry on').click()
        page.screenshot(path=str(OUT/f'{label}-charms.png'),full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Charms overflow {width}'
        page.locator('[data-choice="key"]').click();page.get_by_role('button',name='Pull the lever').click()
        page.get_by_role('heading',name='The door is smaller than you think.').wait_for()
        page.screenshot(path=str(OUT/f'{label}-ticket.png'),full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'),f'Ticket overflow {width}'
        assert page.evaluate('localStorage.getItem("wonder-ticket:v1")') is None
        page.get_by_role('button',name='Save my ticket',exact=True).click()
        page.get_by_role('button',name='Saved on this device',exact=True).click()
        assert page.locator('#saved-count').inner_text()=='1'
        page.get_by_role('button',name='Save an image').click()
        data=page.evaluate('window.exportedImages[0]')
        assert data.startswith('data:image/png;base64,')
        import base64
        (OUT/f'{label}-export.png').write_bytes(base64.b64decode(data.split(',',1)[1]))
        page.get_by_role('button',name='Open my tickets',exact=True).click()
        page.locator('[data-open-ticket]').click()
        page.get_by_role('heading',name='The door is smaller than you think.').wait_for()
        page.get_by_role('button',name='Open my tickets',exact=True).click();page.locator('[data-delete-ticket]').click()
        assert page.locator('#saved-count').inner_text()=='0'
        page.get_by_role('button',name='Close dialog').click()
        page.get_by_role('button',name='Copy the words',exact=True).click()
        page.locator('#copy-text').wait_for()
        assert 'not a prediction' in page.locator('#copy-text').input_value()
        page.get_by_role('button',name='Close dialog').click()
        page.get_by_role('button',name='Visit another door').click();page.locator('[data-choice="space"]').click()
        page.get_by_role('button',name='Carry on').click();page.get_by_role('button',name='Go back').click()
        assert page.locator('[data-choice="space"]').get_attribute('aria-pressed')=='true'
        page.evaluate('''() => {const t=WonderEngine.makeTicket({door:'begin',mood:'ready',charm:'key'});t.title='<img src=x onerror="window.attacked=true">';localStorage.setItem('wonder-ticket:v1',JSON.stringify([t]));}''')
        page.get_by_role('button',name='Open saved tickets').click();page.locator('[data-open-ticket]').click()
        assert page.locator('.ticket h2').inner_text().startswith('<img')
        assert page.evaluate('window.attacked') is None
        assert not errors,errors
        results.append({'viewport':label,'width':width,'status':'pass','mode':'in-memory document + test storage adapter','page_errors':errors})
        context.close()
    browser.close()
(OUT/'sandbox-results.json').write_text(json.dumps({'results':results,'not_tested':['real HTTP hosting','service worker and offline reload','actual browser persistence','Safari','native iOS compilation, signing and device behavior']},indent=2))
print(json.dumps(results,indent=2))
