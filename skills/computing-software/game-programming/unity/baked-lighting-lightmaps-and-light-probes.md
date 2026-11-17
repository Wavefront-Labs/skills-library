---
id: computing-software.game-programming.unity.baked-lighting-lightmaps-and-light-probes
name: baked-lighting-lightmaps-and-light-probes
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-graphics, lightmapping, light-probes, progressive-lightmapper, adaptive-probe-volumes, game-programming]
level: practitioner
status: docs-checked
description: "Unity baked lighting concepts: what lightmaps store, the three light baking backends and their status, UV chart requirements, and what Light Probes are for."
sources: ["https://docs.unity3d.com/Manual/Lightmappers.html", "https://docs.unity3d.com/Manual/LightProbes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baked lighting, lightmaps and light probes

**Goal:** understand what baking gives you, which backend to choose, and when to use light probes.

## Lightmaps
- Lightmapping pre-calculates the brightness of surfaces and stores it in a texture called a lightmap.
  Lightmaps can include direct and indirect light, and are combined with albedo and normals by the
  material's shader.
- Baked data cannot change at runtime. Real-time lights can be overlaid additively but cannot
  interactively change the lightmaps. The manual frames this as trading light movement at gameplay for a
  potential performance gain, suiting less powerful hardware such as mobile.
- A UV chart is one distinct shape in the lightmap (for example one face of a cube) with a margin
  around it. A UV layout is the set of charts for one mesh, with padding separating it from other
  layouts packed into the same atlas.

## Backends
Select with Default Light Baker in the Graphics settings window.
- **Unity Compute Light Baker**: produces lightmaps, Light Probes and Adaptive Probe Volume data; built
  on the SRP Core lighting stack using Compute shaders and the Unified Ray Tracing API. Opt-in, URP and
  HDRP only; some lighting settings behave differently, so you may need to adjust lighting.
- **Progressive Light Baker**: path-tracing based, progressive updates in the Editor, bakes lightmaps and
  Light Probes. Backends: Progressive GPU and Progressive CPU. The Progressive CPU Lightmapper is
  deprecated and will be removed in a future release. It requires non-overlapping UV charts with small
  area and angle errors and sufficient margin between charts.
- Baked lighting may look different after changing backend.

## Light Probes
- Positions in the scene where light is measured during the bake; they store light passing through empty
  space (lightmaps store light hitting surfaces). At runtime, indirect light on dynamic GameObjects is
  approximated from the nearest probes.
- Two uses: primary, high-quality lighting (including bounced indirect) on moving objects; secondary,
  lighting for static scenery that uses Unity's LOD system.
- The page links to Adaptive Probe Volumes (APV) in URP as an additional resource.

## Checked
Date: 2026-11-07

Read in full: "Introduction to lightmaps and baking" and "Light Probes" (the latter is a short overview
with one link). The linked sub-pages (Choose a light baking backend, Lightmapping: Getting started,
Unity Compute Light Baker, APV) were not opened.

Removed because neither page confirms it: Mixed Lighting Mode options, Contribute and Receive Global
Illumination settings, Generate Lightmap UVs and UV2 advice, texel density and Scale in Lightmap, all the
sample counts, bounces, padding and size numbers, OIDN filtering, Lighting Data Asset notes, Light Probe
Group placement and tetrahedral interpolation, "URP 17+", Light Probe Proxy Volumes, Reflection Probes,
all Gotchas and the Verify list. The tag `reflection-probes` was dropped as the topic is no longer covered.

Method: documentation only; no commands were run.
