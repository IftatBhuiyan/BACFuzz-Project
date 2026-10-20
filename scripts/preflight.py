#!/usr/bin/env python3
"""Offline setup inventory. Does not import upstream or expose environment values."""
import ast
import hashlib
import platform
import shutil
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[1]
upstream = root / '.upstream/BACFuzz'
passed = blocked = 0

def check(label, ok, detail=''):
    global passed, blocked
    passed += bool(ok)
    blocked += not ok
    print(f"{'PASS' if ok else 'BLOCKED'} {label} {detail}".rstrip())

print('Platform:', platform.system(), platform.machine())
print('Python:', platform.python_version())
check('Linux experiment host', platform.system() == 'Linux')
check('Python 3.11 baseline (locally validated; Linux pending)', platform.python_version_tuple()[:2] == ('3', '11'))
if (upstream / '.git').exists():
    revision = subprocess.check_output(['git', '-C', str(upstream), 'rev-parse', 'HEAD'], text=True).strip()
    check('Pinned upstream', revision == (root / 'upstream.lock').read_text().strip(), revision)
    clean = not subprocess.check_output(['git', '-C', str(upstream), 'status', '--porcelain'], text=True).strip()
    check('Upstream unchanged', clean)
    req = upstream / 'bacfuzz/requirements.txt'
    print('requirements.txt SHA256:', hashlib.sha256(req.read_bytes()).hexdigest())
    # Inspect tracked artifact source only, excluding generated environments and captures.
    tracked = subprocess.check_output(['git', '-C', str(upstream), 'ls-files', '-z', '--', 'bacfuzz'], text=True)
    sources = [upstream / name for name in tracked.split('\0') if name.endswith('.py')]
    errors = []
    for source in sources:
        try:
            ast.parse(source.read_text(encoding='utf-8-sig'), filename=str(source))
        except (SyntaxError, UnicodeError) as error:
            errors.append(f'{source.relative_to(upstream)}: {error}')
    check(f'Python source parse ({len(sources)} files; no imports)', not errors)
    for error in errors:
        print(error)
else:
    check('Upstream checkout', False, 'Run bash scripts/fetch-upstream.sh')
for tool in ('docker', 'git', 'curl', 'nc', 'timeout', 'xvfb-run'):
    check(f'{tool} on PATH', shutil.which(tool) is not None)
if shutil.which('docker'):
    for args in (['docker', 'version'], ['docker', 'compose', 'version']):
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=15)
            check(' '.join(args), result.returncode == 0)
            # Avoid printing daemon connection details or local context secrets.
        except subprocess.TimeoutExpired:
            check(' '.join(args), False, 'timed out')
print(f'Summary: {passed} passed, {blocked} blocked; live crawl/checker/SQL validation NOT RUN')
raise SystemExit(1 if blocked else 0)
