---
id: computing-software.computer-graphics-engineering.rendering-techniques.terrain-rendering-clipmaps
name: terrain-rendering-clipmaps
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, terrain-rendering, clipmaps, geometry-clipmaps, cdlod, quadtree-lod, heightmap]
level: sme
status: docs-checked
description: "Render large heightmap terrain with geometry clipmaps (Losasso, Hoppe) and CDLOD quadtrees (Strugar): LOD ranges, vertex morphing, toroidal updates."
sources: ["https://hhoppe.com/geomclipmap.pdf", "https://github.com/fstrugar/CDLOD/blob/master/cdlod_paper_latest.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terrain rendering: clipmaps and quadtrees

## 1. Geometry clipmaps (Losasso and Hoppe, SIGGRAPH 2004)
- A terrain pyramid cached as nested regular grids centred on the viewer, at successive
  power-of-two resolutions. Each level is an n x n array of vertices in a video-memory vertex
  buffer, accessed toroidally (2D wraparound with mod on x and y) so shifting a level needs no
  copy of old data; only the newly exposed L-shaped region is filled.
- Each vertex carries (x, y, z, z_c) where z_c is the height in the next-coarser level, used for
  transition morphing. Each level also has an 8-bit normal map at twice the geometry resolution
  (one normal per vertex is too blurry), recomputed on update, plus optional colour or attribute
  images.
- Regions: the clip region is the stored world extent, the active region the extent to render
  (a square centred at the viewer), and the render region the hollow frame
  active(l) minus active(l+1). If updates cannot keep up the clip region falls behind and the
  active region is cropped to it. Constraints include nested clip regions, an active region
  within its clip region, perimeters on "even" vertices for a watertight boundary with the
  coarser level, and a render region at least two grid units wide.
- Size: for a 640 pixel window and 90 degree field of view the paper found n = 255 works well,
  about a 3 pixel screen-space triangle (normal maps at twice the resolution give about 1.5
  pixels per texture sample). Viewer-centred regions allow instant rotation but n must grow as
  the field of view narrows. Looking straight down from height, unnecessarily fine levels are
  disabled when viewer height exceeds a level-dependent threshold.
- Updates: coarse-to-fine order, stopping when a budget is exceeded, so fast movement
  loses fine detail near the viewer. New data is predicted from the coarser level with an
  interpolatory subdivision (four-point scheme, weights -1/16, 9/16, 9/16, -1/16), coarser levels
  being filled from decompressed terrain and finer ones synthesised.
- Transitions: geometry near each render region's outer boundary morphs to the coarser level
  with `z' = (1 - alpha) * z + alpha * z_c`, alpha computed from the vertex's grid coordinates
  relative to the continuous viewer position (not time-based): zero except in a transition
  region of width about n/10 grid units where it ramps linearly to 1 at the outer perimeter. The
  work takes about 10 vertex shader instructions. Textures also blend between the level and its
  coarser level using the same alpha (the paper disables hardware mipmapping for this).

## 2. CDLOD (Strugar)
- The heightmap is organised into a quadtree of constant depth; one fixed-size grid mesh
  (commonly 16x16 to 128x128) is transformed in the vertex shader to cover each selected node,
  with heights displaced from a heightmap texture fetch. A quadtree depth level corresponds to a
  LOD level; each successive LOD has four times as many nodes and triangles.
- LOD ranges: precalculated distances where each range is twice the previous one; the last
  represents the total view distance. A morph area, usually the last 15 to 30 percent of every
  range, defines where higher detail morphs into lower.
- Selection: traverse the quadtree each frame, testing node bounding boxes against the LOD range
  spheres and the frustum (min/max maps provide the bounds).
- Morph is per vertex, based on the vertex's own LOD metric: vertices with an odd grid index
  move toward the even neighbour `(i - i/2, j - j/2)` as `morphK` goes from 0 to 1, so each block
  of eight triangles becomes two and the node matches the coarser LOD with no seams or
  T-junctions. Edge vertices must use a distance function consistent across the dataset so
  neighbouring nodes agree. Height uses a bilinear sample in the morph region.
```hlsl
float2 morphVertex(float2 gridPos, float2 vertex, float morphK) {
    float2 fracPart = frac(gridPos.xy * g_gridDim.xy * 0.5) * 2.0 / g_gridDim.xy;
    return vertex.xy - fracPart * g_quadScale.xy * morphK;
}
```

## Gotchas
- Skipping the morph or transition blend leaves gaps or T-junction cracks between levels.
- The clipmap PDF at the cited URL is the 2004 submission draft; confirm details in the final paper.

## Verify
- [ ] Wireframe flight at speed: no popping or cracks, screen-space triangle density roughly constant.

## Checked

Method: docs-checked 2026-11-09 against the geometry clipmaps PDF (overview, regions, update, and rendering and transition sections read) and the CDLOD paper (selection, LOD ranges and morph sections read). Dropped the NVIDIA GPU Gems chapter and mikejsavage page (not read), heightmap format, splat-map texturing, float precision, physics and 10 km claims, and the skirts remark.
