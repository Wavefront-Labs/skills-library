---
id: computing-software.computer-graphics-engineering.shader-programming.sdf-boolean-and-smooth-operations
name: sdf-boolean-and-smooth-operations
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, sdf-raymarching, smooth-min, sdf-operations, csg, domain-repetition]
level: practitioner
status: docs-checked
description: "Combine signed distance fields with union, subtraction, intersection, smooth-min blends, rounding, onion, repetition and transforms while keeping distances valid."
sources: ["https://iquilezles.org/articles/smin/", "https://iquilezles.org/articles/distfunctions/", "https://mercury.sexy/hg_sdf/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDF boolean and smooth operations

## 1. Booleans
```glsl
float opUnion(float a, float b)      { return min(a, b); }
float opSubtract(float a, float b)   { return max(a, -b); }   // a minus b
float opIntersect(float a, float b)  { return max(a, b); }
```
Results are bounds (distance may be underestimated) inside or near the seams; sphere tracing
still works but may take more steps.

## 2. Smooth min (polynomial, Quilez)
```glsl
float smin(float a, float b, float k) {          // k = blend radius in world units
  float h = max(k - abs(a - b), 0.0) / k;
  return min(a, b) - h * h * k * 0.25;
}
float smax(float a, float b, float k) { return -smin(-a, -b, k); }
// smooth subtraction: smax(a, -b, k)
```
The smooth-min article also covers blending material attributes with the same factor.

## 3. Modifiers
```glsl
float opRound(float d, float r) { return d - r; }          // inflate / round edges
float opOnion(float d, float t) { return abs(d) - t; }     // hollow shell
vec3  opRep(vec3 p, vec3 c)     { return p - c * round(p / c); }   // infinite repetition
vec3  opRepLim(vec3 p, float c, vec3 l) { return p - c * clamp(round(p / c), -l, l); }
```
Transforms: evaluate the SDF at the **inverse-transformed point**; rigid transforms keep exact
distances, uniform scale is exact with `sdf(p / s) * s`; non-uniform scale only gives a bound.

## Gotchas
- Plain repetition only works for shapes symmetric about the tile boundaries; naive use renders wrongly otherwise (see Quilez's domain repetition article).
- Smooth union, subtraction and intersection give bounds, not exact distances.

## Checked
2026-11-01. Confirmed against iquilezles.org distfunctions and smin pages: min/max booleans, polynomial smooth-min (equivalent to his quadratic form with k scaled), round/onion/limited repetition, exact rotation/translation/uniform scale, bound for non-uniform scale and smooth ops. Removed: material blend line, the twist/bend step-size advice, and the large-k material gotcha (not in sources). opRep rewritten to Quilez's form.
Method: documentation only; no commands were run.

## Verify
- [ ] Visualise distance with iso-line colouring on a slice plane; lines evenly spaced.
