---
id: creative-arts.game-design.systems-and-mechanics.self-determination-theory-in-games
name: self-determination-theory-in-games
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, self-determination-theory, sdt, player-motivation, competence, autonomy, relatedness, pens, intrinsic-motivation, rigby-ryan]
level: practitioner
status: draft
description: "Apply self-determination theory (competence, autonomy, relatedness) to game design and evaluate it with the PENS questionnaire, avoiding extrinsic rewards that crowd out intrinsic play."
sources:
  - https://selfdeterminationtheory.org/
  - https://selfdeterminationtheory.org/SDT/documents/2006_RyanRigbyPrzybylski_MandE.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Self-determination theory in games

**Goal:** design for durable intrinsic motivation by satisfying three basic
psychological needs, and measure whether you did.

Self-determination theory (Deci and Ryan) holds that well-being and intrinsic motivation
come from satisfying **competence**, **autonomy** and **relatedness**. Ryan, Rigby and
Przybylski (2006, "The Motivational Pull of Video Games") showed these needs predict
game enjoyment and future play; Rigby and Ryan's PENS (Player Experience of Need
Satisfaction) measures them plus presence/immersion and intuitive controls.

## Design levers per need
| Need | Means | Levers |
|---|---|---|
| Competence | feeling effective, growing mastery | clear feedback, optimal challenge, visible progress, fair failure |
| Autonomy | acting by choice, volition | meaningful choices, multiple paths, customisation, no coercive timers |
| Relatedness | connection to others | co-op, guilds, NPCs who acknowledge the player, shared goals |

## Procedure
1. For each core loop, write how it supports each need.
2. Look for **need thwarting**: punishing failure without learning (competence), forced
   linear "do this now" sequences or manipulative monetisation (autonomy), toxic
   multiplayer or lonely worlds (relatedness).
3. **Be careful with extrinsic rewards:** SDT research on the "overjustification"
   effect suggests controlling rewards can undermine intrinsic interest. Informational
   rewards ("you mastered X") support competence; controlling rewards ("log in or lose
   your streak") undermine autonomy.
4. **Measure with PENS-style items** after playtests (licensed instrument; or similar
   validated scales). Compare builds, not absolute numbers.

## Gotchas
- Autonomy is not "infinite freedom"; too many choices without guidance reduces
  competence. Structured choice is the target.
- Relatedness can come from NPCs and the developer's voice, not only multiplayer.
- PENS is a commercial instrument (Immersyve); check licensing before formal use.

## Verify
- [ ] Each core loop mapped to the three needs.
- [ ] Need-thwarting features listed with mitigations.
- [ ] Post-playtest need-satisfaction questionnaire collected and compared across builds.
