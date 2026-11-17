---
id: computing-software.computer-graphics-engineering.rendering-techniques.voxel-cone-tracing-gi
name: voxel-cone-tracing-gi
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, global-illumination, voxel-cone-tracing, vxgi, voxelization, conservative-rasterization, 3d-textures]
level: advanced
status: draft
description: "Implement voxel cone tracing GI: conservative voxelisation, radiance injection, anisotropic mips, diffuse and specular cone tracing, and its leaking and memory limits."
sources: ["https://research.nvidia.com/publication/2011-09_interactive-indirect-illumination-using-voxel-cone-tracing", "https://developer.nvidia.com/gpugems/gpugems2/part-v-image-oriented-computing/chapter-42-conservative-rasterization", "https://github.com/Friduric/voxel-cone-tracing"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Voxel cone tracing (VXGI / SVOGI)

Crassin et al. 2011. Represents the scene as a mipmapped voxel volume of radiance and occlusion,
then approximates hemisphere integration with a few cones that sample increasingly coarse mips.

## 1. Voxelisation
- Render scene geometry into a 3D texture (e.g. 128^3-256^3, or a clipmap around the camera).
- Per triangle, project along its dominant axis (geometry shader chooses X/Y/Z) to maximise
  rasterised area; enable **conservative rasterisation** so thin triangles don't skip voxels.
- Fragment shader writes albedo, normal, emission to 3D textures with `imageStore` (average with
  atomics when multiple fragments hit one voxel: `imageAtomicCompSwap` running average or
  `r32ui`-packed RGBA8).

## 2. Light injection
For each voxel: compute direct lighting (sample the shadow map) times albedo plus emission ->
radiance volume. Optionally a second bounce by cone tracing from voxels.

## 3. Mip filtering
Generate mips of the radiance/opacity volume. **Anisotropic** voxels (6 directional values per
voxel, one per face direction) reduce light leaking through thin walls at coarse mips; costs 6x
memory for mips.

## 4. Cone tracing
```glsl
vec4 coneTrace(vec3 origin, vec3 dir, float aperture) {   // aperture = tan(half-angle)
    vec4 acc = vec4(0); float dist = voxelSize;            // start offset avoids self-sampling
    while (acc.a < 0.95 && dist < maxDist) {
        float diameter = max(voxelSize, 2.0 * aperture * dist);
        float mip = log2(diameter / voxelSize);
        vec4 s = textureLod(radianceVol, worldToVoxelUVW(origin + dir * dist), mip);
        acc += (1.0 - acc.a) * s;                            // front-to-back compositing
        dist += diameter * 0.5;
    }
    return acc;
}
```
- Diffuse: 5-9 wide cones (~60 degree) around the normal, cosine weighted.
- Specular: one cone along the reflection vector with aperture from roughness.
- AO falls out of accumulated alpha.

## 5. Limits
- Memory: 256^3 RGBA8 = 64 MB per volume before mips/anisotropy; clipmaps or sparse octrees
  (SVO, original paper) reduce it.
- Light leaking through walls thinner than a voxel, especially at coarse mips.
- Revoxelising dynamic objects every frame is costly; static/dynamic split.
Largely superseded by DDGI/probes and ray-traced GI on RT hardware, but still useful without RT.

## Gotchas
- Self-occlusion: offset cone origin along the normal by ~1 voxel.
- Voxel aliasing when the camera moves with a clipmap: snap clipmap origins to voxel size.

## Verify
- [ ] Debug view of voxel radiance matches the lit scene.
- [ ] Indirect bounce from a bright wall appears without obvious leaking into adjacent rooms.
