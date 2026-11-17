---
id: computing-software.computer-graphics-engineering.rendering-techniques.diffuse-brdfs-lambert-burley-oren-nayar
name: diffuse-brdfs-lambert-burley-oren-nayar
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, physically-based-shading, burley-diffuse, oren-nayar, lambert, disney-brdf, diffuse-brdf, pbr]
level: advanced
status: docs-checked
description: "Choose diffuse BRDFs: Lambert, Disney/Burley with roughness-dependent grazing retro-reflection, and Oren-Nayar for rough matte, with the energy caveat."
sources: ["https://media.disneyanimation.com/uploads/production/publication_asset/48/asset/s2012_pbs_disney_brdf_notes_v3.pdf", "https://www1.cs.columbia.edu/CAVE/publications/pdfs/Oren_SIGGRAPH94.pdf", "https://google.github.io/filament/Filament.md.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diffuse BRDFs

## 1. Lambert
`f_d = albedo / PI`: constant in all directions. The Disney notes point out that a Lambert shader's
`n . l` factor belongs to the lighting integral, not the BRDF. Filament chooses Lambert as its
default diffuse term: it is extremely efficient, gives results "close enough to more complex
models", and the more sophisticated models make image-based lighting and spherical harmonics
harder to express.

## 2. What measured materials do (Disney notes, 2012)
Few measured materials are Lambertian. Many show a drop (a shadowed edge) in grazing
retro-reflection, and others show a peak. This is strongly correlated with roughness: smooth
surfaces, with a higher specular peak, tend to have a shadowed edge, and rough surfaces tend to
have a peak instead. The shadow on smooth surfaces is predicted by the Fresnel equations (more
energy is reflected, less refracted for diffuse re-emission, at grazing angles). The Oren-Nayar
model predicts a retro-reflective increase for rough surfaces and flattens the diffuse shape, but
the Disney authors found its peak weaker than the measured data and the flattening not present in
rough measured materials.

## 3. Disney / Burley diffuse
Burley's model gives a roughness-dependent retro-reflection at grazing angles. Filament lists it
as (Fresnel-like factors with a grazing value f90):
```glsl
float F_Schlick(float u, float f0, float f90) {
    return f0 + (f90 - f0) * pow(1.0 - u, 5.0);
}
float Fd_Burley(float NoV, float NoL, float LoH, float roughness) {
    float f90 = 0.5 + 2.0 * roughness * LoH * LoH;
    float lightScatter = F_Schlick(NoL, 1.0, f90);
    float viewScatter = F_Schlick(NoV, 1.0, f90);
    return lightScatter * viewScatter * (1.0 / PI);
}
```
Filament's equation writes the roughness term as alpha while the listing names the parameter
`roughness`; confirm which remapping your engine passes in. Filament notes the model is not
energy conserving as expressed, and decided the extra cost was not justified by the small
quality gain. In its comparison the two spheres look very similar, with the Disney one showing
retro-reflection at grazing angles.

## 4. Oren-Nayar
Oren and Nayar (SIGGRAPH 1994) model a rough surface as a collection of Lambertian facets
arranged in V-shaped cavities, with roughness given by the standard deviation of the facet slope
angle. Such a surface is inherently non-Lambertian because of foreshortening, and brightness
depends on view direction; their measurements (for example a clay vase and the moon's flat
appearance) agree with the model. They give a full integral model and a simpler functional
approximation; implement it from the paper's equations rather than from memory.

## 5. Choosing
| Need | Pick |
|---|---|
| Cheapest, simplest, compatible with SH and image-based lighting | Lambert |
| Roughness-aware grazing retro-reflection, matching Disney-style shading | Burley (watch energy) |
| Very rough matte surfaces (clay, moon) | Oren-Nayar |

## Gotchas
- Check whether a formula expects perceptual roughness or alpha (roughness squared); mixing them
  changes the look.
- Clamp NoL and NoV before using them in trigonometric forms.

## Verify
- [ ] Furnace test: white albedo in a uniform white environment never exceeds 1 (Burley may fail this without renormalisation).
- [ ] Side by side with a reference renderer on a sphere at several roughness values.

## Checked
2026-11-09. Read: Burley, "Physically-Based Shading at Disney" course notes (Lambert note,
measured retro-reflection and its roughness correlation, Oren-Nayar and Hanrahan-Krueger
comparison), Oren and Nayar 1994 (facet model and V-cavities; the formula constants did not
extract from the PDF so they are not reproduced), and Filament (Lambert choice, Burley equation
and listing, non-energy-conserving note). Removed: the Oren-Nayar shader snippet and its
0.33 / 0.09 / 0.45 constants, Fujii's improvement, OpenPBR EON, the Frostbite energy
renormalisation constants, the mobile statement, the (1 - F) and metallic combination advice,
and the Mitsuba reference suggestion.
Method: docs-checked 2026-11-09 against the Disney 2012 BRDF notes, Oren and Nayar 1994 and the Filament documentation.
