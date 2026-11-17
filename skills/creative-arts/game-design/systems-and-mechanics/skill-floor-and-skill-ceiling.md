---
id: creative-arts.game-design.systems-and-mechanics.skill-floor-and-skill-ceiling
name: skill-floor-and-skill-ceiling
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, skill-ceiling, skill-floor, depth, accessibility-of-play, easy-to-learn-hard-to-master, mastery, competitive-games, difficulty-design]
level: advanced
status: draft
description: "Design for a low skill floor and a high skill ceiling: separate execution from decision depth, layer advanced techniques, and check that skill differences show in outcomes."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://www.sirlin.net/articles/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Skill floor and skill ceiling

**Goal:** new players can do something satisfying quickly (low floor), and expert
players keep finding room to improve for years (high ceiling): "easy to learn, hard to
master" (often called Bushnell's Law).

## Definitions
- **Skill floor:** the minimum skill needed to play meaningfully and have fun.
- **Skill ceiling:** the level beyond which more skill no longer improves outcomes.
- **Depth:** how many distinct layers of skill sit between them.

## Techniques for a low floor
- Simple core verbs with immediate feedback.
- Forgiving defaults (generous timing windows, auto-combos, simple control schemes).
- Safe early content; outcomes that feel good even when sub-optimal.

## Techniques for a high ceiling
- **Execution layers:** advanced inputs (cancels, animation tech, movement tricks) that
  are optional but better.
- **Decision layers:** positioning, resource timing, prediction (yomi), build planning.
- **Interaction between systems** so mastery is combinatorial, not memorised.
- **Opponent-driven depth:** in competitive games, the ceiling is often other players.

## Procedure
1. List the skills the game rewards, ordered from first-session to expert.
2. For each, ask: is it required at the floor? If yes and it is hard, add a simpler
   path (e.g. simple-input mode) or move it later.
3. Check **outcome sensitivity to skill**: in playtests or matches, does the more
   skilled player win at a rate you intend? Too high = brutal for novices; too low =
   skill doesn't matter.
4. For competitive games, check whether simplified inputs give an advantage or
   disadvantage at high level; designers usually accept a small trade-off to keep the
   expert path worth learning.

## Gotchas
- Raising the ceiling with obscure, untaught techniques creates a hidden knowledge gap;
  teach or surface them eventually (training modes, challenges).
- A high skill ceiling in matchmaking-less multiplayer means novices meet experts;
  needs matchmaking (see `creative-arts.game-design.systems-and-mechanics.matchmaking-and-skill-rating`).
- "Depth" that is only memorisation of numbers is shallow; prefer decisions.

## Verify
- [ ] Skill ladder written from first session to expert.
- [ ] First-session players succeed at the core loop within minutes.
- [ ] Measured win/score gap between skill bands matches intent.
