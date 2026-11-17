---
id: computing-software.computer-graphics-engineering.rendering-techniques.anisotropic-specular-brdf
name: anisotropic-specular-brdf
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, physically-based-shading, anisotropic-specular, anisotropic-ggx, brushed-metal, khr-materials-anisotropy, tangent-space, pbr]
level: advanced
status: docs-checked
description: "Implement anisotropic GGX specular for brushed metal: tangent frames, alpha_t/alpha_b from roughness and anisotropy, bent-reflection IBL, glTF KHR_materials_anisotropy."
sources: ["https://google.github.io/filament/Filament.md.html#materialsystem/anisotropicmodel", "https://github.com/KhronosGroup/glTF/tree/main/extensions/2.0/Khronos/KHR_materials_anisotropy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Anisotropic specular

## 1. Parameterisation
Two roughnesses along the tangent (T) and bitangent (B). Filament follows Kulla (2017) because it
allows sharp highlights (Neubelt-Pettineo and Burley give alternative mappings):
```glsl
float at = max(alpha * (1.0 + anisotropy), 0.001);   // alpha = perceptualRoughness^2
float ab = max(alpha * (1.0 - anisotropy), 0.001);   // anisotropy in [-1, 1]
```
glTF `KHR_materials_anisotropy` (ratified) instead raises the roughness along the anisotropy
direction: `alpha_t = mix(alpha, 1.0, strength^2)` and `alpha_b = alpha`, with
`alpha = roughness^2`. Parameters: `anisotropyStrength` (default 0), `anisotropyRotation`
(radians counter-clockwise from the tangent, default 0), `anisotropyTexture` (red/green = direction
in [-1, 1] in tangent space, blue = strength multiplied by `anisotropyStrength`, linear). With no
texture the default is the +X direction at full strength.

## 2. Anisotropic GGX
Burley's anisotropic NDF with Heitz's height-correlated visibility, as in Filament:
```glsl
float D_GGX_Aniso(float NoH, float ToH, float BoH, float at, float ab) {
    float a2 = at * ab;
    vec3 d = vec3(ab * ToH, at * BoH, a2 * NoH);
    float d2 = dot(d, d);
    float b2 = a2 / d2;
    return a2 * b2 * b2 / PI;
}
float V_SmithGGXCorrelated_Aniso(float at, float ab, float ToV, float BoV, float ToL, float BoL, float NoV, float NoL) {
    float lambdaV = NoL * length(vec3(at * ToV, ab * BoV, NoV));
    float lambdaL = NoV * length(vec3(at * ToL, ab * BoL, NoL));
    return 0.5 / (lambdaV + lambdaL);
}
```
The NDF needs the tangent and bitangent as well as the normal. Setting `anisotropy` to 0 gives
`at = ab = alpha`, which collapses to the isotropic GGX terms.

## 3. Tangent frame
- glTF: a primitive using the extension MUST have a defined tangent space (NORMAL and TANGENT
  attributes, or a normal texture on the material), and SHOULD supply NORMAL and TANGENT because
  the core spec does not mandate a tangent-derivation algorithm. When both `normalTexture` and
  `anisotropyTexture` exist they SHOULD share texture coordinates.
- The glTF sample builds the direction from the texture (`rg * 2 - 1`), rotates it by
  `anisotropyRotation`, maps it through the TBN matrix to get `T`, and takes
  `B = cross(geometricNormal, T)`.
- The direction in the texture is the direction in which highlights stretch; the micro-grooves run
  perpendicular to it. A per-texel direction map can therefore encode radial or circular patterns.

## 4. Image-based lighting
Prefiltered cubemaps are isotropic. Filament uses the "bent reflection vector" of McAuley (2015),
based on Revie (2012): a rough approximation, the alternative being importance sampling. Negative
`anisotropy` swaps the direction so highlights follow the bitangent instead of the tangent:
```glsl
vec3 anisotropicDirection = anisotropy >= 0.0 ? bitangent : tangent;
vec3 anisotropicTangent = cross(anisotropicDirection, v);
vec3 anisotropicNormal = cross(anisotropicTangent, anisotropicDirection);
vec3 bentNormal = normalize(mix(n, anisotropicNormal, anisotropy));
vec3 r = reflect(-v, bentNormal);
```

## Gotchas
- Clamp `at` and `ab` to a small minimum (Filament uses 0.001) so the NDF stays finite.
- The bent-normal IBL is an approximation, not an exact integral.

## Verify
- [ ] On a test disc with radial tangents, highlights stretch along the tangent direction, perpendicular to the grooves.
- [ ] `anisotropy` = 0 reproduces isotropic GGX.

## Checked
2026-11-08. Read in full: Filament materials guide (anisotropic model and anisotropy IBL sections),
Khronos KHR_materials_anisotropy README. Confirmed: at/ab mapping (Kulla 2017), 0.001 clamp, NDF and
visibility code, glTF parameters, defaults, texture channels, roughness mix formula, tangent-space
requirements, bent reflection vector listing and sign handling. Removed: the Disney 2012 course
notes source (the PDF could not be read as text here and the skill relies on Filament's restatement),
MikkTSpace, re-orthogonalisation snippet, the roughness-scaled bend factor, the hair-model remark and
unsourced seam and aliasing claims.
Method: documentation only; no commands were run.
