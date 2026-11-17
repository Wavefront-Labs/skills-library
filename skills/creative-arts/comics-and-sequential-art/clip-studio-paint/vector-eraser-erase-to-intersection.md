---
id: creative-arts.comics-and-sequential-art.clip-studio-paint.vector-eraser-erase-to-intersection
name: vector-eraser-erase-to-intersection
category: creative-arts
field: comics-and-sequential-art
product: clip-studio-paint
tags: [clip-studio-paint, csp-vector-layer, csp-vector-eraser, up-to-intersection, overshoot-lines, vector-inking, clean-line-art]
level: practitioner
status: draft
description: "Clean overshooting ink lines in Clip Studio Paint with the vector eraser: Erase touched area, Up to intersection and Whole line modes, plus settings that avoid erasing wanted strokes."
sources:
  - https://help.clip-studio.com/en-us/First_Topic.htm
  - https://tips.clip-studio.com/en-us
  - https://www.clipstudio.net/en/functions/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vector eraser: erase to intersection

**Goal:** draw confident overshooting strokes, then remove the overshoot to the exact
crossing point in one swipe.

## Setup
- Ink on a **Vector layer** (Layer > New layer > Vector layer).
- Eraser tool > **Vector** sub tool (or enable vector eraser options on another eraser).

## Modes (Tool property > Vector eraser)
| Mode | Effect |
|---|---|
| Erase touched area | behaves like a normal eraser on vector strokes |
| **Up to intersection** | removes the stroke segment touched, up to where it crosses other lines |
| Whole line | removes the entire stroke touched |

## Settings that matter
- "Erase all layers" / "Refer to other layers": decide whether intersections with
  lines on other layers count (useful when figure and background inks are separate).
- Eraser size: smaller gives precision; one swipe over the overshoot is enough.

## Workflow
1. Ink with deliberate overshoots at corners and crossings (faster, more confident
   lines).
2. Swipe each overshoot with Up to intersection.
3. Zoom to check corners; undo and use Erase touched area for awkward spots.

## Gotchas
- Raster layers ignore vector modes; check the layer type icon.
- Lines that only nearly touch have no intersection; the whole stroke may vanish. Undo
  and extend the crossing line first.

## Verify
- [ ] No overshoots left at intersections.
- [ ] No wanted strokes removed accidentally.
