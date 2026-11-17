---
id: computing-software.game-programming.unreal-engine.pso-caching-and-shader-hitches
name: pso-caching-and-shader-hitches
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, pso-cache, shader-compilation, hitches, d3d12, vulkan, game-programming]
level: practitioner
status: draft
description: "Remove first-use shader hitches in Unreal with PSO caching: bundled PSO cache collection and expansion, UE5.3+ PSO precaching, and validating with stats."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/optimizing-rendering-with-pso-caches-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/pso-precaching-for-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/manually-creating-bundled-pso-caches-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PSO caching and shader hitches

**Goal:** no stutter the first time an effect, material or level is seen on D3D12/Vulkan/Metal.

## Why hitches happen
Modern APIs compile Pipeline State Objects (shaders plus render state) at draw time if not
prepared; compiling takes milliseconds to hundreds of milliseconds.

## PSO precaching (UE5.2+, default on in 5.3+ for D3D12)
`r.PSOPrecaching=1`: when components load, the engine predicts PSOs their materials need and
compiles them asynchronously. Optionally delays drawing until ready (`r.PSOPrecache.ProxyCreationWhenPSOReady=1`
skips drawing a proxy until its PSO compiled; objects pop in rather than hitch). Covers most mesh
draws, not every global shader or rare state.

## Bundled PSO cache (still recommended alongside)
1. Package a build with `r.ShaderPipelineCache.Enabled=1` and `-logPSO` (or
   `r.ShaderPipelineCache.LogPSO=1`), play through all content (automated flythroughs). Recorded
   `.rec.upipelinecache` files appear in `Saved/CollectedPSOs`.
2. Gather the `.shk` stable key files produced by the cook (`Saved/Cooked/.../Metadata/PipelineCaches`).
3. Expand: `UnrealEditor-Cmd.exe MyGame -run=ShaderPipelineCacheTools expand *.rec.upipelinecache *.shk MyGame_PCD3D_SM6.spc`.
4. Put the `.spc` in `Build/<Platform>/PipelineCaches/` and repackage; the game precompiles them at
   startup (batch size via `r.ShaderPipelineCache.BatchSize`, during loading screens with
   `r.ShaderPipelineCache.PrecompileBatchTime`).

## Validate
- `stat PSOPrecache` / `r.PSOPrecache.Validation=2` reports missed PSOs at runtime.
- Unreal Insights: look for `PSO creation` spans on the render/RHI thread during gameplay.
- Test with a cleared driver shader cache (driver caches hide problems on dev machines).

## Gotchas
- Material or engine changes invalidate recorded PSOs; recollect regularly (CI flythroughs).
- Too many precompiled PSOs lengthen first launch; show a progress UI.

## Verify
- [ ] On a clean machine with a cleared driver cache, first playthrough shows no PSO hitches above budget.
