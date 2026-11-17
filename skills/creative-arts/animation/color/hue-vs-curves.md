---
id: creative-arts.animation.color.hue-vs-curves
name: hue-vs-curves
category: creative-arts
field: animation
product: color
tags: [hue-vs-curves, secondary-grading, hue-vs-hue, hue-vs-sat, hue-vs-lum, sat-vs-sat, lum-vs-sat, davinci-resolve, palette-adjustment]
level: practitioner
status: draft
description: "Use Resolve's hue-vs-hue/sat/lum and sat/lum-vs-sat curves for fast, keyless palette adjustments across animated shots without visible matte edges."
sources:
  - https://documents.blackmagicdesign.com/UserManuals/DaVinci_Resolve_19_Reference_Manual.pdf
  - https://www.blackmagicdesign.com/products/davinciresolve/training
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hue-vs curves

**Goal:** shift, saturate or darken a colour family everywhere in the shot without drawing a key.
Curves change colours as a smooth function of hue (or saturation/luma), so there is no matte edge
to chatter.

## The curves (Resolve Curves palette)

| Curve | Does | Example |
|---|---|---|
| Hue vs Hue | rotates one hue toward another | push teal grass toward green |
| Hue vs Sat | saturates/desaturates by hue | calm an over-bright red prop |
| Hue vs Lum | brightens/darkens by hue | darken a bright yellow sky in night grade |
| Lum vs Sat | saturation by brightness | desaturate shadows for a filmic look |
| Sat vs Sat | compresses or expands saturation | tame neon highlights |
| Sat vs Lum | luma by saturation | darken the most saturated areas |

## Procedure

1. Serial node after primaries.
2. In Hue vs X, click the colour in the viewer with the curve open: Resolve adds three points
   around that hue.
3. Drag the middle point; adjust outer points to narrow the affected range.
4. Watch the vectorscope to see the hue
   family move.

## Animation-specific notes

- Palettes are precise, so hue-vs curves act like precise palette edits: fix a sequence where a
  colour drifted in the paint/texture stage without re-rendering.
- Lum vs Sat (pull saturation from shadows) keeps cel shadows from turning muddy-saturated.
- Hue vs Lum is the riskiest: in 8-bit or compressed sources it breaks gradients; prefer it on
  float/EXR renders.

## Gotchas

- Narrow, steep curves produce visible banding or edge artefacts on antialiased lines; keep
  points spread.
- A hue curve affects every object of that hue, including ones you did not look at; scrub the whole
  shot and sequence.
- Skin and character colour in a series must stay on-model; check against the character colour
  bible after curve moves.

## Verify

Bypass/enable the node over several shots of the sequence; only the intended colour family moves,
gradients stay smooth, line art shows no new fringes.
