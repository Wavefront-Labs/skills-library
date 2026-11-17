---
id: computing-software.computer-graphics-engineering.shader-programming.sdf-3d-primitive-library
name: sdf-3d-primitive-library
category: computing-software
field: computer-graphics-engineering
product: shader-programming
tags: [computer-graphics-engineering, shader-programming, sdf-raymarching, sdf-primitives, signed-distance-functions, sdf, raymarching, sphere-tracing]
level: practitioner
status: draft
description: "Reference 3D signed distance primitives for ray marching: sphere, box, round box, torus, capsule, cylinder, cone, plane, and transforms that keep them exact."
sources: ["https://iquilezles.org/articles/distfunctions/", "https://mercury.sexy/hg_sdf/", "https://iquilezles.org/articles/sdfxor/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 3D SDF primitive library

All functions take `p` already in the primitive's local space and return signed distance
(negative inside). Exact SDFs give the fastest, artefact-free sphere tracing.

```glsl
float sdSphere(vec3 p, float r) { return length(p) - r; }

float sdBox(vec3 p, vec3 b) {
    vec3 q = abs(p) - b;
    return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0);
}

float sdRoundBox(vec3 p, vec3 b, float r) { return sdBox(p, b - r) - r; }

float sdTorus(vec3 p, vec2 t) {            // t.x major radius, t.y tube radius, axis = y
    vec2 q = vec2(length(p.xz) - t.x, p.y);
    return length(q) - t.y;
}

float sdCapsule(vec3 p, vec3 a, vec3 b, float r) {
    vec3 pa = p - a, ba = b - a;
    float h = clamp(dot(pa, ba) / dot(ba, ba), 0.0, 1.0);
    return length(pa - ba * h) - r;
}

float sdCylinder(vec3 p, float h, float r) {   // capped, axis = y, half-height h
    vec2 d = abs(vec2(length(p.xz), p.y)) - vec2(r, h);
    return min(max(d.x, d.y), 0.0) + length(max(d, 0.0));
}

float sdPlane(vec3 p, vec3 n, float h) { return dot(p, n) + h; }   // n normalised

float sdCone(vec3 p, vec2 c, float h) {        // c = (sin, cos) of half-angle, tip at origin
    vec2 q = h * vec2(c.x / c.y, -1.0);
    vec2 w = vec2(length(p.xz), p.y);
    vec2 a = w - q * clamp(dot(w, q) / dot(q, q), 0.0, 1.0);
    vec2 b = w - q * vec2(clamp(w.x / q.x, 0.0, 1.0), 1.0);
    float k = sign(q.y);
    float d = min(dot(a, a), dot(b, b));
    float s = max(k * (w.x * q.y - w.y * q.x), k * (w.y - q.y));
    return sqrt(d) * sign(s);
}
```

## Transforms
- **Translate/rotate**: apply the inverse transform to `p` (`p = (invModel * vec4(p,1)).xyz`).
  Rigid transforms keep the field exact.
- **Uniform scale**: `sdf(p / s) * s`.
- **Non-uniform scale** breaks the distance property; the result is a bound at best. Multiply by
  `min(s.x, s.y, s.z)` to stay conservative (slower marching).
- **Rounding**: `sdf(p) - r` inflates any shape. **Onion/shell**: `abs(sdf(p)) - thickness`.
- **Elongation**: `q = p - clamp(p, -h, h); sdf(q)` stretches a shape exactly.
- **Revolution/extrusion**: build 3D from 2D SDFs: `sd2D(vec2(length(p.xz) - o, p.y))`.

## Gotchas
- `min` of exact SDFs is exact outside but only a bound inside; smooth unions are bounds too.
- Twist/bend deformations are not Lipschitz-1; scale the march step (0.5-0.8) or you overshoot.
- hg_sdf uses the opposite axis conventions in places; check before mixing libraries.

## Verify
- [ ] Visualise `abs(sdf)` on a slicing plane as iso-lines; spacing uniform for exact primitives.
- [ ] Normals from central differences continuous on every primitive.
