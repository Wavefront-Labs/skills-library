---
id: computing-software.game-programming.unity.urp-hand-written-hlsl-shaders
name: urp-hand-written-hlsl-shaders
category: computing-software
field: game-programming
product: unity
tags: [unity, urp-hlsl-shader, urp, hlsl, shaderlab, srp-batcher, game-programming]
level: practitioner
status: docs-checked
description: "Hand-written URP shaders: the ShaderLab LightMode and UniversalMaterialType Pass tag values URP uses, unsupported legacy tags, and what the SRP Batcher does."
sources: ["https://docs.unity3d.com/6000.0/Documentation/Manual/urp/writing-custom-shaders-urp.html", "https://docs.unity3d.com/6000.0/Documentation/Manual/urp/urp-shaders/urp-shaderlab-pass-tags.html", "https://docs.unity3d.com/Manual/SRPBatcher.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hand-written URP HLSL shaders

**Goal:** a custom URP shader whose Passes are picked up by the right part of the pipeline and that batches with the SRP Batcher.

## Where to start
Unity's "Writing custom shaders in URP" page groups the resources: examples of writing a custom shader in URP, built-in shader methods in URP (the HLSL helper library), making a URP shader compatible with the SRP Batcher, and the URP shader keywords and macros reference. Take code samples and helper names from those pages for your URP version rather than from older built-in pipeline shaders.

## LightMode Pass tag
The `LightMode` value tells the pipeline which Pass to run in which part of rendering. If a Pass has no `LightMode` tag, URP uses `SRPDefaultUnlit` for it.

| Value | What the Pass does (per the URP reference) |
|---|---|
| `UniversalForward` | Renders geometry and evaluates all light contributions; used in the Forward Rendering Path |
| `UniversalGBuffer` | Renders geometry without evaluating light; for Passes that must run in the Deferred Rendering Path |
| `UniversalForwardOnly` | Like `UniversalForward`, but URP can use it in both the Forward and Deferred paths; use it when a Pass must render with the Forward path even under Deferred (the page's example: Clear Coat normals that do not fit the GBuffer) |
| `DepthNormalsOnly` | Depth and normal prepass; use with `UniversalForwardOnly` in the Deferred path, and add it if you use the SSAO Renderer Feature |
| `Universal2D` | Renders objects with 2D lights; used by the 2D Renderer |
| `ShadowCaster` | Renders object depth from the light's perspective into the shadow map or a depth texture |
| `DepthOnly` | Renders only depth from the Camera's perspective into a depth texture |
| `Meta` | Runs only when baking lightmaps in the Editor; stripped from shaders when building a Player |
| `SRPDefaultUnlit` | Draws an extra Pass (the page's example is an object outline); valid in both Forward and Deferred; the default when no `LightMode` is set |
| `MotionVectors` | Adds motion vector support to the shader |

- A shader that must render in both Forward and Deferred declares two Passes, tagged `UniversalForward` and `UniversalGBuffer`.
- A shader that must always render with the Forward path declares only a `UniversalForwardOnly` Pass.
- In the Deferred path, if the `DepthNormalsOnly` Pass is missing, Unity does not generate the ambient occlusion around the mesh.

## UniversalMaterialType Pass tag
Used in the Deferred Rendering Path. `Lit` (default when the tag is not set; PBR specular model) or `SimpleLit` (Blinn-Phong specular model). During the G-buffer Pass Unity uses stencil to mark which pixels use which type.

## SRP Batcher
- Supported in URP, HDRP and custom Scriptable Render Pipelines; not in the Built-in Render Pipeline.
- It reduces render-state changes between draw calls (rather than the number of draw calls) by combining a sequence of GPU `bind` and `draw` commands into an SRP batch.
- To get larger batches use as few shader variants as possible; any number of materials sharing the same shader is fine.
- Material data persists in GPU constant buffers, so unchanged materials cause no render-state changes.
- For the rules that make a URP shader compatible, follow Unity's "Make a URP shader compatible with the SRP Batcher" page.

## Gotchas
- URP does not support these `LightMode` tags: `Always`, `ForwardAdd`, `PrepassBase`, `PrepassFinal`, `Vertex`, `VertexLMRGBM`, `VertexLM`. Port built-in pipeline multi-pass lighting accordingly.

## Verify
- [ ] Each Pass the pipeline needs (forward or GBuffer, `ShadowCaster`, `DepthOnly`, `DepthNormalsOnly` if using SSAO) carries the right `LightMode`.

## Checked
Confirmed against the URP "Writing custom shaders" index, the ShaderLab Pass tags in URP reference and the SRP Batcher page: tag values and their descriptions, the `SRPDefaultUnlit` default, unsupported tags, `UniversalMaterialType` default, SRP Batcher pipeline support and mechanism. Removed because the cited pages do not state them: the sample shader, `CBUFFER`/`UnityPerMaterial` rules, the Inspector compatibility message, lighting function names, shader keywords and `UsePass` advice.
Method: docs-only read of cited pages, 2026-11-08
