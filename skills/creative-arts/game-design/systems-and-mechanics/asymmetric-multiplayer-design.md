---
id: creative-arts.game-design.systems-and-mechanics.asymmetric-multiplayer-design
name: asymmetric-multiplayer-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, systems-and-mechanics, asymmetric-design, multiplayer-design, one-vs-many, role-design, competitive-balance]
level: practitioner
status: draft
description: "Design asymmetric multiplayer (1-vs-many, differing roles or win conditions): role fantasy, information asymmetry, balancing by win-rate and time-to-outcome."
sources:
  - https://mitpress.mit.edu/9780262240451/rules-of-play/
  - https://www.gamedeveloper.com/design/asymmetric-gameplay-in-multiplayer-games
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asymmetric multiplayer design

**Goal:** sides that play differently yet each have a fair, readable chance to win.

## Kinds of asymmetry
| Axis | Example |
|---|---|
| Numbers (1 vs many) | Dead by Daylight, Evolve |
| Abilities / roles | Team Fortress 2 classes, Natural Selection 2 aliens vs marines |
| Information | hidden-movement games (Scotland Yard, Fury of Dracula) |
| Goals | one side escapes, the other prevents |
| Resources / tempo | economy side vs aggression side |

## Steps
1. **Write each side's fantasy in one line** (the stalker, the survivors) and list the verbs
   only that side has.
2. **Give every side counterplay** to the other's strongest verb (hide vs track, stun vs chase).
3. **Map information:** who sees what and when; asymmetric information is the cheapest
   lever to tune.
4. **Pick balance metrics:** win-rate per side by skill bracket, plus time-to-outcome
   and share of close games. Target roughly 45-55% per side at matched skill.
5. **Tune with dials, not redesign:** cooldowns, objective count, hunter speed ratio,
   reveal intervals.
6. **Matchmaking:** the solo side carries the match; its queue is usually the bottleneck,
   and its skill rating needs its own pool.

## Gotchas
- Coordinated groups (voice chat) overpower designs balanced on solo-queue data; track
  results by party size.
- The solo side feels all the pressure; give them recovery tools so one mistake is not final.
- A side nobody wants to play kills queues; watch role pick-rate as a health metric.
- Hidden information leaks via streams and external tools; design reveals assuming partial leakage.

## Verify
- [ ] One-line fantasy and exclusive verbs per side.
- [ ] Counterplay listed for each strong verb.
- [ ] Win-rate per side by bracket and party size within band.
- [ ] Role pick-rate and queue time monitored.
