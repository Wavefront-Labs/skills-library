---
id: creative-arts.animation.vector-graphics.animate-symbols-tweens
name: animate-symbols-tweens
category: creative-arts
field: animation
product: vector-graphics
tags: [animate-symbols, adobe-animate, graphic-symbol, movie-clip, classic-tween, library-panel, nested-symbols, sync-graphic, first-frame, cutout-animation]
level: practitioner
status: draft
description: "Build Adobe Animate characters from graphic and movie clip symbols: when to use each, library organisation, nested timelines synced to the main timeline, and classic tweens."
sources:
  - https://helpx.adobe.com/animate/using/symbols.html
  - https://helpx.adobe.com/animate/using/classic-tweens.html
  - https://helpx.adobe.com/animate/using/symbol-instances.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Animate symbols for character animation

**Goal:** reusable, swappable character parts (heads, mouths, hands) in Adobe Animate that scrub and render
correctly frame by frame.

## Symbol types

| Type | Timeline | Use |
|---|---|---|
| **Graphic** | synced to the parent timeline (scrubbable, renders in exported video) | character parts, mouth charts, lip sync, anything animated for video |
| **Movie clip** | independent timeline (plays at runtime) | interactive/HTML5 content, filters and blend modes, effects needing runtime |
| **Button** | four state frames | interactivity only |

For animation destined for video, use graphic symbols: movie clips' internal animation doesn't show when scrubbing
and can export as frozen frames.

## Swapping drawings: first frame control

A graphic symbol containing a mouth chart (one drawing per frame) can be set per instance in Properties -
Looping: **Single Frame** and **First** = frame number of the desired mouth. The Frame Picker panel shows
thumbnails for picking. This is the core of Animate lip sync and hand-pose swaps.

## Library organisation

Folders per character, then parts (`MIA/head`, `MIA/mouths`, `MIA/hands`); names with prefixes so swapping
(Properties - Swap) is fast. Keep registration points at pivots (neck base, shoulder) before animating.

## Classic tweens on rigs

- Classic tweens interpolate instance transforms between keyframes; set easing with the Ease panel or custom
  curves.
- Rotate around the transformation point (white circle), moved to the joint for each instance.
- Animate's layer parenting (parent view in the timeline) makes simple FK rigs: child layers follow parent layers.

## Gotchas

- Nested graphic symbols must have enough frames: a 10-frame blink symbol on a 30-frame span loops unless set to
  Play Once or Single Frame.
- Breaking apart symbols for quick fixes destroys reuse; edit in place instead.
- Changing a symbol's registration point after animating shifts every instance.

## Verify

Scrub the main timeline: every nested animation follows, mouth swaps change on the right frames, and an exported
video shows the same as the scrub.
