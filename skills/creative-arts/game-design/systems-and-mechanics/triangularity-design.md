---
id: creative-arts.game-design.systems-and-mechanics.triangularity-design
name: triangularity-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, triangularity, schell, lens-of-triangularity, meaningful-choice, risk-reward, space-invaders-ufo, safe-vs-risky, balance]
level: practitioner
status: draft
description: "Apply Schell's Lens of Triangularity: offer a safe low-reward option and a risky high-reward option, and tune the reward so the risky option is worth considering."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triangularity

**Goal:** a recurring choice between playing it safe for a small reward or taking a
risk for a large one, balanced so that the choice is genuinely interesting.

Schell (2nd ed.) ch13 calls this "triangularity" (one of the most exciting meaningful choices).
His example: the UFO in Space Invaders - the player can keep shooting the safe,
advancing invaders, or risk lining up a shot on the high-value UFO, possibly letting
invaders close in. Lens of Triangularity questions: Do I have a triangularity now? If
not, how can I get one? Is my attempt at triangularity balanced - are the rewards
commensurate with the risks?

## Building one
1. Identify the default safe action and its reward.
2. Add a risky alternative that is:
   - **optional** (the player can always choose safe),
   - **visible** (they see the opportunity and the danger),
   - **time-limited or costly** (taking it costs time, position, health or resources).
3. Set the risky reward using the rough guideline: reward should scale with the
   probability of failure. Start with expected value of the risky option a little
   *above* the safe option (players are risk-averse), then tune by observation.
4. Make the risk/reward **change with context** (low health makes risk worse; trailing
   in score makes reward more valuable). That variability keeps the choice alive.

## Examples by genre
| Genre | Safe | Risky |
|---|---|---|
| shooter | snipe from cover | push for the power weapon |
| platformer | main path | coin trail over a pit |
| board game | take the guaranteed 2 points | bid for the contested 5-point tile |
| roguelike | skip the elite room | fight the elite for a relic |

## Gotchas
- If the reward is too small, players ignore the risky option; too large, it becomes
  mandatory and the safe option is dead.
- Hidden risk is not triangularity; the player must be able to estimate the danger.
- Rewards that compound (permanent upgrades) make early risky choices disproportionately
  powerful; consider transient rewards.

## Verify
- [ ] At least one triangularity per core loop identified.
- [ ] Risky option taken by a meaningful minority to majority of testers, varying with context.
- [ ] Reward and risk both visible at decision time.
