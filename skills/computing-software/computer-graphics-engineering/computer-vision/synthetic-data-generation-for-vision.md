---
id: computing-software.computer-graphics-engineering.computer-vision.synthetic-data-generation-for-vision
name: synthetic-data-generation-for-vision
category: computing-software
field: computer-graphics-engineering
product: computer-vision
tags: [computer-graphics-engineering, computer-vision, cv-data-evaluation, synthetic-data, domain-randomization, blenderproc, sim-to-real, data-generation]
level: advanced
status: draft
description: "Generate synthetic training data for vision: BlenderProc/Replicator pipelines, domain randomisation, physically based rendering, automatic labels, and closing the sim-to-real gap."
sources: ["https://github.com/DLR-RM/BlenderProc", "https://docs.omniverse.nvidia.com/extensions/latest/ext_replicator.html", "https://arxiv.org/abs/1703.06907"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Synthetic data generation

## When it helps
Rare events, dangerous scenarios, expensive labels (6D pose, depth, dense masks, keypoints), new
products with CAD models but no photos.

## Pipeline (BlenderProc)
```python
import blenderproc as bproc
bproc.init()
objs = bproc.loader.load_obj("part.obj")
light = bproc.types.Light(); light.set_type("POINT")
for i in range(N):
    for o in objs: o.set_location(np.random.uniform([-0.2,-0.2,0],[0.2,0.2,0.3])); o.set_rotation_euler(bproc.sampler.uniformSO3())
    light.set_location(bproc.sampler.shell(center=[0,0,0], radius_min=1, radius_max=2, elevation_min=10, elevation_max=89))
    light.set_energy(np.random.uniform(100, 1000))
    cam = bproc.math.build_transformation_mat(bproc.sampler.sphere([0,0,0], 1.0, "SURFACE"), [0,0,0])
    bproc.camera.add_camera_pose(cam)
bproc.renderer.enable_segmentation_output(map_by=["instance", "class"])
data = bproc.renderer.render()
bproc.writer.write_coco_annotations("out", instance_segmaps=data["instance_segmaps"], colors=data["colors"])
```
NVIDIA Omniverse Replicator, Unity Perception and Kubric are alternatives.

## Domain randomisation
Randomise textures, lighting, backgrounds (real photos as backgrounds work well), camera intrinsics
and pose, distractor objects, occlusion, noise and blur. Goal: reality looks like one more variation.

## Photorealism
Path-traced rendering with PBR materials, realistic camera effects (lens distortion, motion blur,
sensor noise, JPEG) narrows the gap; mismatched intrinsics/FOV are a common silent failure.

## Mixing with real data
Pretrain on synthetic and fine-tune on a small real set, or mix (e.g. 10 to 20 percent real). Always
evaluate on **real** held-out data only.

## Gotchas
- Labels from renders are perfect, including truncated/occluded objects that humans would not label:
  match labelling conventions (visibility thresholds).
- Diversity beats volume: 10k varied images often beat 1M similar ones.

## Verify
Train real-only, synthetic-only and mixed models; compare on the real test set by slice.
