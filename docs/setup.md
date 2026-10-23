# Environment and reproducibility

## Provenance
We use [websecfuzz/BACFuzz](https://github.com/websecfuzz/BACFuzz) at commit `94470790c0941c7cb628712b81e10e154d97928a`, recorded in `upstream.lock`. The authors' full checkout stays under ignored `.upstream/BACFuzz`; their existing results are not our experimental data. We do not edit or relicense their source. No root license file was found in the pinned artifact.

## Repeatable dependency setup
Use a dedicated disposable Linux VM for experiments. Python 3.11 is our locally validated baseline; Linux runtime validation is still pending. The setup command also works for local preparation without launching a target.

```sh
bash scripts/fetch-upstream.sh
bash scripts/setup-python.sh
.local/venv/bin/python scripts/check-runtime.py
```

The setup helper needs Git and Python 3.11 (`python3.11` on PATH). To select an existing interpreter, set `BACFUZZ_PYTHON` to its executable path. It creates/reuses `.local/venv`, installs `configs/requirements-recovered.txt`, checks package compatibility, records installed versions, and validates package provenance, YAML, and upstream imports. It uses uv when available and otherwise the environment's pip. The uv route has been executed successfully; the pip fallback and Linux setup have not yet been executed.

Each attempt saves private stage logs and its exit status under `.local/setup/<UTC-time>-<pid>/`. A failed stage stops setup and identifies its log. Failures before an output directory can be created, such as a missing interpreter or upstream checkout, are reported directly. Setup does not deploy an application, log in, collect requests, or call a model. Re-running it preserves the environment and does not reset experiment data. Package installation requires network access.

### Exact-version dependency recovery
The original requirements contain 62 exact version pins. On October 20, PyPI installation failed because `litellm==1.44.4` was unavailable. The recovery manifest includes the unchanged requirements and binds LiteLLM to the official `BerriAI/litellm` v1.44.4 commit `3f96a8c6674ccab8f10a254d7b959e8adbed055d`. All 62 installed versions matched the upstream pins. Source recovery is not proof of byte-identical recovery of the historical PyPI wheel, and these pins do not provide a complete hash-locked environment.

The authors' `setup.sh` calls missing `bacfuzz/get-pip.py`, uses `source venv` instead of an activation-file path, and only dry-runs browser OS dependency installation. Our helper uses explicit interpreter paths and stores its environment outside upstream. It avoids their extra unpinned `pip install pytest-playwright`; requirements already pin pytest-playwright 0.5.1 and Playwright 1.45.1.

## Browser preparation
Install browser binaries separately, then request the browser startup check:

```sh
.local/venv/bin/python -m playwright install chromium
.local/venv/bin/python scripts/check-runtime.py --browser
```

For Linux OS libraries, use the VM administrator's supported package workflow; Playwright's `install-deps chromium` can request elevated package installation. Both auto-login and MainDriver use `headless=False`, so a graphical display or Xvfb is required for the actual crawl. Our browser check starts headless Chromium without opening a page; it does not validate headed/Xvfb operation or login.

## Isolated execution host
SPHERE project `bacfuzz` is approved. Arian `hunter493ncgj` and Tam `hunter493byej` are Active Members. On October 23 we created `reproduction.bacfuzz`, shared gateway `dev.bacfuzz`, and reservation `smoke001` with one Ubuntu `2404` VM named `runner`, requiring at least four cores and 8 GB memory. SPHERE reports successful activation and zero public ingresses. The one-day reservation expires October 24; copy evidence to persistent storage before release. The model is in `configs/sphere-model.py`, saved in SPHERE as revision `a3c9e0ee7d9255661e5681d017fe4661f441c37e`.

Direct Jupyter startup on the VM failed with a 30-second server-response timeout. JupyterLab on the dedicated gateway works. SSH from the gateway reached the dedicated runner. It reports Ubuntu 24.04.4 LTS and x86_64. The account requires a password for sudo; noninteractive sudo failed. Direct root SSH was denied. Actual package/runtime versions and target readiness remain to validate. We have not installed or run the WUT in this reservation yet.

The supplied target mounts `/var/run/docker.sock`, shares `shared-tmpfs`, and publishes web 8088 and phpMyAdmin 8801 on all interfaces by default. Taamim must inspect it, confine VM ingress and egress, and document any loopback-port changes before starting it. A container alone is not sufficient isolation for this artifact. Use only supplied fixture accounts and data inside the disposable VM; keep all tests within the provided WUT. Do not launch the authors' experiment script on a personal Docker host.

Record the Linux image/release, CPU architecture, Python patch version, Docker Engine/Compose versions, installed package snapshot, browser version, resolved target image IDs/digests, and reset procedure on the actual experiment host. Docker image tags alone are not digest pins. `python scripts/preflight.py` inventories host readiness and parses tracked upstream source without imports; it intentionally reports blockers on an unprepared Mac.

DeepSeek is used in MainDriver parameter filtering too. Arian must confirm credentials, budget, and allowed API traffic before collection. Do not print the key, put it in YAML, or capture `env`/`set -x` in transcripts. Raw request/login/SQL evidence and logs belong under ignored `.local/` or the ignored upstream checkout. Review and redact examples before publishing selected evidence.

See [runtime evidence](../evidence/runtime-setup-checks.txt), [progress](environment-progress.md), and [MainDriver protocol](main-driver.md). Local checks are not Linux reproduction, account verification, request collection, or vulnerability validation.
