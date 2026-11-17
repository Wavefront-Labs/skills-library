---
id: computing-software.cybersecurity-defensive.application-security.zap-baseline-scan
name: zap-baseline-scan
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [dast, zap-baseline-scan, owasp-zap, passive-scan, ci-dast, rules-tsv, zaproxy]
level: practitioner
status: docs-checked
description: "Run the ZAP baseline scan in CI against a deployed app: Docker invocation, config file to tune WARN, FAIL and IGNORE, authenticated scans and reading the exit code."
sources: ["https://www.zaproxy.org/docs/docker/baseline-scan/", "https://www.zaproxy.org/docs/docker/about/", "https://www.zaproxy.org/docs/automate/automation-framework/", "https://www.zaproxy.org/docs/docker/api-scan/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ZAP baseline scan

**Goal:** a fast, safe DAST check on every deploy that flags missing headers, cookie flags, info leaks and other passive findings.

## What it does
`zap-baseline.py` runs the ZAP spider against the target for (by default) 1 minute, waits for passive scanning to finish, and reports. It performs no attacks (no active scan), so ZAP documents it as suitable for CI/CD, even against production sites.

## Run
```
docker run --rm -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://staging.example.com -c rules.tsv -r report.html -J report.json -I
```
- `-m 5` spider minutes; `-j` also runs the AJAX spider (the default for `-j`) for SPAs.
- `-I` do not return failure on warnings; omit it to fail.
- Exit codes: 0 success, 1 at least one FAIL, 2 at least one WARN and no FAIL, 3 any other failure.
- `-g rules.tsv` generates a config file with every rule set to WARN, to edit.
- File params (`-c`, `-r`, `-J`, `-g`) need the working directory mounted at `/zap/wrk/`.

## Tune with the config file
All alerts are WARN by default. Edit the generated file: change `WARN` to `IGNORE` or `FAIL` per rule id (text after the id is informational):
```
10020	FAIL	(X-Frame-Options Header Scanner)
10021	FAIL	(X-Content-Type-Options Header Missing)
10027	IGNORE	(Information Disclosure - Suspicious Comments)
```
`<rule-id>	OUTOFSCOPE	<regex>` lines skip URLs for a rule (`*` means all rules). A `-p` progress file marks known issues as in progress. Keep the files in the repo and review changes like code.

## Authentication
The baseline scan is unauthenticated unless you supply a context: `-n` loads a context file and `-U` names a user defined in it. For richer setups use the Automation Framework (`zap.sh -cmd -autorun <plan>.yaml`, as in the Docker docs), and `-z` passes extra ZAP options such as `-config key=value`. Follow the ZAP authentication docs for the method (form, JSON, header).

## Gotchas
- SPA with almost no crawlable links: add `-j`, or seed from the OpenAPI spec with `zap-api-scan.py`.
- A WAF in front can block the spider; allow-list the scanner in test environments.
- The baseline scan is migrating to the Automation Framework (`--auto`, `--autooff`, `--plan-only`); check the current docs before relying on one mode.

## Verify
- [ ] Report lists the expected URLs (spider reached the app).
- [ ] A rule set to FAIL that matches produces exit code 1 and breaks the pipeline.

## Checked
2026-11-01 against the ZAP docs pages Baseline Scan, Docker About, Automation Framework and API Scan: confirmed the 1-minute default spider, no attacks, options `-t -c -g -m -r -J -I -j -n -U -z -p`, exit codes 0 to 3, WARN default, FAIL/IGNORE/OUTOFSCOPE config syntax, rule ids 10020, 10021 and 10027, `zap.sh -cmd -autorun`, and the Automation Framework migration flags. Removed: rule ids 10038 and 10096, the Authorization header replacer `-z` example, the GitHub Action option names and the claim that a full scan modifies data (not on the fetched pages).
Method: documentation only; no commands were run.
