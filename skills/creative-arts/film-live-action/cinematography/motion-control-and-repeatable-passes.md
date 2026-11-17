---
id: creative-arts.film-live-action.cinematography.motion-control-and-repeatable-passes
name: motion-control-and-repeatable-passes
category: creative-arts
field: film-live-action
product: cinematography
tags: [cinematography, film-live-action, motion-control-rig, repeatable-moves, bolt-arm, moco-passes, motion-control-vfx, repeat-pass, milo, clean-plate-pass, twinning]
level: practitioner
status: draft
description: "Use motion control for repeatable moves and VFX passes: rig types (Milo, Bolt), programming moves, multi-pass shooting (clean plate, twins, elements), and exporting move data to VFX."
sources:
  - "https://www.mrmoco.com (Mark Roberts Motion Control - Bolt, Milo, Flair software)"
  - "American Cinematographer Manual (ASC, 11th ed.) - motion control and visual effects photography"
  - "https://www.vesglobal.org (Visual Effects Society Handbook - on-set VFX data)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Motion control and repeatable passes

**Goal:** camera moves that repeat exactly, so multiple passes (actor, clean plate,
twin, miniature, element) composite seamlessly.

## 1. Rigs
- **Milo** (track-based crane arm) and **Cyclops**: larger moves, repeatable, on track.
- **Bolt / Bolt X** (high-speed robotic arm): fast moves for products, food and
  high-speed photography (often with Phantom cameras).
- **Small moco**: motorised sliders and heads (eMotimo, Kessler) for repeatable moves on
  a budget.
Operated by a **motion control operator** with software (e.g. Flair) controlling
axes: track, rotate, lift, arm, pan, tilt, roll, focus, zoom, iris.

## 2. Programming moves
- Teach keyframes by jogging the rig with a handwheel or controller, or import a move
  from previs/techvis.
- Play back at reduced speed, then full; check frame-rate-dependent moves (high-speed
  passes need the rig to run at a matching speed or scaled).
- Set **target frames** and timing; record the move.

## 3. Multi-pass shooting
- **Action pass** with actors.
- **Clean plate** pass (same move, no actors) for removal/compositing.
- **Twinning**: actor plays both roles in separate passes; split screen or matte later.
- **Element passes**: smoke, practical lights, miniatures; scale moves for miniatures.
- **Lighting passes**: separate passes per light for compositing control.
Lock lighting between passes (no drift - LED sources are stable; daylight is not).

## 4. Data to VFX
Export the move (camera position/rotation per frame, lens data) in formats VFX can use
(.fbx, .ma, ASCII); record lens focal length, focus distance, sensor size. Slate each
pass with pass number. VFX supervisor confirms the data on set.

## 5. Planning and safety
Moco rigs are heavy and fast: exclusion zones, emergency stops, operator controls. Allow
time - set-up 2-4 hours; each pass at full speed plus playback.

## Gotchas
- Daylight changing between passes - passes don't match.
- Lens or focus changed between passes.
- Move data not exported or lens data missing.
- Bolt moves near people without exclusion zones.

## Verify
- [ ] Rig chosen for move size/speed; operator booked.
- [ ] Move programmed and rehearsed; passes listed.
- [ ] Lighting and lens locked across passes; passes slated.
- [ ] Move and lens data exported and confirmed by VFX.
