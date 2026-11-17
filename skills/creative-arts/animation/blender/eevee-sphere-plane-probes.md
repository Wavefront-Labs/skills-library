---
id: creative-arts.animation.blender.eevee-sphere-plane-probes
name: eevee-sphere-plane-probes
category: creative-arts
field: animation
product: blender
tags: [blender, eevee, light-probes, eevee-sphere-probe, sphere-probe, plane-probe, reflections]
level: practitioner
status: docs-checked
description: "Use EEVEE sphere and plane light probes for reflections: influence, falloff, clipping, custom parallax, resolution, plane probe limits and cost."
sources:
  - https://docs.blender.org/manual/en/latest/render/eevee/light_probes/sphere.html
  - https://docs.blender.org/manual/en/latest/render/eevee/light_probes/plane.html
  - https://docs.blender.org/manual/en/latest/render/eevee/limitations/limitations.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eevee-sphere-plane-probes

Goal: correct local reflections in EEVEE where screen-space rays fail.

## Sphere probe

A light probe sphere records the light incoming from many directions at a single location. It is used for smooth and semi-rough reflections, blends smoothly to light probe volume lighting for fully diffuse reflections, and is the fallback when a ray misses with Raytracing on. Sphere probes are shadowed by light probe volumes, to reduce light leaking.

Object Data > Probe:
- **Type**: Sphere or Box influence volume. **Radius / Size**: a probe only influences nearby surfaces; the zone is set by this size and object scaling. **Falloff**: percentage of the influence distance in which the influence fades linearly.
- **Capture > Clipping Start / End**: near and far clip distances for the capture. In the viewport the capture only happens when the probe data or position changes; in renders it happens at the start of each frame.
- **Custom Parallax**: by default the influence volume is also the parallax volume (the volume the recorded light is projected onto, which should roughly fit the surroundings). Enable Custom Parallax to change its shape and radius independently.
- **Resolution** of all sphere probes is set in the scene's Light Probes settings (Light Probe Spheres Resolution). The world has its own internal sphere probe with a resolution in World settings (see eevee-world-sun-extraction).
- Viewport Display: Data, Clipping, Influence and Parallax overlays.

## Plane probe

A light probe plane records the light for all visible points on a plane, in the specular reflection direction only. It suits smooth planar surfaces (mirrors, water, polished floors).

- Each visible plane probe increases render time, because the scene is rendered for each one.
- Plane probes only work when the raytracing method is Screen-Trace; they accelerate tracing and fill in the data missing from screen-space tracing.
- Reflections and volumetrics are not supported inside plane probes.
- **Distance**: influence distance from the plane; only surfaces whose normals align with the reflection plane receive the reflection. **Parallax**: affects reflections on Blended materials and Shader to RGB evaluation. **Clipping Offset**: how far below the plane the near clip sits when capturing; increasing it can fix reflection contact problems.
- Placement: without Backface Culling, snapping the probe onto the surface captures the underside; move it slightly above the surface or disable its visibility in the object visibility panel.

## Limits

EEVEE supports up to 128 active sphere probes and up to 16 active plane probes inside the view frustum.

## Verify

View the floor from the camera angle. Reflections of walls should line up with the real walls (adjust Custom Parallax), and the mirror should show what is missing from the screen-space result.

## Checked

Date: 2026-10-27. Documentation: Blender 5.2 manual (EEVEE Light Probe Sphere, Light Probe Plane, Limitations). Confirmed: properties listed, Screen-Trace requirement and cost for planes, probe count limits. Wrong claims fixed: plane probes only work with Screen-Trace and do not support reflections or volumetrics inside them; the per-scene resolution setting is "Light Probe Spheres Resolution". Removed unconfirmed: which-surface-to-use table, "at most a few per shot", overlapping-probe blending note.
Method: documentation only; no commands were run.
