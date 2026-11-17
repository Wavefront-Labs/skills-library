---
id: computing-software.computer-graphics-engineering.shader-programming.lighting-shaders-blinn-phong-to-pbr
name: lighting-shaders-blinn-phong-to-pbr
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [shader-programming, shaders, glsl, hlsl, wgsl, vertex-shader, fragment-shader, pixel-shader, lighting, blinn-phong, pbr, cook-torrance, ggx, schlick-fresnel, smith-geometry, metallic-roughness, normal-mapping, tangent-space, gamma, linear-workflow, srgb, tone-mapping, hdr, energy-conservation]
level: advanced
status: draft
description: "Write lighting shaders correctly: spaces and normals, Blinn-Phong, a metallic-roughness Cook-Torrance GGX BRDF, normal mapping, and the linear-light/tone-mapping rules that make it look right."
sources: ["https://learnopengl.com/PBR/Theory", "https://google.github.io/filament/Filament.html", "https://blog.selfshadow.com/publications/s2013-shading-course/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lighting shaders: Blinn-Phong to PBR

**Goal:** write vertex/fragment shaders that light surfaces plausibly under any light,
with the inputs (normals, spaces, colour encoding) correct — most "my lighting looks wrong"
bugs are input bugs, not BRDF bugs. GLSL shown; HLSL/WGSL map one-to-one.

## 1. Get the inputs right
- Do lighting in **one consistent space** (world or view). Transform normals with the
  **normal matrix** = `transpose(inverse(mat3(model)))`, not `mat3(model)` — they differ
  under non-uniform scale. Compute it on the CPU, not per vertex.
- Re-`normalize` interpolated normals in the fragment shader; interpolation shortens them.
- **Linear light:** textures authored as colour (albedo/base colour, emissive) are sRGB —
  sample them through an sRGB texture format (hardware decodes) or decode manually; data
  maps (normal, roughness, metalness, AO) are linear. Light in linear, then tone map, then
  encode to sRGB once at the end (or write to an sRGB render target).
- Use HDR intermediate targets (`RGBA16F`) so bright lights don't clip before tone mapping.

## 2. Blinn-Phong (cheap, still useful for stylised/mobile)
```glsl
vec3 N = normalize(vNormal);
vec3 L = normalize(uLightPos - vWorldPos);
vec3 V = normalize(uCameraPos - vWorldPos);
vec3 H = normalize(L + V);
float NdotL = max(dot(N, L), 0.0);
float spec  = pow(max(dot(N, H), 0.0), uShininess) * float(NdotL > 0.0);
vec3 color  = uAlbedo * NdotL * uLightColor + uSpecColor * spec * uLightColor;
```
Blinn's half-vector exponent is roughly 2–4× Phong's for a similar highlight size.
It isn't energy-conserving: brighter highlights don't get narrower; artists compensate by hand.

## 3. PBR: metallic-roughness Cook-Torrance
The standard real-time model (glTF, Unreal, Unity, Filament):
```glsl
const float PI = 3.14159265;
float D_GGX(float NdotH, float a) {           // a = roughness^2 (perceptual remap)
    float a2 = a * a; float d = NdotH * NdotH * (a2 - 1.0) + 1.0;
    return a2 / (PI * d * d);
}
float V_SmithGGXCorrelated(float NdotV, float NdotL, float a) {   // includes the 1/(4 NdotL NdotV)
    float a2 = a * a;
    float gv = NdotL * sqrt(NdotV * NdotV * (1.0 - a2) + a2);
    float gl = NdotV * sqrt(NdotL * NdotL * (1.0 - a2) + a2);
    return 0.5 / (gv + gl);
}
vec3 F_Schlick(float VdotH, vec3 F0) { return F0 + (1.0 - F0) * pow(1.0 - VdotH, 5.0); }

vec3 shade(vec3 N, vec3 V, vec3 L, vec3 baseColor, float metallic, float perceptualRough, vec3 radiance) {
    vec3 H = normalize(V + L);
    float NdotV = max(dot(N, V), 1e-4), NdotL = max(dot(N, L), 0.0);
    float NdotH = max(dot(N, H), 0.0), VdotH = max(dot(V, H), 0.0);
    float a = max(perceptualRough * perceptualRough, 0.002);   // avoid a=0 singularity
    vec3 F0 = mix(vec3(0.04), baseColor, metallic);            // dielectrics ≈ 4% reflectance
    vec3 F  = F_Schlick(VdotH, F0);
    vec3 spec = D_GGX(NdotH, a) * V_SmithGGXCorrelated(NdotV, NdotL, a) * F;
    vec3 diffuse = (1.0 - F) * (1.0 - metallic) * baseColor / PI;  // metals have no diffuse
    return (diffuse + spec) * radiance * NdotL;
}
```
- Light units: with the `/PI` in the diffuse term, a directional light's `radiance` is
  its illuminance; be consistent across engine and tools or exposure will be off.
- Point/spot lights: inverse-square falloff `1/d²` with a smooth window to zero at the
  light's range (Unreal/Filament-style), not linear falloff.
- Ambient/IBL: split-sum approximation — prefiltered environment cubemap (mip by
  roughness) + a 2D BRDF LUT + irradiance (SH or small cubemap) for diffuse. Without IBL,
  metals render black outside direct highlights.

## 4. Normal mapping
- Build TBN from the vertex tangent (with `w` = handedness: `B = cross(N, T) * tangent.w`),
  Gram–Schmidt orthogonalise T against N, then `N = normalize(TBN * (tex * 2.0 - 1.0))`.
- Normal maps must use the same tangent basis they were baked with (MikkTSpace is the
  common standard) and the right green-channel convention: OpenGL-style (+Y up: Blender,
  Unity) vs DirectX-style (−Y: Unreal, Substance's DirectX preset). Inverted bumps = flip G.
- Normal maps must be sampled from a **linear** (non-sRGB) texture.

## 5. Tone mapping
Apply exposure, then a curve (ACES fitted, AgX, Khronos PBR Neutral, Reinhard), then sRGB
encode. Clipping linear values straight to 8-bit looks harsh and desaturated in highlights.

## Gotchas
- Specular aliasing (sparkling) on rough-looking detail at distance: use specular
  anti-aliasing (roughness widening from normal variance, e.g. Toksvig-style) or ensure
  normal map mips are generated properly.
- `pow(x, y)` with `x < 0` is undefined — clamp dot products first.
- Precision: on mobile `mediump` can break GGX at low roughness; use `highp` for the specular term.

## Verify
- [ ] A white furnace test (uniform white environment, white albedo) gives roughly uniform
      brightness — no glowing rims (energy gain) or dark discs.
- [ ] Non-uniformly scaled objects light correctly (normal matrix).
- [ ] Same asset matches a reference renderer (Blender, glTF sample viewer) under the same HDRI.
- [ ] Albedo sampled as sRGB, data maps as linear; output encoded once.
- [ ] Normal map bumps go the right way (check with a known test texture).
