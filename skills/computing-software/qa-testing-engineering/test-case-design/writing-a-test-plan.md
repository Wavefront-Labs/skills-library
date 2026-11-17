---
id: computing-software.qa-testing-engineering.test-case-design.writing-a-test-plan
name: writing-a-test-plan
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-plan, test-planning, test-process, testware, istqb, ieee-29119-3, test-strategy, scope, test-approach]
level: practitioner
status: docs-checked
description: "Write a lean, useful test plan: context, scope in/out, approach per risk, environments, entry/exit criteria, schedule, roles and the risks to the plan itself."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Writing a test plan

**Goal:** a plan people actually read, that records the decisions (what, how deep, who, when) and the assumptions they rest on.

## Sections that earn their place
1. **Context**: release/feature, test basis documents (with versions), stakeholders.
2. **Scope**: in scope and, more importantly, explicitly *out* of scope (with the reason: covered elsewhere, low risk, not testable yet).
3. **Risk register summary**: top product risks and the test depth each gets (link the full risk analysis, see `risk-matrix-likelihood-impact`).
4. **Approach**: per test level and test type, which techniques, automated vs manual, which tool. A table works:

| Area | Risk | Level | Technique | Automated? | Owner |
|---|---|---|---|---|---|
| Payments | High | System + API | BVA, decision table | API yes, UI smoke | QA-A |
| Profile edit | Low | System | EP, exploratory charter | no | QA-B |

5. **Environments and data**: which env, refresh cadence, test accounts, third-party sandboxes.
6. **Entry / exit / suspension criteria** (measurable).
7. **Schedule and milestones**, tied to dev milestones, not calendar dates alone.
8. **Deliverables**: reports, defect summary, completion report.
9. **Project risks**: risks to the testing itself (env late, key tester leaving) with mitigations.

## Gotchas
- A plan copied from a template with every heading filled is a smell. Delete sections that carry no decision.
- Agile teams: a one-page plan per release plus per-story acceptance criteria beats a 40-page document. The decisions still need writing down.
- Version the plan with the code (Markdown in the repo) so changes are reviewable.
- Get sign-off from the people who own the risks (product owner), not just QA management.

## Verify
Hand the plan to a new team member: can they say what will not be tested and why, and when testing ends? If not, the plan is missing decisions.

## Checked

2026-10-28. Confirmed: Section list is judgement; no source-specific claims remain. Removed: Syllabus section number and the ISO/IEC/IEEE 29119-3 structure attribution (ISO page blocked).

Method: documentation only; no commands were run.
