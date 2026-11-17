---
id: computing-software.qa-testing-engineering.test-case-design.organisational-test-policy-and-strategy
name: organisational-test-policy-and-strategy
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-strategy-document, test-policy, test-strategy, iso-29119, test-process]
level: practitioner
status: draft
description: "Write an organisational test policy and test strategy: objectives, levels, approaches, entry/exit norms, tooling and metrics that project test plans inherit."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iso.org/standard/81291.html
  - https://softwaretestingstandard.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Organisational test policy and test strategy

**Goal:** set the testing rules once at organisation level so project test plans tailor rather than reinvent. ISO/IEC/IEEE 29119-2/-3 define the documents.

## Test policy (1-2 pages, rarely changes)
- Why the organisation tests and what quality means here (link to business goals).
- Test process framework adopted (e.g. 29119, ISTQB terms).
- Roles and independence expectations; training and certification.
- How test effectiveness is evaluated (escaped defects, change failure rate).
- Improvement approach (retrospectives, TMMi/TPI assessments).

## Test strategy (organisational, per product line)
| Section | Content |
|---|---|
| Risk approach | how product risks are identified and drive depth |
| Test levels and types | which levels exist, who owns each, mandatory non-functional types |
| Techniques | minimum techniques per level (e.g. BVA for validation, branch coverage >= 80% on new code) |
| Entry/exit norms | defaults projects inherit |
| Environments and data | tiers, data masking rules |
| Automation | pyramid targets, frameworks, CI gating |
| Defect management | severity scheme, workflow, SLAs |
| Metrics and reporting | standard dashboard |
| Deviations | how a project gets a waiver |

## Process
Draft with QA leads, review with engineering and product heads, publish versioned, review yearly or after a major incident.

## Gotchas
- A strategy nobody can deviate from gets ignored; define the waiver path.
- Keep it about *what and why*; tools change, so name them in an appendix.
- Agile teams still need it: it becomes the team working agreements and Definition of Done.

## Verify
A sampled project test plan references the strategy and lists its deviations explicitly.
