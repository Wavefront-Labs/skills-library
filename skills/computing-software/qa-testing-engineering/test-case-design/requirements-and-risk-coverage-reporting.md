---
id: computing-software.qa-testing-engineering.test-case-design.requirements-and-risk-coverage-reporting
name: requirements-and-risk-coverage-reporting
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [coverage-reporting, requirements-coverage, risk-coverage, traceability, test-reporting]
level: practitioner
status: draft
description: "Report requirements and risk coverage: traceability queries, covered vs tested vs passed, gaps by priority, and presenting coverage honestly to stakeholders."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Requirements and risk coverage reporting

**Goal:** answer "what have we tested and what is still unknown?" in terms stakeholders care about: requirements and risks, not test case counts.

## Levels of coverage per item
1. **Covered:** at least one test linked.
2. **Executed:** all linked tests run on the current build.
3. **Passed:** all linked tests passed and no open blocking defect linked.

Report all three; "covered" alone hides that tests have not run.

## Producing it
- Xray: Test Coverage report by requirement and by version/test environment.
- TestRail: references field + Coverage for References report.
- Spreadsheet: requirement list with link counts from the tool export; pivot by status.
- Automation: tag tests with requirement or risk IDs and aggregate JUnit results per tag in CI.

## Present
- Table by priority or risk level: total, covered %, executed %, passed %.
- List **gaps** explicitly: high-priority requirements without tests, failing or blocked items with the defect ID.
- Show trend from the previous report.
- State limitations: coverage is only as good as the links and the test depth; a requirement with one shallow test counts as covered.

## Verify
Every committed requirement and high risk appears with covered/executed/passed status, gaps are listed by priority, and the numbers reproduce from the tool query.
