---
id: creative-arts.animation.principles.applying-timing-and-spacing
name: applying-timing-and-spacing
category: creative-arts
field: animation
product: principles
tags: [animation, timing, spacing, spacing-chart, frame-count, weight, ease-in, ease-out, exposure-sheet, x-sheet, dope-sheet, graph-editor, moving-hold, drag-and-overlap, pose-to-pose, cel, cg]
level: practitioner
status: draft
description: "How to set frame counts and spacing charts (not just keyframe curves) to read as weight, speed and mood, tool-agnostic."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Applying timing and spacing

Timing is *how many frames* an action takes; spacing is *how the frames are
distributed* within that count (the gaps between drawings/keys). Two actions
with identical frame counts read completely differently depending on spacing —
this is the single most common thing new animators get backwards: they fix
"floaty" or "stiff" motion by changing the frame count when the real problem is
the spacing curve. This skill is craft-level and applies whether you're
spacing drawings on an exposure sheet, placing keys in Blender's Graph Editor,
or setting easing curves in After Effects/Rive/CSS.

## Timing: how many frames
- Count in **frames at your project's fps**, not seconds — "12 frames" means
  something concrete, "half a second" doesn't tell you the spacing.
- Rough starting counts at 24fps (verified against hand-drawn and 3D practice,
  adjust by weight/mood — these are not laws):
  - A sharp take/accent (eye blink, snap reaction): 2–4 frames to the extreme.
  - A quick gesture (hand point, head snap): 6–10 frames.
  - A walk step (contact to contact): ~12 frames brisk, ~16–18 neutral, 22+
    tired/heavy.
  - A full-body settle after a big action (landing, sitting): 8–14 frames of
    overshoot + settle, on top of the main action's frames.
- **Heavier = more frames to speed up, fewer frames to slow down.** A bowling
  ball takes longer to get moving and longer to stop than a tennis ball — but
  once moving, heavy things don't idle at a "cruise" pace the way light,
  energetic things do. Translate mood into frame count before touching
  curves: a sluggish character gets MORE frames per beat, an excited one
  gets FEWER.
- Don't space every beat evenly. A scene with uniform frame counts across all
  actions reads as mechanical regardless of easing — vary counts beat to beat
  the way real line delivery varies pace.

## Spacing: where inside those frames
- Draw or chart the **in-betweens' spacing**, not just the two extremes. Bunch
  (close together) near the extremes for ease-in/ease-out (slow-in, slow-out —
  principle #6), spread them in the middle where the object is at speed.
- A spacing chart is a strip of tick marks under the action showing the gap
  between each in-between — literally space on paper/screen, not time. Even
  if you never draw one by hand, think in this shape: tight-tight-wide-wide-
  wide-tight-tight for an ease-in/out arc; tight-wide-wide-wide-wide-wide for
  a hard snap-into-motion (anticipation release).
- In keyframe tools this maps to the easing curve shape in the Graph Editor /
  Timeline, not frame count: a Bezier ease has bunched tangent handles near
  the extremes; a linear curve has even spacing (reads mechanical, use only
  for pure mechanical objects — conveyor belts, not characters); a
  **moving hold** is near-zero spacing (flat curve) with a tiny drift so it
  doesn't look frozen.
- For snappy/limited (cel, 2D-on-3D, stop-motion-style) work, spacing can be
  **stepped**: hold a pose flat for several frames then snap-cut to the next
  with almost no in-between spacing at all — this is a spacing choice, not a
  timing one, and it's what makes limited animation read as deliberate rather
  than cheap when done on purpose.

## Gotchas
- Changing fps (e.g. exporting a 24fps test to a 30fps deliverable) without
  rescaling frame counts changes the *timing* even though the spacing shape
  stays the same — always re-derive frame counts for the target fps, don't
  just drop the same keyframe numbers in.
- Easing presets in off-the-shelf tools (CSS `ease-in-out`, generic Bezier
  defaults) are tuned for UI motion, not performance — they're almost always
  too gentle/symmetrical for character work. Treat them as a starting point,
  then hand-adjust handle weight so the bunch near the extreme is tighter
  than the default.
- "More frames" is not automatically "better" or "more polished." Padding a
  beat with extra hold frames without a reason (no new information, no
  change in thought) just reads as slow, not weighty. Every added frame
  should buy either weight, comedic timing, or a beat of thought — not be a
  default safety margin.
- Uncertain: exact frame-count numbers above are a practitioner's working
  defaults at 24fps for a human-scale character; for non-human creatures,
  mechanical objects, or very different fps targets (12fps stop-motion,
  60fps game loops) these need rescaling by eye on a real shot — treat the
  counts as starting points, not verified universals.

## Verify
- [ ] Beat has a frame count stated in frames at your actual project fps,
      not "a few frames" or seconds.
- [ ] Spacing (easing curve/chart) is drawn or set independently of the
      frame count — you can point to where it's bunched vs. spread.
- [ ] A fast/light action and a slow/heavy action in the same shot use
      visibly different frame counts, not just different curves.
- [ ] No beat has uniform, evenly-spaced in-betweens unless the subject is
      genuinely mechanical (then confirm that's the intent).
- [ ] Re-timed for the actual output fps if it differs from the fps the
      counts were planned at.

Related: `creative-arts.animation.principles.twelve-principles` (slow-in/
slow-out, timing as a named principle), `creative-arts.animation.principles.squash-and-stretch-in-production`
(how spacing interacts with volume on impact frames),
`creative-arts.animation.principles.anticipation-and-follow-through-staging`
(timing the wind-up/settle around a main action).
