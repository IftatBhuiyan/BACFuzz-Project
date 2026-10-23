# Progress — October 23, 2026

We prepared Iftat's shared setup and MainDriver portion without changing the upstream research source. [PR #1](https://github.com/IftatBhuiyan/BACFuzz-Project/pull/1) contains the setup snapshot, dependency recovery, runtime tooling, validation evidence and remaining blockers.

## Completed
- Pinned upstream artifact and traced auto-login, role configuration, request storage and checker handoff.
- Created a five-minute driver configuration and validated its YAML, target, time budget and role order.
- Recovered unavailable LiteLLM 1.44.4 from its exact official source commit; verified all 62 upstream package versions and package compatibility.
- Added repeatable dependency setup with private stage logs and installed-version evidence; fresh and repeated setup both passed.
- Added runtime checks: versions/provenance, configuration, imports and headless browser startup all passed locally (4 passed, 0 failed, 0 skipped with `--browser`). These are preparation checks, not experimental results.
- Fixed preflight to inspect tracked source only. A temporary generated-file regression probe passed; all 52 upstream Python sources parse. Current Python 3.11 host inventory has 7 passes and 4 blockers.
- Created and obtained approval for the separate SPHERE `bacfuzz` project. Both teammates are Active Members.
- Created dedicated `reproduction` experiment, shared `dev` gateway, compiled single-host model and one-day `smoke001` reservation. SPHERE reports successful activation of one VM, with zero public ingresses. Gateway JupyterLab works. Direct node Jupyter failed with a 30-second response timeout, saved for the report.

- Added a read-only capture inventory for the five CVE_2025_0802 roles. Actual upstream serializer compatibility and five error/privacy cases passed with synthetic fixtures (6 passed, 0 failed). This prepares the checker handoff; it does not count as live collection.

## Remaining work for Iftat
1. Finish administrator access on runner. Gateway SSH works and verified Ubuntu 24.04.4 LTS / x86_64, but sudo requires a password and direct root SSH is denied. Direct node Jupyter also timed out. First setup attempt hit an unwritable /project path before package installation; use a dedicated home-directory path on the VM.
2. Run our dependency setup and headed/Xvfb checks on Linux. The recorded four-pass result is local macOS preparation.
3. Integrate Tam's isolated WUT and verified fixture accounts. Preserve our own loopback binding and fresh-run logging requirements.
4. Collect a bounded request corpus and check per-role completeness, login context and selected request behavior. MainDriver's DeepSeek dependency requires Arian's approved provider setup. A manual browser baseline is a distinct milestone.
5. Save run commands, timestamps, exit status, configuration hashes and private request artifacts. Hand the collection/configuration to Arian and record limitations.
6. Update our own slides and report with actual evidence, then rehearse our five-minute portion. Google Slides 1–6 were updated October 23; partners' sections remain theirs to update.

Arian owns DeepSeek, mutation and ActiveChecker. Tam owns target/account and SQL validation evidence. We have not completed a live collection, checker campaign or reproduced vulnerability. No result is inferred from infrastructure success.

## Evidence
See [setup validation](../evidence/repository-setup-checks.txt), [runtime preparation](../evidence/runtime-setup-checks.txt), and [environment progress and errors](environment-progress.md). Original offline outputs remain in `evidence/initial-checks.txt`; subsequent raw logs, screenshots, dependency snapshots and SPHERE errors remain privately under ignored `.local/`.

The inventory tool and source observations follow merged PR #1. The October 23 follow-up records their synthetic evidence and the dedicated SPHERE provisioning, without captured authentication material.
