---
id: creative-arts.comics-and-sequential-art.comic-colouring.scroll-background-colour-gradients
name: scroll-background-colour-gradients
category: creative-arts
field: comics-and-sequential-art
product: comic-colouring
tags: [comic-colouring, digital-comic-colour, scroll-background-gradient]
level: practitioner
status: draft
description: "Colour the gutter and background of vertical-scroll comics with gradients that shift mood and time across an episode, and transition smoothly between scenes on screen."
sources:
  - https://www.webtoons.com/en/creators101/webtoon-canvas
  - https://books.google.com/books?vid=ISBN9780823010301
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Colour gradients for scroll backgrounds

**Goal:** in vertical-scroll comics, the space between panels carries mood and
transitions rather than being dead white.

## Uses
- Scene transition: background shifts from day blue to sunset orange to night navy
  across the scroll.
- Emotional beat: white gutter fades to black for a horror reveal.
- Flashback: background tint matches the flashback colour code.

## Method
1. Build the episode on one tall canvas (or full-length assembly) before slicing.
2. Background layer under all panels; draw long gradients over 2000-6000 px
   of scroll for slow shifts, shorter for sharp changes.
3. Keep text areas (balloons placed in the gutter) on stable values for legibility.
4. Avoid banding: work in 16-bit or add slight noise/dither on long gradients;
   check after JPEG export.
5. Slice for upload only after the gradient is final; gradients across slice seams
   must match exactly (export at the same quality settings).

## Gotchas
- Dark mode readers and phone brightness: test on a phone at low brightness.
- Very saturated gradients cause eye strain over a long scroll.

## Verify
- [ ] No banding or seam lines in exported slices.
- [ ] Gutter colours support the scene changes.
