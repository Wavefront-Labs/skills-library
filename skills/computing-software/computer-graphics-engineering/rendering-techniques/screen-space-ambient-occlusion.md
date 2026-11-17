---
id: computing-software.computer-graphics-engineering.rendering-techniques.screen-space-ambient-occlusion
name: screen-space-ambient-occlusion
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, ssao, ambient-occlusion, gtao, hbao, depth-buffer, bilateral-blur, xe-gtao]
level: advanced
status: docs-checked
description: "Screen-space ambient occlusion: normal-oriented hemisphere SSAO with noise rotation and blur, versus horizon-based GTAO (XeGTAO) with near-field radius and denoise."
sources:
  - https://learnopengl.com/Advanced-Lighting/SSAO
  - https://github.com/GameTechDev/XeGTAO
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Screen-space ambient occlusion

**Goal:** darken creases and contact areas from depth (and normals), then apply the result to ambient light only.

## 1. Hemisphere SSAO (LearnOpenGL)
Crytek's sphere kernel made flat walls look gray because about half the samples land in the surface behind the pixel. Use a hemisphere kernel oriented along the surface normal instead.
- Kernel: generated in tangent space with the normal along +z; x and y vary in [-1, 1], z in [0, 1]. The page uses 64 samples, scaled with an accelerating interpolation so most samples sit near the origin.
- Noise: a 4x4 tile of random rotation vectors (z = 0, rotating about the normal), `GL_REPEAT`, tiled over the screen by `texCoords * (screenSize / 4)`. This cuts the samples needed.
- Inputs: G-buffer view-space position (floating point, clamp-to-edge) and normal.
```glsl
vec3 randomVec = texture(texNoise, TexCoords * noiseScale).xyz;
// TBN from fragPos normal and randomVec (Gram-Schmidt), then per sample:
samplePos = fragPos + TBN * samples[i] * radius;      // radius 0.5, kernelSize 64 in the page
// project samplePos, read sampleDepth from the position buffer at that xy
float rangeCheck = smoothstep(0.0, 1.0, radius / abs(fragPos.z - sampleDepth));
occlusion += (sampleDepth >= samplePos.z + bias ? 1.0 : 0.0) * rangeCheck;   // bias 0.025
occlusion = 1.0 - (occlusion / kernelSize);
```
- Bias helps tune the look and avoids acne. The range check keeps far-away depth from occluding; a hard cut-off would leave visible borders, hence `smoothstep`.
- Blur: the repeating noise pattern is visible, so blur the AO texture. The page averages texels in a -2..2 window, matching the 4x4 noise size.
- Apply: the output is used to scale the ambient lighting component.

## 2. GTAO (XeGTAO)
XeGTAO (MIT, DirectX/HLSL; Intel archived and stopped maintaining it in April 2024) implements Jimenez et al. 2016 Ground Truth Ambient Occlusion, which uses a radiometrically-correct AO equation.
- Three compute passes: PrefilterDepths (view-space depth MIP chain), MainPass (core GTAO, unfiltered AO plus edge info), Denoise (spatial filter). Inputs are the depth buffer and optional screen-space normals; the output is a single-channel AO buffer.
- Defaults: full resolution, 3 slices per pixel, 6 samples per slice (18 spp); a lower preset uses 2 slices of 4 samples (8 spp).
- Samples along a slice use `x = pow(x, 2)` to catch thin crevices; x is the normalized distance to the maximum 'Effect radius' (world space).
- Near-field bounding: distant samples are attenuated over a 'Falloff range' beyond the effect radius, which gives stable, predictable results.
- Denoise: 5x5 depth-aware spatial filter, with TAA used for the temporal part when available.
- Optional bent normals add roughly 25% to the cost.

## Limits and gotchas
- The depth buffer is a view-space heightfield, so thin features at depth discontinuities cast too much occlusion and haloing appears; the larger the radius, the worse the mismatch. Keep the radius small relative to scene features. XeGTAO exposes a 'Thin occluder compensation' setting (default 0).
- Sampling far from the pixel is memory-bandwidth bound; XeGTAO samples a depth MIP chain for distant samples.
- Generic SSAO samples are unphysical compared with GTAO; expect to tune radius and bias per scene.

## Verify
- [ ] Flat walls are not gray (hemisphere, not sphere, kernel).
- [ ] No visible noise tile after blur or denoise.
- [ ] No halo around foreground objects at your chosen radius.
- [ ] AO multiplies ambient light only.

## Checked
2026-11-08. Confirmed against the LearnOpenGL SSAO chapter (hemisphere rationale, 64-sample kernel, 4x4 noise, bias 0.025, radius 0.5, range check, blur window, ambient scaling) and the XeGTAO README (passes, defaults, sample distribution, falloff, denoise, bent normals cost, thin occluder discussion, MIP bandwidth, archived status). Removed: the Activision paper source (unreadable), the Real-Time Rendering book source and its timing figure, the 0.3-1.5 m radius range, the Lagarde specular occlusion claim, and the half-resolution and linear-depth advice (not on pages read).
Method: documentation only; no commands were run.
