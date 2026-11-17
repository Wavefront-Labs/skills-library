---
id: creative-arts.game-design.playtesting-and-balance.affinity-mapping-and-issue-severity
name: affinity-mapping-and-issue-severity
category: creative-arts
field: game-design
product: playtesting-and-balance
tags: [game-design, playtesting-and-balance, affinity-mapping, issue-severity, synthesis, usability, severity-rating, playtest-analysis]
level: practitioner
status: draft
description: "Cluster raw playtest observations into themes with affinity mapping, then rate each issue's severity and frequency so the fix list is ordered by evidence, not by loudness."
sources:
  - https://www.gdcvault.com
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Affinity mapping and issue severity

**Goal:** turn a pile of sticky notes and session logs into a ranked list of problems.

## Procedure
1. **One observation per note.** Write what happened ("tester 4 placed the token and asked what the red die was"), not an interpretation or a fix.
2. **Silent grouping:** the team sorts notes into clusters without talking first, then names each cluster with a short problem statement ("players cannot tell whose turn it is").
3. **Merge and split** clusters until each has one cause; record how many distinct testers contributed (not how many notes).
4. **Rate severity per issue.** A common scale is Jakob Nielsen's usability severity rating: 0 not a problem, 1 cosmetic, 2 minor, 3 major, 4 usability catastrophe. Rate frequency (how many testers) and impact (blocks play, causes errors, only annoys) separately, then combine.
5. **Order the backlog:** blockers and high-frequency issues first; cheap fixes alongside. Mark each issue with its source sessions so engineers or rule writers can check the evidence.
6. **Separate problems from solutions.** Keep suggested fixes in a different column and test them in the next round.

## Gotchas
- Raters should score independently before discussing; seniority skews group scores.
- One vivid tester is not a pattern; count testers, not volume.
- Clusters named after solutions ("add a tutorial") hide the actual problem.

## Verify
- [ ] Every cluster lists tester count and source sessions.
- [ ] Severity and frequency recorded separately.
- [ ] Top issues map to a planned change and a re-test.
