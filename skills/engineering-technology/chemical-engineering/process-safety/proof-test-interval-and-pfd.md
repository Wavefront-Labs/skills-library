---
id: engineering-technology.chemical-engineering.process-safety.proof-test-interval-and-pfd
name: proof-test-interval-and-pfd
category: engineering-technology
field: chemical-engineering
product: process-safety
tags: [chemical-engineering, process-safety, ps-lopa-and-sil, proof-test-interval-and-pfd, proof-test-interval, pfdavg, 1oo2, 2oo3, common-cause-beta, proof-test-coverage, lambda-du, safety-instrumented-function, mttr]
level: advanced
status: gated
description: "Calculate PFDavg for SIF architectures (1oo1, 1oo2, 2oo3) from failure rates, proof test interval, coverage and common cause, and choose the test interval to meet a target."
sources:
  - "https://webstore.iec.ch/"
  - "https://www.aiche.org/ccps"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proof test interval and PFDavg

**Goal:** a test interval and architecture that meet the target PFDavg, with arithmetic you can check. Final SIL verification must be done by competent functional safety engineers using validated tools and data (IEC 61511).

## Simplified equations (low demand, constant failure rates; per IEC 61508 Part 6 style approximations)
The forms below were re-derived by numerical integration of unavailability over one test interval (independent channels): 1oo2 gives (lambda_DU TI)^2/3, 2oo3 gives about (lambda_DU TI)^2 (3 (lambda t)^2 less a small cubic term) and the imperfect-test form matches to 5 digits. The wording of IEC 61508-6 itself is paywalled (gated: unconfirmed, source is paywalled or blocked).
- **1oo1**: PFDavg = lambda_DU TI/2 (plus a small term from detected failures if repair time is long).
- **1oo2**: PFDavg = [(1 - beta) lambda_DU TI]^2/3 + beta lambda_DU TI/2.
- **2oo3**: PFDavg = [(1 - beta) lambda_DU TI]^2 + beta lambda_DU TI/2.
- **Imperfect proof test** (coverage C, full test or replacement interval LT): PFDavg(1oo1) = lambda_DU [ C TI/2 + (1 - C) LT/2 ].
Here lambda_DU is the dangerous undetected failure rate (per hour, converted to per year consistently), beta the common cause factor (often 1 to 10% by checklist (gated: unconfirmed, source is paywalled or blocked)).

## Worked example
lambda_DU = 0.01 per year per channel, TI = 1 year, beta = 0.05.
- 1oo1: 0.01 x 1/2 = 5e-3.
- 1oo2: [(0.95)(0.01)(1)]^2/3 = 3.0e-5, plus 0.05 x 0.01/2 = 2.5e-4, total about 2.8e-4 (recomputed: 2.80e-4). The common cause term dominates, so adding redundancy beyond this gains little unless beta falls.
- Halving TI to 0.5 year in 1oo1: 2.5e-3.

## Choosing TI
1. Target PFDavg from the required SIL.
2. Solve for TI at the selected architecture; practical TI aligns with turnarounds and online test capability (partial stroke testing of valves adds partial coverage; credit it only with documented coverage).
3. Reconcile with the maintenance plan; the test procedure must reflect the SRS and cover the full loop from sensor to final element.

## Gotchas
- Mixing units (per hour versus per year) is the classic error.
- Test coverage below 100% for final elements (valve leakage, stroke time) must be accounted for.
- Bypasses during testing need compensating measures.

## Verify
- [ ] Hand calculation matches software within a small tolerance.
- [ ] Test interval and coverage assumptions are in the maintenance plan.
