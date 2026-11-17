---
id: computing-software.computer-graphics-engineering.rendering-techniques.hatching-and-stroke-based-rendering
name: hatching-and-stroke-based-rendering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, hatching, tonal-art-maps, cross-hatching, stroke-based-rendering, stylised-rendering]
level: sme
status: docs-checked
description: "Render pen-and-ink hatching in real time with Praun et al. tonal art maps: nested strokes, 6-way tone blending, lapped textures, object-space coherence."
sources: ["https://hhoppe.com/hatching.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hatching and stroke-based styles

Source: Praun, Hoppe, Webb and Finkelstein, "Real-Time Hatching" (SIGGRAPH 2001). The challenges
it names: limited run-time computation, frame-to-frame coherence among strokes, and control of
stroke size and density under dynamic viewing.

## 1. Tonal art maps (TAMs)
- Strokes are pre-rendered into a sequence of mip-mapped hatch images, one per tone: a tonal art
  map. Unlike conventional texture maps, minification must keep screen-space stroke density
  roughly constant (art maps of Klein et al. define custom mip levels with similar aims), so each
  mip level is constructed deliberately, not by filtering.
- Nesting property: every stroke in a texture image also appears in the same place in all darker
  tones, and every stroke at a coarser mip level appears in the finer levels. Blending
  neighbouring images in the grid then changes only a few pixels, which avoids "swimming
  strokes" and pops.
- The paper defines 6 tone levels so the images can be packed in two textures used on all
  triangles (the paper notes Hertzmann and Zorin target 4 levels).

## 2. Rendering with TAMs
Selecting one tone per face pops and has discontinuities across edges; interpolating two tones
per face looks faceted; one tone per vertex is smooth in space but pops in time due to rounding.
The paper's scheme brackets the continuous tone at each vertex (blending the two consecutive tone
images), then combines the three vertices barycentrically across the face. Both blends are
linear, so this is a linear blend of 6 images per face (12 with mip-mapping); the hardware
mip-mapping blends resolution levels.
- Single-pass version: the grayscale TAM images are packed, 6 consecutive tones in the R, G, B
  channels of two textures. Blend ratios are encoded in vertex diffuse and specular colours and
  interpolated; the result is two dot products added together.
- For ink-like strokes the authors tried thresholding the tone, using clamp(8t - 3.5), a close
  step function: new strokes then appear as gradually lengthening black strokes rather than
  darkening gray ones, at the cost of jaggies on the antialiased stroke edges (supersampling
  might help).

## 3. Stroke placement
- The paper chooses object-space coherence over image-space coherence, which is easier to keep
  consistent but harder to align strokes with surface features. Strokes can be aligned with
  semantic features or curvature (Hertzmann and Zorin).
- Parametrised surfaces use TAMs directly (a toroidal tiling in the paper's sphere and cylinder
  examples). Surfaces without a good global parametrisation use lapped textures: overlapping
  patches that are topological discs, with irregular boundaries and small alpha ramps that
  feather them; hatch images suit this because they lack low-frequency components that would
  reveal patch boundaries.

## Gotchas
- Without nested strokes, tones pop when lighting changes.
- Default filtered mipmaps do not preserve stroke density; author custom mips.

## Verify
- [ ] A rotating light sweeps through all tones without popping; zooming keeps stroke density roughly constant on screen.

## Checked

Method: docs-checked 2026-11-09 against the Real-Time Hatching PDF (abstract, introduction, TAM construction and sections 5 and 6 read; the stroke generation section 4 was not read in detail). Dropped the invented GLSL weighting shader, the "shower door" screen-space remarks, silhouette and crease additions, and the shadow-softening advice.
