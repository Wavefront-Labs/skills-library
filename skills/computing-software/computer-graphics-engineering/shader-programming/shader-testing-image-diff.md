---
id: computing-software.computer-graphics-engineering.shader-programming.shader-testing-image-diff
name: shader-testing-image-diff
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, shader-debugging, shader-testing, image-diff, golden-images, nvidia-flip, swiftshader, lavapipe, ci]
level: advanced
status: docs-checked
description: "Test shaders automatically: golden images with perceptual diffs (FLIP), unit-testing shader functions in compute, CPU emulation and CI on software GPUs."
sources: ["https://github.com/NVlabs/flip", "https://github.com/google/swiftshader", "https://docs.mesa3d.org/drivers/llvmpipe.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing shaders

## 1. Golden-image tests
1. Render a fixed scene (fixed camera, seed, time, resolution) headless.
2. Read back the image; compare with a stored reference.
3. Fail if the error exceeds a threshold; save the diff image as a CI artefact.

Comparison metrics:
- Exact compare fails across GPUs/drivers (rounding, filtering differences).
- Per-pixel max abs error with tolerance and a max count of differing pixels.
- **NVIDIA FLIP** (`pip install flip-evaluator`; `flip -r ref.png -t test.png`) gives a perceptual
  error map and a mean error; choose your own threshold on the mean and on high-error pixels.
- Keep references per backend/vendor if differences are legitimate.

## 2. Unit-test shader functions
Compile the function under test into a compute shader that evaluates it over a grid of inputs and
writes results to a buffer; compare with a CPU reference (numpy) within tolerance. Good for
BRDFs, packing/unpacking (octahedral normals, RGBM), colour transforms, hashing.

## 3. Run shaders on the CPU
- Write shader code in a subset shared between C++ and HLSL/GLSL (glm/HLSL++ types,
  `#define float3 vec3`), and unit-test on the CPU with standard frameworks.
- Software rasterisers for CI without GPUs: **SwiftShader** (CPU implementation of Vulkan) and
  Mesa **llvmpipe** (CPU rasteriser). Results can differ from hardware; use them for regression
  detection, not ground truth.

## 4. What to test
- Each material/feature toggle in isolation on a simple scene (sphere grid, furnace test).
- Edge cases: zero roughness, grazing angles, black/white albedo, NaN inputs.
- Platform matrix in nightly runs on real devices.

## Gotchas
- Nondeterminism from atomics, async compute or TAA history breaks image tests: disable or fix seed
  and frame count.
- Different texture compression encoders produce different images; test with uncompressed assets
  or fixed encoder versions.

## Verify
- [ ] CI produces diff images on failure; references updated only via a reviewed commit.
- [ ] Shader function tests cover packing/encoding functions round-trip.

## Checked
- 2026-10-28. Confirmed in the NVlabs/flip README: `pip install flip-evaluator` and `flip -r referenceImage.png -t testImage.png`. Confirmed SwiftShader is a CPU-based Vulkan implementation and llvmpipe is a Mesa software driver.
- Removed: FLIP threshold example, Slang CPU-target claim, lavapipe and WARP (not on the fetched pages).
Method: documentation only; no commands were run.
