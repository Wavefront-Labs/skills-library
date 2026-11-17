---
id: computing-software.qa-testing-engineering.test-case-design.risk-register-linked-to-tests
name: risk-register-linked-to-tests
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [risk-register-tests, risk-based-testing, traceability, risk-coverage, test-management]
level: practitioner
status: draft
description: "Maintain a product risk register linked to tests: risk IDs, levels, test depth, traceability in the test tool, and risk coverage reports for release decisions."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Risk register linked to tests

**Goal:** every product risk has tests proportional to its level, and you can report "what risk remains" rather than "how many tests passed".

## Register fields
Risk ID | Description (what could go wrong, for whom) | Area/feature | Likelihood | Impact | Level (matrix result) | Test approach and depth | Linked tests | Status (open, mitigated, accepted) | Owner | Last reviewed.

## Linking
- In Jira/Xray: create risks as issues (or use a custom issue type) and link tests with "tests" relations; Xray coverage then shows per risk.
- In TestRail: a custom field or reference (`refs`) holding risk IDs; filter runs by risk.
- In code: tag automated tests with the risk ID (`@pytest.mark.risk("R-12")`, Playwright `tag: '@R-12'`) so results can be aggregated per risk in CI.

## Depth by level (example policy)
- High: multiple techniques, independent review, automated regression, exploratory charters.
- Medium: core techniques, key regression automated.
- Low: checklist or smoke only.

## Reporting
Per risk: tests planned, executed, passed, open defects. A risk is "mitigated" only when its tests passed and no blocking defects remain. Show untested high risks first.

## Verify
No high risk lacks linked tests, the coverage report can be generated from the tool or CI tags, and the go/no-go pack includes the per-risk status.
