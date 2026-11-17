---
id: creative-arts.animation.blender.technical-animation-finaling
name: technical-animation-finaling
category: creative-arts
field: animation
product: blender
tags: [technical-animation, finaling, character-finaling, cleanup, intersection, popping, sim-repair, cache, qc, post-animation, shot-finishing]
level: advanced
status: verified
description: "Shot finishing between animation/sim and lighting: detect and fix intersections, pops, cache defects and silhouette breaks — the studio 'finaling' department, done procedurally."
sources: []
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# SKILL: Technical animation / character finaling

**Goal:** no shot reaches lighting/render with a defect that animation and sim each
assumed the other owned. At a feature studio this is a whole department (character
finaling / technical animation) precisely because the handoff gap is where defects
live: cloth intersecting a thigh, hair through a collar, a one-frame pop in a
mocap-retargeted clip, an eyelid that never quite closes. One person plus automation
replaces the department with a **detector pass + a small toolbox of local fixes**.

## 1. Detect mechanically, fix locally

Never scrub looking for problems — list them. Per shot, run a checker over the frame
range and emit `(frame, object, defect, magnitude)`:

- **Pops:** per-bone world-position delta between consecutive frames; flag deltas
  over ~N× the running median (retarget seams, cycle joins, constraint flips).
- **Intersections:** for each hero pair (garment↔body, hair↔shoulders, hand↔prop),
  sample proximity — a BVH overlap count or a shrinkwrap-distance probe on proxy
  meshes is enough at stylized tier. Flag sustained negative clearance.
- **Contacts:** feet below ground plane / floating at contact frames (foot bone z vs
  floor at frames where the clip says planted).
- **Face closure:** blink/viseme channels that never reach their endpoints (an
  eyelid at 0.93 forever reads as staring; endpoints are a data check, not a look).
- **Silhouette breaks:** render the matte at proof resolution and diff area frame to
  frame; a silhouette that jumps without a cut is a pop the bone check missed.

## 2. The fix toolbox (cheapest first)

1. **Re-time, don't re-pose:** a pop at a cycle join is fixed by nudging the
   f-modifier/offset, not by keying over it.
2. **Local counter-key:** one corrective key on the offending bone/shape over 3–5
   frames, eased; never a full-range re-key of a working clip.
3. **Push geometry, not animation:** persistent garment↔body clearance is a
   Solidify/shrinkwrap offset or a vertex-group thickness fix on the garment —
   solve the class, not the frame.
4. **Per-shot override layer:** keep fixes in a shot-level action/NLA layer over the
   library clip, so the clip stays clean for the next shot that uses it.
5. **Cache repair last:** re-sim only the failed range with tightened settings;
   a full re-sim for a 10-frame defect is the expensive path.

## 3. Order and ownership

Finaling runs **after** performance + sim, **before** lighting — defects fixed after
lighting invalidate the lighting. Everything found goes in the shot's defect list
even if declined ("reads fine at final framing" is a legitimate disposition — at
WIDE, centimetre intersections are invisible; spend where the camera is close).

## 4. The law

**A defect list with dispositions per shot, or the pass didn't happen.** The
department's real product is the guarantee downstream: lighting can trust every
incoming cache. Automation makes the guarantee affordable; the checklist makes it
real.

## 5. Implemented detector (verified on a series cut)

The minimum that catches "people stuck in walls" and tearing, run inside the shot
scene before any pixel renders, writing `<shot>/finaling.json` for the episode QC to
aggregate:

- **Clipping:** sample every Nth vertex of each character's evaluated body at three
  frames (first, mid, last); ray-parity (+x, odd hit count = inside) against a BVH
  per closed set mesh (kit pieces, barriers, vehicles — props and characters excluded,
  the huge shell slabs skipped by vertex count); plus a ground test (z < −3 cm).
  Report `<char> f<frame>: n sampled verts inside <object>` when n ≥ 3.
- **Tearing:** compare each evaluated edge length to its rest length from the mesh
  data; count edges beyond 2.5×. Red above a small threshold (see below).

Rest lengths come from `mesh.data`, evaluated geometry from
`object.evaluated_get(depsgraph).to_mesh()` after `scene.frame_set(f)`. Ray parity
is unreliable on open planes (interior walls); upgrade to signed distance when those
start clipping. Verified CLEAN on an alley two-shot and a single that had read as
intersecting in an earlier cut; the report is what the episode scorecard's
clipping/tearing rows are filled from, so the eye never has to find these again.

**Make sure the detector is actually running.** The tearing check compares edge
counts before comparing lengths; an inverted-hull outline (a Solidify modifier)
doubles the evaluated edge count, so on every outlined character the check silently
skipped. It only came alive when the hull was switched off for a flat-2D look, and
immediately found ~900 stretched edges on one character and ~270 on another, all in
the hands. Disable shell modifiers on the evaluated copy (or compare base edges only)
and log the counts the check compared, so "0" can be told apart from "never ran".

**The tear it found: a restyled mesh on an un-restyled skeleton.** A proportion pass
widened every vertex by a build factor (1.10x) and scaled the head about the neck,
but left the armature's rest bones where they were. Hands ~0.7 m out in T-pose ended
up centimetres off their own bones and swung about the wrong pivots in every clip:
the owner's "mangled arms". Any transform applied to skinned rest vertices must be
applied to the edit bones (head and tail) by the same function. Same for a
finger-shortening pass: shorten the finger bones about the knuckle along with the
mesh, or every bend throws the vertices backwards. Fixed, the count fell 896 → 2.

Threshold: a handful of stretched edges per shot is face shape keys at full value;
a broken rig is hundreds. Red at > ~40, not at 1.

## Verify

- [ ] Checker runs per shot and emits (frame, object, defect, magnitude) rows.
- [ ] Every row has a disposition: fixed (how) / declined (why, with framing noted).
- [ ] Fixes live in override layers; library clips and caches stay pristine.
- [ ] Re-running the checker after fixes reports zero undispositioned rows.
- [ ] Blink/viseme endpoint check passes for every speaking/on-camera character.

See also: `mocap-retarget.md`, `cloth-simulation.md`, `facial-animation.md`,
`../pipeline/dailies-review.md`.
