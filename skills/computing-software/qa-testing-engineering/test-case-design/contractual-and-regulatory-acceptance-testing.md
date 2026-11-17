---
id: computing-software.qa-testing-engineering.test-case-design.contractual-and-regulatory-acceptance-testing
name: contractual-and-regulatory-acceptance-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [contractual-acceptance-testing, regulatory-acceptance-testing, acceptance-testing, test-levels, compliance-testing]
level: practitioner
status: draft
description: "Plan contractual and regulatory acceptance testing: acceptance criteria from the contract or regulation, witness tests, evidence packs and sign-off."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-principles-software-validation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contractual and regulatory acceptance testing

**Goal:** prove formally that the system meets a contract or a regulation, with evidence that survives an audit or a dispute. CTFL v4.0 2.2.1 acceptance testing forms.

## Contractual acceptance
- **Basis:** the contract's acceptance criteria, statement of work, SLAs. Extract every "shall" into a numbered criteria list agreed by both parties before testing starts.
- **Plan:** acceptance test specification reviewed and signed by the customer; entry criteria (system test complete, defect thresholds).
- **Execution:** customer representatives witness or execute; results signed per test; deviations logged with severity and agreed disposition (fix before acceptance, accept with concession, out of scope).
- **Exit:** acceptance certificate; often triggers payment, so define "accepted with open minor defects" precisely.

## Regulatory acceptance
- **Basis:** the regulation or standard (FDA 21 CFR Part 11 and software validation guidance, IEC 62304, EU MDR, PCI DSS, SOX controls, DO-178C, accessibility law).
- Map each applicable clause to requirements and tests (traceability matrix is the core artefact).
- Validate the process too: controlled test scripts, version-controlled environments, tool qualification where required, independent review.
- Evidence: executed scripts with signature/date, screenshots or logs, deviation reports, summary report referencing the regulation.

## Practice
1. Do a dry run internally before the witnessed run.
2. Freeze build and environment configuration for the formal run; record hashes.
3. Pre-agree how to handle a failure mid-run (stop, continue, retest window).

## Gotchas
- Vague contract criteria ("user friendly", "fast") must be made measurable before signing the test spec.
- Changing test scripts during a formal run invalidates them; raise a deviation instead.
- Auditors check ALCOA+ principles for records (attributable, legible, contemporaneous, original, accurate).

## Verify
Every contractual/regulatory clause traces to an executed, signed test or a documented rationale for non-applicability.
