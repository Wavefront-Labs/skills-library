---
id: creative-arts.game-design.systems-and-mechanics.cooperative-play-design
name: cooperative-play-design
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, co-op-design, cooperative-games, multiplayer-design, interdependence, role-design, drop-in-drop-out, revive-mechanics, scaling, fellowship]
level: practitioner
status: draft
description: "Design co-op play that needs cooperation: interdependent roles, shared resources, revive and failure rules, difficulty scaling by player count, and drop-in/drop-out."
sources:
  - https://www.routledge.com/The-Art-of-Game-Design-A-Book-of-Lenses-Third-Edition/Schell/p/book/9781138632059
  - https://users.cs.northwestern.edu/~hunicke/MDA.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cooperative play design

**Goal:** co-op where players need each other and talk to each other (MDA's fellowship
aesthetic), rather than single-player experiences happening side by side.

## Levels of interdependence
| Level | Description | Example pattern |
|---|---|---|
| Parallel | same space, independent | everyone shoots their own enemies |
| Supportive | helping is optional and beneficial | heals, buffs |
| Interdependent | tasks require multiple players | one holds the door, one goes through |
| Asymmetric roles | each player has different info or abilities | one reads the manual, one defuses |
More interdependence = more fellowship, but more frustration if a partner is absent or
weak.

## Tools that create cooperation
- **Complementary abilities** (no one can do everything).
- **Shared resources** that force negotiation (one health pool, shared ammo).
- **Split information** (asymmetric knowledge).
- **Combo actions** (two players' moves combine for bonus effects).
- **Revive mechanics:** downed players can be revived; creates rescue moments.
- **Proximity incentives** (staying together is safer).

## Practical systems
1. **Scaling by player count:** enemy HP/number, puzzle requirements and resources.
   Test every supported count; 1-player in a 4-player design is often broken.
2. **Drop-in/drop-out:** what happens to progress, loot and difficulty when players
   join or leave mid-session.
3. **Shared vs personal rewards:** personal loot avoids arguments; shared loot creates
   negotiation (and conflict).
4. **Failure rules:** individual death vs team wipe; time to rejoin.
5. **Skill gaps:** let stronger players help without carrying completely (roles suited
   to different skill levels).
6. **Communication:** ping system for players not using voice.

## Gotchas
- Mandatory interdependence + matchmaking with strangers can be miserable; offer
  solo/bot fallback or role flexibility.
- One dominant role (the "real" player) makes others passengers; give every role
  decisions.
- Couch co-op needs shared-screen camera solutions (see camera design).

## Verify
- [ ] Interdependence level chosen per mode.
- [ ] All supported player counts playtested.
- [ ] Join/leave and failure rules documented.
- [ ] Playtest groups talk to coordinate (observed).
