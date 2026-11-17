---
id: computing-software.qa-testing-engineering.test-case-design.requirements-traceability-matrix
name: requirements-traceability-matrix
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [traceability-matrix, requirements-traceability, test-process, coverage, bidirectional-traceability, jira, xray, istqb]
level: practitioner
status: draft
description: "Build and maintain bidirectional traceability from requirements and risks to tests, results and defects, and use it for coverage and impact analysis."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://docs.getxray.app/display/XRAY/Requirement+Coverage
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Requirements traceability

**Goal:** answer three questions quickly: is every requirement tested, what does this failing test affect, which tests must rerun when requirement X changes. ISTQB CTFL v4.0 1.4.4.

## What to link
Requirement / user story / risk -> test condition -> test case -> test run result -> defect.

## Practical implementations
- **Test management tool**: Xray/Zephyr "Tests" issue links to stories; coverage report per story/version. TestRail: `References` field with Jira keys.
- **Automation-native**: tag tests with the requirement id and generate the matrix from results.
  - pytest: `@pytest.mark.req("PAY-123")`, collect via a `pytest_collection_modifyitems` hook or JUnit XML properties (`record_property("req", "PAY-123")`).
  - Playwright: `test('refund', { annotation: { type: 'req', description: 'PAY-123' } }, ...)`.
  - JUnit 5: `@Tag("PAY-123")`.
- **Spreadsheet** only for small, one-off projects; it rots immediately.

## Using it
- Coverage: requirements with zero linked tests, or only failed/not-run tests.
- Impact analysis: requirement changed -> linked tests to update and rerun.
- Reporting: pass rate *per requirement/risk* is what stakeholders understand, not per test.

## Gotchas
- Many-to-many links are normal; do not force 1:1.
- Traceability to obsolete requirements gives false coverage. Prune when stories close.

## Verify
Pick three random requirements and three random failed tests; you can trace each in both directions in under a minute.
