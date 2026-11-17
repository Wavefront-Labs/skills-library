---
id: computing-software.computer-graphics-engineering.rendering-techniques.kuwahara-and-painterly-filters
name: kuwahara-and-painterly-filters
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, kuwahara, anisotropic-kuwahara, painterly-rendering, post-processing, structure-tensor]
level: sme
status: draft
description: "Build painterly post-processing: Kuwahara, generalized and anisotropic Kuwahara via the structure tensor, with performance and parameter guidance."
sources: ["https://www.kyprianidis.com/p/pg2009/", "https://www.kyprianidis.com/p/npar2011/", "https://www.realtimerendering.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Painterly and Kuwahara filters

## 1. Basic Kuwahara
Split the (2r+1)^2 window into 4 overlapping quadrants, compute each one's mean and variance, output the mean
of the lowest-variance quadrant. Edges survive because a quadrant straddling an edge has high variance.
Artefact: blocky, square brush marks.

## 2. Generalized Kuwahara (Papari)
8 sectors on a disc with smooth Gaussian-weighted sector kernels; weight each sector mean by
`1 / (1 + stddev^q)` (q around 8) instead of hard minimum selection. Removes blockiness and flicker.

## 3. Anisotropic Kuwahara (Kyprianidis)
1. Structure tensor from Sobel gradients `(gx*gx, gy*gy, gx*gy)`, Gaussian-blurred (sigma ~2).
2. Per pixel eigen-decomposition: orientation `phi` and anisotropy `A = (l1-l2)/(l1+l2)`.
3. Stretch the disc into an ellipse along the edge: axes scaled by `alpha/(alpha+A)` and `(alpha+A)/alpha`,
   alpha = 1.
4. Generalized sector weighting inside the ellipse.
Brush strokes then follow image features.

## Performance
- r=6 anisotropic at 1080p costs several ms; run at half resolution and upsample with a joint bilateral, or
  use the polynomial sector weights (Kyprianidis 2011) that avoid a kernel texture.
- Compute shader with shared-memory tiles for the window reads.

## Paint look extras
- Canvas texture multiply, mild colour quantisation, edge darkening via difference of Gaussians.
- Apply after tone mapping (works on display values), before UI and film grain.

## Gotchas
- Flicker on noisy input: run after TAA and smooth the structure tensor.
- Large radii smear faces; mask characters by stencil or depth.

## Verify
- [ ] Edges stay crisp, flat regions become stroke-like, no square blocks, stable under slow camera motion.
