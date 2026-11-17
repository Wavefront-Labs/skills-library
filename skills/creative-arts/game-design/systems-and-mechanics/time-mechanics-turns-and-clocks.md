---
id: creative-arts.game-design.systems-and-mechanics.time-mechanics-turns-and-clocks
name: time-mechanics-turns-and-clocks
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, time-mechanics, turn-structure, real-time, clocks, timers, races, pause, schell-mechanics, game-mechanics-basics, active-time-battle]
level: practitioner
status: draft
description: "Choose and tune a game's time model: discrete turns vs real time, hybrids (ATB, pausable real time), clocks, countdowns, races, and controls over time like pause and rewind."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Time mechanics: turns and clocks

**Goal:** a deliberate time model that matches the decisions you want: deep thought,
pressure, or a mix.

Schell (2nd ed.) ch12 lists time as a basic mechanic: discrete (turn-based) or continuous (real
time), with clocks and races as tools and with controls that let players change time
(pause, slow, rewind).

## Choose the model
| Model | Produces | Examples / notes |
|---|---|---|
| Strict turns | deliberation, planning | chess; risk of downtime (see tabletop analysis-paralysis skills) |
| Simultaneous turns | bluffing, no downtime | programmed-move games; needs a reveal step |
| Real time | pressure, reflexes | action games |
| Pausable real time | tactics under pressure, but player-controlled | many RTS/RPGs |
| Active time / gauge | hybrid; speed stat matters | ATB systems in classic JRPGs |
| Tick/impulse | fine-grained turn order by speed | initiative tracks, time-track games where actions cost time units |

## Clocks and pressure tools
- **Countdown:** fixed deadline; creates urgency but punishes slow learners.
- **Race:** first to X; pressure comes from opponents, not the clock.
- **Escalation clock:** threat rises per turn (doom tracks); time cost of every action.
- **Progress clocks** (Blades in the Dark style segmented clocks) visualise both player
  progress and threats.
- **Turn timers / chess clocks** in tabletop to cut analysis paralysis.

## Tuning
1. Decide where you want **thinking time** and where you want **reaction time**; put the
   hard decisions in the former.
2. Measure decision time in playtests; if the median turn is far longer than intended,
   simplify choices or add a timer.
3. For real time, test with novices: a speed that feels relaxed to designers is often
   overwhelming. Offer speed settings where the design allows.

## Gotchas
- Mixing real-time pressure with heavy information reading (long tooltips) produces
  frustration.
- Rewind/undo mechanics change the whole design: risky choices stop being risky.
- Online simultaneous games need tie-break rules for same-tick actions.

## Verify
- [ ] Time model chosen with a stated reason linked to the target decisions.
- [ ] Pressure tools listed and placed.
- [ ] Measured decision times match intent within playtest groups.
