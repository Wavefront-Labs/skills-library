---
id: computing-software.qa-testing-engineering.test-case-design.testing-roles-and-responsibilities
name: testing-roles-and-responsibilities
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-manager-role, testing-roles, test-management, raci, test-organisation]
level: practitioner
status: draft
description: "Define test management and testing roles: test manager vs tester duties, a RACI across activities, and how roles map onto agile teams."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing roles and responsibilities

**Goal:** make it explicit who plans, designs, executes and decides. CTFL v4.0 1.4.5 separates the **test management role** from the **testing role**; one person may hold both.

## Test management role
Test planning and strategy alignment, monitoring and control, estimation, risk management with stakeholders, reporting, defect process ownership, coordinating environments and resources, completion activities.

## Testing role
Test analysis, design, implementation, execution, automation, reporting defects, reviewing test basis and peers' tests.

## RACI example
| Activity | Test manager | Tester | Developer | Product owner |
|---|---|---|---|---|
| Test plan | A/R | C | C | C |
| Risk analysis | A | R | R | R |
| Test design | C | A/R | C | C |
| Unit tests | I | C | A/R | - |
| Acceptance criteria | C | R | C | A |
| Go/no-go recommendation | R | C | C | A (decides) |
| Defect triage | A | R | R | R |

## In agile teams
No separate test manager per team: management tasks spread across the team, Scrum Master and a QA chapter lead (strategy, coaching, cross-team metrics). Testers act as quality coaches; developers own unit/component tests.

## Gotchas
- Testers recommend, product owners/business decide release; never let QA be the sole gate.
- Unclear ownership of environments and test data is the most common source of blocked testing; give them an owner.
- Independence (who tests whose work) is a separate decision from role assignment.

## Verify
For each activity in the test plan, one Accountable person is named and known to the team.
