---
id: creative-arts.animation.blender.crowd-animation
name: crowd-animation
category: creative-arts
field: animation
product: blender
tags: [blender, crowd, background-characters, cycles, desync, phase-offset, variation, instancing, lod, nla, baking, procedural, pipeline, secondary-characters]
level: advanced
status: docs-checked
description: "Make many background characters feel alive cheaply in Blender: offset cycles, desync phase and timing, pose/scale variation, instancing, LOD, pipeline-driven."
sources:
  - https://docs.blender.org/manual/en/latest/editors/nla/sidebar.html
  - https://docs.blender.org/manual/en/latest/editors/dope_sheet/modes/action.html
  - https://docs.blender.org/api/current/bpy.types.NlaStrip.html
  - https://docs.blender.org/manual/en/latest/editors/graph_editor/fcurves/modifiers.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

Counts, percentages and tier splits in this skill are practice, not values from the Blender manual; the manual and Python API docs were used to check NLA, modifier and property names.

# Crowd animation (many characters, alive, cheap)

A crowd is the fastest way to make a production shot read as a *world* and the fastest
way to wreck it: fifty copies of one loop, all breathing on the same frame, screams
"render farm". The craft is almost entirely about **desync and variation** — breaking
the identical-robot look with the cheapest possible means. You are not hand-animating
fifty characters; you are animating a handful of cycles and then destroying their
sameness. This builds directly on `procedural-idle-life` (the always-on floor each body
needs) and uses the cycle/offset tools from `graph-editor-polish`.

## The identical-robot look (what you're fighting)

Two tells give a fake crowd away instantly:

1. **Phase lock** — everyone's cycle is on the same frame. All heads bob up together, all
   feet plant together, every idle sways left in unison. The eye catches synchronised
   motion across bodies before it catches anything else.
2. **Pose/shape lock** — everyone is the same height, same pose, same facing, same
   silhouette. Even desynced, a row of identical statues reads as wallpaper.

Beat both and a crowd of cheap cycles reads as a living street. Everything below is in
service of those two.

## Build a small library of cycles, not many

- Author **3-6 base cycles** by hand (or adapt from hero work): e.g. idle-stand-A,
  idle-stand-B (weight on other foot), slow-walk, browse/look-around, lean-and-chat.
  Each is one clean looping action following `body-mechanics` and made cyclic with the
  **Cycles modifier** (`graph-editor-polish`).
- Put each cycle in an **NLA strip** (Nonlinear Animation editor) as an action. NLA is
  the crowd workhorse: you can slide a strip in time (offset), scale its length (retime
  with **Playback Scale**), blend between two, and loop it with **Repeat** — per instance,
  non-destructively. Push the base action down to an NLA track (Dope Sheet Action Editor
  **Push Down**, which leaves the object without an active action), then each background
  character references the strips.
- Favour actions that loop seamlessly (last key == first key; the action's Cyclic
  Animation / Manual Frame Range can mark the loop range) so you can set the strip to
  **Repeat** and let it run the length of the shot.

## Desync: the single most important step

For every instance, offset in BOTH time and phase so no two share a frame:

- **Time offset (frame start):** shift each character's NLA strip by a random number of
  frames (e.g. `strip.frame_start_ui += random.randint(0, cycle_len)`). Per the Python
  API, `frame_start_ui` also moves the strip's end frame, whereas `frame_start` changes
  only the start, so use `frame_start_ui` to slide a whole strip. Now the same walk cycle
  plants feet at different moments across the crowd.
- **Phase offset on procedural channels:** the breathing/sway/blink layer from
  `procedural-idle-life` is sine-driven with a per-character `phase` — seed it off the
  instance index so nobody breathes, sways, or blinks in lockstep. Desynced blinking
  across a cast is the classic giveaway; seed it per body.
- **Timing/speed variation:** scale each NLA strip's playback (`strip.scale`, the
  Playback Scale, default 1.0) by a small random amount (practice) so cycles run at slightly different tempos — this also prevents them drifting back into
  phase over a long shot (same-length loops eventually re-sync; different lengths never do).
- **Rule of thumb:** if you can see two characters "pulsing" together anywhere in frame,
  you haven't desynced enough.

## Variation: kill the shape lock

Cheap, high-impact, done once per instance:

- **Non-uniform scale** per body: ±5-12% overall, plus small independent X/Y/Z so not
  everyone is the same build. Keep it subtle — too much reads as caricature unless the
  show wants it.
- **Pose/facing variation:** rotate each instance's `root` to face slightly differently,
  stagger positions so the crowd isn't a grid, and mix which base cycle each one uses.
- **Palette/material variation:** swap a material index or tint per instance (hair/shirt
  colour). For cel shading this is huge — a sea of the same flat colour reads as one
  object; varied flats read as many people. Ties to `cel-shading`.
- **Mirror some instances** (negative X scale) to double your silhouettes for free —
  watch for text/asymmetric detail that would flip.
- **A few "feature" bodies:** 2-3 characters near camera get a bit of unique hand touch
  (a gesture, a head turn on a beat) so the eye has something specific to land on. The
  back of the crowd can be pure cycle.

## Instancing, baking, and cost

- **Instance the geometry** (linked duplicates / collection instances) so fifty bodies
  don't multiply mesh memory. The rig/action can be shared; the per-instance variation
  lives in the empty/root transform, the NLA offset, and the material override.
- **Bake before render** on the data-driven pipeline: bake each instance's final
  animation (procedural + NLA offsets resolved) to keys or to an Alembic/point cache so
  the renderer isn't evaluating sine drivers and NLA blends per frame across the whole
  crowd. Bake, then Decimate (`graph-editor-polish`) if you need the curves editable.
- **LOD by distance:** background/far characters don't need the full rig. Tiers:
  - *Near* — full rig, baked, with a feature touch.
  - *Mid* — base cycle, desynced, no hand touch, maybe reduced subdiv.
  - *Far* — lowest subdiv, simplest idle cycle (even just the breathing/sway layer), or a
    near-static body with only a blink. At that distance the detail is invisible;
    spend nothing on it.
  Drive the tier off camera distance so the budget goes where the eye looks.

## Crowd flow, spacing, and entrances

A crowd isn't just posed bodies — it has to occupy space believably over time:

- **Avoid interpenetration and the parade-ground grid.** Stagger positions off a grid
  (jitter each slot by a random offset), and for walking crowds give each a slightly
  different heading and speed so paths don't cross through each other. You don't need a
  full boids simulation for a background street — hand-placed lanes with jittered spacing
  read fine and are deterministic (a sim is a last resort when a crowd must genuinely
  path-find around obstacles; it's expensive and non-repeatable without caching).
- **Personal space reads as real.** People don't stand evenly spaced; they clump
  (pairs/groups chatting) and leave gaps. Cluster 2-4 instances facing each other on the
  "chat" cycle, then scatter singletons between. Clumping-plus-gaps reads human; even
  spacing reads as placed props.
- **Staggered entrances/exits:** if the crowd moves through frame, offset each body's
  start time so they enter raggedly, not as a wall. Fade LOD up as they approach camera.

## Depth and the eye's path

Compose the crowd in depth, not a flat band. Near bodies (the LOD *near* tier with hand
touches) anchor the eye; mid and far tiers fill volume. Keep the busiest motion away from
the shot's focal point unless the crowd IS the subject — a background crowd should
support the hero, so bias its biggest moves to the edges and keep the area behind the
hero's head calmer so reads don't collide. For a cel show the flat colours stack in
depth, so vary tint value (lighter far, where atmospheric recession applies) as part of
the per-instance variation.

## Driving it from the pipeline (production)

Because the renderer is data-driven, the crowd is best described as **data, not
hand-placement**: a shot spec lists crowd instances with position, base-cycle id, frame
offset, scale, tint, and LOD tier; the build script instantiates, offsets, and bakes
them. Seed every random from the instance index (or a shot seed) so the crowd is
**deterministic** — the same shot rebuilds identically, which matters for a reproducible
render farm and for re-rendering a fixed shot. A Python loop over `bpy.data.objects`
that sets `nla_tracks[...].strips[...].frame_start/scale`, the `root` transform, and the
material index per instance from that spec is the whole system.

## Verify (pass/fail)

- [ ] **No phase lock:** no two visible characters share cycle frames — feet plant, heads
      bob, and idles sway at different moments. Scrub and watch for any two "pulsing"
      together. (fail = render-farm look)
- [ ] **Blinks/breathing desynced** per body (seeded phase), not a synchronised cast.
      (fail = robot tell)
- [ ] **Shape variation:** varied height/build (non-uniform scale), facing, pose, and
      material/tint — not a grid of identical silhouettes. (fail = wallpaper)
- [ ] **Different cycle lengths/speeds** so the crowd doesn't drift back into sync over
      the shot. (fail = re-sync by the end)
- [ ] **Instanced geometry + baked animation** before render; **LOD** applied so far
      bodies cost almost nothing. (fail = farm chokes on full rigs)
- [ ] 2-3 near-camera bodies have a specific hand touch for the eye to land on; the crowd
      has focal points, not uniform mush. (fail = nothing to look at)
- [ ] Crowd is **deterministic** from the shot spec (seeded), so a rebuild/re-render is
      identical. (fail = crowd reshuffles every build)

See `procedural-idle-life` (the per-body always-on floor), `graph-editor-polish` (cycles,
bake, simplify), `body-mechanics` (the base cycles), `cel-shading` (per-instance flats),
`twelve-principles`.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release RST) and current Python API docs.
Confirmed: NLA strip Playback Scale and Repeat (sidebar docs); `NlaStrip.scale` (default 1.0), `repeat`, `frame_start` and `frame_start_ui` semantics; Dope Sheet Action Editor Push Down; Cycles F-modifier; action Cyclic Animation and Manual Frame Range. Fixed: sliding a whole strip needs `frame_start_ui` (changing `frame_start` alone changes only the start); "Simplify" is Decimate. Removed: ±10-20% scale, ±5-12% variation and "EEVEE Next" wording (no doc coverage; marked practice).
Method: documentation only; no commands were run.
