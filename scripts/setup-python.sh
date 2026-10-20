#!/usr/bin/env bash
# Install dependencies only. Does not launch the WUT, crawl, or call a model.
set -euo pipefail
umask 077
cd "$(dirname "$0")/.."
python_cmd=${BACFUZZ_PYTHON:-python3.11}
upstream=.upstream/BACFuzz
[[ -d "$upstream/.git" ]] || { echo 'Fetch upstream first: bash scripts/fetch-upstream.sh'; exit 1; }
[[ "$(git -C "$upstream" rev-parse HEAD)" == "$(cat upstream.lock)" ]] || { echo 'Upstream revision does not match upstream.lock'; exit 1; }
"$python_cmd" -c 'import sys; assert sys.version_info[:2] == (3, 11), "Python 3.11 required"'
log_dir=".local/setup/$(date -u +%Y%m%dT%H%M%SZ)-$$"
mkdir -p "$log_dir"
printf 'Setup logs (private): %s\n' "$log_dir"
trap 'result=$?; printf "%s\n" "$result" > "$log_dir/exit-status.txt"' EXIT
stage() {
  local label=$1
  shift
  echo "Running $label"
  if "$@" > "$log_dir/$label.log" 2>&1; then
    printf 'PASS %s\n' "$label"
  else
    local result=$?
    printf 'FAIL %s (exit %s); inspect the private log.\n' "$label" "$result"
    return "$result"
  fi
}
if [[ ! -e .local/venv ]]; then
  stage create-venv "$python_cmd" -m venv .local/venv
fi
stage python-version .local/venv/bin/python -c 'import sys; print(sys.version); assert sys.version_info[:2] == (3, 11)'
if command -v uv >/dev/null 2>&1; then
  stage installer-version uv --version
  stage install uv pip install --python .local/venv/bin/python -r configs/requirements-recovered.txt
  stage compatibility uv pip check --python .local/venv/bin/python
  stage installed-versions uv pip freeze --python .local/venv/bin/python
else
  stage installer-version .local/venv/bin/python -m pip --version
  stage install .local/venv/bin/python -m pip install -r configs/requirements-recovered.txt
  stage compatibility .local/venv/bin/python -m pip check
  stage installed-versions .local/venv/bin/python -m pip freeze --all
fi
stage runtime-check .local/venv/bin/python scripts/check-runtime.py
printf 'Dependency setup complete. Browser installation is separate; see docs/setup.md.\n'
