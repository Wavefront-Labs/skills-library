---
id: computing-software.computer-graphics-engineering.rendering-techniques.halftone-and-screen-tone-shading
name: halftone-and-screen-tone-shading
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, halftone, screen-tone, manga-shading, comic-shading, dot-pattern, non-photorealistic-rendering]
level: practitioner
status: draft
description: "Render halftone and manga screen-tone shading: rotated dot grids driven by light intensity, CMYK-style angles, screen vs object-space anchoring and antialiasing dots."
sources: ["https://en.wikipedia.org/wiki/Halftone", "https://weber.itn.liu.se/~stegu/webglshadertutorial/shadertutorial.html", "https://www.cyanilux.com/tutorials/halftone-shader-breakdown/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Halftone and screen tones

## 1. Dot halftone
Tone is represented by dot size on a regular rotated grid: dark = big dots.
```glsl
float halftone(vec2 fragPx, float tone, float cellPx, float angle) {   // tone 0 = white, 1 = black
    mat2 R = mat2(cos(angle), -sin(angle), sin(angle), cos(angle));
    vec2 p = R * fragPx / cellPx;
    vec2 cell = fract(p) - 0.5;
    float radius = sqrt(tone) * 0.7071;                 // area-proportional radius; 0.707 covers cell
    float d = length(cell) - radius;
    float aa = fwidth(d);
    return 1.0 - smoothstep(-aa, aa, d);                 // 1 = ink
}
```
Tone comes from lighting (`1 - NdotL` or luminance after shading). `sqrt(tone)` keeps ink area
proportional to tone.

## 2. CMYK look
Run halftone per channel with classic screen angles (C 15, M 75, Y 0, K 45 degrees), subtract inks
from white paper: `col = vec3(1) - c*cyanInk - m*magentaInk - ...` (or multiply). Stefan Gustavson's
WebGL tutorial implements antialiased CMYK halftoning.

## 3. Manga screen tones
- Fixed-size dots, lines or cross-hatching patterns at 2-3 tone levels selected by thresholds on
  lighting (cel bands), rather than continuous dot size.
- Pattern texture (tileable) chosen per band; blend with hard step.

## 4. Anchoring
- **Screen space** (gl_FragCoord): authentic print look, but the pattern "shower-doors" (stays fixed
  while objects move).
- **Object/UV space**: sticks to objects, but dots scale with distance; compensate by choosing cell
  size from screen-space derivatives and blending between two octaves (like art-maps for hatching).

## Gotchas
- Without fwidth antialiasing, dots alias and moire in motion.
- Very small cells on high-DPI screens become grey mush; expose cell size in physical pixels.

## Verify
- [ ] Gradients render as smoothly varying dot sizes without moire.
- [ ] Pattern behaviour under camera motion matches the art direction (screen vs object anchored).
