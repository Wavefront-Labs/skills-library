---
id: creative-arts.game-design.systems-and-mechanics.designing-for-emergent-actions
name: designing-for-emergent-actions
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, resultant-actions, emergent-gameplay, operative-actions, verbs, schell-mechanics, game-mechanics-basics, emergence, systemic-design]
level: advanced
status: draft
description: "Increase emergent play by maximising resultant actions per operative action: add verbs that act on many objects, goals reachable many ways, and side effects."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Designing for emergent actions

**Goal:** a small set of verbs that combines into many meaningful strategies, so players
discover play the designer did not script.

Schell (2nd ed.) ch12 distinguishes **operative actions** (the basic verbs: move, jump, capture)
from **resultant actions** (meaningful strategies that arise from using the verbs in
context: protecting a piece, setting a trap, sacrificing to gain tempo). Emergent
gameplay is a high ratio of interesting resultant actions to operative actions.

## Schell's five tips for emergent actions
1. **Add more verbs** - but each must interact with the others; isolated verbs add
   complexity without emergence.
2. **Verbs that can act on many objects** - "shoot" that can hit enemies, locks, ropes,
   lights and explosive barrels creates more combinations than "shoot enemy".
3. **Goals achievable more than one way** - stealth, combat, talking, or going around.
4. **Many subjects** - multiple pieces/units the player controls (chess: six piece types).
5. **Side effects that change constraints** - an action that also alters the space or
   rules (a fire spreads, a wall breaks, a moved piece opens a line).

## Procedure
1. List operative actions (verbs) and objects in a verb x object matrix.
2. Fill each cell: what happens? Blank or "nothing" cells are candidates for new
   interactions (can you burn the door? push the barrel?).
3. Add interactions that have **readable, consistent rules** (fire burns wood, always),
   so players can predict and plan.
4. Playtest and log **player-invented strategies**; count them. The number of distinct
   strategies per verb is a rough emergence measure.
5. Check emergent strategies for **degenerate** outcomes (one dominant exploit) and fix
   via rules, not special cases.

## Gotchas
- Special-case rules ("fire burns wood except this door") kill trust in the system.
- Emergence makes content and QA harder: every new object multiplies interactions.
- Players only use what they can perceive; teach the rules of interaction early.

## Verify
- [ ] Verb x object matrix exists with few unexplained blanks.
- [ ] At least one goal can be reached by three distinct methods.
- [ ] Player-invented strategies logged from playtests.
