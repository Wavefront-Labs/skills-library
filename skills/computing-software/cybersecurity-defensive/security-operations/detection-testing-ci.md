---
id: computing-software.cybersecurity-defensive.security-operations.detection-testing-ci
name: detection-testing-ci
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [detection-as-code, detection-testing-ci, unit-tests, ci-pipeline, attack-data, regression-testing, github-actions]
level: advanced
status: draft
description: "Test detections in CI: schema linting, unit tests against recorded true-positive and benign samples, replaying attack data, and gating deploys on results."
sources: ["https://github.com/splunk/contentctl", "https://github.com/splunk/attack_data", "https://github.com/elastic/detection-rules"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detection CI with unit tests and replayed data

**Goal:** every detection change is proven to still fire on known-bad data and stay quiet on
known-good data before it reaches production.

## Test levels
1. **Lint/schema:** rule parses, required metadata present (owner, ATT&CK, severity,
   data source), IDs unique. `sigma check`, `contentctl validate`, `python -m detection_rules test`.
2. **Conversion:** the rule converts for each target backend without errors.
3. **Unit tests:** run the rule against small recorded samples:
   `tests/<rule-id>/positive.json` must produce at least one hit;
   `tests/<rule-id>/negative.json` (benign look-alikes) must produce none.
4. **Integration replay:** ingest attack datasets (Splunk attack_data, Mordor/OTRF
   Security-Datasets, your own Atomic Red Team captures) into an ephemeral SIEM and run all
   rules; compare against expected hits.

## Practical setup
- Ephemeral targets: Splunk in a container (`splunk/splunk` image) loaded with test data;
  Elasticsearch container for Elastic rules; for Sentinel, a dev workspace and the
  Log Analytics query API.
- Splunk's `contentctl test` automates: builds an app, spins up Splunk, replays the attack
  data referenced in each detection YAML, and checks results.
- For SPL/KQL without a vendor harness, a small runner: ingest sample, run query via REST
  API, assert result count.

## Pipeline (GitHub Actions sketch)
```yaml
on: [pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install sigma-cli pysigma-backend-splunk
      - run: sigma check rules/
      - run: python ci/run_unit_tests.py --target splunk --rules rules/ --tests tests/
```
Require the job to pass before merge; deploy from main only.

## Recording test data
Capture real positives during incident work or purple-team runs (export the raw events,
scrub secrets and PII), plus benign events from the noisiest legitimate tool that resembles
the attack. Store with the rule.

## Gotchas
- Sample timestamps go stale; the runner should rewrite times to now or search all time.
- Tests that only check "query runs" prove nothing; assert counts.
- Field mappings in the test SIEM must match production or tests pass while prod fails.

## Verify
Break a rule deliberately (change a field name) in a branch; CI must fail.
