---
id: creative-arts.game-design.systems-and-mechanics.boss-design-and-phases
name: boss-design-and-phases
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, boss-design, combat-design, boss-phases, attack-patterns, skill-test, arena-design, rogers, action-games]
level: practitioner
status: draft
description: "Design a boss fight as a test of what the level taught: attack pattern vocabulary, phases that escalate, arena use, checkpointing, and tuning for fairness."
sources:
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Boss design and phases

**Goal:** a boss that tests the skills the preceding section taught, with readable
patterns, escalating phases and a fair, memorable climax.

Rogers (Level Up!, boss chapter) treats bosses as final exams for a level's mechanics
and discusses patterns, weak points and the arena as part of the design.

## Procedure
1. **Write the exam:** which 2-3 skills or verbs from the level does this boss test?
   A boss requiring a skill never taught feels unfair.
2. **Attack vocabulary:** 3-5 attacks per phase, each with a distinct telegraph (see
   `creative-arts.game-design.systems-and-mechanics.attack-telegraphing`) and a clear
   answer (dodge, block, move, interrupt).
3. **Phases** (typically 2-3), triggered by health thresholds:
   | Phase | Purpose | Change |
   |---|---|---|
   | 1 | teach the patterns | slower, fewer attacks |
   | 2 | combine | new attack + mixes, faster recovery |
   | 3 | climax | arena change or desperation attack |
   Announce phase changes (animation, music, arena change) and give a breath.
4. **Openings:** define when the boss is vulnerable (after a combo, weak point exposed);
   make the punish window obvious.
5. **Arena:** shape supports the fight (pillars for cover, edges as hazards); avoid
   camera problems in tight arenas.
6. **Checkpoint immediately before**, short walk-back (or none), skippable intro
   cutscene on retry.
7. **Tune:** measure attempts to win across testers; target varies by game, but steep
   attempt counts with no learning trend indicate unreadable patterns.

## Gotchas
- Huge HP pools stretch fights without adding challenge; prefer more phases or faster
  patterns.
- Random attack selection with no tells is unlearnable; randomness should vary order,
  not readability.
- Instant-kill attacks need generous tells.
- Minion spam in boss fights shifts the test away from the boss; use deliberately.

## Verify
- [ ] Boss tests named skills taught earlier.
- [ ] Every attack has a telegraph and an answer.
- [ ] Phase triggers and transitions documented.
- [ ] Retry loop under ~15 seconds from death to fight.
- [ ] Attempt data shows players improving across tries.
