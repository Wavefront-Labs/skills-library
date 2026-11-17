---
id: creative-arts.animation.blender.cycles-path-guiding
name: cycles-path-guiding
category: creative-arts
field: animation
product: blender
tags: [blender, cycles, path-guiding, openpgl, indirect-lighting]
level: practitioner
status: docs-checked
description: "Use Cycles path guiding (Open PGL) to cut noise in hard indirect lighting such as light through a door gap; training samples, surface/volume toggles, CPU-only limit."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/sampling.html
  - https://docs.blender.org/manual/en/latest/render/cycles/gpu_rendering.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# cycles-path-guiding

Goal: reduce noise in scenes where finding a path to a light is difficult for regular path tracing, for example a room lit through a small door opening.

## Settings (Render Properties > Sampling > Path Guiding)

Path guiding learns important light directions over time, improving as more samples are taken.

- Only available when rendering on a CPU. The GPU Rendering page lists it as not supported on any GPU.
- **Training Samples**: maximum samples used for training. 0 keeps training until the end of the render. The manual says 128 to 256 is usually enough for accurate guiding; higher values give minor quality gains with longer render times.
- **Surface**: path guiding for the diffuse and glossy components of surfaces.
- **Volume**: path guiding inside volumes.

## Related

- Light portals (area light Portal option) guide the path tracing manually for interior scenes lit by the environment; the manual cross-links them from the Path Guiding section.
- Path guiding can help with caustics in some scenes but is not designed for complex caustics, which are harder to learn.

## Gotchas

- Compare guided and unguided renders at equal render time rather than equal samples, using Time Limit (see cycles-time-limit).
- Keep guiding settings the same for every frame of a shot.
- A fast GPU without guiding may still beat CPU with guiding; measure both on the target machine.

## Verify

Render the same frame on CPU with guiding on and off at the same time limit, and compare noise in the darkest indirectly lit area.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (Cycles Sampling, GPU Rendering, light settings for portals). Confirmed: CPU-only, GPU not supported, Training Samples meaning and 128 to 256 guidance, Surface/Volume toggles, caustics note. Removed unconfirmed: version gate, default training value, advanced option names, scene-type lists.
Method: documentation only; no commands were run.
