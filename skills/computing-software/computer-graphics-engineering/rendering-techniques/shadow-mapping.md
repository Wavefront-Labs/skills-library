---
id: computing-software.computer-graphics-engineering.rendering-techniques.shadow-mapping
name: shadow-mapping
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [rendering-techniques, shadow-mapping, shadows, cascaded-shadow-maps, csm, pcf, percentage-closer-filtering, shadow-acne, peter-panning, depth-bias, slope-scaled-bias, texel-snapping, shimmering, vsm, cascade-splits, shadow-stabilization]
level: advanced
status: docs-checked
description: "Real-time shadow maps per the DirectX SDK articles: two-pass algorithm, acne vs Peter Panning, tight frusta, texel snapping, cascades, PCF and variance shadow maps."
sources: ["https://learn.microsoft.com/en-us/windows/win32/dxtecharts/common-techniques-to-improve-shadow-depth-maps", "https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Shadow mapping

**Goal:** shadows that are stable when the camera moves, free of acne and light leaks, and soft
enough to look natural. The claims below follow the two Microsoft DirectX technical articles
cited in `sources`; other engines' parameter values are not given here.

## 1. The algorithm
Shadow depth maps are a two-pass algorithm.
1. **Pass 1:** render the geometry into a depth buffer from the light's point of view.
2. **Pass 2:** transform each vertex by the camera and by the light's view-projection-texture
   matrix (the pass 1 matrix plus a scale and translate from -1..1 clip space to 0..1 texture
   space, with Y flipped). In the pixel shader, index the pass 1 depth with the X and Y texture
   coordinate and compare it against the Z texture coordinate.

## 2. Artifacts and what causes them
- **Perspective aliasing:** pixels in view space do not map one-to-one to shadow texels;
  pixels near the near plane are closer together and need more shadow resolution. Cascaded
  shadow maps (CSMs) are the most popular fix. PSMs and LSPSMs skew the light projection but
  do not solve it; a logarithmic parameterisation would be needed.
- **Projective aliasing:** occurs as the tangent plane of the geometry becomes parallel to the
  light rays. Techniques that help perspective aliasing also help this.
- **Shadow acne:** erroneous self-shadowing, caused by depth quantised over a whole texel and by
  precision differences between the fixed-function depth write and the shader-computed depth.
  Mitigate with tight light-frustum near and far planes, slope-scaled depth bias and other bias.
- **Peter Panning:** objects look detached and floating because the depth offset is too large and
  the depth test wrongly passes. Aggravated by poor depth precision; tight near and far planes
  help.

## 3. Techniques that improve basic shadow maps
- **Slope-scaled depth bias:** steep polygons (relative to the light) suffer more projective
  aliasing, so each depth value may need a different offset. Direct3D 10 hardware can bias a
  polygon by its slope: a large bias for polygons seen edge-on to the light and none for
  polygons facing it.
- **Tight projection:** transform the eight view-frustum corners into light space, take the
  min and max X and Y as the orthographic bounds. Clipping to the scene AABB is tighter but can
  change the projection size frame to frame, which breaks texel snapping.
- **Near and far planes:** the closer together, the more precise the depth buffer. The article's
  preferred method intersects the scene bounds with the four known light-frustum planes and
  takes the min and max Z of the clipped result (`ComputeNearAndFar` in the CascadedShadowMaps11
  sample). Using the whole-scene AABB can waste precision; using only the view frustum can crop
  casters.
- **Texel-sized light movement (fixes shimmering edges):** shimmering comes from the light
  projection being recalculated as the camera moves. For directional lights, divide the
  orthographic min and max X and Y by world units per texel, floor, and multiply back. World
  units per texel is the view-frustum bound divided by the buffer size. The texture must be one
  pixel larger in width and height so coordinates do not index outside it.
- **Back or front face culling in the shadow pass:** standard back-face culling is the default.
  Front-face culling is a common option but needs correct front and back geometry (impractical
  for sprite-based foliage) and makes Peter Panning and gaps at the base of walls more likely.
- **Shadow-friendly geometry:** hard edges have tiny depth disparity so a small offset removes
  their shadow; thin objects such as walls should have backs; outside faces should be back-facing.

## 4. Cascaded shadow maps
Partition the camera frustum into sub-frusta, compute an orthographic projection for each,
render a shadow map for each, then in the pixel shader pick the right map and sample it.
- **Splits:** recalculating splits every frame makes edges shimmer, so use a static set of
  cascade intervals per scenario. More splits are needed when the scene's Z range is large (for
  example a camera near the ground with distant objects visible); fewer for overhead views.
  More splits near the eye are valuable.
- **Fit to scene vs fit to cascade:** fit to scene gives all frusta the same near plane (cascades
  overlap and the projection is padded to the maximum frustum size, which avoids artifacts when
  the camera moves). Fit to cascade uses each interval's own near and far planes, wastes less
  resolution, but the projection grows and shrinks with view orientation.
- **Cascade selection:** interval-based (compare view depth against the partition depths) is
  slightly faster; map-based (test the texture coordinate against each cascade's bounds) uses the
  cascades more efficiently when maps do not align.
- **Blend band:** with filtering, a visible seam appears where cascades meet. Test both cascades
  in a band between them and linearly interpolate; use a dynamic branch so most pixels read one.
- **Dueling frusta:** light and camera facing each other is a hard case for most algorithms;
  CSMs cope better than most, and it is common to constrain light and camera to avoid it.

## 5. Filtering
- **PCF:** blurring depth values and then comparing does not soften shadows; it only moves the
  hard edge. PCF returns the fraction of subsamples that pass the depth test (a four-tap filter
  with 1 of 4 passing is 25 percent shadowed; with linear interpolation of subtexel coordinates
  the result is smooth rather than 5 discrete values). Larger kernels can use a weighted
  (for example Gaussian) N by N grid whose weights sum to 1.
- **PCF and depth bias:** large kernels compare against neighbouring texels that refer to other
  positions, so more bias is needed, which risks Peter Panning. A per-texel bias from `ddx` and
  `ddy` of the light-view-space position fits the depth to a plane for the neighbouring texels;
  it is computationally heavy, so use it when GPU time is spare. Compute the derivatives on
  light-view-space coordinates, not the cascade-specific ones, or divergent cascade choice in a
  2 by 2 pixel quad produces seams.
- **PCF with CSMs:** PCF on texture arrays is a Direct3D 10.1 feature, so the sample puts the
  cascades in one large buffer. Pad each cascade's rim by half the PCF kernel size.
- **VSMs:** store depth and depth squared in a two-channel map that can be blurred, mipmapped and
  anisotropically filtered; Chebyshev's inequality estimates the lit fraction. Main drawback is
  light bleeding where shadows overlap. Raising the result to a power damps it; layered VSMs
  fix it at the cost of many maps. VSMs trade texture bandwidth (PCF) for maths, and look good at
  low resolution.

## Gotchas
- Fit the frusta and near/far planes tightly before reaching for fancier algorithms.
- Keep the light projection size constant per frame if you snap to texels.
- Very high shadow resolution can lose small objects such as telephone wires and hurt texture
  access performance.

## Verify
- [ ] No acne on lit surfaces and contact shadows stay attached (adjust bias, not just add more).
- [ ] Rotating and strafing the camera: no shimmering edges.
- [ ] Cascade seams invisible with blending on.
- [ ] Shadow pass cost measured in a GPU profiler.

## Checked
Checked 2026-11-08 against both cited Microsoft Learn DirectX articles (Common Techniques to
Improve Shadow Depth Maps; Cascaded Shadow Maps). Removed because the pages do not state them:
GL, D3D and Vulkan bias parameter values, normal-offset ranges, PCSS cost, split formula and
lambda, shadow distance caps, texture budgets, point and spot light recipes, and the Real-Time
Rendering book source. The article's view that front-face culling is risky replaced the earlier
advice to cull front faces.
Method: docs-only read of cited pages, 2026-11-08
