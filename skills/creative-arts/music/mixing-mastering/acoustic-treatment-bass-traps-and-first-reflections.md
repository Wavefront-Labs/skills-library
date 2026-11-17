---
id: creative-arts.music.mixing-mastering.acoustic-treatment-bass-traps-and-first-reflections
name: acoustic-treatment-bass-traps-and-first-reflections
category: creative-arts
field: music
product: mixing-mastering
tags: [mixing-mastering, monitoring, room-acoustics, acoustic-treatment, bass-traps, first-reflections, mirror-trick, broadband-absorber, rockwool, diffusion, rt60, room-eq-wizard, rew, room-modes]
level: practitioner
status: draft
description: "Treat a small mixing room: corner bass traps, first-reflection absorbers found with the mirror trick, ceiling cloud, when diffusion helps, and measuring with REW."
sources: ["Mike Senior, Mixing Secrets for the Small Studio (2nd ed.), ch. 1 (room treatment)", "https://www.roomeqwizard.com/help/", "F. Alton Everest and Ken Pohlmann, Master Handbook of Acoustics (McGraw-Hill)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Acoustic treatment: bass traps and first reflections

**Goal:** a small room where what you hear is the mix, not the room.

## 1. Priorities (biggest gain first)
1. Correct speaker and listening placement (see monitor-placement skill).
2. **Bass trapping** in corners.
3. **First-reflection** absorption (side walls, ceiling, desk).
4. Rear wall absorption/diffusion (if the room allows distance).

## 2. Bass traps
- Low frequencies build up in corners: put thick broadband absorbers (**10-20 cm** mineral wool/rockwool or fibreglass, density ~40-60 kg/m3, with an air gap if possible) straddling wall-wall corners floor to ceiling, and wall-ceiling corners.
- Thicker and deeper is better; thin foam (2-5 cm) does almost nothing below 500 Hz.
- Front corners behind speakers first, then rear corners.

## 3. First reflections
- **Mirror trick**: sit at the listening position; have someone slide a mirror along the side wall; wherever you can see a speaker's tweeter in the mirror is a reflection point. Repeat on the ceiling (cloud) and for both speakers.
- Place **broadband panels (10 cm)** at those points, ideally with a 5-10 cm air gap behind.
- Desk reflection: move speakers forward, angle them, or use a desk with a sloped/cut-out surface.

## 4. Rear wall and diffusion
- In small rooms the rear wall is close: thick absorption there controls the flutter and late reflections.
- **Diffusers** only work with enough distance (more than ~2-3 m to the listener); otherwise use absorption.

## 5. Don't over-deaden
- Covering every wall with thin foam kills the highs but leaves the bass boomy: a dull, unbalanced room. Aim for broadband control, not silence.

## 6. Measure
- REW + a calibrated measurement mic (e.g. UMIK-1): take a sweep at the listening position before and after. Look at frequency response (modes as peaks/dips below 300 Hz) and the waterfall/decay (long ringing at mode frequencies shows where trapping is needed).
- Room-correction software (Sonarworks SoundID, Dirac) can fix residual tonal issues **after** treatment, not instead of it.

## Gotchas
- Untreated mineral wool sheds fibres: wrap in breathable fabric.
- Bass traps behind furniture or too thin to matter.

## Verify
- REW before/after: smoother low end, shorter decay times at modal frequencies.
- Mixes translate better to other systems (car, earbuds) than before.
