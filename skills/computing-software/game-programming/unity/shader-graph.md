---
id: computing-software.game-programming.unity.shader-graph
name: shader-graph
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-graphics, shader-graph, urp, sub-graphs, custom-function-node, material-properties, game-programming]
level: practitioner
status: draft
description: "Build URP/HDRP shaders in Shader Graph: targets and master stack, exposed properties, sub-graphs, keywords and variant cost, Custom Function nodes and driving materials from code."
sources: ["https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.shadergraph@17.0/manual/Custom-Function-Node.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shader Graph

**Goal:** artist-editable shaders (dissolve, hit flash, triplanar, water) that compile to few variants
and are driven cleanly from gameplay code.

## Setup
- Create > Shader Graph > URP > Lit / Unlit / Sprite Lit / Fullscreen. **Graph Settings** pick the
  target (URP/HDRP/Built-in), material type, surface (Opaque/Transparent), alpha clipping, two-sided.
- The **master stack** has Vertex (position, normal) and Fragment (base color, normal, metallic,
  smoothness, emission, alpha) blocks.

## Properties
- Blackboard properties become material properties. Set a clear **Reference** name (`_DissolveAmount`);
  code uses the reference, not the display name.
- Uncheck **Exposed** for values set only globally (`Shader.SetGlobalFloat("_GlobalWind", w)`).
- Keep per-material properties compatible with the **SRP Batcher** (Shader Graph does this automatically:
  everything in the UnityPerMaterial CBUFFER).

## Driving from code
```csharp
static readonly int Dissolve = Shader.PropertyToID("_DissolveAmount");
renderer.material.SetFloat(Dissolve, t);          // .material clones the material (leak + breaks batching)

// per-instance without cloning:
var mpb = new MaterialPropertyBlock();
renderer.GetPropertyBlock(mpb); mpb.SetFloat(Dissolve, t); renderer.SetPropertyBlock(mpb);
```
MaterialPropertyBlocks break SRP Batcher compatibility for that renderer; for many hit-flashing
enemies, either accept it or use per-material instances created once (`new Material(shared)`, destroyed
with the object).

## Sub-graphs and custom code
- Sub Graph for reusable chunks (triplanar sampling, noise). Inputs/outputs typed.
- **Custom Function** node: inline string or `.hlsl` file with `void MyFunc_float(float3 In, out float3 Out)`;
  provide `_float` and `_half` versions for precision modes. Guard previews with `#ifdef SHADERGRAPH_PREVIEW`
  (e.g. for main light access).

## Keywords and variants
- Boolean/Enum **Keywords**: `Shader Feature` (stripped if no material uses it; set per material in
  editor) vs `Multi Compile` (always compiled; use only for runtime toggles). Every keyword multiplies
  variants: 3 multi_compile booleans = 8x.
- Prefer a float property + `Branch` node (both sides evaluated) for cheap toggles over new keywords.
- Local keywords (default) don't consume the global keyword limit.

## Gotchas
- Transparent graphs don't write depth; sorting issues are expected, not a bug.
- Normal maps: sample with Type = Normal, and set texture import Type = Normal map.
- Vertex displacement needs bounds padding or the mesh is culled while still on screen.

## Verify
- [ ] Frame Debugger shows SRP Batch groups intact for the new shader.
- [ ] Build log / Shader variant collection shows the expected variant count.
