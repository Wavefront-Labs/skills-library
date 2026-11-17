---
id: computing-software.computer-graphics-engineering.shader-programming.polar-coordinate-radial-patterns
name: polar-coordinate-radial-patterns
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, procedural-patterns, polar-coordinates, radial-patterns, atan2, kaleidoscope, book-of-shaders]
level: practitioner
status: draft
description: "Make radial shader patterns with polar coordinates: atan angle/radius mapping, angular repetition, spirals, sunbursts, radial UV for textures and the atan seam fix."
sources: ["https://thebookofshaders.com/07/", "https://iquilezles.org/articles/sdfrepetition/", "https://registry.khronos.org/OpenGL-Refpages/gl4/html/atan.xhtml"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Polar coordinates and radial patterns

## 1. Convert
```glsl
vec2 p = uv * 2.0 - 1.0;            // centre at origin
p.x *= aspect;
float r = length(p);
float a = atan(p.y, p.x);           // -PI..PI (HLSL: atan2(y, x))
```

## 2. Shapes from r(a)
```glsl
float f = 0.5 + 0.1 * cos(a * 5.0);             // 5-petal flower
float mask = 1.0 - smoothstep(f - 0.01, f + 0.01, r);
float gear = smoothstep(-0.5, 1.0, cos(a * 10.0)) * 0.2 + 0.5;
```
Use `fwidth(r - f)` for the edge width instead of a fixed 0.01 to stay crisp at any resolution.

## 3. Angular repetition (kaleidoscope)
```glsl
const float N = 6.0;
float sector = 6.2831853 / N;
float ai = a - sector * floor((a + 0.5 * sector) / sector);   // -sector/2..sector/2
vec2 q = r * vec2(cos(ai), sin(ai));                          // draw once in q, repeats N times
q.y = abs(q.y);                                               // mirror for kaleidoscope
```

## 4. Spirals, rays, rings
```glsl
float spiral = fract(a / 6.2831853 + r * 3.0 - time);
float rays   = smoothstep(0.0, 0.1, abs(fract(a * 8.0 / 6.2831853) - 0.5));
float rings  = fract(r * 10.0 - time);
```

## 5. Radial texture mapping
`vec2 polarUV = vec2(a / 6.2831853 + 0.5, r);` maps a strip texture around a circle (portals,
radar sweeps, tunnel effects with `vec2(a/TAU, 1.0/r + time)`).

## Gotchas
- The atan seam at a = +-PI breaks derivatives: textures sampled with `polarUV` show a one-pixel
  line. Fix with `textureGrad` using derivatives of a seam-free version, or compute derivatives from
  `fwidth` of `atan(p.y, abs(p.x))` style alternatives.
- `atan(y, x)` with both zero is undefined; guard the centre pixel.
- Repetition count N must be an integer or a visible seam appears at the wrap.

## Verify
- [ ] No seam along the negative x axis.
- [ ] Shape edges remain 1-2 pixels wide at all resolutions.
