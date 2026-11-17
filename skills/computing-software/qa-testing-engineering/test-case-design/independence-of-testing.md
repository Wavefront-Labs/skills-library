---
id: computing-software.qa-testing-engineering.test-case-design.independence-of-testing
name: independence-of-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [independence-of-testing, tester-independence, testing-principles, istqb, author-bias, independent-verification, ivv]
level: practitioner
status: docs-checked
description: "Choose the right level of test independence: developer, peer, team tester, separate test team, external IV&V. Balance bias reduction against communication cost."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Independence of testing

**Goal:** reduce author bias where it matters without isolating testers from the team. ISTQB CTFL v4.0 1.5.3.

## Levels (low to high)
The syllabus names four levels:
1. Author tests own work (no independence).
2. Peers from the same team (some independence).
3. Testers from outside the author's team but within the organisation (high independence).
4. Testers from outside the organisation (very high independence).

## Choosing
- Use several levels together (syllabus example): developers perform component and component integration testing, the test team performs system and system integration testing, business representatives perform acceptance testing.
- A higher level of independence may be needed in some situations, such as safety-critical systems.
- Independence does not replace familiarity: developers can efficiently find many defects in their own code.

## Benefits and drawbacks
- Benefit: independent testers are likely to recognise different kinds of failures and defects, and can verify, challenge or disprove stakeholders' assumptions.
- Drawbacks: isolation from the development team (poor collaboration, communication problems, adversarial relationship), developers may lose a sense of responsibility for quality, and testers may be seen as a bottleneck or blamed for delays.

## Gotchas
- Independence is about who decides what to test and judges the result, not about sitting in a different building.

## Verify
For each high-risk area, the plan names at least one tester who did not build it.

## Checked
Date 2026-11-01. Documentation release: ISTQB CTFL Syllabus v4.0.1, section 1.5.3 (downloaded PDF).
Confirmed: section number, independence levels, benefits, drawbacks, multiple-levels example. Corrected the five-level list to the syllabus's four. Removed unconfirmed claims: named regulatory standards and the external-team remark.
Method: documentation only; no commands were run.
