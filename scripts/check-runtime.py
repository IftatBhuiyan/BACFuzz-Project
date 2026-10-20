#!/usr/bin/env python3
"""Check local runtime readiness without starting a target or calling a model."""
import argparse
import importlib.metadata as metadata
import json
import os
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--browser', action='store_true', help='Also start headless Chromium, without opening a page')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
upstream = root / '.upstream/BACFuzz'
passed = failed = 0


def check(name, action):
    global passed, failed
    try:
        detail = action()
    except Exception as error:
        failed += 1
        print(f'FAIL {name}: {error}')
    else:
        passed += 1
        print(f'PASS {name}' + (f': {detail}' if detail else ''))


def versions():
    assert sys.version_info[:2] == (3, 11), 'Use the Python 3.11 project environment'
    revision = subprocess.check_output(['git', '-C', str(upstream), 'rev-parse', 'HEAD'], text=True).strip()
    assert revision == (root / 'upstream.lock').read_text().strip(), 'Upstream pin mismatch'
    lines = [line.strip() for line in (upstream / 'bacfuzz/requirements.txt').read_text().splitlines() if line.strip()]
    for line in lines:
        name, expected = line.split('==')
        actual = metadata.version(name)
        assert actual == expected, f'{name}: expected {expected}, installed {actual}'
    origin = json.loads(metadata.distribution('litellm').read_text('direct_url.json') or '{}')
    assert origin.get('url') == 'https://github.com/BerriAI/litellm.git', 'LiteLLM source URL mismatch'
    assert origin.get('vcs_info', {}).get('commit_id') == '3f96a8c6674ccab8f10a254d7b959e8adbed055d', 'LiteLLM source commit mismatch'
    return f'{len(lines)} exact upstream package pins and LiteLLM source commit'


def config():
    import yaml
    data = yaml.safe_load((root / 'configs/driver-smoke.yaml').read_text())
    assert data['PROJECT_NAME'] == 'CVE_2025_0802', 'Unexpected target'
    assert data['HOMEPAGE_URL'] == 'http://localhost:8088/', 'Unexpected target URL'
    assert data['RUNNING_TIME'] == {'h': 0, 'm': 5}, 'Unexpected campaign duration'
    assert data['USER_ROLES'] == ['Admin', 'LeaveManager', 'Salary', 'BorrowManager', 'Anonymous'], 'Unexpected role order'
    return 'five-minute driver configuration'


def imports():
    # Do not pass provider secrets or arbitrary environment settings to upstream imports.
    env = {key: os.environ[key] for key in ('PATH', 'HOME', 'LANG', 'TMPDIR', 'SYSTEMROOT') if key in os.environ}
    env.update(LITELLM_LOCAL_MODEL_COST_MAP='True', DO_NOT_TRACK='1', PYTHONDONTWRITEBYTECODE='1')
    result = subprocess.run([sys.executable, '-c', 'import fuzzer'], cwd=upstream / 'bacfuzz/fuzzer', env=env,
                            capture_output=True, text=True, timeout=45)
    if result.returncode:
        # Output stays in the private setup log when invoked by setup-python.sh.
        raise RuntimeError(result.stderr.strip() or f'import exit {result.returncode}')
    return 'fuzzer/MainDriver imported; init and main not called'


def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as playwright:
        instance = playwright.chromium.launch(headless=True)
        try:
            return f'Chromium {instance.version}; no page opened'
        finally:
            instance.close()


check('versions and provenance', versions)
check('YAML configuration', config)
check('upstream imports', imports)
if args.browser:
    check('browser startup', browser)
else:
    print('SKIP browser startup (use --browser after installing Chromium)')
print(f'Summary: {passed} passed, {failed} failed, {0 if args.browser else 1} skipped')
print('Target, login, crawl, model calls, checker and SQL validation NOT RUN')
raise SystemExit(1 if failed else 0)
