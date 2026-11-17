---
id: computing-software.game-programming.unreal-engine.pcg-framework-graphs
name: pcg-framework-graphs
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, pcg-framework, procedural-content-generation, pcg-graph, open-world, game-programming]
level: practitioner
status: draft
description: "Author Unreal PCG graphs: PCG Volume and Component, point sampling, filters, attribute ops, static mesh spawners, partitioning and runtime generation."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview", "https://dev.epicgames.com/documentation/en-us/unreal-engine/using-pcg-generation-modes-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-node-reference-in-unreal-engine"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PCG framework graphs

**Goal:** forests, rocks and props scattered by rules, re-generating when the landscape changes.

## Setup
Enable the **Procedural Content Generation Framework** plugin (and PCG Geometry Script Interop if
needed). Place a **PCG Volume** (has a PCG Component) and assign a **PCG Graph** asset.

## Graph basics
Data flows as point sets with attributes ($Position, $Rotation, $Scale, $Density, $Seed, custom).
Typical forest graph:
1. **Get Landscape Data** / Surface Sampler (points per square metre, point extents).
2. **Density filters**: Density Noise, Distance (from splines/roads), Difference (subtract road
   spline areas), Normal To Density (slope).
3. **Transform Points**: random rotation/scale ranges, offsets.
4. **Self Pruning** to avoid overlapping trees.
5. **Static Mesh Spawner** with weighted mesh list; spawns into ISM/HISM components.
Inspect a node (A key / Debug) to visualise points; attribute list view shows values.

## Inputs and subgraphs
- Splines: Get Spline Data, Spline Sampler for roadside props or fences.
- Actor data: Get Actor Data with tags to read hand-placed exclusion volumes.
- Subgraphs and graph parameters (User Parameters) make reusable building blocks;
  Graph Instances override parameters per volume.

## Generation modes
- **Generate On Load** / On Demand in editor (results saved as part of the level).
- **Partitioned**: with World Partition, the PCG Component splits into partition actors per grid cell
  so generation and streaming work per cell.
- **Runtime generation** (Generation Trigger: Generate At Runtime) with the PCG Generation Radii, for
  infinite or dynamic content; costs runtime CPU.

## Gotchas
- Seeds: changing node order or parameters reseeds results; lock seeds for art-approved areas.
- Spawned meshes need collision settings on the spawner if gameplay needs them.
- Large point counts in the editor are slow; debug on a small volume first.
- Cleanup: Regenerate clears previous results only for components it owns.

## Verify
- [ ] Moving a road spline regenerates vegetation around it; profiles show acceptable generation time.
