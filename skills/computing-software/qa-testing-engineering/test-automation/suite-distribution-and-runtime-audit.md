---
id: computing-software.qa-testing-engineering.test-automation.suite-distribution-and-runtime-audit
name: suite-distribution-and-runtime-audit
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [suite-distribution-audit, test-pyramid, test-suite-metrics, ci-runtime, test-strategy]
level: practitioner
status: draft
description: "Audit a test suite's distribution and runtime by layer: count tests and time per layer from CI reports, find slow and redundant tests, and set targets."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://martinfowler.com/articles/practical-test-pyramid.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Auditing suite distribution and runtime by layer

**Goal:** measure the actual shape of the suite (not the diagram on the wiki), and find where time and flakiness go.

## Collect
- Classify tests by layer: directory convention (`tests/unit`, `tests/integration`, `e2e/`), markers/tags (`@pytest.mark.integration`, JUnit `@Tag`), or project (Playwright projects).
- Pull per-test durations and outcomes from JUnit XML across the last N CI runs (`pytest --durations=50`, `--junitxml`, Jest `--json`, Playwright JSON reporter).

```python
import glob, xml.etree.ElementTree as ET, collections
t = collections.defaultdict(lambda: [0, 0.0])
for f in glob.glob('reports/**/*.xml', recursive=True):
    for tc in ET.parse(f).iter('testcase'):
        layer = tc.get('classname', '').split('.')[1]   # adapt to naming
        t[layer][0] += 1; t[layer][1] += float(tc.get('time', 0))
for k, (n, s) in t.items(): print(f'{k:12} {n:6} tests {s/60:7.1f} min')
```

## Analyse
- Count and runtime per layer; ice-cream cone if E2E count or time dominates.
- Top 20 slowest tests: sleeps, repeated logins, unneeded UI setup (use API setup).
- Flake rate per layer from retry data.
- Redundancy: E2E tests that re-check rules already covered by unit tests (compare test names and requirement tags).
- Wall-clock vs total CPU time: parallelism efficiency.

## Act and set targets
Targets such as: PR pipeline under 10 minutes, E2E under 10% of test count, no test over 60 s without justification. Push down redundant E2E checks; delete tests with no unique value.

## Verify
An audit table of count, runtime and flake rate per layer exists, with dated targets, and re-running it a quarter later shows movement.
