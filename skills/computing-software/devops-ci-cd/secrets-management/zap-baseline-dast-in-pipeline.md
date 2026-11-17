---
id: computing-software.devops-ci-cd.secrets-management.zap-baseline-dast-in-pipeline
name: zap-baseline-dast-in-pipeline
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, zap-baseline, owasp-zap, shift-left-security, dast]
level: practitioner
status: docs-checked
description: "Run OWASP ZAP baseline (passive) and API scans against a deployed preview or staging environment in CI, tune rules with a config file and gate on new alerts only."
sources: ["https://www.zaproxy.org/docs/docker/baseline-scan/", "https://github.com/zaproxy/action-baseline"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DAST in the pipeline with ZAP baseline

ZAP baseline spiders the target for a short time and reports **passive** findings (headers,
cookies, information leaks). Safe for most environments; active (full) scans attack the target and must only hit disposable targets.

## Run
```bash
docker run --rm -v "$PWD:/zap/wrk:rw" -t ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py -t https://pr-123.preview.example.com -c zap-rules.tsv -r zap.html -J zap.json -m 3 -I
```
- `-m 3` spider minutes (default 1); `-j` uses the modern spider in addition to the traditional one.
- `-I` do not fail on warnings (only FAIL-level rules fail).

GitHub Action: `zaproxy/action-baseline`.

## Rule config (zap-rules.tsv)
```
10021	FAIL	(X-Content-Type-Options Header Missing)
10015	IGNORE	(Incomplete or No Cache-control and Pragma HTTP Header Set)
```
Generate a starting file with `-g zap-rules.tsv` (all rules set to WARN), then set levels deliberately.

## Gating strategy
- Start with WARN everywhere, triage, then promote important rules to FAIL.
- Authenticated scanning needs a context file (`-n`) and a user (`-U`, must be defined in that context file); unauthenticated scans see only what is public.
- Run against the PR's ephemeral environment after deploy, not production.

## Verify
- [ ] A rule set to FAIL that matches makes the job exit with code 1; the report artifact is attached to the run.

## Checked

2026-10-28. Confirmed against the ZAP baseline scan docs page: zap-baseline.py, ghcr.io/zaproxy/zaproxy:stable image, flags -t -c -g -m (default 1) -r -J -I -j -n -U, alerts default to WARN and a config file changes rules to FAIL or IGNORE, tab-separated rule file format, rule ids 10021 and 10015, exit code 1 on at least one FAIL; zaproxy/action-baseline repo. Removed: zap-full-scan.py, zap-api-scan.py and action-api-scan, Automation Framework zap.yaml, rule ids 10038 and 10096, the issue-opening claim of the action and the AJAX-spider description of -j.

Method: documentation only; no commands were run.
