---
id: computing-software.qa-testing-engineering.test-automation.tests-as-code-vs-tool-storage
name: tests-as-code-vs-tool-storage
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [tests-as-code, test-management-tools, version-control, gherkin, test-repository, docs-as-code]
level: practitioner
status: draft
description: "Decide between storing tests as code in version control and in a test management tool: trade-offs, hybrid patterns, syncing results, and review workflows."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://docs.getxray.app/display/XRAYCLOUD/Testing+with+Cucumber
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tests-as-code vs test management tool storage

**Goal:** choose where test definitions live so they stay versioned with the product, reviewable and reportable.

## Tests-as-code (in the repo)
Automated tests, Gherkin features, and even manual test specs as Markdown live in Git next to the code.
- **Pros:** versioned with the code (branch has matching tests), reviewed in PRs, no licence cost, refactorable, CI reports results directly.
- **Cons:** non-technical stakeholders cannot browse easily; manual execution tracking and coverage reporting need extra tooling.

## Tool storage (TestRail, Xray, Zephyr, qTest)
- **Pros:** execution tracking for manual tests, traceability reports, dashboards, audit trails, approvals for regulated contexts.
- **Cons:** drifts from code on branches, duplicated maintenance, licence cost.

## Hybrid patterns
- **Code is the source of truth for automated tests;** CI pushes results to the tool (Xray JUnit/Cucumber import, TestRail `trcli`), auto-creating tool entries keyed by test name or ID tag.
- **Gherkin in the repo, synced to Xray:** Xray can import features and export them back; pick one direction as master to avoid conflicts.
- **Manual and exploratory tests** in the tool, or as Markdown charters in the repo for engineering-heavy teams.
- Stable IDs in test names or tags (`@TEST-123`) so results map even after renames.

## Decision guide
Regulated or large manual effort: tool as reporting layer, code for automation. Small, highly automated team: everything as code with CI dashboards. In every case avoid hand-maintaining the same test in both places.

## Verify
For each test type the team can name one master location, results flow automatically from CI into reports, and no test is maintained twice by hand.
