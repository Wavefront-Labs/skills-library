---
id: computing-software.computer-graphics-engineering.rendering-techniques.alpha-to-coverage-and-hashed-alpha
name: alpha-to-coverage-and-hashed-alpha
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, transparency, alpha-to-coverage, hashed-alpha, alpha-testing, msaa, stochastic-transparency]
level: advanced
status: gated
description: "Render foliage and fences without sorting: alpha-to-coverage with MSAA, sharpened alpha, hashed alpha testing with TAA, and mip coverage preservation."
sources: ["https://github.com/KhronosGroup/Vulkan-Docs/blob/main/chapters/fragops.adoc", "https://github.com/KhronosGroup/OpenGL-Refpages/blob/main/gl4/html/glEnable.xhtml", "https://casual-effects.com/research/Wyman2017Hashed/index.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Alpha to coverage and hashed alpha

## 1. Alpha to coverage (needs MSAA)
The fragment's alpha is converted into a coverage mask (higher alpha covers more samples; the pattern is implementation specific). Enable:
GL `glEnable(GL_SAMPLE_ALPHA_TO_COVERAGE)`, Vulkan `alphaToCoverageEnable` in
`VkPipelineMultisampleStateCreateInfo`, D3D12 `BlendState.AlphaToCoverageEnable`.
Sharpen alpha so edges stay crisp but anti-aliased:
```glsl
float a = texture(albedo, uv).a;
a = (a - cutoff) / max(fwidth(a), 1e-4) + 0.5;    // ~1 pixel transition
outColor = vec4(col, a);
```
Order independent, depth writes on, no sorting.

## 2. Hashed alpha test (no MSAA, with TAA)
Compare alpha to a stable per-pixel noise threshold instead of a constant:
```glsl
float hashedThreshold(vec3 objPos) {   // Wyman & McGuire: stable under motion via object-space hash (constants (gated: unconfirmed, source is paywalled or blocked))
  float maxDeriv = max(length(dFdx(objPos)), length(dFdy(objPos)));
  float pixScale = 1.0 / (0.1 * maxDeriv);   // scale constant (gated: unconfirmed, source is paywalled or blocked)
  vec2 s = vec2(exp2(floor(log2(pixScale))), exp2(ceil(log2(pixScale))));
  float a0 = hash3D(floor(s.x * objPos)), a1 = hash3D(floor(s.y * objPos));
  float f = fract(log2(pixScale));
  return clamp(mix(a0, a1, f), 1e-6, 1.0);
}
if (alpha < hashedThreshold(vObjPos)) discard;
```
TAA averages the noise into smooth partial coverage; distant foliage keeps density (claim from the paper, (gated: unconfirmed, source is paywalled or blocked)).

## 3. Mip coverage
Alpha tested textures thin out in lower mips. Rescale alpha per mip so the fraction above cutoff
matches mip 0 (coverage-preserving mip generation).

## Gotchas
- Hashed alpha without TAA looks noisy; with TAA it can shimmer if motion vectors are wrong.
- Shaders that discard or write coverage can disable early depth tests on some hardware; consider a depth prepass.

## Verify
- [ ] Distant trees keep their density; edges anti-aliased; no sorting artefacts.

## Checked

2026-10-26: OpenGL-Refpages glEnable (GL_SAMPLE_ALPHA_TO_COVERAGE exists), Vulkan-Docs fragops.adoc (alphaToCoverageEnable and alphaToOneEnable are members of VkPipelineMultisampleStateCreateInfo and modify the fragment alpha and coverage mask) and the Microsoft sdk-api D3D12_BLEND_DESC page (AlphaToCoverageEnable), read 2026-10-26. The Wyman and McGuire hashed alpha paper page is a script-rendered page that could not be read, so the hash scale constant and the TAA behaviour are marked gated. Removed the exact half-coverage statement and the non-MSAA no-op claim, which the Vulkan text does not state.

Method: documentation only; no commands were run.
