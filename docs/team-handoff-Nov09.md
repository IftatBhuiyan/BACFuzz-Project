# Team handoff — November 9, 2026

## Pull the current work

Use `main` for the shared work. PR #2 records the environment, collection and documentation integration.

From an existing checkout with no conflicting local changes:

```sh
git fetch origin
git switch main
git pull --ff-only
```

For a new checkout:

```sh
git clone https://github.com/IftatBhuiyan/BACFuzz-Project.git
```

If Git reports local changes or a conflict, preserve that work and resolve it before switching. Do not reset or overwrite another member's changes.

## Current result

The isolated SPHERE runtime is restored. The four runtime checks passed, both target containers are running, the fixture login helper completed for five contexts, and provider preflight succeeded. Our first five-minute MainDriver-only campaign exited 0 and produced **310 structurally accepted native captures**: 173 GET and 137 POST. The parameter dictionary is present; the inventory also exited 0 with no rejected/unexpected entries.

Read [the lab record](experiment-Nov09-main-driver.md) and [reviewed results](../evidence/main-driver-Nov09-summary.json). The October 135-request HAR baseline is a separate experiment. Neither count establishes a vulnerability.

## Use these resources

- SPHERE project: `bacfuzz`; experiment: `reproduction`; activation: `reproduction.reproduction.bacfuzz`.
- Shared gateway: `dev.bacfuzz`, JupyterHub at `https://dev-bacfuzz.xdc.sphere-testbed.net/jupyter`.
- Private evidence: `/project/bacfuzz/evidence-Nov09-run001/` on the gateway. It contains restoration logs, run metadata, the native corpus, login states and an integrity manifest.
- Runner checkout: `~/BACFuzz-Project`; live native files under `.upstream/BACFuzz/bacfuzz/attack_surface/CVE_2025_0802/` and `login_state/CVE_2025_0802/`.
- Prepared configuration: `configs/driver-smoke.yaml`; inventory helper: `scripts/inventory-captures.py`.

Raw authenticated captures and login states stay in private project storage. Git contains tooling and reviewed summaries. A fresh clone alone does not retrieve the private corpus.

## Next responsibilities

**Iftat:** maintain the isolated runtime and collection evidence, help reproduce collection/configuration paths, and preserve the current bundle before any additional run.

**Arian:** inspect the native corpus/dictionary and verify loading with ActiveChecker. Coordinate a bounded checker experiment and retain configuration, errors, model information and candidate requests. The preflight served `deepseek-flash`; do not assume it is the paper's DeepSeek-V3. Structural inventory acceptance does not guarantee checker compatibility.

**Taamim:** verify the intended permissions and selected operation, resolve the CVE endpoint discrepancy, and interpret backend SQL evidence for checker candidates. A SQL modification alone does not prove unauthorized access.

**Together:** agree on one run owner and target state before running again. MainDriver interactions may have modified fixture data. Preserve this run, decide whether the next stage needs a clean fixture or the current state, and record any reset rather than silently changing it. We have not executed ActiveChecker or confirmed a vulnerability.

Both SPHERE resources expire **December 9 at 4 PM**. Extend both before then to cover the December 13 final; SPHERE currently rejects dates more than 30 days ahead. Rotate exposed credentials and configure replacements securely before further use; do not post keys in chat or commit them.
