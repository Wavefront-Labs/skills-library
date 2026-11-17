---
id: computing-software.qa-testing-engineering.test-case-design.residual-risk-reporting
name: residual-risk-reporting
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [residual-risk, risk-based-testing, test-reporting, release-readiness, risk-coverage]
level: practitioner
status: draft
description: "Report residual risk at a milestone: per-risk test coverage, outcomes and open defects, what remains untested, and a clear recommendation stakeholders can act on."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iso.org/standard/81291.html
  - https://www.istqb.org/certifications/test-manager
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reporting residual risk

**Goal:** tell decision makers what risk remains if they release now, in their language, not as test counts.

## Per-risk status
| Risk | Level | Tests planned/run/passed | Open defects (sev) | Untested | Residual | Note |
|---|---|---|---|---|---|---|
| R3 VAT miscalc EU B2B | H | 42/42/40 | 1 major | none | Medium | 2 failing cases: reverse-charge for NO; fix in 1.4.1 |
| R7 checkout perf at peak | H | 3/2/2 | 0 | soak test | Medium | 8h soak not run, env unavailable |
| R12 avatar upload | L | 4/4/4 | 0 | none | Low | |

Residual risk = original level adjusted by evidence: passed rigorous testing lowers it; failures, gaps and untested areas keep it high.

## Content of the report
1. Headline: recommendation (release / release with conditions / do not release) in one sentence.
2. Risks that remain high or medium, each with consequence, workaround and owner.
3. What was not tested and why (descoped, blocked, environment).
4. Open defects mapped to risks (not just a count by severity).
5. Conditions: monitoring, feature flag, rollback plan, follow-up fix date.

## Visuals
Risk matrix before vs after testing (dots moved); a stacked bar per risk area of covered/failed/untested.

## Gotchas
- "98% pass rate" hides the 2% that matter; always tie failures to risks.
- Reporting no residual risk is not credible; there is always some.
- The release decision belongs to the business owner; the tester provides the information and a recommendation.

## Verify
Every high risk from the register appears with evidence, untested areas are explicit, and the owner signed off the decision with the report attached.
