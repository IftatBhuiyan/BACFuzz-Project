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
- Created dedicated `reproduction` experiment, shared `dev` gateway, compiled single-host model and one-day `smoke001` reservation. SPHERE reports successful activation of one VM, with zero public ingresses. Gateway JupyterLab and SSH work. The earlier direct-node Jupyter timeout remains in our error record.

- Added a read-only capture inventory for the five CVE_2025_0802 roles. Actual upstream serializer compatibility and five error/privacy cases passed with synthetic fixtures (6 passed, 0 failed). This prepares the checker handoff; it does not count as live collection.

## Latest experimental progress — October 23

The corrected Linux setup passed all four runtime checks and a headed Chromium/Xvfb check. We built and started the supplied application/database containers inside the dedicated VM, preserving an internal Docker network and accessing the target through a loopback-only relay. We retained and resolved the registry IPv6, seed-file readability and inactive port-mapping problems. See [deployment and first baseline](browser-baseline.md).

Our separate Playwright landing-page baseline completed with exit 0 across four fixture accounts and Anonymous. It saved **135 local HTTP requests**, including assets: 132 HTTP 200s and three HTTP 403s. Eight external-resource attempts were blocked, producing 143 total HAR entries. Expected dashboard/login-page heuristics passed in all five contexts. This establishes an initial normal-browser baseline, not MainDriver output, full role-policy validation, broad coverage or a reproduced flaw.

## Remaining work for Iftat
1. Review the baseline with Tam and establish the intended permissions before interpreting the observed responses.
2. Integrate Arian's approved DeepSeek access/budget into the full MainDriver path. No provider call was made in our baseline.
3. Execute the configured driver smoke campaign, inspect its native YAML/dictionary outputs and preserve complete run metadata. HAR files are not a validated ActiveChecker replay corpus.
4. Prepare the full checker handoff to Arian, then incorporate results and limitations into our own slides/report and rehearse our roughly five-minute portion.
5. Preserve private evidence before the runner reservation expires October 24. The first run bundle is backed up in the BACFuzz project's persistent shared XDC storage, readable by its three members and not world-readable.

Arian owns DeepSeek, mutation and ActiveChecker. Tam owns target-permission and SQL validation. We have not run MainDriver/ActiveChecker or reproduced a vulnerability. Our Google Slides progress slide and three-page study guide reflect the baseline separately from those remaining stages.

## Evidence
See [setup validation](../evidence/repository-setup-checks.txt), [runtime preparation](../evidence/runtime-setup-checks.txt), and [environment progress and errors](environment-progress.md). Original offline outputs remain in `evidence/initial-checks.txt`; subsequent raw logs, screenshots, dependency snapshots and SPHERE errors remain privately under ignored `.local/`.

The inventory tool and source observations follow merged PR #1. The October 23 follow-up records their synthetic evidence and the dedicated SPHERE provisioning, without captured authentication material.
