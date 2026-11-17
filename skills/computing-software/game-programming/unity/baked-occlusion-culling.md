---
id: computing-software.game-programming.unity.baked-occlusion-culling
name: baked-occlusion-culling
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-occlusion-culling, occlusion-culling, rendering-performance, game-programming]
level: practitioner
status: docs-checked
description: "Bake Unity occlusion culling: when it pays, Occluder and Occludee Static setup, Bake tab settings, Occlusion Portals and the visualization tools."
sources: ["https://docs.unity3d.com/Manual/OcclusionCulling.html", "https://docs.unity3d.com/Manual/occlusion-culling-getting-started.html", "https://docs.unity3d.com/Manual/class-OcclusionPortal.html", "https://docs.unity3d.com/Manual/occlusion-culling-window.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Baked occlusion culling

**Goal:** stop rendering GameObjects completely hidden behind others.

## When it pays
- Cameras do frustum culling by default; occlusion culling additionally excludes Renderers entirely
  obscured by nearer ones.
- Built-in occlusion culling runs runtime calculations on the CPU, which can offset the CPU it saves, so
  it is most likely to help when the project is GPU-bound due to overdraw.
- Baked data is loaded into memory at runtime; ensure enough memory.
- It works best where small, well-defined areas are separated by solid GameObjects (rooms joined by
  corridors).
- Dynamic GameObjects can be occluded but cannot occlude others; the built-in system is not suitable if
  scene geometry is generated at runtime.
- In URP or HDRP you can instead enable GPU occlusion culling (sub-pages not opened).

## Setup
1. Static Occluder: medium to large solid GameObject (wall, building) with a Terrain or Mesh Renderer,
   opaque, not moving at runtime. With LOD groups, LOD0 is used to determine what it occludes. Set via
   Inspector Static Editor Flags > Occluder Static.
2. Static Occludee: any Renderer type, not moving at runtime; small or transparent objects are good
   candidates. Set Static Editor Flags > Occludee Static. One GameObject can be both.
3. The Camera's Occlusion Culling property must be enabled.
4. Window > Rendering > Occlusion Culling > Bake tab > Bake. Unity saves the data as an asset and links it
   with the current Scene(s). Clear removes previously baked data.

## Bake tab settings
- **Smallest Occluder** (metres): size of the smallest GameObject that can occlude; the page advises
  choosing the highest value that gives good results for smaller files and faster bakes. A lower value
  gives more, smaller cells, more precision and larger files.
- **Smallest Hole**: diameter of the smallest gap a Camera can see through; same advice. Lower value gives
  more subdivisions within cells.
- **Backface Threshold**: excludes areas where visible occluder geometry is above that percentage
  backfaces; default 100 never removes areas; lower is smaller but can cause visual artifacts.
- Set Default Parameters resets them. Occlusion Areas (Object tab, Create New Occlusion Area) can define
  View Volumes; outside the generated data area Unity does no occlusion culling.

## Occlusion Portals
Closed portal occludes, open one does not. For a door, add an Occlusion Portal component (not Occluder
or Occludee Static; it need not be on the door GameObject). Set `open` in a script, for example
`myOcclusionPortal.open = true;`. Properties: Open, Center (default 0,0,0), Size.

## Visualizing
Keep the Occlusion Culling window and Scene view visible, select a Camera and move it. The Scene popup
has Edit mode (View Volumes) and Visualize mode (Camera Volumes, Visibility Lines, Portals).

## Checked
Date: 2026-11-07

Read in full: the four cited pages (overview, set up a scene, Occlusion Portal, window reference). No
embedded images or code tabs beyond the single portal snippet were visible in the stripped text; the
GPU occlusion culling pages were not opened.

Removed because the pages do not confirm it: "Umbra", the 5 / 1-2 metre suggestions, "Dynamic Occlusion"
renderer toggle, multi-scene bake advice, Frame Debugger use, the Unity 6 GPU Resident Drawer / Forward+
claim, the Gotchas (small props bloat data, rebake in CI, popping and Smallest Hole, "transparent objects
must not be occluders" is replaced by the page's opaque requirement) and the Verify list.

Method: documentation only; no commands were run.
