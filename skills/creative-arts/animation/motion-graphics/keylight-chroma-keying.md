---
id: creative-arts.animation.motion-graphics.keylight-chroma-keying
name: keylight-chroma-keying
category: creative-arts
field: animation
product: motion-graphics
tags: [keylight, keying, chroma-key, green-screen, screen-matte, clip-black, clip-white, after-effects, key-cleaner, mixed-media]
level: practitioner
status: draft
description: "Pull a clean green/blue screen key with Keylight in After Effects: screen colour, screen gain/balance, screen matte clipping, core and edge mattes."
sources:
  - https://helpx.adobe.com/after-effects/using/keying.html
  - https://learn.foundry.com/nuke/content/reference_guide/keyer_nodes/keylight.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keylight chroma keying

**Goal:** live action shot on green/blue (presenters, mixed live-action and animation, reference
actors) cut out cleanly with natural edges.

## Procedure (Keylight 1.2 in AE)

1. Apply Keylight (Effect - Keying - Keylight (1.2)).
2. **Screen Colour**: eyedrop a mid-brightness area of the screen near the subject (not a hot spot
   or shadow).
3. View: **Screen Matte**. Adjust Screen Matte - **Clip Black** up until the background is pure black,
   **Clip White** down until the subject's core is pure white. Move in small steps; over-clipping eats
   fine edges.
4. **Screen Gain** (default 100): raise slightly to clean more background, at the cost of edges.
   **Screen Balance**: adjust when the screen colour is impure.
5. **Clip Rollback** restores edge detail lost to clipping.
6. View: Final Result; check edges over a contrasting background.

## Core + edge approach (for hair and motion blur)

Duplicate the layer: one with a hard key (aggressive clipping) choked in for the solid core, one with
a soft key for edges only. Combine (core over edge). This separates "solid inside" from "soft detail".

## Before keying

- Garbage-mask far areas (rigs, screen edges) with a loose mask first; Keylight then only works on
  the area near the subject.
- Denoise compressed footage slightly; 4:2:0 footage keys with blocky edges; key from the best
  source (ProRes 4:2:2 or raw).

## After keying

- Spill suppression (`creative-arts.animation.motion-graphics.matte-choke-spill-suppression`).
- Light wrap from the new background to integrate edges.

## Gotchas

- Keying from a camera-graded LUT'd proxy loses chroma separation; key the camera original.
- Clipping the matte to perfect black/white everywhere produces hard cut-out edges; keep some grey
  at hair and motion blur.

## Verify

Screen Matte view: background solid black, subject core solid white, edges grey only where detail
lives; Final Result over black, white and the real background shows no green fringe or holes.
