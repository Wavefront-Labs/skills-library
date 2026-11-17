---
id: computing-software.qa-testing-engineering.test-case-design.testing-vs-debugging-handoff
name: testing-vs-debugging-handoff
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [testing-vs-debugging, defect-root-cause-analysis, testing-principles, failure-vs-defect, debugging, istqb]
level: practitioner
status: docs-checked
description: "Separate testing (finding failures) from debugging (finding and fixing the defect), and hand off failures with the evidence developers need to debug fast."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing vs debugging: the hand-off

**Goal:** testers trigger and characterise failures; developers locate and fix defects; testers confirm the fix. ISTQB CTFL v4.0 1.1.2, 1.2.3 (error -> defect -> failure; root cause).

## Vocabulary that keeps reports precise
- **Error (mistake)**: human action. **Defect (fault, bug)**: in the work product. **Failure**: observed deviation at run time. **Root cause**: why the error happened.
- A failure can also come from environment conditions (disk full, wrong config): check those before reporting a code defect.

## What to hand over
1. Exact build, environment, configuration, user/role, data.
2. Steps to reproduce, minimal (see `minimal-reproduction-reduction`).
3. Expected vs actual, with the oracle (spec section, previous version behaviour).
4. Evidence: screenshot/video, HAR, console errors, server log lines with timestamp and request/correlation id, trace id.
5. Narrowing done: which inputs/browsers/versions do and do not fail; first bad build if known (`git-bisect-regression-isolation`).

## After the fix
- **Confirmation test**: rerun the exact failing scenario on the fixed build.
- **Regression around the fix**: neighbours of the changed code.
- **Root cause analysis** for severe or repeated defects: classify the cause (requirement, design, code, environment) and feed it to prevention (`defect-prevention-rca-five-whys`).

## Gotchas
- Testers "debugging" deep into code can be valuable, but report the observed failure first so the clock starts.
- Fix verified only on the developer's machine is not confirmation testing.

## Verify
Developers rarely need to ask follow-up questions on your reports; track that informally.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): sections 1.1.2 and 1.2.3 (testing triggers failures; debugging reproduces, diagnoses and fixes; confirmation then regression testing; environment can cause failures; root cause analysis).
Removed: nothing.
Method: documentation only; no commands were run.
