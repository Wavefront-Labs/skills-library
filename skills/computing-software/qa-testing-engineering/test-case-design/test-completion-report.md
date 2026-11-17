---
id: computing-software.qa-testing-engineering.test-case-design.test-completion-report
name: test-completion-report
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-completion, test-completion-report, test-summary-report, test-process, lessons-learned, testware-archiving, istqb]
level: practitioner
status: draft
description: "Close a test phase properly: check exit criteria, write the completion report with residual risk, archive testware, hand over open defects and capture lessons learned."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iso.org/standard/79429.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Test completion and the completion report

**Goal:** a clean handover and a decision record. ISTQB CTFL v4.0 1.4.1 and 5.3.2; report contents from ISO/IEC/IEEE 29119-3.

## Activities
1. Check every exit criterion with numbers (coverage %, pass rate, open defects by severity).
2. Make sure every defect is closed, deferred with an owner, or converted to a backlog item.
3. Write the report.
4. Archive testware (test cases, scripts, data generators, environment config) with the build/version tested, so maintenance testing can reuse it.
5. Hand over: known issues to support/ops, automation to the team that owns regression.
6. Lessons learned / retrospective: what found defects, what wasted time, what escaped.

## Report skeleton
```
Test completion report: <release> (<build>)
Summary: recommendation (release / release with known issues / do not release) in one paragraph
Scope tested vs planned: deviations and why
Results: tests run/passed/failed/blocked; requirement and risk coverage
Defects: found, fixed, open by severity; notable open issues with workarounds
Residual risks: what was not tested or is weakly tested, and the consequence
Exit criteria: met / not met (with waivers and who approved)
Lessons learned: 3-5 concrete actions
```

## Gotchas
- Lead with the recommendation and residual risk. Stakeholders stop reading after the first paragraph.
- "All tests passed" with 40% of planned tests not run is not a pass. Report the not-run.

## Verify
A reader who was not involved can state what risk remains and who accepted it.
