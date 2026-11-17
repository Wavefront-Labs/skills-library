---
id: computing-software.computer-graphics-engineering.computer-vision.texturing-reconstructed-meshes
name: texturing-reconstructed-meshes
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, reconstruction-3d, mesh-texturing, photogrammetry, texture-atlas, openmvs, mvs-texturing]
level: advanced
status: draft
description: "Texture photogrammetry/MVS meshes from source photos: view selection, seam levelling, UV atlas generation, OpenMVS TextureMesh and mvs-texturing, and colour consistency fixes."
sources: ["https://github.com/nmoehrle/mvs-texturing", "https://github.com/cdcseacave/openMVS", "https://doi.org/10.1007/978-3-319-10602-1_54"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Texturing reconstructed meshes

## Approach (Waechter et al. "Let there be colour")
1. **View selection** per face: pick the image that sees the face most frontally, close and sharp,
   with a smoothness term so neighbouring faces prefer the same view (graph-cut/MRF labelling).
   Photo-consistency check rejects views with occluders (people, cars).
2. **Global seam levelling**: per-vertex colour adjustments so patches from different images meet
   without visible steps.
3. **Local seam levelling**: Poisson editing along seams.
4. **Atlas packing**: charts packed into texture pages, then baked.

## Tools
```bash
# mvs-texturing
texrecon ./scene::undistorted mesh.ply textured --keep_unseen_faces
# OpenMVS (after DensifyPointCloud / ReconstructMesh / RefineMesh)
TextureMesh scene_dense_mesh_refine.mvs --export-type obj --resolution-level 0 --cost-smoothness-ratio 0.1
```
Inputs: **undistorted** images with exact intrinsics/extrinsics matching the mesh frame (from COLMAP
`image_undistorter`).

## Practice
- Decimate/clean the mesh first (remove floaters, fill small holes): texturing amplifies geometry
  errors as smeared textures.
- Capture with locked exposure/white balance; otherwise seam levelling can only partially hide jumps.
- Remove shadows/highlights where possible (overcast light, cross-polarisation) for relightable assets.
- Texture size: choose resolution so texel density roughly matches source image pixel density;
  multiple 8k pages for large scenes.

## Alternatives
For game assets, retopologise and UV unwrap a low-poly mesh, then bake colour from the high-poly
textured mesh (normal map + albedo) in Blender/Substance.

## Verify
Render textured mesh from held-out camera poses and compare against the real photos (PSNR, visual
seams and ghosting).
