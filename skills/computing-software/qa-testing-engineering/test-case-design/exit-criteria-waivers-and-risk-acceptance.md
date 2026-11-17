---
id: computing-software.qa-testing-engineering.test-case-design.exit-criteria-waivers-and-risk-acceptance
name: exit-criteria-waivers-and-risk-acceptance
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [criteria-waiver, risk-acceptance, exit-criteria, release-decision, test-management]
level: practitioner
status: draft
description: "Handle unmet exit criteria: waiver request content, residual risk statement, who may approve, conditions and follow-up, and auditable records."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Exit criteria waivers and risk acceptance

**Goal:** when an exit criterion is not met, the decision to ship anyway is explicit, made by someone with authority, and traceable.

## Waiver request contents
- Criterion not met and the measured value ("2 high-severity defects open vs threshold 0").
- Reason (late fix, environment unavailable, test blocked by third party).
- Residual risk: who is affected, how likely, worst-case impact, detection in production.
- Mitigations: workaround, feature flag off, monitoring/alerts, support briefing, hotfix plan with date.
- Conditions: what must happen after release (fix by version X, re-test, retrospective).
- Expiry: waiver valid for this release only.

## Approval
- The approver is the business risk owner (product owner, release manager, or for regulated systems the quality/compliance authority), not the test team. QA provides the information and a recommendation.
- Record in the release ticket or change request with name, date and the risk statement accepted.

## Follow up
- Track waiver conditions as tickets with owners; review at the next release whether they were met.
- Count waivers per release: a rising trend means criteria are unrealistic or quality is slipping, both worth a retrospective.

## Verify
Every release with an unmet criterion has a waiver record with risk statement, approver and conditions, and conditions are tracked to closure.
