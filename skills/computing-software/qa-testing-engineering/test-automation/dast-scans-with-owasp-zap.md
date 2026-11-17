---
id: computing-software.qa-testing-engineering.test-automation.dast-scans-with-owasp-zap
name: dast-scans-with-owasp-zap
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [owasp-zap, dast, security-testing, zap-baseline, api-scan, ci-quality-gates]
level: practitioner
status: docs-checked
description: "Run OWASP ZAP DAST in CI: baseline and full scans, API scans from OpenAPI, authenticated scanning, rule tuning via config files, and triaging false positives."
sources:
  - https://www.zaproxy.org/docs/docker/baseline-scan/
  - https://www.zaproxy.org/docs/docker/full-scan/
  - https://www.zaproxy.org/docs/docker/api-scan/
  - https://www.zaproxy.org/docs/automate/automation-framework/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAST scans with OWASP ZAP

**Goal:** find runtime security issues (missing headers, injection, XSS, misconfig) against a running test environment you own. Never scan systems without written authorisation.

## Baseline scan (passive, safe, fast)
```bash
docker run --rm -v "$PWD:/zap/wrk:rw" -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://staging.example.test -c zap-rules.conf -r zap.html -J zap.json
```
Runs the ZAP spider against the target for 1 minute by default (`-m` changes it), waits for passive
scanning to finish, then reports. `-c` takes a config file, `-r` writes the HTML report and `-J` the
JSON document. By default every alert is a WARN.

## Full scan (active attacks)
`zap-full-scan.py -t <url>` performs actual attacks and can run for a long time; run it against a
disposable environment (it creates data and may break things), for example nightly.

## API scan
```bash
zap-api-scan.py -t https://staging.example.test/openapi.json -f openapi -r api.html
```
`-f` takes `openapi`, `soap` or `graphql` (for GraphQL, `-t` is the endpoint URL).

## Rule tuning (`zap-rules.conf`)
```
10021	WARN	(X-Content-Type-Options Header Missing)
```
Each line is a rule ID, an action and a name; change WARN to IGNORE to ignore a rule or to FAIL to
fail the run when it matches. Generate a template with `-g gen.conf` (all rules set to WARN).
Exit codes: 0 success, 1 at least one FAIL, 2 at least one WARN and no FAIL.

## Authenticated scans
Use the Automation Framework (`zap.sh -cmd -autorun plan.yaml`) with a context, an authentication
method and a logged-in indicator; see the ZAP authentication documentation for the methods your
ZAP version supports. Verify the spider reaches authenticated pages.

## Triage
- Confirm each alert manually (reproduce the request in ZAP or curl) before filing.
- Mark false positives in the rules file with a comment and ticket.

## Gotchas
- Unauthenticated scans only see the login page of most apps.
- Active scans against shared environments corrupt other teams' data.
- SPAs: `-j` adds the modern spider (the Ajax spider by default) to the baseline scan.

## Verify
CI fails on a deliberately removed security header, and the authenticated scan report lists URLs behind login.

## Checked
2026-10-31. Confirmed in the ZAP baseline, full-scan, API-scan and Automation Framework pages:
spider default of 1 minute and `-m`, `-c`/`-r`/`-J`/`-g` options, WARN/IGNORE/FAIL actions, rule
10021, exit codes 0/1/2, `zap-full-scan.py` performing attacks, `-f openapi|soap|graphql`, `-j`,
and `-cmd -autorun`. Removed: rule IDs 10038 and 10096, the `ZAP_AUTH_HEADER` environment variable
names, and a statement that FAIL entries "break the build" beyond the documented exit code, because
no fetched page confirms them.
Method: documentation only; no commands were run.
