---
id: computing-software.computer-graphics-engineering.rendering-techniques.gooch-technical-illustration-shading
name: gooch-technical-illustration-shading
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, npr, gooch-shading, technical-illustration, cool-to-warm, non-photorealistic-rendering, cad-visualisation]
level: practitioner
status: docs-checked
description: "Implement Gooch cool-to-warm shading for technical illustration: blend cool and warm tones by N.L, with black edge lines, white highlights and metal banding."
sources: ["https://users.cs.northwestern.edu/~ago820/SIG98/gooch98.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gooch and technical illustration shading

Gooch, Gooch, Shirley, Cohen (SIGGRAPH 1998). Shading uses intermediate intensities and a
cool-to-warm hue shift so that black edge lines and white highlights stay visible. Shaded regions
must not be so dark that edge lines vanish, nor so bright that highlights vanish.

## 1. Tone equation
The paper blends two colours with the cosine term:
`I = ((1 + l.n) / 2) * k_warm + (1 - (1 + l.n) / 2) * k_cool` (their equation 2; with `l.n` in
[-1, 1], so the light should be roughly perpendicular to the gaze direction to show the full
range). The undertones are:
- `k_blue = (0, 0, b)` and `k_yellow = (y, y, 0)`.
- `k_cool = k_blue + alpha * k_d` and `k_warm = k_yellow + beta * k_d` (equation 3), where `k_d` is
  the object's diffuse colour.
- Free parameters: `b` and `y` set the strength of the temperature shift; `alpha` and `beta` set
  how much of the object colour and luminance shift show. The paper's figures use
  b = 0.4, y = 0.4, alpha = 0.2, beta = 0.6 and also b = 0.55, y = 0.3, alpha = 0.25, beta = 0.5,
  and says the exact values are not crucial. Choose intermediate values.
```glsl
uniform vec3 surfaceColor;           // k_d
const vec3 kBlue = vec3(0.0, 0.0, 0.55), kYellow = vec3(0.3, 0.3, 0.0);
const float alpha = 0.25, beta = 0.5;

vec3 gooch(vec3 N, vec3 L) {
    vec3 kCool = kBlue   + alpha * surfaceColor;
    vec3 kWarm = kYellow + beta  * surfaceColor;
    float t = (1.0 + dot(N, L)) * 0.5;          // 0 facing away, 1 facing light
    return mix(kCool, kWarm, t);
}
```
The paper places the single light up and to the right and keeps it fixed, since vision assumes
light comes from above.

## 2. Lines and highlights
- Edge lines are the surface boundaries, silhouettes and discontinuities (creases), drawn as
  black curves.
- Highlights are white, from a single light source.
- The paper generated edge lines interactively for polygonal objects with Markosian et al.'s
  technique and mentions image-processing techniques as another route.

## 3. Metal
Illustrators show metal with alternating dark and light bands. The paper maps twenty stripes of
random intensity between 0.0 and 0.5 along the parametric axis of maximum curvature, with the
stripe closest to the light direction set to white, interpolating colours between stripe
centres. A cool-warm variant of metal shading exists for scenes mixing metal and matte objects.

## 4. Fixed-function approximation
With negative light colours, equation 2 can be approximated with two lights in directions l and
-l of intensities `(k_warm - k_cool)/2` and `(k_cool - k_warm)/2` plus an ambient term of
`(k_cool + k_warm)/2`, with the object colour white and the Phong highlight turned off (negative
blue light caused jarring artifacts). Each object needs its own light colours.

## Gotchas
- Without edge lines and highlights the shading alone looks flat; the paper's point is the
  combination.
- Pure black-to-object-colour tones (the paper's diffuse extreme) make shading dark where l.n is
  near 0 and defeat the edge lines.

## Verify
- [ ] Shape reads clearly in a still image: cool side away from the light, warm side toward it.
- [ ] Edge lines are visible in the shaded areas and highlights visible in the lit areas.

## Checked
2026-11-09. Read: Gooch, Gooch, Shirley, Cohen 1998 (sections on shading models, equations 2 and
3, parameter values for Figures 7 and 8, metal stripes, fixed-function approximation, edge lines
and highlights; the PDF text lost some symbols so the equations were reconstructed from the
surrounding prose). Removed: the specular-highlight code with the `100 * R.V - 97` form (an RTR4
form, not in the paper), the silhouette and crease techniques (inverted hull, dihedral angle
thresholds, line widths), presentation and background tips, tone-mapping advice, and the
Real-Time Rendering and Stanford sources (not read).
Method: docs-checked 2026-11-09 against Gooch et al. SIGGRAPH 1998 "A Non-Photorealistic Lighting Model For Automatic Technical Illustration".
