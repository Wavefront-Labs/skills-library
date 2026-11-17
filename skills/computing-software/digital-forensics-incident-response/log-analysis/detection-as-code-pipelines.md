---
id: computing-software.digital-forensics-incident-response.log-analysis.detection-as-code-pipelines
name: detection-as-code-pipelines
category: computing-software
field: digital-forensics-incident-response
product: log-analysis
tags: [detection-ci-pipeline, detection-as-code, sigma, ci-cd, detection-engineering, dfir]
level: advanced
status: draft
description: "Run detection-as-code: rules in Git, schema and syntax linting, Sigma conversion with pySigma, unit tests against sample events, CI deployment to the SIEM and drift checks."
sources: ["https://github.com/SigmaHQ/pySigma", "https://sigmahq.io/docs/digging-deeper/backends.html", "https://github.com/elastic/detection-rules", "https://learn.microsoft.com/en-us/azure/sentinel/ci-cd", "https://github.com/splunk/security_content"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detection-as-code pipelines

Treat detections like software: version control, review, automated tests, automated deployment. It stops "someone edited the rule in the console" outages and makes incident-driven detections reach production fast and safely.

## Repository layout
```text
rules/
  windows/credential_access/lsass_access_unusual.yml   # Sigma or native format
  windows/credential_access/lsass_access_unusual.md    # ADS documentation
tests/
  lsass_access_unusual/true_positive.json             # sample events
  lsass_access_unusual/false_positive_backup.json
pipelines/                                            # pySigma processing pipelines (field mappings)
.github/workflows/ci.yml
```
Elastic `detection-rules` and Splunk `security_content` are public examples of this pattern.

## CI stages (on every pull request)
1. **Lint/schema**: YAML validity, required metadata (id, author, ATT&CK tags, severity, ADS link), unique IDs; `sigma check` for Sigma rules.
2. **Convert**: `sigma convert -t splunk -p splunk_windows rules/` or Kusto/Elastic backends with your field-mapping pipeline; fail on conversion errors.
3. **Unit test**: run converted queries against sample events (local engine, a test index, or the SIEM's API on a dev workspace) and assert true positives hit and known false positives do not.
4. **Peer review**: required approval; reviewers check logic, blind spots and expected volume.

## CD (on merge)
- Deploy via API: Sentinel repositories feature or ARM/Bicep templates, Splunk REST (`saved/searches`), Elastic detection-rules `kibana import-rules`, or vendor Terraform providers.
- Tag releases; keep a changelog linked to incidents and tickets.

## Operations
- **Drift detection**: scheduled job compares deployed rules to Git and alerts on console edits.
- **Health**: track rule errors, run times, alert volume per rule; auto-open tickets for noisy or failing rules.
- **Emergency path**: during an incident, a fast-track PR with a single reviewer, still through CI.

## Gotchas
- Field-mapping pipelines are where most conversion bugs live; test against real data from each log source.
- Sample events must be refreshed when log schemas change (agent upgrades).
- Secrets for SIEM APIs belong in CI secret stores, with least-privilege service principals.

## Verify
A deliberately broken rule fails CI, a valid rule merged to main appears in the SIEM within the expected time, and the drift job reports zero differences.
