---
id: creative-arts.game-design.playtesting-and-balance.rite-method-testing
name: rite-method-testing
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, rite-method, games-user-research, rapid-iterative-testing, usability-test, microsoft-games-user-research, iteration, playtesting]
level: advanced
status: draft
description: "Run RITE (Rapid Iterative Testing and Evaluation): fix issues between participants as soon as they are clear, with decision-makers observing, to converge on a usable design in days."
sources:
  - https://www.microsoft.com/en-us/research/publication/using-the-rite-method-to-improve-products-a-definition-and-a-case-study/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RITE method testing

**Goal:** fix usability problems during a test series rather than after it, so each new
participant tests an improved build.

RITE (Rapid Iterative Testing and Evaluation) was described by Medlock, Wixon, Terrano,
Romero and Fulton (Microsoft, 2002), with a case study on the tutorial of *Age of Empires
II*. Changes are made as soon as a problem and its fix are clear - sometimes after a
single participant.

## Requirements
- **Decision-makers observe** every session (designer, producer) so changes are agreed
  immediately.
- **The team can change the build quickly** (between participants or overnight).
- **Clear task-based goals** (usually onboarding/tutorial or UI flows).
- **A usability specialist** to judge when a problem is clear enough to fix.

## Procedure
1. Define tasks and success criteria (as in standard usability testing).
2. Schedule participants with buffers between them for fixes.
3. After each participant, the team reviews issues:
   - Obvious cause and obvious fix -> change now.
   - Unclear cause -> wait for more participants.
4. Track each issue: first seen, fix applied, whether it recurred after the fix.
5. Continue until several participants in a row complete tasks without serious issues.
6. Report the issue/fix timeline.

## Issue tracking table
| Issue | Seen in P# | Fix | Applied before P# | Recurred? |
|---|---|---|---|---|
| players miss the build menu | 1, 2 | pulse icon + prompt | 3 | no |

## Gotchas
- Fixes can introduce new problems; that's why later participants still matter.
- Not suited to questions about fun or balance (need many unchanged sessions).
- Without decision-makers present, RITE degrades to slow normal testing.

## Verify
- [ ] Decision-makers attended sessions.
- [ ] Issue tracking table with fix and recurrence columns.
- [ ] Final participants completed tasks without serious issues.
