---
id: computing-software.qa-testing-engineering.test-automation.owasp-asvs-and-wstg-test-basis
name: owasp-asvs-and-wstg-test-basis
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [owasp-asvs, owasp-wstg, security-requirements, security-test-plan, security-testing]
level: advanced
status: draft
description: "Use OWASP ASVS as security requirements and WSTG as the test method: pick a level, map requirements to tests, track coverage and record evidence."
sources:
  - https://owasp.org/www-project-application-security-verification-standard/
  - https://owasp.org/www-project-web-security-testing-guide/
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Using OWASP ASVS and WSTG as a test basis

**Goal:** turn "test the security" into a finite, auditable checklist: ASVS says *what* must be true, WSTG says *how* to test it.

## Pick the ASVS level
- **L1:** baseline for all apps; largely testable black-box.
- **L2:** apps handling sensitive or personal data; the usual target.
- **L3:** high-value (banking, health, critical infrastructure); needs design review and code access.

Agree the level with the product owner and security lead; it becomes the security acceptance criteria.

## Build the test matrix
1. Download the ASVS requirement list (CSV/JSON in the OWASP repo). Filter to your level and drop chapters that do not apply (e.g. no GraphQL) with a written reason.
2. Per requirement add: WSTG test ID(s) (e.g. ASVS session requirements map to WSTG-SESS-01..), technique (automated scan, manual, code review, config review), owner, status, evidence link.
3. Feed automatable items into the pipeline: ZAP baseline/API scan, dependency scanning, header checks, SAST rules.
4. Manual items go into exploratory charters with WSTG as the guide ("WSTG-ATHZ-02 bypass authorization schema, as roles X and Y").

## Running it
- Re-test requirements touched by each release; full pass before major releases or annually.
- Record failures as defects with the ASVS ID in the title so coverage and defect data join.
- Report: pass/fail/not-applicable count per ASVS chapter.

## Gotchas
- ASVS is requirements, not a pentest script; verification without evidence does not count.
- Check that the ASVS version cited in contracts matches the one you test against (IDs changed between 4.0 and 5.0).

## Verify
Every in-level ASVS requirement has status and evidence or a justified not-applicable, and failed items link to defects.
