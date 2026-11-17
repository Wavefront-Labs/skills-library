---
id: computing-software.game-programming.game-engine-architecture.asset-dependency-graphs-and-incremental-builds
name: asset-dependency-graphs-and-incremental-builds
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, asset-dependency-graph, incremental-builds, asset-pipeline, game-programming]
level: practitioner
status: draft
description: "Build assets incrementally: dependency graphs, content-hash cache keys including tool versions, dependency discovery during import, and shared build caches."
sources: ["https://docs.unity3d.com/Manual/AssetDatabase.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/derived-data-cache"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Asset dependency graphs and incremental builds

**Goal:** after changing one texture, rebuild only what depends on it, and never ship stale data.

## Graph
Nodes: source assets and built artifacts. Edges: a build step's inputs (source files, other assets,
settings, tool version) -> outputs.
```text
hero.fbx ----\
hero_mat.json --> build_mesh(hero) --> hero.mesh
hero_albedo.png -> compress(BC7) ------> hero_albedo.tex --> referenced by hero_mat
```

## Cache keys
Key each step by a hash of: input content hashes (not timestamps), step parameters (platform,
compression quality), and the **tool/version** (importer code version). Unity's AssetDatabase v2
import keys and Unreal's Derived Data Cache keys follow this model, letting a shared cache serve
artifacts to the whole team (Unity Accelerator, Unreal shared DDC / Zen server).

## Discovering dependencies
Importers report what they read while running (a material reports the shader and textures it
referenced; an FBX importer reports external texture paths). Record these dynamically; static
declarations always drift. Include "negative" dependencies (a file that was looked up but missing)
so adding it later triggers a rebuild.

## Build execution
- Topological order; run independent steps in parallel.
- Check cache: hit -> fetch artifact; miss -> build -> store.
- Remove outputs whose inputs disappeared (orphans).

## Pitfalls
- Non-deterministic outputs (timestamps embedded, unordered map iteration) defeat caching; make
  importers deterministic and verify by rebuilding twice and comparing hashes.
- Forgetting tool version in the key ships stale artifacts after importer changes.

## Verify
- Touch a texture; build log shows only its dependents rebuilt.
- Clean build vs incremental build produce byte-identical packages.
