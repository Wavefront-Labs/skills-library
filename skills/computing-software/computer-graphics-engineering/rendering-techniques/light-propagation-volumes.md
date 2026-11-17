---
id: computing-software.computer-graphics-engineering.rendering-techniques.light-propagation-volumes
name: light-propagation-volumes
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, light-propagation-volumes, lpv, reflective-shadow-maps, spherical-harmonics, cryengine]
level: advanced
status: docs-checked
description: "Implement light propagation volumes as in CryEngine 3: RSM point cloud injection into SH volumes, iterative propagation, nested cascades, bleeding fixes."
sources: ["https://advances.realtimerendering.com/s2009/Light_Propagation_Volumes.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Light propagation volumes (LPV)

Source: the Crytek chapter on light propagation volumes in CryEngine 3 (Kaplanyan and
Dachsbacher technique): fully dynamic diffuse global illumination with no precomputation, using
spherical harmonics (SH) radiance volumes.

## 1. Algorithm (four parts)
1. **Radiance point set from a reflective shadow map (RSM)**: render the scene into an RSM using
   the classical layout; its texels are the secondary light sources (virtual point lights). The
   chapter reduces their number with an intensity-aware clustering importance down-sampling filter.
2. **Injection**: each VPL is projected into 2-band SH (four coefficients) and added into the
   closest cell of a volume texture, by point-based rendering of surfels (just an additive
   accumulation, since RSM texels are much smaller than a grid cell). The chapter's computations
   are for a directional light like the sun; other light types are similar with care for the
   perspective transform. Only RSM generation and injection repeat per primary light, injecting
   into the same shared volume.
3. **Propagation**: several sequential iterations, each one discrete step of light propagation
   in grid space. Each cell is treated as a cube; directional energy passes between adjacent
   faces to neighbouring cells, with results accumulated into the radiance volume.
4. **Scene lighting**: the final volume is sampled with the world-space position of each pixel,
   as in a forward renderer, or (as CryEngine 3 does, because of its deferred lighting) rendered
   as a deferred volume primitive into the diffuse light accumulation buffer. Irradiance for a
   diffuse surface is obtained by integrating a cosine lobe in the SH basis in the shader.
   Hardware rendering into volume textures greatly improves performance (hardware trilinear).

## 2. Cascades
Hierarchical cascaded LPVs are nested inside each other (unlike cascaded shadow maps, the
solution around the camera is preserved), giving higher resolution near the viewer. Radiance is
injected into the appropriate finer grid in overlapping regions, propagation runs on all grids
independently, and rendering adds the contributions of all grids. A separate RSM is rendered for
each cascade, allowing control of which objects are injected where.

## 3. Problems and fixes named in the chapter
- Trilinear sampling of the sparse SH grid causes light bleeding through thin double-sided
  geometry and self-illumination. Shift each VPL's injection by up to half a cell toward the
  surface normal and the light direction; this alone is not enough.
- Anisotropic upsampling of the volume is used for rendering. Alternatives discussed: a
  larger shift (rejected: shifts the whole distribution), adding "antiradiance" from back faces
  at injection (rejected: needs the RSM rendered twice), and others.
- 2-band SH is low frequency, and the grid approximation limits spatial locality.
- Secondary occlusion is not handled during propagation; CryEngine used screen-space ambient
  occlusion for it.

## Gotchas
- Volumes in the chapter were 32 x 32 x 32 texels; check the dimensions your scene needs.

## Verify
- [ ] Coloured bounce visible from a lit red wall; no light through thin double-sided geometry.
- [ ] Stable as the light moves.

## Checked

Method: docs-checked 2026-11-09 against the Crytek LPV chapter PDF (overview, RSM, injection, propagation, rendering, shifting and anisotropic upsampling, cascades, results sections read; the appendices and full propagation maths were not read). Dropped the geometry volume step, the 8-16 iteration count, the 3 x 32^3 cascade size, the SH evaluation in direction -N, the damping advice, CryEngine/UE4 history remarks and the other two sources (not read).
