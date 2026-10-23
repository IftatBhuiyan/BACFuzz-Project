# First normal-browser baseline — October 23, 2026

We deployed the supplied CVE_2025_0802 application in the dedicated SPHERE runner and completed a separate Playwright landing-page baseline. It captured **135 local HTTP requests** across four fixture-account contexts and Anonymous, including assets. The HAR files also record eight aborted external-resource requests. This is actual application traffic, but it is not MainDriver execution, broad crawl coverage or a reproduced vulnerability. See the reviewed [counts](../evidence/browser-baseline-Oct23.txt) and [Linux preparation checks](../evidence/linux-runtime-checks-Oct23.txt).

## Deployment changes and errors

Original upstream files remain separate from our group additions. We generated a private Compose copy under `.local/wut/` and used `--project-directory` to preserve its relative build/volume paths. The Compose project is `bacfuzz-smoke001` on the dedicated runner only. We started `db` and `web`; phpMyAdmin was not started.

- Published application ports were restricted to loopback in the generated configuration, and the default Docker network was set `internal: true`.
- The first image build failed fetching a PHP layer through an unroutable IPv6 Docker Hub address. An IPv4 HTTPS probe reached the registry. We temporarily mapped the registry hostname to its observed IPv4 address, retained normal TLS verification, completed the build, and removed the temporary mapping afterward. Do not treat that address as a permanent pin.
- The first MySQL initialization failed because the copied seed SQL file was unreadable by the image's database user. We added `COPY --chmod=0644` to the generated inline DB Dockerfile. We reset only our newly created, partially initialized fixture DB and rebuilt it. No experimental collection existed at the reset point.
- Docker recorded the requested loopback binding but did not expose an active host mapping on the internal-only network. We retained that network and used an unprivileged loopback relay: `socat TCP4-LISTEN:8088,bind=127.0.0.1,reuseaddr,fork TCP4:<web-container-IP>:80`. We observed the listener on `127.0.0.1:8088` and a target HTTP 200 response. Resolve the actual web-container IP again if recreating it; do not assume a fixed address.

Observed target runtime: PHP 8.3.6, UOPZ 7.1.1, Xdebug 3.5.3, PCOV 1.0.12, and the supplied MySQL 8.4.0 image. The upstream recipe installs some extensions without exact pins, so these observed versions and saved image IDs matter. PHP CLI inspection reported duplicate OPcache/GD loading and an `allow_url_include` deprecation warning; we retained them without changing the authors' instrumentation configuration. We have not validated the SQL oracle.

## Collection method and limits

The executed collector is retained as `scripts/collect-browser-baseline.py`. It is specific to the runner checkout at `~/BACFuzz-Project`, imports the supplied auto-login fixture, then revisits one landing page per role while recording private HAR files and screenshots. Its browser sessions block non-local origins during HAR collection. The supplied auto-login stage runs before this capture stage. The collector does not import MainDriver, mutate parameters or call a model.

We used fresh generated output directories and kept captured login states with the HAR bundle. The initial-page/dashboard checks are limited heuristics, not a completed role-permission matrix. All recorded methods are GET. Three local responses were 403; these require contextual review, not an automatic vulnerability or enforcement claim. Counts include page assets.

HAR files are a different format from the MainDriver request YAML and parameter dictionary. Do not pass this bundle to ActiveChecker as if that handoff had been validated. Arian's approved provider integration remains necessary for the full driver path, and Tam's application-permission/SQL work remains separate.

## Private handoff

The raw bundle was backed up on the dedicated shared XDC under the BACFuzz project directory, with group access for the three BACFuzz members and no world access. The owner's `~/BACFuzz-evidence-latest-path.txt` points to its exact location. It contains runtime/build logs, private generated configuration, browser captures, login states, screenshots and the reviewed summary. Keep those files outside Git and public slide assets. Save evidence before the runner reservation expires October 24.
