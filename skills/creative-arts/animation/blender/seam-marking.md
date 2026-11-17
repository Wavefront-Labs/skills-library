---
id: creative-arts.animation.blender.seam-marking
name: seam-marking
category: creative-arts
field: animation
product: blender
tags: [blender, uv, seams, seam-marking, mark-seam, seams-from-islands, unwrap]
level: practitioner
status: docs-checked
description: "Mark UV seams in Blender: Ctrl E Mark Seam, shortest-path Tag Seam, Seams from Islands, placement rules for low-distortion unwraps, and Live Unwrap when seams change."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/uv/unwrapping/seams.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/selecting/linked.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/tools/tool_settings.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# seam-marking

Goal: seams that unwrap with low distortion and stay where nobody looks.

## Marking

- Select edges in Edit Mode (`Alt LMB` for edge loops), then `Ctrl E` > **Mark Seam** or **Clear Seam** (Edge > Mark/Clear Seam, also UV > Mark/Clear Seam in the 3D Viewport and in the UV Editor).
- Fast tagging: click the start element, `Ctrl LMB` the destination to select the shortest path (Select > Select Linked > Shortest Path). In its redo panel set **Edge Tag** to *Tag Seam* to mark the path as seams directly. Other options: *Face Stepping*, *Topology Distance*, *Fill Region* (`Shift Ctrl LMB`).
- Check a seam with Select Linked in Face mode: it selects connected faces up to the seam, so unexpected selection means the seam is not continuous. Seams need not be continuous as long as they resolve regions that may stretch.

## Recover seams

UV > **Seams from Islands** (UV Editor) adds seams at the boundaries of existing UV islands; useful when modifying UVs of an already unwrapped mesh.

## Where to place

- Hide seams where they will not be seen; fewer seams mean fewer texturing breaks, more seams mean less stretching.
- Bilateral objects (heads, bodies): seam along the mirror axis so both halves can overlap in one texture space.
- A seam at a hairline limits what unwraps when you select linked faces from the front.
- Think of cutting the object apart to spread it flat with as little tearing as possible; separate sub-meshes unwrap by themselves.
- Projection painting deals with seams more easily than 2D texturing.

## Workflow

Mark seams, unwrap, adjust seams and repeat, then adjust UVs manually. Live Unwrap (Sidebar > Tool > Options > UVs) recomputes the unwrap each time an edge's seam state changes.

## Verify

Unwrap (`U`) and check the UV Editor's Display Stretch overlay: mostly blue, islands as expected.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the Seams, UV Operators, Select Loops and Select Linked pages: Ctrl E menu, Seams from Islands, shortest-path Edge Tag Tag Seam, Live Unwrap, placement guidance. Removed unconfirmed claims about red seam colour, Mark Sharp option, which unwrap methods read seams, and the Mirror modifier note.
Method: documentation only; no commands were run.
