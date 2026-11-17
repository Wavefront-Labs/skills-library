---
id: computing-software.computer-graphics-engineering.rendering-techniques.image-based-lighting-split-sum
name: image-based-lighting-split-sum
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, local-illumination, image-based-lighting, ibl, split-sum, prefiltered-environment-map, brdf-lut, ggx-importance-sampling, irradiance-map]
level: advanced
status: docs-checked
description: "Implement split-sum image-based specular lighting: prefiltered GGX environment mips by roughness, a BRDF integration LUT, Hammersley sampling, seam and bright-dot fixes."
sources: ["https://learnopengl.com/PBR/IBL/Specular-IBL"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Image-based lighting: split sum

**Goal:** indirect specular lighting from an HDR environment that matches the direct-light BRDF, using
two texture lookups. Epic Games' split sum approximation splits the specular integral into a
pre-filtered environment map and a BRDF integration map (LearnOpenGL, Specular IBL).

## 1. The approximation
The specular integral is split into `integral(L_i dw) * integral(f_r n.w dw)`:
- the first factor is the pre-filtered environment map, convolved per roughness level, one level per
  mip of a cubemap;
- the second assumes constant white radiance and depends only on `N.V` and roughness, stored as a 2D
  LUT holding a scale (red) and a bias (green) applied to the Fresnel term F0.
```glsl
vec3 R = reflect(-V, N);
const float MAX_REFLECTION_LOD = 4.0;                       // 5 mips: 0..4
vec3 prefilteredColor = textureLod(prefilterMap, R, roughness * MAX_REFLECTION_LOD).rgb;
vec3 F = FresnelSchlickRoughness(max(dot(N, V), 0.0), F0, roughness);
vec2 envBRDF = texture(brdfLUT, vec2(max(dot(N, V), 0.0), roughness)).rg;
vec3 specular = prefilteredColor * (F * envBRDF.x + envBRDF.y);   // do not also multiply by kS
vec3 kD = (1.0 - F) * (1.0 - metallic);
vec3 ambient = (kD * irradiance * albedo + specular) * ao;
```
Approximation made when prefiltering: the view direction is assumed equal to the normal and reflection
direction (`N = R = V`). The cost is that grazing-angle specular reflections are lost, which is generally
considered acceptable.

## 2. Prefilter the environment cubemap
- Allocate a cubemap (the tutorial uses RGB16F, 128x128 per face at mip 0, "likely enough for most
  reflections"; raise it for many smooth materials) with `GL_LINEAR_MIPMAP_LINEAR` minification, and
  render each mip with `roughness = mip / (maxMipLevels - 1)`, halving the framebuffer size per mip.
- For each texel, take N = R = V and loop over Hammersley low-discrepancy samples (tutorial: 1024),
  GGX importance-sample a half vector, reflect to L, accumulate `radiance * NdotL` for `NdotL > 0` and
  divide by the total weight.
```glsl
vec3 ImportanceSampleGGX(vec2 Xi, vec3 N, float roughness) {
    float a = roughness * roughness;                    // Epic squares roughness
    float phi = 2.0 * PI * Xi.x;
    float cosTheta = sqrt((1.0 - Xi.y) / (1.0 + (a*a - 1.0) * Xi.y));
    float sinTheta = sqrt(1.0 - cosTheta*cosTheta);
    vec3 H = vec3(cos(phi) * sinTheta, sin(phi) * sinTheta, cosTheta);
    vec3 up = abs(N.z) < 0.999 ? vec3(0,0,1) : vec3(1,0,0);
    vec3 tangent = normalize(cross(up, N)), bitangent = cross(N, tangent);
    return normalize(tangent * H.x + bitangent * H.y + N * H.z);
}
```
Hammersley sample i of N is `vec2(float(i)/float(N), RadicalInverse_VdC(i))`; bit operations are
unavailable on some targets such as WebGL and OpenGL ES 2.0, which need a loop-based Van der Corput.

## 3. BRDF integration LUT
- Move F0 out of the integral using the Fresnel-Schlick form: the two integrals are the scale
  `integral f_r (1 - (1 - w_o.h)^5) n.w` and the bias `integral f_r (1 - w_o.h)^5 n.w`.
- Render a 2D quad whose texture coordinates are `N.V` (x) and roughness (y); per sample, importance
  sample GGX, accumulate `(1 - Fc) * G_Vis` into A and `Fc * G_Vis` into B with
  `Fc = (1 - VdotH)^5` and `G_Vis = G * VdotH / (NdotH * NdotV)`, then average.
- For IBL the Schlick-GGX geometry term uses `k = alpha^2 / 2` (direct lighting uses
  `(alpha + 1)^2 / 8`). The tutorial passes roughness itself as alpha there and notes this matches
  Epic's LUT.
- The tutorial stores it as a 512x512 `GL_RG16F` texture with `GL_CLAMP_TO_EDGE`; it does not depend
  on any environment, so compute or load it once.

## 4. Practical issues
- **Cubemap seams at high roughness**: enable `glEnable(GL_TEXTURE_CUBE_MAP_SEAMLESS)` so sampling
  filters across faces.
- **Bright dots** in rough mips of high-contrast HDR maps: more samples may not be enough. Sample a mip
  of the source cubemap chosen from the sample's PDF instead (credited to Chetan Jags):
```glsl
float D = DistributionGGX(NdotH, roughness);
float pdf = (D * NdotH / (4.0 * HdotV)) + 0.0001;
float saTexel  = 4.0 * PI / (6.0 * resolution * resolution);
float saSample = 1.0 / (float(SAMPLE_COUNT) * pdf + 0.0001);
float mipLevel = roughness == 0.0 ? 0.0 : 0.5 * log2(saSample / saTexel);
```
  The source cubemap needs trilinear filtering and generated mipmaps.
- Precompute the irradiance and pre-filter maps once and store them (for example in a format that holds
  mips such as .dds) rather than at every startup; tools such as cmftStudio and IBLBaker can generate them.
- Reflection probes with interpolation and parallax correction give local IBL; the tutorial skips
  them.

## Checked
2026-11-08. Confirmed against LearnOpenGL "Specular IBL": split sum factors, white-radiance LUT, `N = R = V` assumption, 5 mip levels and `MAX_REFLECTION_LOD`, 128x128 base, Hammersley and GGX importance sampling code, squared roughness, BRDF LUT derivation, `k` for IBL, 512x512 RG16F, seamless cubemaps, PDF-based mip selection for bright dots, precompute-once advice and tools. Fixed: the PDF expression in the earlier draft used `dot(H, N)` in the denominator (the page uses `HdotV`). Removed: Epic's course notes and Filament page (unreadable or empty), the spherical-harmonics diffuse advice, multiscatter compensation, luminance clamping, "256-512 base" and LUT size ranges, and the claim about ignoring local occlusion.
Method: documentation only; no commands were run.

## Verify
- [ ] Furnace test: white environment, white non-metal sphere looks uniformly ~white at all roughnesses.
- [ ] Matches a reference path tracer render of a sphere array within tolerance.
- [ ] No bright dots in rough mips with a sunny HDRI.
