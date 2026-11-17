---
id: transportation-logistics.spaceflight-spacecraft-operations.crewed-spacecraft.ascent-entry-monitoring-and-abort-modes
name: ascent-entry-monitoring-and-abort-modes
category: transportation-logistics
field: spaceflight-spacecraft-operations
product: crewed-spacecraft
tags: [crewed-spacecraft, astronaut, ascent, entry, reentry, abort-modes, launch-escape, pad-abort, abort-to-orbit, crew-dragon, starliner, orion, soyuz, manual-piloting, cue-cards, flight-data-file, malfunction-procedures, g-load, deorbit-burn, parachutes, splashdown, landing]
level: advanced
status: draft
description: "How crews monitor ascent and entry against abort-mode boundaries, the cue-card callouts, when to take manual control, and the generic structure of abort and entry procedures."
sources: ["NASA Flight Data File structure (public descriptions)", "NASA Commercial Crew program public mission briefings", "Apollo/Shuttle abort-mode documentation (public histories)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ascent and entry monitoring and abort modes

**Goal:** know at every second of ascent and entry what you would do if something
failed, recognise the cue in time, and execute the procedure without improvising.
*Specific numbers and switch names differ by vehicle (Crew Dragon, Starliner, Orion,
Soyuz); this skill gives the generic structure — your vehicle's Flight Data File wins.*

## 1. Ascent: think in abort regions
Ascent is divided into **abort regions** set by altitude, velocity and dynamic pressure:
| Region (generic) | Typical abort | What crew watches |
|---|---|---|
| Pad / low altitude | Launch escape motors pull capsule away; parachute landing near pad or offshore | Escape system armed, wind limits |
| Max-Q & mid-ascent | Escape system abort; downrange water landing | Booster health, attitude rates, chamber pressures (via cues) |
| Late ascent | Abort to downrange landing zones selected by velocity | Velocity callouts vs. landing-zone boundaries |
| Near orbit | Abort-to-orbit / press-to-MECO, then fix in orbit | Inertial velocity, perigee |
Modern capsules abort **automatically** on detected booster failures; the crew's job
is to confirm the cue, back up a failed auto-sequence (a manual abort handle/command),
and call out the region so the ground and crew share the picture.

## 2. Callouts and cue cards
- Each crew member has an assigned monitoring set (e.g. commander: trajectory/attitude;
  pilot: systems/cabin pressure). Callouts are fixed words ("Max-Q", "Abort region 2",
  velocity marks) — no paraphrasing.
- Cue cards and electronic displays list the **boundary velocities** and what changes
  at each one. Rehearse until the next boundary is anticipated, not read.
- Cabin pressure and suit integrity are monitored continuously; a cabin leak during
  ascent drives a suit-closure and possibly an abort decision.

## 3. Manual piloting modes
- Manual is a **backup** for failed automation: attitude hold, rate damping,
  translation for docking, and in some vehicles manual entry-attitude control.
- Rule: hands off unless a cue says the automation has failed or the ground calls it.
  Taking manual control "to help" an auto-sequence is a leading training error.

## 4. Entry
1. Deorbit preparation: suits on and leak-checked, seats configured, stowage secured
   (loose items become projectiles at several g).
2. Deorbit burn: monitor Δv residuals against the burn table; know the
   underburn/overburn procedure (trim burn, alternate landing zone, or second burn).
3. Trunk/service-module separation confirmed before entry interface.
4. Entry: monitor g-load (typically ~3.5–4.5 g for lifting capsule entry; ballistic
   backup entries can exceed 8 g), heat-shield attitude, roll guidance.
5. Communications blackout (plasma) for several minutes is expected — have the
   loss-of-signal time on your timeline so it is not mistaken for a failure.
6. Parachute sequence: drogues, then mains; know the minimum-good-chute count and
   cues if a main fails to inflate.

## Gotchas
- Fatigue and g-load degrade reading accuracy; rely on trained cues and shapes on the
  display, not mental arithmetic.
- Off-nominal entries (ballistic) land far uprange/downrange — recovery forces need the
  updated landing point you call down.
- Never skip a leak check to stay on timeline.

## Verify
- [ ] You can name the active abort region and the next boundary at any point on the ascent profile.
- [ ] Manual-abort backup action and its cue are known without looking.
- [ ] Deorbit-burn residual limits and the underburn response are on your card.
- [ ] Blackout start/end times are marked on the entry timeline.
