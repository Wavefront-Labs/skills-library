---
id: computing-software.game-programming.game-engine-architecture.material-systems-and-shader-permutations
name: material-systems-and-shader-permutations
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, shader-permutations, material-system, shader-variants, game-programming]
level: practitioner
status: draft
description: "Control shader permutation explosion: keyword combinations, static vs dynamic branching, variant stripping, pipeline caches and precompiling PSOs to avoid hitches."
sources: ["https://docs.unity3d.com/Manual/shader-variant-stripping.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/pso-precaching-for-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Material systems and shader permutations

**Goal:** flexible materials without millions of shader variants, long builds or runtime stutter.

## Where permutations come from
Each `#if FEATURE` compile-time switch doubles variants: 20 boolean keywords = 1 million combinations
per pass per platform. Multiplied by passes (depth, shadow, GBuffer, forward), vertex factories
(static, skinned, instanced) and quality levels.

## Control strategies
- **Dynamic branching** on uniform values for features that don't change register pressure much;
  modern GPUs handle coherent uniform branches cheaply.
- **Static switches** only for features that change performance significantly (e.g. parallax
  occlusion, many texture samples).
- **Ubershader + specialisation constants** (Vulkan) let the driver specialise at PSO creation without
  separate source compiles.
- **Strip unused variants** at build: collect which keyword combinations materials actually use
  (Unity `IPreprocessShaders.OnProcessShader` / shader variant collections, URP stripping settings).
- Limit artists to a material model with curated options rather than arbitrary feature toggles.

## Runtime hitches
D3D12/Vulkan compile full pipeline state objects (PSOs); first use mid-gameplay causes hitches.
- Record PSOs used during playtests (Unreal PSO caching, bundled pipeline caches), precompile at
  load or in the background.
- Unreal 5 PSO precaching creates PSOs when components load rather than at draw time.
- Vulkan `VkPipelineCache` saved to disk between runs; D3D12 driver caches help on repeat runs only.
- Unity: `ShaderVariantCollection.WarmUp` and Graphics State Collections (Unity 6) for PSO warmup.

## Metrics
Track variant count per shader, build time, shader memory, and first-use hitches (frame spikes
correlated with PSO compile events).

## Verify
- Fresh-cache playthrough with frame-time capture: no PSO compile spikes in gameplay.
- Variant count report per build compared against a budget in CI.
