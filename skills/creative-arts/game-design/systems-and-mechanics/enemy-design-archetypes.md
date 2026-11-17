---
id: creative-arts.game-design.systems-and-mechanics.enemy-design-archetypes
name: enemy-design-archetypes
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, enemy-design, combat-design, enemy-archetypes, enemy-roles, ai-behaviour, encounter-building, rogers, action-games]
level: practitioner
status: draft
description: "Design an enemy roster by role (fodder, tank, ranged, flanker, support, disruptor), attributes and behaviours, so combinations create varied encounters."
sources:
  - https://www.gdcvault.com/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Enemy design archetypes

**Goal:** a roster where each enemy asks the player a distinct question, so mixing them
produces encounters that need different answers.

Rogers (Level Up!, enemy design chapter) describes enemies through attributes such as
size, speed, movement pattern, attack type, health and behaviour, and stresses that each
enemy should demand a different response from the player.

## Role taxonomy
| Role | Question it asks | Typical traits |
|---|---|---|
| Fodder | can you handle numbers? | low HP, simple attack, swarms |
| Tank / bruiser | can you deal sustained damage or avoid big hits? | high HP, slow, heavy attacks |
| Ranged / artillery | can you close distance or use cover? | stays back, telegraphed shots |
| Flanker / rusher | can you watch your sides? | fast, attacks from off-screen |
| Support / healer | can you prioritise targets? | buffs/heals others, fragile |
| Disruptor | can you adapt? | stuns, pushes, blocks paths, steals |
| Shielded / puzzle | do you know the trick? | weak spot, requires a specific verb |

## Procedure
1. **Start from player verbs:** each enemy should make at least one verb more valuable
   (shielded enemies reward the parry; flyers reward ranged attacks).
2. **Write an enemy card:** role, silhouette, movement, attacks (with telegraphs),
   weak points, HP tier, behaviour states, introduction level.
3. **Silhouette and colour readability:** players must identify the type instantly at
   combat distance.
4. **Plan introductions:** each new enemy appears first alone in a safe setting, then in
   combination (see `creative-arts.game-design.level-design.enemy-placement-and-composition`).
5. **Variants:** reuse a base enemy with one changed property (armoured, faster,
   elemental) to extend the roster cheaply; make the change visible.
6. **Combination matrix:** list pairs that create interesting problems (tank shields
   ranged; healer behind fodder).

## Gotchas
- Enemies that only differ in HP and damage do not ask new questions.
- Too many disruptors (stun-lock) remove player agency.
- Off-screen attackers need audio/visual warnings.

## Verify
- [ ] Each enemy card names the question it asks and the verb it rewards.
- [ ] Silhouettes distinguishable in a greyscale screenshot at play distance.
- [ ] Combination matrix with at least five interesting pairings.
