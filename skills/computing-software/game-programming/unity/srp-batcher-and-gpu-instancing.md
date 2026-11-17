---
id: computing-software.game-programming.unity.srp-batcher-and-gpu-instancing
name: srp-batcher-and-gpu-instancing
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-graphics, srp-batcher, gpu-instancing, draw-calls, game-programming]
level: advanced
status: docs-checked
description: "Reduce draw-call CPU cost in URP: how the SRP Batcher and GPU instancing work, their compatibility limits, and when each applies."
sources: ["https://docs.unity3d.com/Manual/SRPBatcher.html", "https://docs.unity3d.com/Manual/GPUInstancing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SRP Batcher and GPU instancing

**Goal:** cut render-thread CPU time spent setting up draws, picking the right mechanism per case.

## The two mechanisms
| Mechanism | What it does | Notes from the Unity manual |
|---|---|---|
| **SRP Batcher** | Reduces render-state changes between draw calls by combining sequences of `bind` and `draw` GPU commands into SRP batches; keeps material data persistent in GPU memory | Supported in URP, HDRP and custom SRPs; not in the Built-in Render Pipeline |
| **GPU instancing** | Renders many GameObjects that share the same mesh and material in a single draw call; each instance can have different properties such as colour or scale | Compatible with all render pipelines, with limits below |

## SRP Batcher
- It lowers CPU time for scenes with many materials that use the same shader variant. Each SRP batch
  should contain as many `bind` and `draw` commands as possible, so use as few shader variants as
  possible; you can still use as many different materials with the same shader as you like.
- Material content persists in GPU memory, and a dedicated code path manages a large per-object GPU
  constant buffer for per-object properties.

## GPU instancing
- Benefits depend on platform and GPU: Unity must collect, combine and upload properties for each
  draw call, so overhead can outweigh the gain. The manual says benefits are better on mobile than
  on desktop.
- Compatible meshes (with prebuilt materials): Mesh Renderer components, and meshes rendered from
  script with APIs such as `Graphics.RenderMeshInstanced`. Skinned Mesh Renderer is not supported.
- Compatible shaders: most prebuilt materials (look for the Enable GPU Instancing property) and
  Shader Graph materials in URP or HDRP.
- Lighting: dynamic objects lit by Light Probes, static objects using lightmaps (Contribute GI set,
  same lightmap texture), and objects using Light Probe Proxy Volumes.

## Interaction
In URP or HDRP, GPU instancing works with custom shaders only if you disable the SRP Batcher or make
the shader incompatible with it. In the Built-in pipeline, instancing does not work with Shader Graph
shaders. Unity also has a "Choose a method for optimizing draw calls" page for alternatives.

## Verify
- [ ] Measure render-thread CPU time before and after; instancing can cost more than it saves.
- [ ] Confirm each instanced renderer is a Mesh Renderer, not a Skinned Mesh Renderer.

## Checked

Method: docs-checked 2026-11-09 against the Unity manual pages "Scriptable Render Pipeline Batcher in URP" and "Introduction to GPU instancing" (both read in full).
Removed as unconfirmed: static batching, dynamic batching and GPU Resident Drawer rows, the SRP-Batcher-takes-precedence claim, CBUFFER/UnityPerMaterial shader rules, MaterialPropertyBlock incompatibility, the 1023-instance limit, RenderMeshIndirect and UNITY_INSTANCING_BUFFER advice, and the Frame Debugger, Profiler and Stats window guidance.
