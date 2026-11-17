---
id: computing-software.qa-testing-engineering.test-case-design.fmea-product-risk-analysis
name: fmea-product-risk-analysis
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [fmea, failure-mode-effects-analysis, product-risk-analysis, rpn, risk-based-testing, istqb-ta]
level: advanced
status: draft
description: "Use FMEA for product risk analysis: list failure modes per function, rate severity, occurrence and detection, compute RPN or action priority, and derive tests."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta
  - https://asq.org/quality-resources/fmea
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FMEA for product risk analysis

**Goal:** a structured, bottom-up risk analysis for safety- or money-critical systems, where every function's ways of failing are listed and ranked, and tests target the worst.

## Worksheet columns
Function/item | Failure mode | Effect | Severity (S 1-10) | Cause | Occurrence (O 1-10) | Current controls | Detection (D 1-10, 10 = unlikely to detect) | RPN = S x O x D | Recommended action/tests | Owner | Revised S/O/D.

## Method
1. Decompose the system into functions or components (from requirements or architecture).
2. For each, brainstorm failure modes with dev, ops and domain experts: no output, wrong output, late output, partial output, intermittent, unintended output.
3. Rate with agreed scale definitions (write them down, especially for Detection).
4. Rank by RPN, but also treat any Severity 9-10 as high regardless of RPN (AIAG-VDA FMEA replaces RPN with Action Priority tables partly for this reason).
5. For top items define actions: tests (techniques and depth), design changes, monitoring that improves detection.
6. Re-rate after actions to show risk reduction.

## Example row
Payment capture | double charge on retry | customer charged twice | S 9 | non-idempotent retry | O 4 | none | D 7 | RPN 252 | idempotency tests, concurrent duplicate test, reconciliation alert | owner: payments QA.

## Tips
- Time-box sessions; FMEA is expensive, so use it for critical subsystems, lighter risk matrices elsewhere.
- Link each test to the FMEA row so coverage of high-risk failure modes is reportable.

## Verify
Every function has failure modes rated with documented scales, all high-severity or high-RPN rows have linked tests or actions, and revised ratings are recorded.
