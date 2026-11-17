---
id: computing-software.qa-testing-engineering.test-case-design.hotfix-and-emergency-change-testing
name: hotfix-and-emergency-change-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [hotfix-testing, emergency-change-testing, regression-testing, confirmation-testing, change-management]
level: practitioner
status: docs-checked
description: "Test a production hotfix fast and safely: reproduce, confirm the fix, targeted regression, deploy verification, and the retrospective backfill afterwards."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://sre.google/sre-book/emergency-response/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hotfix and emergency change testing

**Goal:** shorten the cycle without skipping the checks that prevent a second incident.

## Minimum path
1. **Reproduce** the failure on the production version (same build tag) in a non-production environment; capture the failing input as an automated test.
2. **Branch from the released tag**, not from main, so unreleased changes do not ride along.
3. **Confirmation test:** the new test fails before the fix, passes after.
4. **Targeted regression:** change impact analysis on the diff; run unit/API tests for touched modules plus the smoke suite and the critical-journey E2E set.
5. **Peer review** of code *and* of the test evidence; emergency changes still get a second pair of eyes.
6. **Deploy with a safety net:** canary or staged rollout, feature flag if possible, rollback plan written and tested.
7. **Verify in production:** synthetic check or log/metric query showing the error rate drop.

## Afterwards (within days)
- Merge the fix forward into main; run the full regression pack there.
- Record the emergency change per change-management policy.
- Retro: why did tests miss it? Add the missing test at the cheapest level.

## Decision aid: hotfix vs wait
Hotfix when impact (users, money, security, data) outweighs the risk of an under-tested change; otherwise mitigate (flag off, config change, rollback) and fix in the normal release.

## Gotchas
- Most hotfix incidents come from fixing on main and shipping unrelated changes.
- Data corruption bugs need a data repair plan tested too, not only a code fix.
- Skipped checks must be listed in the change record so the risk is visible.

## Verify
The hotfix PR shows: reproduction test, impact-based regression run, reviewer approval, rollback plan, and production verification evidence.

## Checked

2026-10-28. Confirmed: Process steps are judgement; the SRE Book emergency-response page was read and makes no figure claims used here. Removed: The "typical budget 15-60 min" figure and the "CAB retroactive approval" detail.

Method: documentation only; no commands were run.
