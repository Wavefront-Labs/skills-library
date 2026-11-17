---
id: creative-arts.animation.principles.twelve-principles
name: twelve-principles
category: creative-arts
field: animation
product: principles
tags: [animation, twelve-principles, keyframes, timing, overlap, anticipation, cel, performance]
level: practitioner
status: verified
description: "The 12 animation principles as Blender keyframe recipes, cel-style: ease arcs, snap accents (CONSTANT), overlap, anticipation."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The 12 Principles — applied in Blender (cel/MD style)

Disney's 12 principles are the craft of making keyframes read as *performance*,
not interpolation. This is the animator's seat. Applied to a production's limited
cel style (hold-heavy, snappy), verified on the Ep1 `pixel_enter` shot.

## The principles, as keyframe recipes
1. **Squash & stretch** — volume-preserving deform on impact/stretch. Cel/MD uses
   it sparingly on hero beats (a hop landing, a reaction pop). Scale on one axis,
   inverse on the others, back to 1 within 2–3 frames.
2. **Anticipation** — wind-up before an action. Pixel's entrance: a small pull-back
   (`key_loc(1, 4.25)`) before the settle forward. Nothing big moves without a
   tell first.
3. **Staging** — one clear idea per shot; silhouette reads against the bg. Light
   and camera serve it (the MD cool rim exists to pop the silhouette).
4. **Pose-to-pose** (not straight-ahead) — block the extremes first (key poses),
   let breakdowns/holds fill. Suits limited animation: strong held poses +
   snappy transitions.
5. **Follow-through & overlapping action** — loose parts lag the body. Pixel's
   antennae perk *after* the body settles and drag back (`f85→100→120`), never
   in lockstep with the hop.
6. **Slow in / slow out** — ease on the extremes. BUT: viseme swaps and hard
   accents use **CONSTANT** interpolation (snap), not ease — that's the cel look.
   Mix: ease the body arcs, snap the expressions.
7. **Arcs** — limbs/heads travel on curves, never straight lines. Check the
   motion path; a head turn dips slightly.
8. **Secondary action** — supports the main (antennae perk reinforces "excited
   hello", doesn't compete).
9. **Timing** — frame counts = weight + mood. Snappy = fewer frames between
   extremes. ~8–12f for a beat accent at 24fps.
10. **Exaggeration** — push beyond literal. MD/Rick&Morty push expressions and
    takes hard; realism is not the target, *readability* is.
11. **Solid drawing** — poses obey 3D volume/weight even stylized. Keep contact
    (feet planted), avoid floaty roots.
12. **Appeal** — clear, charismatic design in motion. Clean silhouette, no twins
    (symmetrical identical limbs), eye-catching asymmetry.

## Cel-style ground rules (what makes it read as 2D-on-3D, not CG)
- **Hold on poses.** Stepped/held frames, not constant motion. A pose can sit 6–12f.
- **Snap the accents.** CONSTANT interpolation on expression/viseme/take frames.
- **Ease only the arcs** (body travel, camera). Default Bezier there.
- **On 2s where it suits** — render every frame but animate changes every 2nd
  frame for the hand-drawn cadence (optional per shot).
- **Camera is an actor** — slow push adds energy to a static talk (verified:
  30mm 0.6-unit push over the shot).

## Blender how-to (verified)
- Keyframe `location`/`rotation_euler` on the character ROOT empty for body;
  on loose-part objects for overlap.
- `fcurve.keyframe_points[].interpolation = 'CONSTANT'` for snaps;
  leave `'BEZIER'` for eased arcs. Set per-fcurve, not globally.
- Motion-path check: select root, Object ▸ Motion Paths ▸ Calculate (in GUI); or
  trust arc keyframes (dip the midpoint).

## Self-check before calling a shot animated
- [ ] Every big move has anticipation + a settle (overshoot/follow-through).
- [ ] Loose parts lag & drag (not lockstep).
- [ ] Accents snap (CONSTANT), arcs ease (BEZIER) — not all one or the other.
- [ ] Silhouette reads at the key pose; feet/contact planted (no float).
- [ ] One clear idea; secondary action supports not competes.

See lip-sync (viseme snaps), camera-cinematography (push/arc), character-blockout.
