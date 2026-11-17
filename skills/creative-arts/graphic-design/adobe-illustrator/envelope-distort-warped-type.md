---
id: creative-arts.graphic-design.adobe-illustrator.envelope-distort-warped-type
name: envelope-distort-warped-type
category: creative-arts
field: graphic-design
product: adobe-illustrator
tags: [graphic-design, adobe-illustrator, illustrator, illustrator-type, envelope-distort, make-with-warp, make-with-mesh, make-with-top-object, warp-effect, arched-text, vintage-lettering]
level: practitioner
status: draft
description: "Warp type and art into shapes with Illustrator Envelope Distort (warp, mesh, top object) or the Warp effect, keep text editable, control fidelity and expand for output."
sources:
  - https://helpx.adobe.com/illustrator/using/reshape-using-envelopes.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Envelope distort and warped type

**Goal:** arched, bulging or shape-fitted lettering (vintage badges, packaging labels) that remains editable.

## Three ways to make an envelope (Object > Envelope Distort)
1. **Make with Warp** (Alt+Shift+Ctrl+W / Opt+Shift+Cmd+W): presets Arc, Arc Lower/Upper, Arch, Bulge,
   Shell, Flag, Wave, Fish, Rise, Fisheye, Inflate, Squeeze, Twist; Bend %, horizontal/vertical distortion.
2. **Make with Mesh** (Alt+Ctrl+M / Opt+Cmd+M): rows x columns grid; drag mesh points with Direct Selection
   for custom distortions.
3. **Make with Top Object** (Alt+Ctrl+C / Opt+Cmd+C): draw the target shape (e.g. a banner shape) on
   top of the text, select both - text fills the shape.

## Edit
- **Edit Contents** (Object > Envelope Distort > Edit Contents, or the Control bar toggle): change the
  text itself; the envelope reapplies.
- **Edit Envelope:** adjust the warp or mesh points.
- Reset with Warp / Reset with Mesh to switch type.
- **Envelope Options:** Fidelity (higher = closer fit, more points), Anti-alias for rasters, Distort
  Appearance / Linear Gradients / Pattern Fills (include them in the distortion).

## Effect > Warp vs Envelope
Effect > Warp applies the same presets as a **live effect** in the Appearance panel - fully editable
text, easy to toggle, can be part of a graphic style. Fewer controls than mesh envelopes. Prefer it for simple arcs.

## Quality tips
- Distortions thin or thicken strokes unevenly; choose robust, even-weight typefaces (slab, bold sans).
- Strong warps distort letter proportions noticeably; for logos, consider drawing custom lettering
  or adjusting outlined glyphs by hand after the warp.
- Type on a path (see that skill) gives arcs without distorting letterforms - often better for badges.

## Output
Object > Envelope Distort > **Expand** (or Object > Expand Appearance for the Warp effect) for files going
to other apps, cutters or SVG. Keep the live master.

## Verify
- [ ] Text editable in the master; expanded copy for delivery.
- [ ] Letter weights visually even after distortion at final size.
