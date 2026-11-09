# BACFuzz: environment restoration and first native MainDriver collection

**Course:** Hunter College CSCI 493 — Introduction to Computer Security  
**Work date:** November 9, 2026  
**Group:** Iftat Bhuiyan, Arian Berisha and Taamim Naamid  
**Work area:** Iftat's environment preparation, configuration, request collection and evidence preservation

## 1. Purpose and outcome

We restored our dedicated BACFuzz environment after the earlier SPHERE reservation expired, then completed our first native MainDriver-only collection against the authors' supplied `CVE_2025_0802` application. The campaign exited with status **0**. Our read-only inventory accepted **310 role-separated captures**, found the shared parameter dictionary and reported a structurally complete collection.

This is progress beyond the October browser baseline. The October experiment recorded normal browser HAR traffic; this run executed BACFuzz's own MainDriver and generated its native YAML corpus. The two counts measure different collection procedures and must not be presented as a direct improvement percentage or added together.

We have **not** run ActiveChecker or confirmed an access-control vulnerability in this campaign. The immediate outcome is a native collection and the evidence needed for the next integration stage.

## 2. Where we started

The SPHERE dashboard initially showed `reproduction` under project `bacfuzz` as **Undeployed**, with no attached reservation or gateway. Its compiled experiment revision was still available. We redeployed the saved revision rather than modifying another course environment.

The gateway's persistent home still contained our October evidence pointer and archive. The pointer identified `/project/bacfuzz/evidence-Oct23-2NQnSl`. The newly provisioned runner was a fresh VM: its old node-local Docker installation, Python environment and application containers were absent. This explains why project approval and membership alone did not make the environment ready to run again.

We did not change Snort, SYN-flood, firewall, Lab 5 or Lab 6 environments.

## 3. SPHERE resources and lifetime

| Item | Verified state |
|---|---|
| Project | `bacfuzz` |
| Experiment | `reproduction.bacfuzz` |
| Saved revision | `a3c9e0ee7d9255661e5681d017fe4661f441c37e` |
| New reservation/activation | `reproduction.reproduction.bacfuzz`, Activated |
| Runner | Ubuntu 24.04.4 LTS, x86_64; 4 cores and 8 GB RAM allocated |
| Shared gateway | `dev.bacfuzz`, SSH name `dev-bacfuzz`, attached to the BACFuzz activation |
| Working access | Gateway JupyterLab and SSH from the gateway to `runner` |
| Reservation and gateway expiration | December 9, 2026, 4:00 PM as displayed by SPHERE |

We requested availability through the December 13 final deadline. SPHERE rejected that date with **“Date cannot be more than 30 days from now.”** We extended both resources to December 9 within the permitted window. They still need a further extension before that expiration to cover December 13. We did not create an automatic renewal.

## 4. Software and provenance

| Component | Recorded version or revision |
|---|---|
| Python | 3.11.17, installed with uv |
| uv | 0.13.5 |
| Docker Engine/client | 29.1.3 |
| Docker Compose | 2.40.3 |
| Playwright | 1.45.1, from the upstream dependency pins |
| Chromium | 127.0.6533.17 |
| BACFuzz artifact | `94470790c0941c7cb628712b81e10e154d97928a` |
| Recovered LiteLLM | 1.44.4 from official source commit `3f96a8c6674ccab8f10a254d7b959e8adbed055d` |
| Inventory tooling restored after campaign | Group revision `31661519bb3f3d1790b233c66aee5a1e343bd496` |

The initial clone used GitHub's default branch, whose recorded revision begins `18135f5`. That branch lacked `scripts/inventory-captures.py`. After the campaign, we fetched and checked out the report's recorded group-tooling revision above, preserving the run and earlier diagnostic failure. The research artifact itself stayed at the same pinned upstream commit. This distinction matters when repeating the work: cloning the default group branch was insufficient to recover all of our tooling. The exact initial group SHA is retained in `restore/environment.txt`.

Dependency restoration used `scripts/fetch-upstream.sh` and `scripts/setup-python.sh`. We retained the source-recovery approach for LiteLLM instead of silently upgrading it. All 62 package pins and compatibility checks passed.

The final Linux runtime checker reported **4 passed, 0 failed, 0 skipped**:

1. Dependency versions and LiteLLM source provenance.
2. Five-minute YAML configuration loading.
3. Upstream fuzzer/MainDriver imports without invoking initialization or a campaign.
4. Headless Chromium startup.

We installed Xvfb and the browser's OS dependencies. The supplied headed-browser login workflow then completed under Xvfb. The runtime checker alone did not establish target or login readiness; those were separate checks.

## 5. Target deployment and isolation

We generated `.local/wut/compose.yaml` from the supplied application example. The generated configuration:

- Uses an internal Docker network.
- Requests web access only through `127.0.0.1:8088`.
- Removes database host ports and omits phpMyAdmin.
- Applies our recorded SQL seed permission correction, `COPY --chmod=0644`, in the generated database Dockerfile.

The research source remained unchanged; our local configuration addition and generated Compose file are distinct from upstream code edits. We built only the `db` and `web` services using Compose project name `bacfuzz-reproduction`. The build completed with exit **0**, and both containers started.

Docker again failed to expose the requested host mapping on the internal network. We restored an unprivileged `socat` listener bound to **127.0.0.1:8088**, resolving the current web container address dynamically. Early HTTP probes returned `000` during startup, and the relay recorded an initial connection refusal. A later probe returned **HTTP 200**. We did not reuse the old container address or expose the application publicly.

Target image identifiers are preserved in `restore/target-image-ids.txt` and the campaign metadata. The new image's PHP extension versions were not separately inventoried during this session; the October extension-version list must not automatically be relabeled as the November runtime.

## 6. Problems encountered and corrective actions

| Observation | Action and result |
|---|---|
| Browser control initially timed out; later the app's browser identifier changed | Recovered the current in-app tab through the browser inventory. No SPHERE authentication protections were changed. |
| Old reservation and gateway were absent | Redeployed the saved BACFuzz revision and created/attached the dedicated shared gateway. |
| Fresh runner lacked previous installations | Reinstalled pinned Python tooling, dependencies, Docker and Chromium, recording stage logs and exit files. |
| Noninteractive SSH reported `sudo: a password is required` | A persistent interactive SSH session passed `sudo -v`; `sudo -n id` returned uid 0 in that session. No sudo policy was changed. |
| Chromium download warned about missing system libraries | Installed the OS dependencies; Chromium startup subsequently passed. |
| Build printed a PECL channel-protocol warning | Preserved the warning. It did not prevent this build from completing. |
| Internal-network host port was inactive | Restored the loopback relay and verified HTTP 200. |
| First standalone login check used the wrong config path | Saved the failure and retried with an absolute config path. |
| Next login check supplied a Python dict instead of upstream Config | Saved the AttributeError; retried using the upstream Config loader. The helper then exited 0 and all five state files existed. |
| Inventory helper absent from the default group branch | Saved the missing-tool error, restored the recorded tooling revision and reran the inventory successfully. |

We retained unsuccessful attempts rather than treating every setup step as an uninterrupted success.

## 7. Provider and account readiness

The supplied automatic-login helper completed for Admin, LeaveManager, Salary, BorrowManager and Anonymous. Five corresponding storage-state files were present. Their existence and helper completion do not establish the entire role/permission matrix; operation-specific authorization remains a separate evaluation task.

A minimal DeepSeek preflight returned **HTTP 200**, with 6 prompt tokens and 1 completion token. The requested alias was `deepseek-chat`; the response identified the served model as **deepseek-flash**. This records a difference from the paper's reported DeepSeek-V3 setup. The preflight's token count is not the campaign's total usage or cost.

The API credential was stored in 1Password and entered through a hidden `read -rs` prompt into the campaign shell environment. We cleared that variable afterward. A final exact-key scan of **372 files** across run metadata, restoration logs, the native corpus and login states found **0 matches**. This check covered that API key, not every possible secret; native session/capture material remains private.

## 8. First native MainDriver campaign

| Setting | Value |
|---|---|
| Run identifier | `main-driver-Nov09-001` |
| Target | Authors' supplied `CVE_2025_0802` application |
| Role order | Admin, LeaveManager, Salary, BorrowManager, Anonymous |
| Configuration | `configs/driver-smoke.yaml`, copied as `group-driver-smoke.yaml` for upstream configuration loading |
| Configured duration | 0 hours, 5 minutes |
| Mode | `--only-driver y`; checker disabled |
| Display | `xvfb-run -a` |
| Outer watchdog | 10 minutes; TERM followed by KILL after a 30-second grace period |
| Start | November 9, 2026, 21:48:06 UTC |
| End | November 9, 2026, 21:53:20 UTC |
| Wall time | 5 minutes 14 seconds, including initialization/login and shutdown |
| Main process exit | **0** |

Before launch, the target's native corpus directory contained no existing files. We preserved the precheck login states, configuration copy/hash, upstream SHA and target image identifiers in the private run directory.

The collection command, executed from `bacfuzz/fuzzer`, was:

```sh
timeout --signal=TERM --kill-after=30s 10m \
  xvfb-run -a "$HOME/BACFuzz-Project/.local/venv/bin/python" -u \
  fuzzer.py --config group-driver-smoke.yaml --only-driver y
```

Standard output/error went to the private `driver.log`; timestamps and exit status were saved separately. We did not execute the authors' long driver-plus-checker campaign.

### Final native capture inventory

| Role | GET | POST | Accepted captures | Rejected entries |
|---|---:|---:|---:|---:|
| Admin | 69 | 53 | 122 | 0 |
| LeaveManager | 31 | 30 | 61 | 0 |
| Salary | 45 | 37 | 82 | 0 |
| BorrowManager | 25 | 15 | 40 | 0 |
| Anonymous | 3 | 2 | 5 | 0 |
| **Total** | **173** | **137** | **310** | **0** |

The inventory exited **0**, reported **0 unexpected entries**, found the parameter dictionary and set `complete: true`. A final log-marker check counted zero Python tracebacks, AuthenticationError, RateLimitError and APIConnectionError markers. That is a diagnostic summary, not proof that every application request succeeded. These are native stored corpus entries, not a packet count or a count of vulnerabilities, unique endpoints or successful actions. The dictionary's presence/structure does not prove that every value has been semantically validated or that checker replay will succeed.

## 9. Evidence and storage

The complete private bundle is on the persistent BACFuzz gateway:

```text
/project/bacfuzz/evidence-Nov09-run001/
  restore/         installation, build, login and provider checks
  run-metadata/    campaign log, config, timestamps, hashes and inventories
  native-corpus/  role YAML files and shared parameter dictionary
  login-states/   fixture browser storage states
  SHA256SUMS      evidence integrity manifest
```

The directory is assigned to group `bacfuzz`, with group read/traverse access and no world access. Restoration logs were also initially copied to the owner's `~/BACFuzz-restore-Nov09/` directory. The shared bundle is the handoff location; preserve its files before any later run.

| Evidence | What it supports |
|---|---|
| `restore/environment.txt` | Group/upstream revisions, Docker/Compose versions and disk snapshot |
| `restore/runtime-check.log` and `.exit` | Four successful Linux runtime checks |
| `restore/apt-*.log`, `browser-os-deps.*`, `chromium-install.*` | Installation outputs, warnings and stage exits |
| `restore/target-build.*`, `target-start.*`, `target-image-ids.txt` | Image build/start and target identity |
| `restore/loopback-relay.*`, `http-readiness.txt` | Local connectivity issue, relay and HTTP readiness |
| `restore/fixture-login*.log` and `.exit`, `login-state-presence.json` | Failed helper invocations, successful correction and state-file presence |
| `restore/provider-preflight.json` and `.exit` | Provider access and served-model observation |
| `run-metadata/start-utc.txt`, `end-utc.txt`, `driver.exit` | Campaign timing and process result |
| `run-metadata/driver.log` | Detailed execution evidence; private because it may include authenticated request material |
| `run-metadata/inventory.txt` and `.exit` | Final role/method counts and structural acceptance |
| `run-metadata/credential-scan.json` | Exact API-key scan result |
| `SHA256SUMS` | Backup integrity; the manifest check completed with exit 0 |

Only reviewed summaries and sanitized proofs belong in Git. Do not publish raw YAML, parameter values, login states, generated configuration containing fixture credentials, or the unreviewed driver log.

## 10. What this establishes and what remains

We now have a working isolated target, restored runtime, successful provider preflight and a completed native MainDriver corpus. This is a concrete experimental milestone for Iftat's collection work.

The next stage is to inspect representative captures privately with the group, verify role permissions for the chosen operation, and test the native corpus/dictionary with ActiveChecker. Arian's mutation/checker work and Taamim's permission/SQL interpretation are needed to determine whether a candidate action is actually unauthorized. A successful collection or HTTP response does not establish that conclusion.

Before repeating or extending the run:

1. Preserve this bundle and use a fresh run identifier/output area.
2. Verify the target's state; MainDriver's browser interactions may have changed fixture data.
3. Confirm the model configuration, provider allowance and any spending limit for the longer campaign.
4. Record target image identifiers, runtime/config differences and the role order again.
5. Extend both SPHERE resources beyond December 9 to cover the December 13 final deadline.

## 11. Report-ready progress paragraph

On November 9, we restored the isolated BACFuzz runner after our previous SPHERE reservation expired. We recovered the pinned dependency environment, passed four Linux runtime checks and rebuilt the supplied web/database target. We resolved the internal-network port-mapping problem with a loopback-only relay, completed the supplied role-login workflow and verified provider access. We then executed our first five-minute native MainDriver-only campaign, which exited successfully and produced 310 accepted role-separated captures: 173 GET and 137 POST. The shared parameter dictionary was present and the structural inventory passed. We preserved configuration, version records, failed setup attempts, logs, session states and corpus files in private group storage with an integrity manifest. ActiveChecker replay and permission-aware SQL validation remain the next experimental stages.

## 12. Supporting project references

- [Pinned BACFuzz research artifact](https://github.com/websecfuzz/BACFuzz/tree/94470790c0941c7cb628712b81e10e154d97928a).
- [Recorded group-tooling revision](https://github.com/IftatBhuiyan/BACFuzz-Project/tree/31661519bb3f3d1790b233c66aee5a1e343bd496).
- [MainDriver procedure](main-driver.md), [setup notes](setup.md), [October baseline](browser-baseline.md), and [November readiness record](../evidence/sphere-readiness-Nov09.txt).

These notes describe our own observations. They do not replace the research paper or establish that the preprint and final accepted manuscript are identical.
