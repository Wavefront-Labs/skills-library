---
id: computing-software.qa-testing-engineering.test-case-design.errors-defects-failures-and-root-causes
name: errors-defects-failures-and-root-causes
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [error-defect-failure, failure-causes, testing-principles, defect-taxonomy, istqb]
level: practitioner
status: docs-checked
description: "Use error, defect, failure and root cause correctly when analysing problems, including false positives/negatives and failures caused by the environment."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Errors, defects, failures and root causes

**Goal:** precise terms lead to the right fix. CTFL v4.0 1.2.3.

## Chain
**Root cause** (e.g. time pressure, ambiguous spec, unfamiliar API) -> **error/mistake** by a human -> **defect** (fault, bug) in a work product (requirement, design, code, test script) -> when executed under certain conditions -> **failure** (observable deviation from expected behaviour).

## Key points
- Not every defect causes a failure (dead code, condition never hit).
- Not every failure is caused by a defect in the code: environment (expired certificate, full disk), hardware, radiation/EMI, misconfiguration, or a defect in the **test** itself.
- A defect in the requirements produces a correct implementation of the wrong thing; tests derived from the same spec will pass.

## Applying it
When triaging a failure: reproduce, decide product vs test vs environment, then locate the defect (debugging), then ask why the error was made (root cause) and what process change prevents the class (defect prevention).

## Gotchas
- Reports should describe the failure (symptom) and not guess the defect unless evidenced.
- Counting "bugs" mixes defects and failures: one defect may produce many failure reports; deduplicate by defect.
- Root cause is a process/human factor, not "line 42"; line 42 is the defect location.

## Verify
Your defect records separate symptom (failure), location (defect) and root cause fields.

## Checked
2026-11-01. Confirmed against the ISTQB CTFL Syllabus v4.0.1 (2024-09-15): section 1.2.3 (error -> defect -> failure; defects in requirements, code, test scripts; some defects never cause a failure; environmental conditions such as radiation or electromagnetic fields can cause failures; root cause and root cause analysis).
Removed: the results vocabulary table and the unfetched glossary source.
Method: documentation only; no commands were run.
