---
id: creative-arts.graphic-design.adobe-photoshop.blur-gallery-and-lens-blur
name: blur-gallery-and-lens-blur
category: creative-arts
field: graphic-design
product: adobe-photoshop
tags: [graphic-design, adobe-photoshop, photoshop, smart-filters, blur-gallery, lens-blur, field-blur, tilt-shift, depth-of-field]
level: practitioner
status: draft
description: "Simulate camera blur with Blur Gallery (field, iris, tilt-shift, path, spin) and Lens Blur with depth maps, bokeh and noise matching."
sources:
  - https://helpx.adobe.com/photoshop/using/blur-gallery.html
  - https://helpx.adobe.com/photoshop/using/lens-blur.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Blur Gallery and Lens Blur

**Goal:** believable optical blur (shallow depth of field, motion, miniature effect) rather than flat Gaussian blur.

## Blur Gallery (Filter > Blur Gallery)
- **Field Blur**: pins with different blur amounts - gradient defocus across the frame.
- **Iris Blur**: elliptical sharp zone with feather handles - portrait/product focus.
- **Tilt-Shift**: sharp band with blurred top/bottom - miniature look, also cast-shadow falloff.
- **Path Blur / Spin Blur**: motion along a drawn path, rotating wheels.
- Effects tab: **Light Bokeh** brightens highlights into bokeh; Noise tab adds grain back so
  blurred areas match unblurred grain.
- Run on a smart object for re-editability; save the mask to channels for reuse.

## Lens Blur (Filter > Blur > Lens Blur)
- Uses a depth map: Focus Distance and a source (layer transparency, mask or a depth channel).
- Build a depth map: alpha channel with black = near (sharp), white = far, gradient between.
  Click the image to set the focal point.
- Iris shape/blade curvature/rotation set bokeh shape; Specular Highlights brightness/threshold
  make bright points bloom like real lenses.
- Current versions offer AI depth estimation automatically for photos.

## Gotchas
- Blurring a cut-out on its own layer bleeds transparency at edges; blur the background plate
  with the subject filled out (Content-Aware Fill) first, then composite the sharp subject above.
- Blur removes grain; always add noise back.

## Verify
- [ ] Focus falloff is gradual and consistent with depth.
- [ ] Blurred areas carry the same grain as sharp areas.
