---
id: computing-software.qa-testing-engineering.exploratory-testing.session-notes-and-debrief
name: session-notes-and-debrief
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [session-notes, session-debrief, proof-debrief, session-based-test-management, exploratory-testing, sbtm-metrics, session-sheets]
level: practitioner
status: draft
description: "Take exploratory session notes and run the debrief with PROOF (Past, Results, Obstacles, Outlook, Feelings), recording TBS time split, bugs, issues and coverage."
sources:
  - https://www.satisfice.com/download/session-based-test-management
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Session note taking and debrief (PROOF)

**Goal:** make exploratory work accountable and reusable: notes that someone else can read, and a debrief that turns them into decisions. Jonathan and James Bach, Session-Based Test Management.

## Session sheet
```
CHARTER: Explore discount codes with stacking and expiry to discover pricing errors
TESTER: ana   START: 2026-10-16 10:00   DURATION: normal (90 min)
TASK BREAKDOWN: test 60% / bug investigation 25% / setup 15%   CHARTER vs OPPORTUNITY: 80/20
DATA FILES: codes.csv, basket-fixtures.json
TEST NOTES:
10:05 applied SAVE10 + FREESHIP in both orders -> totals differ (BUG-1)
10:20 expired code at midnight UTC vs local: rejected 1h early in BST (BUG-2)
10:40 tried 50 codes: UI slows after ~20 (ISSUE-1: is there a max?)
BUGS: BUG-1, BUG-2 (raised as SHOP-812, SHOP-813)
ISSUES: ISSUE-1 max codes undefined; ISSUE-2 admin export lacks code column
```
Notes are timestamped, factual, include data used and oracles; a test idea not tried goes under issues/follow-ups.

## Note-taking techniques
- Write as you go; use a template with shortcuts (`B:` bug, `Q:` question, `I:` idea).
- Screen recording or Rapid Reporter/TestBuddy-style tools for capture.
- Mind maps for coverage.

## PROOF debrief (10-20 min with a lead)
- **Past**: what happened during the session?
- **Results**: what was achieved, bugs found?
- **Obstacles**: what got in the way (environment, data, unclear requirement)?
- **Outlook**: what still needs doing; follow-up charters?
- **Feelings**: how does the tester feel about the area's quality and their coverage?

## After the debrief
- File bugs, raise issues with owners, create follow-up charters.
- Aggregate TBS (test, bug, setup) and coverage across sessions; high setup % signals environment problems.

## Gotchas
- Debriefs skipped "because busy" lose half the value.
- Notes only the tester can read; write for the next tester.

## Verify
Each session has a completed sheet, a debrief within a day, and follow-ups tracked to charters or tickets.
