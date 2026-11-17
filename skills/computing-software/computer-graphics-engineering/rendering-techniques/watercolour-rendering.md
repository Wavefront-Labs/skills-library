---
id: computing-software.computer-graphics-engineering.rendering-techniques.watercolour-rendering
name: watercolour-rendering
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, watercolor, watercolour-rendering, painterly-rendering, edge-darkening, paper-texture, stylised-rendering]
level: advanced
status: draft
description: "Approximate watercolour in real time: paper texture modulation, edge darkening, pigment granulation, colour bleeding via blurred offsets, and wobble with noise-based distortion."
sources: ["https://grail.cs.washington.edu/projects/watercolor/paper_small.pdf", "https://artineering.io/publications/Art-directed-watercolor-stylization", "https://dl.acm.org/doi/10.1145/2643188.2643191"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Watercolour rendering

Curtis et al. 1997 simulated pigment and water physically (offline). Real-time systems (Bousseau
et al. 2006, Montesdeoca et al. MNPR) approximate the visual signatures with image-space passes.

## 1. Visual signatures
| Effect | Real-time approximation |
|---|---|
| Paper texture | modulate colour by a paper height/normal map: `col = mix(col, col * paper, k)` |
| Pigment turbulence (uneven density) | low-frequency noise darkening `col = col^(1 + noise * k)` |
| Granulation | high-frequency paper grain in darker areas |
| Edge darkening (pigment pooling at wet edges) | darken where colour gradient or object edge detected |
| Wobbling / hand tremor | distort UVs by noise before sampling the shaded image |
| Colour bleeding | blur colours across edges selectively (control mask) |
| Gaps and overlaps | offset edges in/out by noise |

## 2. Pipeline sketch
1. Render shaded colour (soft, low-contrast diffuse; avoid sharp specular).
2. **Abstraction**: smooth colour (Kuwahara or bilateral) to remove detail.
3. **Wobble**: `uv += (noise(uv * f) - 0.5) * amp` (paper-anchored noise).
4. **Edge darkening**: `edge = length(gradient(colour))` or depth/normal edges blurred; then
   `col = pow(col, 1 + edge * strength)` (darkening via density).
5. **Pigment density** from turbulence noise and paper: apply density model
   `C' = C - (C - C^2) * (d - 1)` (Bousseau density remapping).
6. Composite on paper colour.

## 3. Art direction
MNPR (Maya/Autodesk) uses painted control maps per effect so artists can place bleeding and edge
darkening where wanted; procedural-only results look uniform.

## Gotchas
- Temporal coherence: screen-space noise swims; anchor noise to object or paper space and accept
  some shower-door look, or use temporally coherent noise.
- Dark, saturated scenes don't read as watercolour; keep palettes light.

## Verify
- [ ] Still frames read as watercolour (edges pooled, paper visible).
- [ ] Animated camera shows acceptable coherence (no crawling noise).
