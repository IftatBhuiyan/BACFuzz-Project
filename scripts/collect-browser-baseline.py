#!/usr/bin/env python3
"""Bounded normal-browser baseline for the provided isolated CVE_2025_0802 WUT.

This is not MainDriver and does not import the fuzzer or call an LLM.
Private HAR/login data must not be published.
"""
import json
import os
from pathlib import Path
import runpy
import tempfile
from types import SimpleNamespace
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path.home() / 'BACFuzz-Project'
FUZZER = ROOT / '.upstream/BACFuzz/bacfuzz/fuzzer'
ROLES = ['Admin', 'LeaveManager', 'Salary', 'BorrowManager', 'Anonymous']
ORIGIN = ('http', 'localhost', 8088)

def permitted(url):
    u = urlsplit(url)
    return (u.scheme, u.hostname, u.port) == ORIGIN

def main():
    os.umask(0o077)
    parent = ROOT / '.local/baseline'
    parent.mkdir(parents=True, exist_ok=True)
    out = Path(tempfile.mkdtemp(prefix='normal-browser-', dir=parent))
    os.chdir(FUZZER)
    fixture = runpy.run_path('../auto_login/CVE_2025_0802.py')
    config = SimpleNamespace(homepages={r: 'http://localhost:8088/' for r in ROLES})
    fixture['main'](config)
    result = {'kind':'scripted normal-browser baseline', 'main_driver':False,
              'model_calls':False, 'roles':{}, 'vulnerability_validated':False}
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        try:
            for role in ROLES:
                state = Path('../login_state/CVE_2025_0802') / f'{role}.json'
                ctx = browser.new_context(storage_state=str(state),
                    record_har_path=str(out / f'{role}.har'),record_har_content='omit')
                counts = {'allowed_requests':0,'blocked_requests':0}
                def route(req_route):
                    if permitted(req_route.request.url):
                        counts['allowed_requests'] += 1
                        req_route.continue_()
                    else:
                        counts['blocked_requests'] += 1
                        req_route.abort()
                ctx.route('**/*', route)
                try:
                    page = ctx.new_page()
                    response = page.goto(config.homepages[role], wait_until='networkidle', timeout=30000)
                    page.wait_for_timeout(1500)
                    page.screenshot(path=str(out / f'{role}.png'), full_page=True)
                    password_fields = page.locator('input[type="password"]').count()
                    dashboard = '/admin' in urlsplit(page.url).path and 'dashboard' in page.inner_text('body').lower()
                    observed = (password_fields > 0) if role == 'Anonymous' else (password_fields == 0 and dashboard)
                    result['roles'][role] = {**counts,'status':response.status if response else None,
                        'expected_login_page_or_dashboard_observed':observed}
                    if not permitted(page.url):
                        raise RuntimeError('Navigation left the isolated target origin')
                    if not observed:
                        raise RuntimeError('Expected baseline page was not observed')
                finally:
                    ctx.close()
                (out / 'summary.json').write_text(json.dumps(result, indent=2))
        finally:
            browser.close()
    (parent / 'latest-path.txt').write_text(str(out))
    print(json.dumps(result, indent=2))
    print('Baseline only: permission policy, MainDriver and vulnerability checks remain separate.')

if __name__ == '__main__':
    main()
