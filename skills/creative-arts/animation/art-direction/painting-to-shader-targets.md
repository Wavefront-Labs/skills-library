---
id: creative-arts.animation.art-direction.painting-to-shader-targets
name: painting-to-shader-targets
category: creative-arts
field: animation
product: art-direction
tags: [art-direction, look-development, shader-style-target, lookdev, npr]
level: advanced
status: draft
description: "Translate a painted key into measurable shader and lighting targets: sample values, edge widths and colour shifts from the painting, then build and compare renders to it."
sources:
  - https://www.gdcvault.com/play/1022031/GuiltyGearXrd-s-Art-Style-The
  - https://books.google.com/books?vid=ISBN9780740797712
  - https://www.khanacademy.org/computing/pixar
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Translating paintings into shader targets

Goal: lookdev hits the painting because the painting has been turned into numbers.

## 1. Analyse the painting
For each material in the key, sample and record:
- Lit colour, shadow colour, and the hue shift between them (shadows cooler? more saturated?).
- Terminator width (hard cel edge vs soft band) and where it sits on the form.
- Highlight shape, size and colour; whether it is coloured by the light or white.
- Rim/backlight presence and width; reflected light colour in shadows.
- Texture visible in lit vs shadow areas (painters often drop texture in shadow).
- Outline weight and where lines disappear.

## 2. Map each observation to a control
| Painting feature | Shader / lighting control |
|---|---|
| Shadow colour shift | toon ramp colour or shadow tint, not a darker light |
| Terminator width | ramp interpolation width / smoothstep range |
| Shadow placement cheats | edited normals, shadow-offset maps per vertex |
| Highlight shapes | stylised specular with thresholds or texture-based highlights |
| Rim | fresnel term with width and colour |
| Lost texture in shadow | blend texture strength by light factor |

## 3. Compare
- Render the same shot the key was painted over, with the same camera.
- Put render and painting side by side and as 50% overlay; compare sampled colours numerically.
- Iterate on one variable at a time; note which differences are acceptable.

## Verify
- [ ] Sampled colour/edge table for each material.
- [ ] Each feature mapped to a shader or lighting control.
- [ ] Side-by-side comparison approved by the art director.

Related: `creative-arts.animation.art-direction.npr-look-targets`,
`creative-arts.animation.art-direction.rendering-style-definition`,
`creative-arts.animation.color.look-development-for-color-pipelines`.
