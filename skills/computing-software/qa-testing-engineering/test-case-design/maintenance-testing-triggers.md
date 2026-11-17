---
id: computing-software.qa-testing-engineering.test-case-design.maintenance-testing-triggers
name: maintenance-testing-triggers
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [maintenance-triggers, maintenance-testing, regression-testing, test-types, impact-analysis]
level: practitioner
status: docs-checked
description: "Plan maintenance testing for each CTFL trigger: modifications, upgrades or migrations, and retirement, scoping tests with impact analysis and data checks."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Maintenance testing triggers

**Goal:** test released systems when they change, scoped by what changed. CTFL v4.0 2.3.

## Triggers and what to test
| Trigger | Examples | Testing focus |
|---|---|---|
| Modification | planned (release-based) enhancements, corrective changes, hot fixes | evaluate that the change works and check for regressions in the unchanged parts |
| Upgrade / migration of the operational environment | moving from one platform to another | tests of the new environment and of the changed software; tests of data conversion when data from another application is migrated in |
| Retirement | an application reaching end of life | data archiving if long retention periods are required; restore and retrieval after archiving |

## Scoping
1. Impact analysis (can be done before the change, to decide whether to make it): which parts of the system could be affected.
2. The scope of maintenance testing typically depends on the degree of risk of the change, the size of the existing system and the size of the change.
3. Maintenance can be planned releases/deployments or unplanned ones (hot fixes).

## Verify
Each maintenance release lists its trigger, impact analysis result and the regression scope chosen from it.

## Checked
2026-11-01. Confirmed against ISTQB CTFL Syllabus v4.0.1 (2024-09-15), section 2.3: the three triggers, data conversion on migration, archiving and restore on retirement, scope factors, impact analysis, planned vs hot-fix releases. Removed (not in the syllabus): configuration-change trigger, retirement checklist, characterization-test and traceability gotchas, glossary source.
Method: documentation only; no commands were run.
