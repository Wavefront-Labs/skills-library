---
id: sports-recreation.esports.sim-racing-esports.rig-setup-braking-and-online-racecraft
name: rig-setup-braking-and-online-racecraft
category: sports-recreation
field: esports
product: sim-racing-esports
tags: [esports, sim-racing-esports, sim-racing, iracing, assetto-corsa-competizione, acc, assetto-corsa, gran-turismo, le-mans-ultimate, rfactor-2, direct-drive, wheelbase, force-feedback, load-cell, pedals, fov, field-of-view, trail-braking, racing-line, consistency, telemetry, safety-rating, incidents, league-racing, racecraft, blue-flag, overtaking]
level: practitioner
status: draft
description: "Sim racing for competition: wheel and pedal setup, field of view, trail braking and consistency practice, and clean online racecraft in iRacing/ACC-style leagues."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sim racing esports — rig, braking and online racecraft

**Goal:** be fast *and* clean. In ranked services (iRacing's Safety Rating,
ACC's Safety/Racecraft ratings) and leagues, incidents cost as much as slow
laps. Consistency wins races; hero laps don't.

## 1. Rig setup that matters
- **Pedals first.** A **load-cell brake** (measures force, not travel) is
  the single biggest hardware upgrade for consistency; muscle memory works
  on pressure. Calibrate max force so 100% braking is a firm but repeatable push.
- **Wheel:** belt or direct-drive both work. Set force feedback to avoid
  **clipping** (FFB saturating at max so detail is lost) — most sims have a
  clipping meter; aim for it to peak only in the heaviest corners.
- **Rotation:** match the car's real steering lock (many sims auto-set it;
  set the wheel driver to 900°+ and let the sim limit it).
- **Field of view:** calculate the *real* FOV from screen width and eye
  distance (online FOV calculators). A correct FOV feels slow but makes
  braking points and distance judgement accurate.
- Mount everything rigidly; a flexing desk or sliding chair ruins braking consistency.

## 2. Driving technique
- **Braking:** hit peak pressure fast at the start (threshold braking), then
  **trail off** smoothly as you turn in. Trail braking loads the front tyres
  for rotation; releasing too fast causes understeer, too slow locks/spins.
- **Look ahead** to the apex and exit, not the bonnet.
- **Exit over entry:** a slightly slower entry for a better exit gains time
  on the following straight.
- **Use references:** brake boards, marks, kerbs. Change one reference at a time.

## 3. Practice structure
1. 10 laps to learn the track at 95% pace.
2. Compare to a faster lap with **telemetry/ghost** (built-in or
   third-party tools): where are you losing — braking point, minimum corner
   speed, throttle application?
3. Fix one corner per session.
4. Run **race-length stints** and measure lap time spread. Target: most laps
   within ~0.5 s of each other before chasing outright pace.
5. Practise starts and the first lap in traffic (AI races help).

## 4. Online racecraft
- **Lap 1, turn 1:** brake earlier than in practice; most incidents happen here.
- **Overtaking:** you must have a meaningful overlap (commonly: front axle
  alongside the other driver's rear axle or further) before turn-in to
  claim space; otherwise yield.
- **Leave a car's width** when side-by-side; hold your line, no late
  defensive moves in braking zones.
- **Blue flags / being lapped:** stay predictable on the racing line;
  don't jump out of the way mid-corner.
- **After a spin:** wait until traffic clears before rejoining; rejoining
  across the track causes the worst crashes.
- **Rating management:** if you're a danger to others, pit or retire; the
  rating hit from incidents outweighs a points finish.

## 5. Leagues
- Read the sporting code: penalties, restart rules, protest process, car setup rules (fixed vs open).
- Arrive with a race-length fuel calculation and pit plan.
- Be polite in chat; disputes go through stewards, not voice comms.

## Gotchas
- Chasing hardware before learning braking.
- Wrong FOV making the car feel "faster" but braking points unreliable.
- Copying aggressive setups you can't drive consistently.
- **Rating-system specifics change between sims and seasons; check each
  service's current rules.**

## Verify
- [ ] Brake calibrated; FFB not clipping on most corners.
- [ ] FOV set from measured geometry.
- [ ] 10-lap stint with lap spread under ~0.5 s.
- [ ] Zero self-caused incidents in the last 3 races.
