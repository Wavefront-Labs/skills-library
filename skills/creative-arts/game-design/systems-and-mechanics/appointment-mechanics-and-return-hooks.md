---
id: creative-arts.game-design.systems-and-mechanics.appointment-mechanics-and-return-hooks
name: appointment-mechanics-and-return-hooks
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, appointment-mechanics, return-hooks, retention, daily-rewards, timers, energy-systems, core-loop, live-ops, ethics]
level: practitioner
status: draft
description: "Design appointment mechanics and return hooks (timers, daily quests, crops, streaks) that bring players back without punishing absence or relying on anxiety."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - http://www.fdg2013.org/program/papers/paper06_zagal_etal.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Appointment mechanics and return hooks

**Goal:** give players a reason to come back tomorrow that they appreciate, not one they
resent.

**Appointment mechanic:** the game sets a time when something will be ready (crops grow
in 4 h, a daily quest resets, an event starts Saturday). **Return hook:** any unresolved
thread at session end that pulls the player back (cliffhanger, almost-complete set,
pending reward).

## Patterns
| Pattern | Respectful version | Coercive version (avoid) |
|---|---|---|
| Timers (build/craft/grow) | completed item waits indefinitely | item spoils if not collected |
| Daily quests | weekly pool; missing days carry over | daily-only, lost forever |
| Login streaks | cumulative calendar, missing a day pauses | streak resets to 0 |
| Energy | caps generous; refills naturally | small cap + paid refills |
| Events | rerun, catch-up shop | FOMO-exclusive rewards |
Zagal, Björk and Lewis ("Dark Patterns in the Design of Games", FDG 2013) list
"playing by appointment" as a temporal dark pattern when the game punishes players who
do not show up at the game's chosen time.

## Design procedure
1. Decide the **desired return cadence** (daily? 3x per week?) from the audience, not
   the revenue target.
2. Make the hook **content-driven first** (new story beat, new map, new challenge) and
   timer-driven second.
3. **Never punish absence beyond lost upside**: what is waiting should still be there.
4. Allow **catch-up** for anything time-limited.
5. Check that the hook **ends**: players can finish a season and feel done.

## Gotchas
- Retention measured at D1/D7/D30 will go up with coercive hooks; so will churn and
  negative reviews later. Measure sentiment alongside retention.
- Notifications are part of the mechanic; default them off or ask, and never send at
  night local time.
- Platform and regional rules may apply to time-limited purchase offers; check current
  consumer-protection guidance.

## Verify
- [ ] Return cadence chosen and justified by audience.
- [ ] No mechanic destroys player progress due to absence.
- [ ] Every time-limited reward has a catch-up path.
