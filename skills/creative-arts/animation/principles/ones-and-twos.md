---
id: creative-arts.animation.principles.ones-and-twos
name: ones-and-twos
category: creative-arts
field: animation
product: principles
tags: [animation, timing-principle, ones-and-twos, on-twos, on-ones, frame-rate, limited-animation, stepped, stylized-cg, spider-verse, strobing]
level: practitioner
status: draft
description: "Choose between animating on ones, twos or mixed exposures: what each buys, when to switch mid-shot, strobing on pans, and stepped-CG 'on twos' setups."
sources:
  - https://books.google.com/books?vid=ISBN9780865478978
  - https://en.wikipedia.org/wiki/Inbetweening
  - https://en.wikipedia.org/wiki/Limited_animation
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Ones and twos

Goal: pick the exposure rate per action. "On ones" = a new drawing/pose every frame (24 per
second); "on twos" = each held for 2 frames (12 per second); "on threes/fours" for limited
styles.

## What each buys
| Exposure | Reads as | Use for |
|---|---|---|
| Ones | smooth, fluid, fast-capable | fast action, camera moves, pans with characters, subtle realistic acting |
| Twos | snappy, crisp, handmade | most 2D TV/feature acting, stylized CG |
| Threes/fours | limited, graphic | anime limited motion, holds with lip sync, budget TV |

Williams' rule of thumb: twos for most things, ones for fast action and when the camera or
background moves - twos against a moving pan strobe.

## Mixing
- Switch to ones for a fast move inside a twos shot (a whip, a fall), then back.
- Characters on twos over a background pan on ones causes a visible jitter: either put the
  character on ones during the pan or pan on twos as well.
- Anime commonly mixes: threes for walks, ones for sakuga action shots.

## Stepped CG on twos (Spider-Verse style)
- Keys on every other frame with constant interpolation, or animate on ones then bake and
  step (Blender: Graph Editor > Key > Bake, then Stepped Interpolation F-Curve modifier with
  step size 2; Maya: bake then set stepped tangents on twos).
- Cameras usually stay on ones; secondary FX may stay on ones.
- Motion blur off or reduced - blur on twos looks wrong.

## Failure modes
- Twos on a character tracked by a camera move: strobing.
- Mixing rates within one character's parts unintentionally (face on ones, body on twos).
- Ones everywhere in a stylized show: loses snap and costs double.

## Verify
- [ ] Exposure chosen per action and noted on the x-sheet/blocking notes.
- [ ] No strobing where character and camera/BG move together.
- [ ] In stepped CG, step offset is consistent across all character controls.

Related: `creative-arts.animation.principles.applying-timing-and-spacing`.
