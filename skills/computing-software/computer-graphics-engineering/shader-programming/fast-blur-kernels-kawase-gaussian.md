---
id: computing-software.computer-graphics-engineering.shader-programming.fast-blur-kernels-kawase-gaussian
name: fast-blur-kernels-kawase-gaussian
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, post-processing-shaders, kawase-blur, dual-kawase, separable-gaussian, gaussian-blur, bloom, linear-sampling]
level: practitioner
status: draft
description: "Implement fast GPU blurs: separable Gaussian with linear-sampling weight tricks, dual Kawase downsample/upsample chains, and choosing kernels for bloom, DoF and UI backdrop blur."
sources: ["https://www.rastergrid.com/blog/2010/09/efficient-gaussian-blur-with-linear-sampling/", "https://community.arm.com/cfs-file/__key/communityserver-blogs-components-weblogfiles/00-00-00-20-66/siggraph2015_2D00_mmg_2D00_marius_2D00_slides.pdf", "https://www.iryoku.com/next-generation-post-processing-in-call-of-duty-advanced-warfare/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fast blur kernels

## 1. Separable Gaussian
A 2D Gaussian is the product of two 1D Gaussians: blur horizontally into a temp target, then
vertically. N x N taps become 2N.

**Linear sampling trick**: bilinear filtering fetches two texels in one tap if you sample between
them with the right offset:
```
w_combined = w1 + w2
offset     = (o1 * w1 + o2 * w2) / w_combined
```
A 9-tap kernel needs 5 fetches. Example 9-tap (sigma ~ 2) after combining:
```glsl
const float offs[3] = float[](0.0, 1.3846153846, 3.2307692308);
const float wts[3]  = float[](0.2270270270, 0.3162162162, 0.0702702703);
vec3 c = texture(src, uv).rgb * wts[0];
for (int i = 1; i < 3; i++) {
    c += texture(src, uv + dir * offs[i] * texel).rgb * wts[i];
    c += texture(src, uv - dir * offs[i] * texel).rgb * wts[i];
}
```

## 2. Dual Kawase (Marius Bjorge, ARM, SIGGRAPH 2015)
Downsample chain then upsample chain; each pass is one cheap kernel. Wide blur radius for very few
taps, great on mobile.
```glsl
// downsample (to half res): centre x4 + 4 diagonal corners
vec3 down(vec2 uv, vec2 hp) {      // hp = half texel of source
    vec3 s = texture(src, uv).rgb * 4.0;
    s += texture(src, uv - hp).rgb + texture(src, uv + hp).rgb;
    s += texture(src, uv + vec2(hp.x, -hp.y)).rgb + texture(src, uv - vec2(hp.x, -hp.y)).rgb;
    return s / 8.0;
}
// upsample (to double res): 8 taps on a diamond
vec3 up(vec2 uv, vec2 hp) {
    vec3 s = texture(src, uv + vec2(-hp.x * 2.0, 0)).rgb + texture(src, uv + vec2(hp.x * 2.0, 0)).rgb
           + texture(src, uv + vec2(0, -hp.y * 2.0)).rgb + texture(src, uv + vec2(0, hp.y * 2.0)).rgb;
    s += (texture(src, uv + vec2(-hp.x, hp.y)).rgb + texture(src, uv + hp).rgb
        + texture(src, uv - hp).rgb + texture(src, uv + vec2(hp.x, -hp.y)).rgb) * 2.0;
    return s / 12.0;
}
```
Blur radius is controlled by number of levels and the offset multiplier.

## 3. Choosing
| Use | Kernel |
|---|---|
| Bloom | downsample chain with 13-tap (CoD AW) filter + tent upsample, additive between levels |
| UI frosted glass | dual Kawase, 3-4 levels |
| Exact Gaussian (DoF CoC, shadows) | separable Gaussian with linear sampling |
| Huge radius | mip chain blur or compute shared-memory sliding window |

## Gotchas
- Downsampling bright HDR pixels with a box filter causes fireflies flickering; use the Karis
  average (weight by 1/(1+luma)) on the first downsample for bloom.
- Odd-sized targets misalign texel centres between levels; compute half-texel from the source size.
- Separable blur on tilers costs two full passes of bandwidth; Kawase at reduced res is cheaper.

## Verify
- [ ] Blur of a single bright pixel is round (no box or diamond shape) at the chosen settings.
- [ ] No flicker on small bright highlights when moving.
