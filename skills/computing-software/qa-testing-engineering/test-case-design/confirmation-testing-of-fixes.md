---
id: computing-software.qa-testing-engineering.test-case-design.confirmation-testing-of-fixes
name: confirmation-testing-of-fixes
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [retesting, fix-verification, confirmation-testing, defect-closure, regression-around-fix]
level: practitioner
status: docs-checked
description: "Confirm a defect fix properly: rerun the original failing scenario on the fixed build, vary around it, check related paths and add a regression test."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Confirmation testing (retesting) of fixes

**Goal:** know the defect is really fixed, not just that the exact original click path no longer fails. ISTQB CTFL v4.0 2.2.3.

## Procedure
1. Check the fixed build is the one deployed (version endpoint / build number) and the fix commit is in it.
2. Rerun the **exact original steps and data**. Expected result now observed.
3. **Vary around it**: other inputs in the same partition, adjacent boundaries, other browsers/roles the bug might apply to, the same code path reached from another screen.
4. Check the **side-effects**: data written correctly, no duplicate records, logs clean.
5. Ensure a **regression test** exists at the lowest sensible level (developer unit test or automated API/UI test). Link it on the ticket.
6. Close with evidence: build, steps, environment, test id.

## Reopen vs new defect
- Same symptom, same root cause: reopen.
- Fix works but caused a different failure: new defect linked to the original (regression caused by fix).

## Gotchas
- "Cannot reproduce anymore" on an intermittent defect is not confirmation; repeat enough times to show the failure no longer occurs.
- Cached assets/old service instances can make an unfixed bug look fixed or vice versa; hard reload, check all instances updated.

## Verify
The ticket shows the build verified, the variations checked and the linked regression test.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): section 2.2.3 (confirmation testing confirms the original defect is fixed; rerun the failed tests and add tests for changes made by the fix; scope depends on risk) and section 1.1 (confirmation preferably by the person who ran the original test).
Removed: the '1 in 10, run 30+' repetition figure.
Method: documentation only; no commands were run.
