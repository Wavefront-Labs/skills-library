---
id: computing-software.qa-testing-engineering.test-case-design.applying-the-seven-testing-principles
name: applying-the-seven-testing-principles
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [testing-principles, seven-testing-principles, pesticide-paradox, defect-clustering, testing-objectives, absence-of-errors-fallacy, istqb]
level: practitioner
status: docs-checked
description: "Use the seven testing principles as decision rules: defect clustering for focus, pesticide paradox for refreshing suites, context dependence and early testing for scope."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Applying the seven testing principles

**Goal:** turn the CTFL v4.0 1.3 principles into concrete planning decisions, not slogans.

| Principle | Decision it drives |
|---|---|
| 1. Testing shows the presence, not absence, of defects | Report residual risk, never "bug-free". |
| 2. Exhaustive testing is impossible | Choose techniques and prioritise by risk; state what is not tested. |
| 3. Early testing saves time and money | Review requirements and designs; test-first; static analysis in the pipeline. |
| 4. Defects cluster together | Pull defect counts per module from the tracker (last 2-3 releases) and put extra depth on the modules with the most defects (the syllabus links clustering to the Pareto principle). |
| 5. Tests wear out (pesticide paradox) | Regression suites that stay green for months find nothing new: vary data (property-based, randomised), add new tests from escaped defects, run exploratory sessions each release. |
| 6. Testing is context dependent | Safety-critical software is tested differently from, say, an e-commerce site. Do not copy strategies across contexts. |
| 7. Absence-of-defects fallacy | Validation matters: test against user needs (UAT, usability) not just the spec. |

## Gotchas
- Defect clustering is evidence-based only if defects are tagged with component; fix the tracker fields first.
- Pesticide paradox does not mean throw away regression tests; it means regression alone is not enough.

## Verify
Your test plan can point to at least one decision justified by each of principles 2, 4 and 5.

## Checked
Date 2026-11-01. Documentation release: ISTQB CTFL Syllabus v4.0.1, section 1.3 (downloaded PDF).
Confirmed: the seven principles and their order, Pareto link for defect clustering, absence-of-defects fallacy. Removed unconfirmed claims: the 20% figure, the git-churn command, and the MC/DC example.
Method: documentation only; no commands were run.
