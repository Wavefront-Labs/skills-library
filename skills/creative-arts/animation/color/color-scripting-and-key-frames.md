---
id: creative-arts.animation.color.color-scripting-and-key-frames
name: color-scripting-and-key-frames
category: creative-arts
field: animation
product: color
tags: [color, color-script, key-frames, thumbnails, palette, mood-board, pre-production, art-direction, storyboard, previs, emotional-arc, animation, film]
level: practitioner
status: draft
description: "Planning a film's emotional color arc as a sequence of small thumbnail keys before a shot is lit or graded"
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Color scripting and key frames

**Goal:** decide, before any shot is lit or rendered, how color and value carry
the story's emotional arc — as a short strip of small thumbnail "key frames,"
one per sequence or beat, that reads at a glance. This is the planning craft
that `creative-arts.animation.color.color-grading` later *realizes* on actual
footage, and that lighting (`lighting`) and the shader/material setup execute
per shot. Confusing the two is the most common mistake: a color script is not
a grade preview and is never rendered from the real asset — it is a fast,
low-fidelity proxy for an idea, made in hours, not days.

## What a color script actually is

A sequence of small (roughly postage-stamp to index-card size) flat-color
thumbnails, one per major beat/sequence, laid out in a single strip or grid in
viewing order. Each thumbnail answers one question: *what is the dominant
value and hue of this moment, and how does it feel next to its neighbors?*
Classic reference points: Pixar's published color scripts (Up, Inside Out) are
the public example of the format — study them for density and arc shape, but
never trace or reuse their actual palettes (sourcing/IP risk; paraphrase the
method, not the art).

Properties that matter more than any individual frame:
- **It is a strip, read in sequence.** The craft is the *relationship* between
  adjacent keys — a single frame means nothing in isolation. If a frame looks
  "good" alone but doesn't contrast or rhyme with its neighbors, it is wrong.
- **Value (light/dark) is decided before hue.** Squint at the strip, or
  desaturate it: the value pattern (where is it dark, where does it open up)
  should still read the story's rhythm. Hue is the second pass.
- **Low fidelity on purpose.** Flat color blocks or soft gradients, no detail,
  no character acting, often painted in minutes per frame in Photoshop/Krita
  or even Blender's grease pencil. Speed lets you iterate the *arc*, not a
  picture. If a key takes more than ~20–30 minutes you've drifted into
  illustration, not scripting.

## Workflow

1. **Break the story into beats**, not shots — usually 15–40 keys for a feature,
   fewer (5–15) for a short or an episode. One key per emotional unit: a scene,
   or a turn within a scene if the mood pivots hard.
2. **Draft the value arc first**, in grayscale or near-grayscale thumbnails.
   Mark where the film is darkest (the low point) and brightest/most open (the
   relief or climax) before touching hue — this is the backbone everything
   else hangs off.
3. **Assign a palette family per act/mood**, not per shot. Reuse the same 3–5
   dominant hues across a whole sequence so cutting within it feels like one
   world; change the family deliberately at a turning point (e.g. "un-gold" —
   the warm-gold family curdled toward sickly green once the mood breaks).
4. **Pitch the strip to the director/showrunner before refining any single
   frame.** The sequence as a whole is the deliverable in review 1; polishing
   one key ahead of approval wastes the fast-iteration advantage of the format.
5. **Hand off as a reference sheet**, not a spec: each key frame + a short
   palette swatch (hex values or a tiny gradient strip) per sequence, pinned
   where lighting and comp can see it. The color script does not dictate exact
   RGB values for the final grade — it dictates *intent* that lighting
   interprets per shot and color-grading realizes per frame.

## Key frames vs storyboard frames vs lighting keys

These three get conflated constantly:
- **Storyboard frame** — composition and staging, usually B&W or flat gray.
  Color is explicitly not its job.
- **Color key / color script frame** — color and value only, loose staging,
  made from or alongside the boards once beats are locked.
- **Lighting key** — a single shot (sometimes the hero/anchor shot a whole
  scene is matched to in grading) rendered at real fidelity to prove the mood
  works in 3D/final medium; this comes *after* the color script and is a
  much higher-fidelity, much more expensive artifact. Don't skip the cheap
  color-script pass and jump straight to an expensive lighting key — that's
  how a studio burns days discovering the arc doesn't work.

## Gotchas

- **Don't paint the color script in the final render's color space** (linear
  EXR, AgX, etc.) — it's a planning tool in whatever display-referred paint
  app is fast, not a preview of the finished grade. Trying to "pre-grade" in
  the color script conflates two different jobs and usually produces palettes
  that don't survive contact with real lighting.
- **A palette family that looks distinct in isolation can collapse once lit**
  (two "different" blues become the same blue under one key light). Flag this
  risk in the handoff note rather than assuming lighting will catch it.
- **Revisit the script after the edit locks**, not just once up front — a cut
  scene or reordered beat breaks the arc's pacing even if no individual key
  changed.
- Uncertain / unconfirmed here: exact thumbnail size/tooling conventions vary
  by studio; there's no single industry-standard dimension or file format for
  a color-script frame, so treat the sizes above as a practical starting
  point, not a rule.

## Verify

1. Squint at (or desaturate) the full strip: the dark/light rhythm still
   matches the story's intended pacing, independent of hue.
2. Hold any two adjacent keys side by side: the palette either clearly
   continues the current family or clearly, deliberately breaks it at a story
   turn — never an accidental drift.
3. Count keys against beats: every major emotional turn in the outline has a
   corresponding key; no key exists that doesn't map to a beat.
4. Ask lighting/comp to name the mood from the key alone, no caption: if they
   can't, the key isn't doing its job.
5. Confirm no individual key took so long to make that revising the whole arc
   feels expensive — if it does, you've drifted from scripting into
   illustration.
