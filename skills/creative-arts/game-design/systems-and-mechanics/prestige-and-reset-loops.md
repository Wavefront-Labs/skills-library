---
id: creative-arts.game-design.systems-and-mechanics.prestige-and-reset-loops
name: prestige-and-reset-loops
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, prestige-system, reset-loop, idle-games, incremental-games, roguelite-meta-progression, new-game-plus, seasons, progression-systems]
level: practitioner
status: draft
description: "Design prestige and reset loops (idle prestige, roguelite meta-progression, NG+, seasonal resets): what is kept, the reset multiplier, and when resetting becomes worth it."
sources:
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prestige and reset loops

**Goal:** a voluntary (or scheduled) reset that trades current progress for a permanent
bonus, so the player replays early content faster and stronger and progression
continues past the point where it would stall.

## Variants
| Variant | Kept after reset | Example form |
|---|---|---|
| Idle/incremental prestige | prestige currency giving a global multiplier | reset when growth slows |
| Roguelite meta-progression | unlocks and permanent upgrades | every death is a reset |
| New Game+ | gear/levels, harder enemies | after completion |
| Seasonal reset | cosmetics, account rewards; characters reset | ladder seasons |

## Prestige maths (idle games)
Prestige currency usually grows sub-linearly with lifetime earnings, e.g.
`prestige = floor(k * sqrt(lifetime_earned))` or a cube root. Kongregate's "Math of
Idle Games" series (Anthony Pecorella) walks through such formulas.
- The **reset is worth it** when the bonus lets the player get back to the current
  point faster than continuing would gain. Design the curve so that point arrives at a
  target interval (e.g. first prestige after 1-2 hours, later ones quicker).
- Show the projected bonus before the player resets.

## Procedure
1. Decide **what resets and what persists**; persistence must feel substantial.
2. Choose the prestige formula and simulate several cycles; plot time-to-previous-peak
   for each cycle. It should shrink.
3. Add **new content per layer** (new mechanics unlocked by prestige), not only a
   multiplier; pure multipliers become rote.
4. Make the first reset **guided**: players fear losing progress. Explain exactly what
   is kept.
5. Plan **multiple prestige layers** if the game is long (prestige of prestige), each
   with a slower cadence.

## Gotchas
- If the first reset is too early, players feel cheated; too late, they quit at the
  stall first.
- Roguelite meta-progression can make skill irrelevant (grind until stats win); some
  designs cap meta power or offer it as optional.
- Seasonal resets must preserve something players value (cosmetics, history).

## Verify
- [ ] Kept/reset table written and shown to players before resetting.
- [ ] Simulated time-to-previous-peak shrinks per cycle.
- [ ] First prestige point arrives at the planned time in playtests.
