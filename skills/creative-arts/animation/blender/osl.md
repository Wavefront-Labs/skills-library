---
id: creative-arts.animation.blender.osl
name: osl
category: creative-arts
field: animation
product: blender
tags: [blender, osl, open-shading-language, script-node, cycles, shader-scripting, custom-shader, procedural-shader, closures, optix-osl, text-editor]
level: sme
status: draft
description: "Open Shading Language in Blender Cycles: enabling OSL, the Script node (text vs .osl file), shader structure, inputs/metadata, closures, procedural patterns, GPU limits, debugging."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# osl

Goal: a custom procedural texture or BSDF that the node editor cannot express, compiled into a Script node that behaves like any other shader node.

## Enabling

Render Properties → Render Engine **Cycles** → *Open Shading Language* tick (under the *Render Engine* row in 4.x; older: Render → *Shading Language*). CPU rendering always supports OSL. **GPU:** OptiX supports OSL since 3.5 (NVIDIA only; limited — no `trace()`, no `printf`; noise and texture calls work); CUDA, HIP, Metal and oneAPI **do not** run OSL — with OSL enabled the whole render falls back to CPU on those devices. Material Preview (EEVEE) ignores Script nodes (shows black/pink) — preview in Rendered view with Cycles.

## Script node

`Shift A → Script → Script`. Modes:
- **Internal**: pick a text block from the Text Editor (write the shader there; the Text Editor's *Templates → Open Shading Language* has starters). Press the **refresh** icon (or `Script → Update` in the Text Editor) after edits — sockets are regenerated from the shader's parameters.
- **External**: a `.osl` (compiled on the fly) or `.oso` (precompiled with `oslc`) file path; relative paths `//shaders/x.osl`. *Auto Update* recompiles when the file changes on disk.
Compile errors print in the Info editor and the system console (Window → *Toggle System Console* on Windows).

## Shader anatomy

```c
shader ring_noise(
    point Pos = P,
    float Scale = 5.0 [[ float min = 0.01, float max = 100 ]],
    float Rings = 8.0,
    color ColorA = color(0.1, 0.1, 0.1),
    color ColorB = color(0.9, 0.8, 0.6),
    output color Color = 0.0,
    output float Fac = 0.0)
{
    point p = Pos * Scale;
    float n = noise("perlin", p);            // "uperlin", "simplex", "usimplex", "cell", "gabor", "hash"
    float r = length(vector(p.x, p.y, 0)) + n * 0.5;
    Fac = 0.5 + 0.5 * sin(r * Rings * M_PI);
    Color = mix(ColorA, ColorB, Fac);
}
```
- Every parameter becomes a socket; type → socket type (`float`, `int`, `color`, `point`/`vector`/`normal`, `string` (file paths/enum-like), `matrix` is not a socket). `output` parameters are outputs. Defaults are socket defaults; metadata `[[ ... ]]` sets UI min/max/description.
- Globals: `P` position, `N` normal, `Ng` geometric normal, `I` view vector, `u`/`v` UV (needs `getattribute("geom:uv", ...)` in Cycles for the active UV map: `getattribute("UVMap", uv)` by name), `time`, `dPdx/dPdy` for filtering, `Ci` (closure output). Attributes: `getattribute("geom:generated", p)`, `getattribute("object:location", loc)`, `getattribute("geom:dupli_generated", ...)`, custom mesh attributes by name (`getattribute("myattr", val)` works for colour/float attributes).
- Spaces: `transform("object", P)`, `transform("world", "camera", v)`; `"common"`, `"shader"`, `"object"`, `"world"`, `"camera"`, `"screen"`, `"raster"`, `"NDC"`.
- Textures: `texture("//tex/image.png", u, v)` (OIIO; `"wrap"`, `"filter"`, `"interp"` options), `environment()`; `texture3d()` and `pointcloud()` are not supported in Cycles.
- **Ray tracing:** `trace(P, dir, "maxdist", d)` + `getmessage("trace", "hit", hit)` / `"hitdist"` — fake AO/curvature/thickness inside a shader (CPU only). Expensive; keep rays few.
- **Closures** (BSDF outputs): declare `output closure color BSDF = 0;` and assign `BSDF = Fac * diffuse(N) + (1-Fac) * microfacet("ggx", N, roughness, eta, 0)`; available: `diffuse`, `oren_nayar`, `translucent`, `reflection`, `refraction`, `transparent`, `microfacet(...)` variants, `microfacet_ggx`, `microfacet_beckmann`, `ashikhmin_shirley`, `emission`, `background`, `holdout`, `ambient_occlusion`, `bssrdf`, `principled_diffuse`, `principled_sheen`, `principled_clearcoat` (the full Principled BSDF is not a single closure — build it from parts or feed your outputs into a Principled node instead), `hair_reflection`/`hair_transmission`, `henyey_greenstein` + `absorption` for volumes. Plug the closure output into the Material Output *Surface*.

## Common uses

- Procedural patterns beyond the node set: hexagonal tiles, Worley with custom distance metrics, gabor noise, fractal flames, layered FBM with explicit loops (`for (int i=0;i<Octaves;i++)`).
- Parametric maths textures where a node tree would be 200 nodes (lens distortions, spirals, text-free gauges).
- `trace()`-based curvature/thickness masks without baking.
- Per-object logic via `getattribute("object:index", idx)` / `getattribute("object:random", r)` — pass per-object parameters as custom mesh attributes rather than relying on string compares.
- Importing shaders from Arnold/RenderMan libraries (standard OSL is portable; remove renderer-specific closures).

## Workflow

1. Text Editor → New → paste the shader (no registration needed; the Script node lists all text blocks).
2. Script node *Internal* → select text → refresh; connect outputs to a Principled or straight to Material Output.
3. Rendered viewport, Cycles CPU (or OptiX), *Viewport Denoising* off while iterating noise patterns.
4. Edit → refresh; errors in Info. `printf("%f\n", x)` appears in the system console (CPU).
5. Lock the version: save as `//shaders/name.osl`, switch the node to External for shared files, or precompile with `oslc` from the OSL toolset (`oslc name.osl` → `name.oso`) for fast loads.

## Performance and limits

- OSL on CPU is 2–5× slower than native SVM nodes for simple shaders; worth it only where nodes can't do it. Avoid loops with hundreds of iterations and `trace()` in reflections.
- No OSL in EEVEE, Workbench or bakes to EEVEE; **Cycles bakes** do support OSL (CPU).
- OptiX OSL: no `trace`, no `printf`, limited string ops; test any `texture()` call on the GPU before committing to it.
- `matrix` parameters, arrays and structs aren't sockets; pass numbers or use `getattribute`.
- Script nodes are not exportable (glTF/USD/FBX): bake to images for handoff (`creative-arts.animation.blender.texture-baking`).

## Gotchas

- Forgot to tick *Open Shading Language*: node renders black.
- Edited text but no refresh: old sockets/behaviour persist.
- `P` in a Script node is world-space; textures swim on moving objects — use `transform("object", P)` or a `point Pos = P` input fed by a Texture Coordinate → Object.
- Output colour is linear; `color("sRGB", r, g, b)` constructor converts if you typed display values.
- Shader name must be a valid identifier and unique per file; two texts with the same `shader` name confuse the compiler cache — rename.
- Render farm: external `.osl` paths must resolve on every node (relative paths, files shipped).

## Verify

- Script node shows your parameters as sockets after refresh; changing a default changes the render.
- CPU Cycles render shows the pattern; switching device to CUDA/HIP shows pink/black (proving it's OSL) and OptiX renders if supported.
- `printf` values appear in the console for one pixel region (wrap in `if (u < 0.01 && v < 0.01)` to avoid flooding).
- Baked image of the OSL output matches the rendered look and the material works in EEVEE with the bake.
