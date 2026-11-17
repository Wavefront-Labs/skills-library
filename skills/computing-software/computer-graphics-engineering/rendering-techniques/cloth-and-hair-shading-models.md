---
id: computing-software.computer-graphics-engineering.rendering-techniques.cloth-and-hair-shading-models
name: cloth-and-hair-shading-models
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, physically-based-shading, cloth-brdf, hair-shading, sheen, charlie-sheen, kajiya-kay, marschner-hair]
level: advanced
status: docs-checked
description: "Shade cloth and hair: Charlie sheen and Ashikhmin velvet for fabric, Kajiya-Kay with shifted dual highlights, and the Marschner R, TT, TRT lobes."
sources: ["https://google.github.io/filament/Filament.md.html#materialsystem/clothmodel", "https://web.engr.oregonstate.edu/~mjb/cs519/Projects/Papers/HairRendering.pdf", "https://www.graphics.stanford.edu/papers/hair/hair-sg03final.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloth and hair shading models

## 1. Cloth
Microfacet BRDFs assume a surface of mirror-like grooves and look rigid, almost plastic, on
fabric. Cloth has a softer specular lobe with a large falloff, fuzz lighting from forward and
backward scattering, and sometimes two-tone specular colour (velvet). Filament's cloth model:
- Distribution: Ashikhmin's velvet NDF (an inverted Gaussian), or the "Charlie" sheen of Estevez
  and Kulla 2017 (an exponentiated sinusoid; softer, simpler, more natural parameterisation).
  Filament omits Estevez and Kulla's shadowing term for cost and uses the visibility term from
  Neubelt and Pettineo instead.
```glsl
float D_Charlie(float roughness, float NoH) {
    float invAlpha = 1.0 / roughness;
    float cos2h = NoH * NoH;
    float sin2h = max(1.0 - cos2h, 0.0078125);   // 2^(-14/2), keeps sin2h^2 > 0 in fp16
    return (2.0 + invAlpha) * pow(sin2h, invAlpha * 0.5) / (2.0 * PI);
}
// Filament specular: Fr = D * V * sheenColor   (F is the sheen colour, no Fresnel term)
```
- Sheen colour directly sets the specular reflectance, allowing two-tone fabrics. For velvet set
  the base colour black or dark and put the chromaticity in the sheen colour; for denim or
  cotton use the base colour for chromaticity with the default sheen colour, or the luminance of
  the base colour.
- Diffuse stays Lambertian, made energy conservative, with an optional non-physical subsurface
  colour term (wrap diffuse, `Fd *= saturate(subsurfaceColor + NoL)`) to mimic scattering,
  partial absorption and re-emission in some fabrics.

## 2. Hair
Strands are thin fibres: the Kajiya-Kay model uses the strand tangent T instead of the normal N
in the lighting equations, assuming the hair normal lies in the plane spanned by T and the view
vector. Specular term: sin(T, H) = sqrt(1 - dot(T, H)^2).

**Marschner et al. (SIGGRAPH 2003)** model a hair fibre as a dielectric cylinder (index of
refraction about 1.55) with a pigmented interior and a surface of tilted cuticle scales. Three
transport modes matter: R (surface reflection, white), TT (transmission through the fibre, a very
bright component focused toward the opposite side) and TRT (internal reflection, coloured, can
form caustics or glints). The scale tilt shifts the R and TRT cones in opposite directions, so
they separate into two visible highlights. Measurements showed the primary highlight continues
all the way around the fibre while the secondary highlight is confined to the side toward the
light, and the scattering depends on the fibre's rotation about its axis (non-circular
cross-section). The full model has terms I have not reproduced here; read the paper before
implementing it.

**Scheuermann (GDC 2004)**, a phenomenological match to those observations: primary highlight
shifted toward the tip, secondary coloured, shifted toward the root, and sparkly. Implementation
from the slides:
```glsl
vec3 shiftT(vec3 T, vec3 N, float shift) { return normalize(T + shift * N); }
float strandSpec(vec3 T, vec3 V, vec3 L, float e) {
    vec3 H = normalize(L + V);
    float TdH = dot(T, H);
    return smoothstep(-1.0, 0.0, TdH) * pow(sqrt(1.0 - TdH * TdH), e);
}
```
- With T pointing root to tip, a positive nudge moves the highlight toward the root and a
  negative nudge toward the tip. Read the shift from a texture to break up uniform patches.
- Two highlights with different colours, exponents and shifted tangents; modulate the secondary
  with a noise texture.
- The Kajiya-Kay diffuse sin(T, L) looks too bright without self-shadowing; the slides use a
  tweaked N.L (`saturate(lerp(0.25, 1.0, dot(N, L)))`) which softens the shadow boundary.

## Gotchas
- Using mesh normals instead of tangents for hair gives plastic-looking highlights.
- A tangent nudge needs a consistent T direction (root to tip) across the mesh.

## Verify
- [ ] Cloth shows a soft, wide sheen and no sharp microfacet highlight.
- [ ] Hair shows two distinct highlights, the second tinted, and they move along the strands as the light moves.

## Checked

Method: docs-checked 2026-11-09 against the Filament materials document cloth section (Ashikhmin, Charlie, sheen colour, subsurface and full BRDF listing read), the GDC 2004 hair slides (Kajiya-Kay, shift and StrandSpecular code, HairLighting diffuse read) and the Marschner 2003 paper (introduction and section 2.1 read; R, TT, TRT, tilt and measurement findings). Dropped glTF sheen and Unreal attributions, the prefiltered Charlie IBL and DFG-channel claim, the 1 minus sheen albedo scaling, the Kajiya-Kay 1989 year, and the practical-hair section (cards, OIT, deep opacity maps) as not confirmed in the sources.
