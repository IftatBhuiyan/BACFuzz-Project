# Environment and reproducibility

## Provenance
Upstream: https://github.com/websecfuzz/BACFuzz.git
Pinned commit: `94470790c0941c7cb628712b81e10e154d97928a` (`upstream.lock`).
We keep the full authors' checkout under ignored `.upstream/BACFuzz` and make no upstream source edits. No root license file was found in the pinned artifact; we have not relicensed or copied its source into our group repository. Existing upstream results are authors' data, not ours.

## Intended execution host
Use a disposable Linux VM, preferably the group's shared SPHERE environment. Host access is not yet established. Python 3.11 is a proposed compatibility baseline for the 2024 dependency pins, not an upstream requirement or a tested runtime. Record Linux image/version, CPU architecture, Python patch version, Docker Engine/Compose versions and browser version on the actual host. Do not treat this Mac's static checks as Linux proof.

The supplied target mounts `/var/run/docker.sock`, shares `shared-tmpfs`, and publishes web 8088 and phpMyAdmin 8801 on all interfaces by default. Taamim must inspect it, confine VM ingress and egress, and document any loopback-port changes before starting it. A Docker container alone is not sufficient host isolation. The target is intentionally vulnerable; use no personal accounts or real data. Keep browser navigation and all tests within the supplied isolated WUT. Do not run the authors' experiment script on a personal Docker host.

## Dependency preparation (inside the isolated Linux VM)
From this repository root, after fetching the pinned checkout:

```sh
python3.11 -m venv .upstream/BACFuzz/bacfuzz/venv
.upstream/BACFuzz/bacfuzz/venv/bin/python -m pip install -r .upstream/BACFuzz/bacfuzz/requirements.txt
.upstream/BACFuzz/bacfuzz/venv/bin/python -m pip check
.upstream/BACFuzz/bacfuzz/venv/bin/python -m playwright install chromium
```

Install OS browser dependencies using the VM administrator's supported package workflow (Playwright's `install-deps chromium` can request elevated package installation). Provide a graphical display or Xvfb: both auto-login and MainDriver launch Chromium with `headless=False`. Do not rerun an unpinned `pip install pytest-playwright`: the supplied requirements already pin it to 0.5.1, Playwright to 1.45.1, PyYAML to 6.0.2 and litellm to 1.44.4. All 62 requirement entries have exact versions; this is not a hash-locked platform-independent environment.

The authors' `setup.sh` calls absent `bacfuzz/get-pip.py`, uses `source venv` rather than `venv/bin/activate`, and only dry-runs browser OS dependency installation. Use the explicit interpreter commands above instead. Dependency resolution, browser installation, `pip check`, Docker build and imports remain unvalidated here.

Save `python --version`, `pip --version`, `pip freeze --all`, `pip check`, Docker/Compose and browser versions plus OS release privately under `.local/<run-id>/`. Review before copying selected evidence into `evidence/`. Never capture `env`, `set -x`, or credentials in terminal transcripts. Docker image tags are not digest pins: Taamim must retain resolved image IDs/digests and target reset procedure for a reproducible run.

DeepSeek is used in MainDriver's parameter filtering too, not just ActiveChecker. Arian must confirm credentials, budget and allowed outbound API traffic before a live crawl. Do not print the key, add it to YAML, or store it in shell history. No provider call was made during setup.
