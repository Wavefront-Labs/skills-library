---
id: computing-software.qa-testing-engineering.test-case-design.test-execution-and-result-logging
name: test-execution-and-result-logging
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-execution-log, test-run-logging, test-execution, test-process, anomaly-reporting]
level: practitioner
status: docs-checked
description: "Execute tests and log results properly: actual vs expected, environment and build identifiers, evidence, anomaly reports and retest records."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
  - https://docs.pytest.org/en/stable/how-to/output.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test execution and result logging

**Goal:** run tests so that every result is reproducible and auditable.

## Before running
- Confirm entry criteria: build ID deployed, smoke passed, test data loaded, environment version recorded.
- Pick the execution schedule from implementation (priority and dependency order).

## Per test, record
| Item | Why |
|---|---|
| Test ID and version | the case may change later |
| Build / commit SHA, environment, browser/device | reproduce the context |
| Tester / pipeline run ID, timestamp | audit |
| Actual result vs expected | the verdict basis |
| Verdict: pass / fail / blocked / not run | progress metrics |
| Evidence: screenshot, log excerpt, request/response, trace | defect triage |
| Linked defect ID | traceability |

## Automated runs
- Emit JUnit XML (`pytest --junitxml=results.xml`, or your runner's JUnit reporter) and archive it with the build number.
- Keep traces/screenshots for failures only to control storage.
- Record retries separately; a pass on retry is "flaky", not "pass".

## When actual != expected
Analyse before reporting: test defect, data or environment issue, or product defect. Raise an anomaly report only for the last, with the evidence above. Re-run confirmation tests after the fix and log them as new executions, not edits.

## Gotchas
- "Blocked" must name the blocker so it is chased.
- Never overwrite a failed result with a later pass; history shows instability.
- Exploratory sessions log too: charter, notes, bugs, time.

## Verify
For any failed test you can name the build, environment, data and evidence without asking the tester.

## Checked

2026-10-28 Confirmed against: pytest docs (creating JUnitXML format files with `--junitxml`). Removed or generalised: the ISTQB section number, the Playwright `--reporter=junit` and `trace` option, and Maven Surefire (not in the fetched pages).

Method: documentation only; no commands were run.
