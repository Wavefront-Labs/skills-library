---
id: creative-arts.animation.scripting.ae-linear-ease-mapping
name: ae-linear-ease-mapping
category: creative-arts
field: animation
product: scripting
tags: [linear-mapping, ae-expressions, expressions, after-effects, linear, ease, easein, easeout, remap-values, audio-driven, clamp]
level: practitioner
status: docs-checked
description: "Remap one value range to another with linear(), ease(), easeIn() and easeOut() in After Effects expressions, driven by time or by a property value."
sources:
  - https://raw.githubusercontent.com/docsforadobe/after-effects-expression-reference/master/docs/general/interpolation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# linear() and ease() value mapping

**Goal:** connect an input (time, or a value such as a slider) to an output range with predictable, clamped results.

## Signatures

All take `t` (the interpolation driver), and each has a 5-argument and a 3-argument form. Values may be numbers or arrays.

- `linear(t, tMin, tMax, value1, value2)`: returns value1 when t <= tMin, value2 when t >= tMax, and a linear blend between.
- `linear(t, value1, value2)`: same with t running from 0 to 1.
- `ease(t, tMin, tMax, value1, value2)` and `ease(t, value1, value2)`: like linear but eased so velocity is 0 at both ends (smooth).
- `easeIn(...)`: tangent is 0 only on the tMin (or value1) side, linear on the other.
- `easeOut(...)`: tangent is 0 only on the tMax (or value2) side, linear on the other.

If `t` is `time`, the interpolation happens over a duration. If `t` is `value`, the expression maps one range of values onto another.

## Recipes (from the reference)

```javascript
// Opacity ramps from 20% to 80% over 0 to 6 seconds
linear(time, 0, 6, 20, 80)

// Convert Opacity 0-100% to 20-80%
linear(value, 0, 100, 20, 80)
```

Same pattern for a slider: `linear(effect("Heat")("Slider"), 0, 100, 0, 360)` maps the slider range to a rotation range (arrays work for colours or positions).

## Gotchas

- Results clamp outside tMin..tMax; compute the linear extrapolation yourself if you need it.
- Mixing array lengths in value1 and value2 is a mistake; keep them the same size.

## Verify

Drive the input to its minimum, maximum and beyond both: output equals the end values and never exceeds them.

## Checked

Method: 2026-11-09 read the Interpolation page of the After Effects expression reference. Removed the audio-amplitude, proximity (length/toWorld) and reversed-range claims, and the Adobe language-reference landing source, as not stated on a page read.
