---
id: creative-arts.animation.blender.procedural-idle-life
name: procedural-idle-life
category: creative-arts
field: animation
product: blender
tags: [blender, idle, breathing, blink, moving-hold, procedural, automation, secondary-motion, dialogue, aliveness, python]
level: advanced
status: verified
description: "Procedural baseline life so automated shots aren't frozen: breathing, idle sway, desynced blinks, and speaker head-motion keyed per character in Blender."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Procedural idle life (the baseline that keeps a character from reading as dead)

A character that holds perfectly still reads as **dead** — this is the single biggest
tell that separates automated/previz output from a real show. Before any hand-animated
performance, every on-screen character needs a cheap, always-on **moving hold**:
breathing, micro-sway, blinks, and (when talking) head motion. This skill is the
procedural layer you key automatically per shot; the hand-animated story beats
(acting-performance) ride ON TOP of it. It is not a substitute for acting — it is the
floor below which a shot looks broken.

## The four always-on channels
Key these across the whole shot, per character, on the character's root/control:
1. **Breathing** — a slow vertical bob (± a few mm) plus a small chest-rise tilt, ~0.2–0.3 Hz
   (one breath every 3–5 s). Sine-driven. This alone reads as "alive".
2. **Idle sway** — a very slow weight shift: root rotation ±~1° and/or a tiny lateral
   drift, ~0.1 Hz. Keeps the silhouette from being a statue.
3. **Blinks** — briefly shut the eyes (squash the eye geometry's vertical scale to ~0.08
   for ~2 frames) every ~2.5–4 s. **Desync per character** (seed the interval off the
   character index) — synchronized blinking across a cast is the robotic giveaway.
4. **Speaker head motion** — only on whoever is talking: a gentle head nod/bob (±~1.5°,
   ~1.3–1.6 Hz) for the duration of the VO, so dialogue has physical energy. Silent
   characters get only channels 1–3.

## Curve choices (Blender)
- Breathing/sway/nod: **BEZIER** interpolation (smooth, organic).
- Blinks: **LINEAR** (snappy open/shut; a blink is fast, not eased).
- Drive the continuous channels from `math.sin(t*2*pi*freq + phase)` where `phase` is
  seeded per character so nobody breathes or sways in lockstep.
- Capture the staged base transform first, then add the offsets around it (don't
  overwrite the character's placed position/facing).

## Keep it SUBTLE
Amplitudes are small on purpose: breath ~0.004 BU, sway ~1.1°, lean ~0.7°, nod ~1.6°.
Over-driven idle looks drunk/floaty — worse than frozen. The goal is "calm and alive",
not "performing". If it's noticeable as motion on a still frame, it's too much.

## Finding the parts to drive (automation)
- Root/control: the character's top transform (e.g. a `TURN` empty or the rig root).
- Eyes for blinks: match meshes by name (`eye*`, `*iris*`) and **exclude** brows
  (`*brow*`). Squash their Z scale; works for both modeled eyes and flat eye-cards, and
  for emissive screen-faces (e.g. a CRT character's screen eyes).

## Verify
- [ ] On playback the character is clearly breathing/shifting — but no single still
      frame looks like it's mid-motion (subtlety check).
- [ ] Eyes blink, and two characters in frame do NOT blink on the same frames.
- [ ] The speaker has extra head energy during the line; silent characters stay calm.
- [ ] The staged position/facing and the lip-sync are unaffected (offsets, not overwrites).

**Verified (proof):** applied in the production `render_shot.py` as `animate_life()` and
rendered on shot EP01_SQ01_SH110 (Ivy, dialogue). Frozen → breathing + sway + desynced
blinks + speaker head-motion over the lip-sync; character reads alive-but-calm.

See acting-performance (the hand-animated layer that rides on top), twelve-principles
(moving holds / secondary action), facial-animation (blinks on thought/direction changes),
shot-renderer (where this is wired into the automated pipeline).

## Verified gotcha: scale features about their GEOMETRY centre, not the object origin
Feature meshes often carry baked geometry far from their origin (a build that applies
transforms can leave eye objects with origins at the character's FEET). Any blink squash
or expression scale applied to object scale then pivots about that origin and teleports
the feature (eyes slid to the chest for 2 frames on every blink before this was caught).
Fix: compute the object-space bound-box centre `c = sum(Vector(v) for v in o.bound_box)/8`,
scale, and compensate location by `c * (1 - s)` per axis - correct for any origin, a no-op
when the origin already sits on the feature.
