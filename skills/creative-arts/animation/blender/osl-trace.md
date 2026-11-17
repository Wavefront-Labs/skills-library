---
id: creative-arts.animation.blender.osl-trace
name: osl-trace
category: creative-arts
field: animation
product: blender
tags: [blender, osl-trace, trace, getattribute, osl, script-node, cycles]
level: advanced
status: docs-checked
description: "Query the scene from OSL in Cycles: trace rays on CPU for proximity or wear, getmessage for hit info, and getattribute for UVs, object data and geometry attributes."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/osl/index.html
  - https://open-shading-language.readthedocs.io/en/main/stdlib.html#renderer-state-and-messages
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# osl-trace

Goal: shaders that react to geometry around them or read per-object/per-vertex data.

## trace (CPU only)

```c
shader proximity(float Dist = 0.2, output float Fac = 0)
{
    int hit = trace(P, N, "maxdist", Dist);   // 1 if a surface is hit along N within Dist
    float d = Dist;
    if (hit) getmessage("trace", "hitdist", d);
    Fac = d / Dist;                            // 0 close to geometry, 1 open
}
```
Cycles supports `trace(point pos, vector dir, ...)`. The `"shade"` parameter is not supported; attributes of the hit object are read with `getmessage("trace", ..)` (see the OSL specification for the message names). Optional `"mindist"` and `"maxdist"` arguments set the distance range. `trace` cannot replace lighting: use it to probe nearby geometry, for example a projected texture blocked by geometry, wear on exposed geometry, or ambient-occlusion-like effects.

The manual marks `trace` as CPU only; on the OptiX GPU backend it is not functional, so the Ambient Occlusion and Bevel nodes do not work with OSL there.

## getattribute

```c
point uv;  getattribute("geom:uv", uv);                // default render UV map
point gen; getattribute("geom:generated", gen);        // generated coords from non-deformed mesh
float idx; getattribute("object:index", idx);          // object unique instance index
float rnd; getattribute("object:random", rnd);         // random per object instance
point loc; getattribute("object:location", loc);
color c;   getattribute("Col", c);                      // a named attribute (UV map, color attribute, geometry nodes output)
float len; getattribute("path:ray_length", len);        // ray distance since last hit
```
`getattribute()` reads geometry attributes: UV maps, color attributes and attributes output from geometry nodes. Built-in names documented for Cycles include `geom:uv`, `geom:generated`, `geom:tangent`, `geom:undisplaced`, `geom:dupli_generated`, `geom:dupli_uv`, `geom:name`, `geom:is_smooth`, `geom:is_curve`, `geom:curve_intercept`, `geom:curve_thickness`, `geom:curve_length`, `geom:curve_tangent_normal`, `geom:is_point`, `geom:point_radius`, `geom:point_position`, `geom:point_random`, `path:ray_length`, `object:random`, `object:index`, `object:location`, `material:index`, and `particle:index`, `age`, `lifetime`, `location`, `size`, `velocity`, `angular_velocity`.

`getattribute` returns an int success flag (OSL specification): check it and fall back to a default when the attribute is missing.

## Gotchas

- Attribute names must match the geometry attributes available on the object being shaded.
- `"mindist"` and `"maxdist"` units are determined by the renderer (OSL specification), so test the distances you pass.
- Test on the device you will render with: trace is CPU only.

## Verify

Proximity Fac darkens in corners like ambient occlusion on CPU; reading `object:random` gives a different value per object instance.

## Checked

2026-10-27 against the Blender 5.2 manual (Cycles > Open Shading Language: Attributes, Trace, Limitations) and the OSL standard library documentation (trace options mindist/maxdist, getmessage). Corrected: `object:index` is the object's unique instance index (not Pass Index), trace is CPU only. Removed unconfirmed attributes (`object:color`, `object:alpha`) and claims about self-hit offsets beyond the OSL options. Method: documentation only; no commands were run.
