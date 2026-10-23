# BACFuzz semester reproduction
Hunter College CSCI 493 · Presentation October 28, 2026

We reproduce selected experiments from [websecfuzz/BACFuzz](https://github.com/websecfuzz/BACFuzz), “BACFuzz: Exposing the Silence on Broken Access Control Vulnerabilities in Web Applications.” This repository contains our setup, configuration, and evidence; upstream authors retain credit for their artifact. We have not reproduced a vulnerability yet.

- [Setup and versions](docs/setup.md)
- [MainDriver collection and handoff](docs/main-driver.md), including offline capture inventory
- [Completed work and blockers](docs/progress.md)
- [First real browser baseline and deployment changes](docs/browser-baseline.md)
- `configs/driver-smoke.yaml`: proposed five-minute collection configuration
- `evidence/`: reviewed, non-sensitive checks; `.local/`: ignored raw run evidence

Start with `bash scripts/fetch-upstream.sh`, then `bash scripts/setup-python.sh` using Python 3.11. The setup helper installs the recovered exact-version dependencies and saves private logs. Use `.local/venv/bin/python scripts/check-runtime.py` for package/config/import checks, or add `--browser` after installing Chromium. See setup notes for Linux browser libraries and isolation.

`python3 scripts/preflight.py` is an offline host inventory. It does not start applications or contact an API. Local dependency/import/browser checks have passed; SPHERE project activation, Linux deployment and experimental collection remain blocked.

Iftat owns shared setup, MainDriver collection, configuration and logs. Arian owns ActiveChecker, DeepSeek and mutation. Taamim owns the isolated Docker target, accounts and SQL validation. One owner runs each target instance at a time.

Do not commit raw HTTP requests, login states, cookies, authorization headers, API keys, database dumps or unreviewed logs. Keep raw evidence in `.local/` or the ignored upstream checkout and share privately. Gitignore is a safeguard, not a secret scanner. Do not use `git add -f` for these paths.
