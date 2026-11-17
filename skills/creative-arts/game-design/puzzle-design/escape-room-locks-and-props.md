---
id: creative-arts.game-design.puzzle-design.escape-room-locks-and-props
name: escape-room-locks-and-props
category: creative-arts
field: game-design
product: puzzle-design
tags: [game-design, puzzle-design, escape-room, maglocks, escape-room-props, combination-locks, rfid, arduino, room-reset, durability, fail-safe]
level: advanced
status: draft
description: "Choose and install escape room locks and props: padlock types, maglocks with fail-safe release, sensors (RFID, reed switches), durability for daily abuse, and reset checklists."
sources:
  - http://scottnicholson.com/pubs/erfacwhite.pdf
  - https://docs.arduino.cc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Escape room locks and props

**Goal:** puzzle hardware that is satisfying, reliable through thousands of games, fast
to reset, and safe.

## Locks
| Lock | Notes |
|---|---|
| Combination padlocks (3/4/5-digit, letter, directional) | cheap, clear; players brute-force short combos - choose digits accordingly |
| Key padlocks | simple; keys get lost; keep spares |
| Maglocks (electromagnetic) | silent, triggered by puzzles; hidden; need power design |
| Solenoid latches | small compartments |
| Lockboxes / hasps | combine with any padlock |
Nicholson's 2015 survey noted that padlock-heavy rooms can feel repetitive; many
operators shifted toward technology-driven props.

## Electronic props
- Sensors: reed switches (magnet detection), RFID/NFC readers (place the right object),
  buttons, light sensors, weight sensors.
- Controllers: Arduino or similar microcontrollers, or commercial escape room controllers.
- Feedback: lights, sounds, motion when solved.

## Safety (non-negotiable; check local fire and building codes)
- Players must always be able to exit: entry doors should not lock players in, or must
  have an immediate release (many jurisdictions require this).
- **Maglocks fail-safe:** they release when power is cut; connect to emergency release
  and fire alarm per code.
- No sharp edges, pinch points, or electrical exposure; low-voltage props.

## Durability and reset
1. Assume players pull, twist and pry everything; over-engineer mounting.
2. Hide wiring in conduit; strain-relieve connectors.
3. **Reset checklist** per room: every lock code set, items returned, props re-armed,
   batteries/power checked; target a reset time between groups.
4. Game master override for every electronic prop (manual trigger) in case of failure.
5. Spares for consumables and fragile props.

## Gotchas
- Props failing mid-game are the most common bad-review cause; log failures and fix.
- Puzzles where the answer is entered on a lock with similar locks nearby cause
  "right answer, wrong lock" confusion; use distinct lock types per puzzle.
- Battery-powered props die at the worst time; prefer mains-powered with checks.

## Verify
- [ ] Exit and fail-safe compliance checked against local code.
- [ ] Every electronic prop has a manual override.
- [ ] Reset checklist written and timed.
- [ ] Prop failure log reviewed weekly.
