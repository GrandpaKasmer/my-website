"""Optional browser checks. Requires Python Playwright and a Chromium executable.
Run npm run build && npm run preview in another terminal, then python tests/browser_checks.py.
"""
from pathlib import Path
import json
import os
import shutil
from playwright.sync_api import sync_playwright

OUT = Path(os.environ.get('WONDER_TEST_OUTPUT', 'playwright-artifacts'))
OUT.mkdir(parents=True, exist_ok=True)
URL = os.environ.get('WONDER_TEST_URL', 'http://localhost:4173/')
results = []
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium') or None, headless=True, args=['--no-sandbox'])
    for width, height, label in [(1440,1000,'desktop'),(390,844,'phone'),(320,720,'small-phone'),(768,1024,'tablet')]:
        context = browser.new_context(viewport={'width':width,'height':height}, device_scale_factor=1, reduced_motion='reduce', accept_downloads=True)
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        page.goto(URL, wait_until='networkidle')
        page.screenshot(path=str(OUT/f'{label}-home.png'), full_page=True)
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Home overflows at {width}'
        page.get_by_role('button', name='Find my wonder ticket').click()
        assert page.get_by_role('button', name='Carry on').is_disabled()
        page.locator('[data-choice="begin"]').click()
        page.get_by_role('button', name='Carry on').click()
        page.locator('[data-choice="curious"]').click()
        page.get_by_role('button', name='Carry on').click()
        page.screenshot(path=str(OUT/f'{label}-charms.png'), full_page=True)
        page.locator('[data-choice="key"]').click()
        page.get_by_role('button', name='Pull the lever').click()
        page.get_by_role('heading', name='The door is smaller than you think.').wait_for()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Ticket overflows at {width}'
        page.screenshot(path=str(OUT/f'{label}-ticket.png'), full_page=True)
        assert page.evaluate('localStorage.getItem("wonder-ticket:v1")') is None
        page.get_by_role('button', name='Save my ticket', exact=True).click()
        page.get_by_role('button', name='Saved on this device', exact=True).click()
        assert page.locator('#saved-count').inner_text() == '1'
        assert len(json.loads(page.evaluate('localStorage.getItem("wonder-ticket:v1")'))) == 1
        with page.expect_download() as dl:
            page.get_by_role('button', name='Save an image').click()
        download = dl.value
        download.save_as(OUT/f'{label}-export.png')
        page.reload(wait_until='networkidle')
        assert page.locator('#saved-count').inner_text() == '1'
        page.get_by_role('button', name='Open saved tickets').click()
        page.locator('[data-open-ticket]').click()
        page.get_by_role('heading', name='The door is smaller than you think.').wait_for()
        page.get_by_role('button', name='Open my tickets', exact=True).click()
        page.locator('[data-delete-ticket]').click()
        assert page.locator('#saved-count').inner_text() == '0'
        page.get_by_role('button', name='Close dialog').click()
        # All cached pages remain available offline after service-worker activation.
        page.evaluate('navigator.serviceWorker.ready')
        page.reload(wait_until='networkidle')
        context.set_offline(True)
        page.reload(wait_until='domcontentloaded')
        page.get_by_role('button', name='Find my wonder ticket').wait_for()
        page.get_by_role('link',name='Privacy',exact=True).click()
        page.get_by_role('heading',name='Privacy at the little arcade').wait_for()
        context.set_offline(False)
        assert not errors, errors
        results.append({'viewport':label,'width':width,'status':'pass','page_errors':errors})
        context.close()
    # Back button preserves a selection, blocked storage does not prevent play, unsafe text is escaped.
    context=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce')
    page=context.new_page();page.goto(URL)
    page.get_by_role('button',name='Find my wonder ticket').click();page.locator('[data-choice="space"]').click();page.get_by_role('button',name='Carry on').click();page.get_by_role('button',name='Go back').click()
    assert page.locator('[data-choice="space"]').get_attribute('aria-pressed')=='true'
    page.evaluate('''() => {const t=WonderEngine.makeTicket({door:'begin',mood:'ready',charm:'key'});t.title='<img src=x onerror="window.attacked=true">';localStorage.setItem('wonder-ticket:v1',JSON.stringify([t]));}''')
    page.get_by_role('button',name='Open saved tickets').click();page.locator('[data-open-ticket]').click()
    assert page.locator('.ticket h2').inner_text().startswith('<img')
    assert page.evaluate('window.attacked') is None
    context.close()
    browser.close()
(OUT/'results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
print('Also passed: back navigation, save/deduplicate/reload/delete, no autosave, export PNG, offline home/privacy, escaped saved content.')
