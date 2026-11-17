---
id: creative-arts.game-design.systems-and-mechanics.writing-design-pillars
name: writing-design-pillars
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, design-pillars, pillar-statements, experience-goals, scope, feature-cutting, vision, creative-direction, video-games, board-games]
level: practitioner
status: draft
description: "Write 3-5 testable design pillars for a game, then use them as a filter to accept, reshape or cut features and settle team arguments."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing design pillars

**Goal:** a short list of statements about the *player's experience* that every feature
must serve, so scope decisions are made against the vision instead of by whoever argues
loudest.

## 1. Draft from the experience, not the feature list
- Start from the essential experience (see
  `creative-arts.game-design.systems-and-mechanics.defining-the-essential-experience`).
- Write each pillar as **what the player feels or does**, not what the game contains.
  - Weak: "Procedural dungeons." (a feature)
  - Strong: "Every run surprises you." (an experience the feature serves)
- Use the format **short slogan + one sentence of meaning + one sentence of what it rules
  out**. The "rules out" line is what makes a pillar useful.

```
PILLAR: "Fragile but clever"
Means:  The player is weaker than every enemy and wins by using the environment.
Rules out: stat-based power fantasies, damage upgrades that trivialise early enemies.
```

## 2. Keep the set small and in tension
- 3 is ideal, 5 is the ceiling. More than five and nothing is ever cut.
- Pillars should pull against each other a little ("tense" vs "approachable"); designing
  inside that tension is where the game's identity lives. If two pillars always agree,
  merge them.
- Rank them. When two pillars conflict on a decision, the higher one wins.

## 3. Use them as a filter
For every proposed feature, score it against each pillar: **supports / neutral / fights**.
| Feature | Pillar 1 | Pillar 2 | Pillar 3 | Decision |
|---|---|---|---|---|
| Crafting | supports | neutral | fights (slows runs) | reshape: crafting only between runs |
- Supports none: cut, however cool.
- Fights the top pillar: cut or reshape.
- Put the table in the design doc so the reasoning survives turnover.

## 4. Revisit at milestones
Pillars may change after a prototype proves the fun is somewhere else. Change them
deliberately, in writing, with the team; never let them drift silently.

## Gotchas
- **Genre labels are not pillars** ("roguelike", "open world"). They name a form, not an
  experience, and filter nothing.
- **Unfalsifiable pillars** ("fun", "high quality", "immersive") pass every feature.
  Test: can you name a feature it would reject? If not, rewrite.
- **Pillars written after the fact** to justify existing features filter nothing. Write
  them before production, then re-check against the prototype.
- Marketing taglines and design pillars overlap but are different documents; the design
  version must include the "rules out" line.

## Verify
- [ ] 3-5 ranked pillars, each phrased as player experience.
- [ ] Every pillar names at least one thing it rules out.
- [ ] At least one existing or proposed feature has been cut or reshaped using them.
- [ ] A new team member can predict a design decision from the pillars alone.
