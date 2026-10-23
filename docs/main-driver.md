# MainDriver collection protocol

At the pinned commit, `bacfuzz/fuzzer/fuzzer.py:init` loads `../configs/config-general.yaml` (or `--config` relative to that configs directory), applies flags, then invokes `../auto_login/<PROJECT_NAME>.py`. CVE_2025_0802 auto-login is hardcoded to localhost:8088 and saves role storage states. Taamim must verify the supplied fixture accounts against the database; we do not copy fixture credentials into our notes.

`main()` starts one MainDriver per role with that storage state; `--only-driver y` disables checker execution. Driver interception records request YAML through `main_driver.py:store_request_to_file_as_attack_surface` to `bacfuzz/attack_surface/CVE_2025_0802/<role>/<number>.yaml`; Dictionary saves `paramval.yaml` in the project directory. Login states live in `bacfuzz/login_state/CVE_2025_0802/`. Request YAML, parameter values and logs may contain authentication material.

The initial candidate is the authors' CVE_2025_0802 example. Preserve role order `Admin LeaveManager Salary BorrowManager Anonymous`: checker code excludes index 0, despite the contradictory lowest-role-first comment in the general YAML. Arian must resolve that discrepancy before interpreting checker output.

## Proposed five-minute smoke run (NOT yet executed)
Prerequisites: isolated VM and WUT approved/prepared by Taamim; roles verified; browser dependencies installed; Arian confirms DeepSeek access and budget. One run owner; fresh target and fresh output directories. Do not reuse previous authors' data or overwrite an earlier group collection.

Copy `configs/driver-smoke.yaml` to `.upstream/BACFuzz/bacfuzz/configs/group-driver-smoke.yaml` as a documented local addition. The YAML explicitly sets h=0, m=5 because CLI zero values are ignored by `if args.hour` / `if args.minute`. Run from `bacfuzz/fuzzer` because paths depend on the working directory. The authors' 24-hour driver plus 24-hour checker script is not our smoke protocol.

```sh
# From group repository root; raw evidence remains ignored/private.
repo_root=$(pwd)
mkdir -p .local/run-001
# In a separate shell whose output is redirected to a private log:
cd .upstream/BACFuzz/bacfuzz/fuzzer
# Use xvfb-run -a if the VM has no graphical session.
"$repo_root/.local/venv/bin/python" -u fuzzer.py --config group-driver-smoke.yaml --only-driver y
```

For a live execution, redirect stdout/stderr to the absolute `.local/run-001/driver.log` path, retain the process exit status separately, and record start/end UTC. Apply an outer watchdog (e.g. GNU `timeout --signal=TERM --kill-after=30s 10m ...`); exit 124 means timeout, not success. A hard stop may prevent final dictionary writes. Five minutes is the internal campaign budget, not a guarantee of total wall time: login precedes crawling. No launch wrapper is supplied until target isolation and account readiness are established.

## Handoff and acceptance
Before every run record owner, upstream SHA and diff, config hash, target image IDs, role order, state reset, seed if any, time budget, environment versions and API model. Save exact command without secrets and exit status. Keep the entire collection together privately, including paramval.yaml, role YAML, login state, driver log and hashes; checker replay relies on these relative paths. Copy the previous run out before another crawl: numbered files can overwrite one another.

Inspect per-role request counts and methods, and verify nonempty meaningful collection and successful role login rather than accepting exit 0 alone. Retain failures and stack traces privately. Share only manually reviewed redacted examples in Git; redact cookies, authorization, passwords, tokens, query/body credentials and response data. Simple regex replacement is not sufficient to guarantee safe publication.

Arian receives collection/config/version metadata for checker work. Taamim receives candidate operations and verifies intended permissions and backend/SQL effects. A successful HTTP status alone is not an authorization violation. Record findings as confirmed, unconfirmed or false positive with evidence. Zero findings in a short run does not establish absence of a vulnerability.

## Offline collection inventory

After preserving a run's private outputs, inspect the capture directory with:

```sh
.local/venv/bin/python scripts/inventory-captures.py ".upstream/BACFuzz/bacfuzz/attack_surface/CVE_2025_0802"
```

The command is read-only and does not import the fuzzer, navigate to the target, replay requests or contact a model. It prints fixed role names, per-role counts and allowlisted HTTP methods. It does not print input paths, filenames, URLs, headers, cookies, bodies, parameter values or parser excerpts. It reads YAML syntax nodes instead of using the upstream Python-object loader. Files larger than 2 MiB, symlinks, malformed YAML and unexpected role-directory entries are rejected and counted without their contents being echoed.

Exit 0 means the **structural inventory is complete**: all five expected roles have at least one request mapping containing a recognized method and nonempty URL fields; no entries were rejected or unexpected; and a nonempty regular `paramval.yaml` exists. Exit 1 means incomplete or unsupported input. Dictionary presence is checked, not dictionary contents or semantic compatibility with the checker. The summary is not a redacted request export. Inspect and share the underlying collection privately with Arian, and review the summary before including it in the report.

A structurally complete inventory does **not** prove successful authentication, distinct permissions, sufficient crawl coverage, valid checker replay or a vulnerability. Login-state evidence and Taamim's permission/SQL checks remain separate gates. Use a fresh output directory for each run: old numbered YAML files can otherwise inflate counts.

### Source observations for our report

We traced `fuzzer.py:init` through role-specific login-state creation, then `MainDriver` request collection. At the pinned revision, `HTTPRequest.py:718–727` serializes `request.__dict__` using YAML and reconstructs requests using `yaml.Loader`. Nested parameter objects may have Python-specific tags, so our inventory inspects nodes without invoking those constructors. `main_driver.py:710–722` writes role-separated numbered files, while `Dictionary.py:250–260` writes the shared parameter dictionary. These files form the handoff to the checker; they can contain credentials and must stay private.

The corpus contains requests selected and retained by MainDriver, rather than a complete network packet capture. `main_driver.py:410–423` deduplicates/stores corpus requests and conditionally writes their YAML. Its `payload_analyze` stage calls the model when `request.num_sysgen > 0`; driver-only execution therefore does not guarantee a model-free campaign. We have inspected these paths but have not yet observed them in a live crawl.

Our offline compatibility probe used the actual upstream `HTTPRequest` serializer to create synthetic captures. It verified the inventory format and error handling; it is not a BACFuzz experiment or a reproduction result. See `evidence/capture-inventory-checks.txt`.
