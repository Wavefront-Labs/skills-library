---
id: computing-software.qa-testing-engineering.exploratory-testing.duplicate-and-cannot-reproduce-defect-handling
name: duplicate-and-cannot-reproduce-defect-handling
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [duplicate-defects, cannot-reproduce, wont-fix, defect-triage, defect-management]
level: practitioner
status: draft
description: "Handle duplicates, cannot-reproduce and won't-fix defects: search before filing, linking, reproduction attempts, closure rules and periodic review of closed-not-fixed bugs."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.satisfice.com/rapid-testing-methodology
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Duplicate, cannot-reproduce and won't-fix handling

**Goal:** close non-actionable defects cleanly without losing real information or hiding a real problem.

## Duplicates
- **Before filing:** search the tracker by error text, component, screen and recent dates (`text ~ "timeout" AND component = Checkout AND created >= -30d`).
- When duplicate: link (`duplicates` / `is duplicated by`), close the newer one with resolution Duplicate, and copy any new evidence (other browser, new steps, more frequency) onto the master. Multiple reports raise the master's priority signal.
- Same symptom, different cause is not a duplicate; when unsure, keep both and link as "relates to".

## Cannot reproduce
1. Ask for missing context: exact build, environment, account/data, browser/device, time (for logs), video/HAR.
2. Attempt reproduction in the reporter's environment and with their data, not just locally.
3. Check logs and traces for the timestamp; the failure may be visible server-side even if not reproducible.
4. If still not reproducible: resolve as Cannot Reproduce with what was tried, and add monitoring or logging if the impact is high. Ask reporters to reopen with new evidence.
5. Intermittent but seen several times is not "cannot reproduce": track it as intermittent.

## Won't fix / works as designed
- Decision by the product owner, with the reason recorded (cost vs impact, planned redesign, intended behaviour).
- If "works as designed" but users keep hitting it, raise a usability or requirement change.
- Add to known issues if customers can encounter it.

## Review
Quarterly, review Cannot Reproduce and Won't Fix closures: recurring symptoms, rising frequency or new evidence reopen them.

## Verify
Closed duplicates are linked to a master, each Cannot Reproduce lists reproduction attempts, and Won't Fix items have an owner's recorded reason.
