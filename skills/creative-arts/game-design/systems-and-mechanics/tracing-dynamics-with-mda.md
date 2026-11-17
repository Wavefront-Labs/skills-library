---
id: creative-arts.game-design.systems-and-mechanics.tracing-dynamics-with-mda
name: tracing-dynamics-with-mda
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, mda-framework, dynamics-analysis, mechanics-dynamics-aesthetics, emergence, systems-design, design-analysis, debugging-design]
level: practitioner
status: draft
description: "Apply the MDA framework to trace why a mechanic produces (or fails to produce) a target feeling: map mechanics to runtime dynamics to aesthetics, and fix at the mechanic layer."
sources:
  - https://users.cs.northwestern.edu/~hunicke/MDA.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Tracing dynamics with MDA

**Goal:** diagnose design problems by following the causal chain from rules to
behaviour to feeling, and fix them where they can actually be fixed: the mechanics.

## The model
- **Mechanics:** the rules and data (actions, algorithms, numbers).
- **Dynamics:** the run-time behaviour that emerges when players act on the mechanics
  over time (bluffing, turtling, snowballing, rushing).
- **Aesthetics:** the emotional responses (the eight kinds of fun).
Designers see the game M -> D -> A; players experience it A -> D -> M. You can only
edit M, so every fix is a mechanic change predicted to shift a dynamic.

## Procedure
1. **Write the symptom as an aesthetic:** "The last third of a match is boring."
2. **Observe the dynamic producing it** (playtest or telemetry): "the leader is obvious
   by turn 8 and everyone else stops trying" (a runaway-leader dynamic).
3. **Find the mechanics feeding the dynamic:** income scales with territory; territory
   makes taking territory easier (a positive feedback loop); scores are public.
4. **Generate mechanic-level fixes, each with its predicted dynamic:**
   | Mechanic change | Predicted dynamic | Risk |
   |---|---|---|
   | hidden scoring | players can't identify leader, keep trying | feels random at reveal |
   | leader pays upkeep per territory | negative feedback, closer games | punishes good play |
   | shorter game (end at turn 10) | less time for snowball | less arc |
5. **Prototype the cheapest fix**, playtest, and check the dynamic changed before
   judging the aesthetic.

The MDA paper's own worked example: Monopoly's late game drags because the mechanics
reward the leader (positive feedback); its suggested fixes are mechanical (e.g. taxes
or catch-up for trailing players).

## Gotchas
- **Fixing at the aesthetic layer** (adding music or a cutscene to make a dull section
  "exciting") rarely works when the dynamic is the cause.
- One mechanic often feeds several dynamics; a fix can break a dynamic you liked. List
  all dynamics a mechanic touches before changing it.
- Dynamics only show up with real play over time; a single short test can miss
  late-game dynamics entirely.

## Verify
- [ ] Symptom written as an aesthetic, dynamic observed (not guessed).
- [ ] Mechanic causes listed, each fix paired with a predicted dynamic.
- [ ] Post-change playtest confirms the dynamic shifted.
