---
id: computing-software.qa-testing-engineering.test-case-design.quality-assurance-vs-quality-control
name: quality-assurance-vs-quality-control
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [qa-vs-qc, quality-control, quality-assurance, testing-principles, process-improvement]
level: practitioner
status: docs-checked
description: "Separate quality assurance (process-oriented, preventive) from quality control (product-oriented, testing) and assign each to the right people and activities."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quality assurance vs quality control

**Goal:** stop calling every tester "QA" without knowing what each activity achieves. CTFL v4.0 1.2.2.

## Definitions
| | Quality assurance | Quality control |
|---|---|---|
| Focus | the **process** | the **product** |
| Nature | preventive | corrective |
| Question | are we building it the right way so defects do not occur? | does this build meet requirements? |
| Examples | coding standards, review process, Definition of Done, training, retrospectives, process audits, CI gates design | testing, formal methods (model checking, proof of correctness), simulation, prototyping |
| Owner | everyone; QA lead/process owner facilitates | testers, developers, reviewers |

Testing is a form of quality control. Test **results** feed QA: defect trends and root causes show which process to fix.

## Applying it
1. List current quality activities and tag each QA or QC.
2. If nearly everything is QC late in the cycle, add QA: requirement reviews, pairing, static analysis in the IDE, DoD criteria.
3. Close the loop: monthly root cause review of escaped defects -> one process change -> measure.

## Gotchas
- A "QA team" that only executes tests at the end is doing QC; expect late, expensive findings.
- QA does not mean "the testers are responsible for quality"; quality is a whole-team responsibility.
- Audits checking that a process was followed (QA) do not prove the product works (QC); you need both.

## Verify
Each escaped defect review produces a process action (QA), not only a new test case (QC).

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): section 1.2.2 (testing is product-oriented and corrective, a major form of quality control; QA is process-oriented, preventive, the responsibility of everyone; test results feed QA as process feedback).
Removed: the unfetched ASQ and glossary sources, and the 'detective' label.
Method: documentation only; no commands were run.
