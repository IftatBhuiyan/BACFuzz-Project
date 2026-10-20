# Environment progress — October 20, 2026

We created a separate SPHERE project, `bacfuzz`, under the `hunter493` class organization. Its project-management and MergeFS status both showed Success. SPHERE assigned Public metadata visibility by default. We uploaded only the project description; no credentials, captures or logs were uploaded. Only the creator is currently listed as a project member; Arian and Taamim have not been added to SPHERE.

We did not modify the Snort, POSIX, Lab 5 or existing XDC environments. We submitted a proposed `reproduction` experiment and a dedicated personal `dev` XDC under `bacfuzz`, but could not verify creation of either. The experiment was absent after refreshing its list. The XDC form stayed open after submission with no visible error, and the XDC list showed only pre-existing containers. We did not create a reservation, activate a node, or start the target. Treat these as unsuccessful provisioning attempts, not completed resources. Browser console error/warning inspection returned no entries; we do not know the backend cause.

## Local dependency experiment

We created an ignored Python 3.11.15 environment at `.local/dependency-check-venv`. Full installation of the pinned upstream requirements failed twice, including an explicit PyPI attempt:

```text
No solution found when resolving dependencies:
Because there is no version of litellm==1.44.4 and you require
litellm==1.44.4, we can conclude that your requirements are unsatisfiable.
```

A live request to the PyPI 1.44.4 metadata endpoint returned HTTP 404. A cached web result still described that release, so we retain the live resolver failure as evidence and do not infer that the authors never published it. We have not silently changed the dependency version or declared the runtime installed.

We separately installed the pinned PyYAML 6.0.2 and loaded `configs/driver-smoke.yaml`. Assertions passed for project `CVE_2025_0802`, five-minute budget, and exact five-role order. This checks configuration parsing on macOS; it does not establish a functioning Linux experiment.

## Evidence retained privately

`.local/dependency-install.log`, `.local/dependency-install-pypi.log`, `.local/yaml-install.log`, and `.local/sphere-setup/dependency-evidence.txt` retain terminal results. `.local/sphere-setup/project-created.png` records project creation; `xdc-submit-unchanged.png` records the stalled form. Browser state snapshots and session notes are in the same directory. These raw artifacts remain ignored and are not published with the initial PR.

Next gates: resolve SPHERE provisioning, obtain a dedicated isolated Linux node, recover or deliberately replace the unavailable dependency with documented provenance and validation, then prepare the target/accounts and confirm approved API access before collection. No HTTP requests or vulnerability results have been collected.

## Follow-up: diagnosed SPHERE gate and recovered dependencies

We inspected the Projects table rather than relying on the project task-status panel. The separate `bacfuzz` project is **Pending**; the **Active** label in its details referred to the Hunter organization. Our earlier task-success observation did not establish project approval. When we attempted to add Tam (`hunter493byej`) as an Active Member, the server returned HTTP 403 with `{"code":7,"message":"Project is not active","details":[]}`. We saved the sanitized response in `.local/sphere-setup/membership-error.json`. Tam has **not** been added. We reviewed the owner project actions and update form: there was no project activation control. The project needs activation by a SPHERE/class administrator before member access and provisioning can proceed. We have not bypassed this gate or reused other labs.

We checked prior Lab 5 chats for Arian Berisha's ID, then Iftat supplied Arian's prior terminal screenshot showing `hunter493ncgj@server`. We will use `hunter493ncgj` for Arian and `hunter493byej` for Tam. Neither has been added: the BACFuzz project's Pending state blocks membership changes.

For LiteLLM, the official `BerriAI/litellm` repository still exposes tag `v1.44.4` at commit `3f96a8c6674ccab8f10a254d7b959e8adbed055d`. We added `configs/requirements-recovered.txt`, which includes all original requirements and binds LiteLLM to that exact official source commit. This preserves the package version rather than upgrading it; it is a source-install variation, not proof of byte-identical recovery of the old PyPI wheel. Upstream files remain unchanged.

Installation using the recovery manifest succeeded in the local Python 3.11.15 environment. We verified all **62 installed package versions** against the upstream pins, and `uv pip check` passed. Fuzzer/MainDriver imports passed without calling initialization or starting a campaign; the child process received no provider API credentials. Playwright 1.45.1 installed and started headless Chromium 127.0.6533.17. We did not navigate to a target or make model calls. These are macOS runtime-preparation checks, not Linux reproduction or request-collection evidence.

Reviewed results: `evidence/runtime-setup-checks.txt`. Private outputs: `.local/dependency-source-recovery.log`, `.local/dependency-recovered-manifest.log`, `.local/dependency-check.log`, `.local/pinned-version-check.log`, `.local/runtime-import.log`, `.local/browser-install.log`, `.local/browser-startup-check.log`, and `.local/installed-dependencies.txt`.

Remaining blockers are SPHERE project activation, adding both confirmed teammate accounts, dedicated Linux resource provisioning, isolated target/account setup and approved DeepSeek access. No experimental HTTP requests have been collected yet. The recovery configuration, reviewed evidence and notes are included in PR #1; raw logs and screenshots remain private.
