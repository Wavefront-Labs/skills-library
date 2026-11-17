---
id: creative-arts.animation.vector-graphics.svg-pipeline-for-motion-graphics
name: svg-pipeline-for-motion-graphics
category: creative-arts
field: animation
product: vector-graphics
tags: [vector, vector-graphics, svg, motion-graphics, gsap, web-animation, css-animation, stroke-dasharray, path-morphing, logo-animation, reduced-motion]
level: practitioner
status: docs-checked
description: "Structure SVG for runtime animation on the web: stable ids and groups, stroke draw-on with getTotalLength, path morphing point counts, and prefers-reduced-motion."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/SVGGeometryElement/getTotalLength
  - https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/stroke-dashoffset
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
  - https://gsap.com/docs/v3/Plugins/MorphSVGPlugin/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SVG pipeline for motion graphics

For animation where the SVG stays SVG in the delivery medium (animated logo, self-drawing icon, kinetic type on a page). For a rendered video file use the compositing path instead.

## 1. Structure the SVG first

A raw export from a design tool is rarely ready for runtime animation.
- Give every element you will target a stable `id` (`logo-mark`, `underline`); auto-generated ids change on re-export.
- Group deliberately: put what animates together in one `<g>` so one transform moves all its children.
- Keep a separate `<g>` with its own `transform` around anything animated independently, which gives it its own pivot without touching path data.
- Convert text to paths only if you must morph or stroke-draw it; live `<text>` stays selectable and re-themeable.

## 2. Stroke draw-on

Animate `stroke-dashoffset` from the path length to 0 with `stroke-dasharray` set to that length. Get the length with `getTotalLength()`, which returns "a float indicating the total length of the path in user units" and takes no parameters; do not guess it. `stroke-dashoffset` is an animatable presentation attribute (default 0) and has a CSS property counterpart that takes priority when both are set.

## 3. Path morphing

Plain interpolation between paths needs compatible point structure, so check point counts before assuming a morph will look right. GSAP's MorphSVGPlugin can morph path data even if the number and type of points do not match; it adds anchor points behind the scenes. Check the vendor's pricing page for the plugin's licence terms.

## 4. Accessibility

Respect `prefers-reduced-motion`: `reduce` means the user asked to remove, reduce or replace motion. Remove large-scale movement such as scaling, panning and parallax first, replace it with gentler alternatives such as opacity fades where feedback still matters, and keep essential motion minimal. Test by enabling the setting on your device.

## Verify

- [ ] Independently animated elements have stable ids and their own transform group.
- [ ] Stroke-draw effects use the path's real `getTotalLength()` value.
- [ ] Any morph pair has verified point structure or uses a library that normalises it.
- [ ] A `prefers-reduced-motion: reduce` rule removes or replaces large motion.

## Checked

2026-11-01. Confirmed against MDN (getTotalLength, stroke-dashoffset, prefers-reduced-motion) and the GSAP MorphSVGPlugin page (sources above). Removed as not confirmed: claims that the GSAP plugins are paid or commercial, GPU acceleration and layout cost of transforms versus geometry attributes, SMIL browser support, Lottie and Bodymovin guidance, filter cost, viewBox scaling advice and library selection opinions.
Method: documentation only; no commands were run.
