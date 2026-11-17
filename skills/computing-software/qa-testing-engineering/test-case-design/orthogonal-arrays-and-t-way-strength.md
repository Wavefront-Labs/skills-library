---
id: computing-software.qa-testing-engineering.test-case-design.orthogonal-arrays-and-t-way-strength
name: orthogonal-arrays-and-t-way-strength
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [orthogonal-arrays, t-way-testing, combinatorial-testing, interaction-strength, nist-acts, covering-arrays]
level: practitioner
status: docs-checked
description: "Choose the interaction strength for combinatorial testing (2-way and above) using fault-interaction evidence, and know covering arrays vs orthogonal arrays."
sources:
  - https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software
  - https://www.nist.gov/publications/practical-combinatorial-testing
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orthogonal arrays and t-way strength

**Goal:** pick a combination strength justified by evidence, not habit. NIST *Practical Combinatorial Testing* (Kuhn, Kacker, Lei, 2010).

## Evidence
NIST describes combinatorial (t-way) testing as a proven method for better testing at lower cost. Take the failure-interaction statistics from the NIST project page and *Practical Combinatorial Testing* rather than from memory (not confirmed here). Higher t adds assurance for critical systems at the cost of more tests.

## Covering arrays vs orthogonal arrays
- **Orthogonal array** OA(N; t, k, v): every t-tuple appears the *same* number of times. Balanced; exists only for certain sizes, often larger.
- **Covering array** CA(N; t, k, v): every t-tuple appears *at least* once. Smaller, any size; what t-way generators such as NIST ACTS produce.
For testing, covering arrays are what you usually want.

## Size intuition
The number of tests grows quickly with the strength t; generate the array with a tool to see the real size for your model. (All combinations of 10 parameters with 4 values each is 4^10 = 1,048,576.)

## Choosing t
- Configuration/compatibility testing: 2-way baseline.
- Business-critical logic with many inputs: 3-way.
- Safety-critical, or interactions known to matter: 4-way+ on the relevant subset (mixed strength via sub-models).

## Tools
NIST ACTS is NIST's tool for t-way test generation (see the NIST ACTS project page); check its documentation for strength limits, constraints and coverage measurement.

## Gotchas
- Strength only covers combinations of the modelled values; poor partitioning undermines everything.
- Higher t without automation becomes too many tests to execute manually.

## Verify
Record the chosen t with rationale, and measure achieved t-way coverage with a tool.

## Checked

- Date: 2026-10-28
- Confirmed: NIST describes t-way testing as a proven method for better testing at lower cost; NIST ACTS project; Practical Combinatorial Testing by Kuhn, Kacker and Lei, published 2010 (NIST pages).
- Removed: the SP 800-142 number, the failure-interaction statistics, Taguchi attribution, PICT and allpairspy claims, test-count estimates, ACTS 6-way and PICT option claims. The 4^10 figure is arithmetic.

Method: documentation only; no commands were run.
