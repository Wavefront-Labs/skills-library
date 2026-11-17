---
id: creative-arts.visual-art.procreate.hold-frames-and-foreground-background-frames
name: hold-frames-and-foreground-background-frames
category: creative-arts
field: visual-art
product: procreate
tags: [visual-art, procreate, hold-frames, hold-duration, background-frames, foreground-frames, animation-assist, onion-skin, cel-animation]
level: practitioner
status: draft
description: "Control timing in Procreate Animation Assist with hold duration per frame and background and foreground frames, to save drawing time and keep animation clean."
sources: ["https://procreate.com/handbook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hold frames and background/foreground frames

**Goal:** extend frames without redrawing, and keep static art out of every frame.

## Hold duration
1. With Animation Assist on, tap a frame in the timeline to open its options.
2. Set **Hold Duration** to make that frame stay on screen for extra frames (see the Handbook for the slider range). A held pose replaces redrawn duplicates, saving effort and file size.
3. Use short holds to add emphasis on key poses and ease in and out of action.

## Background and foreground frames
1. A frame can be set as a **Background** (a layer shown behind every animated frame) or **Foreground** (shown in front), in the same frame options, so that the static scene is drawn once.
2. Typical use: scenery as background; the character animates on top; overlay effects such as rain or vignettes as foreground.
3. Keep them as separate layers in the timeline and avoid making them animated frames by accident.

## Onion skin context
- Onion skin frames and opacity (Animation Assist settings) show previous and next frames as guides while drawing, and their tint colours help distinguish them. See `creative-arts.visual-art.procreate.animation-assist-onion-skins-and-timing`.

## Gotchas
- Holds multiply total duration; recount time when changing fps.
- Deleting or merging a background frame can remove the scene from every frame.
- Foreground frames hide what is drawn beneath if not transparent.

## Verify
- [ ] Playback shows the held pose for the expected time.
- [ ] Background stays static while the character frames change.
