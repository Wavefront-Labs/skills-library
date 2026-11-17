---
id: creative-arts.design-for-form-and-experience.concept-design.lighting-with-hdri-environments
name: lighting-with-hdri-environments
category: creative-arts
field: design-for-form-and-experience
product: concept-design
tags: [hdri-lighting, hdri, image-based-lighting, product-rendering, environment-lighting, render-lighting]
level: practitioner
status: draft
description: "Light product renders with HDRI environments: choose or build a studio HDRI, rotate it for reflections, add area lights, and keep the background separate."
sources:
  - "Koos Eissen and Roselien Steur, Product Design Rendering (BIS Publishers)"
  - "Poly Haven (polyhaven.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# HDRI environment lighting

An HDRI (high dynamic range image) wraps the scene and supplies both light and reflections. On glossy products the HDRI is the reflection, so it must be designed.

## Choose the HDRI
- **Studio HDRIs** (softboxes and strips on a dark or neutral surround) give controlled reflections for hero shots. Free CC0 options exist on Poly Haven.
- **Outdoor HDRIs** suit lifestyle renders but give busy reflections on gloss.
- Resolution: 4K is often enough for lighting; go higher if the HDRI shows in sharp reflections.

## Setup
1. Load the HDRI as the environment and set **brightness** so exposure looks right at normal camera exposure.
2. **Rotate** the environment while watching key surfaces: aim for a long soft highlight along main curves and a dark band that defines edges.
3. **Hide the background from camera** (keep it for reflections) and use a plain or gradient backdrop or a transparent PNG.
4. Add **1-3 area lights** for accents or rim light if the HDRI does not shape the form.
5. Use a **shadow catcher** if compositing.
6. Check **clipping**: no blown highlights on gloss, no crushed blacks on dark parts.

## Custom studio HDRI
Build a simple 3D studio with large soft rectangles and strips as emissive planes, render a spherical panorama saved as .hdr or .exr, and reuse it across products.

## Verify
- [ ] Reflections describe the form rather than show clutter.
- [ ] Rotating the HDRI changes the look in ways you chose.
- [ ] Highlights are not clipped on key surfaces.
