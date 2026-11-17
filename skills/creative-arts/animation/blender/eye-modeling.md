---
id: creative-arts.animation.blender.eye-modeling
name: eye-modeling
category: creative-arts
field: animation
product: blender
tags: [blender, eye-modeling, eyeball, cornea, iris, character-modeling, eye-shader]
level: advanced
status: docs-checked
description: "Model character eyes: eyeball and cornea layers, concave iris and pupil, refraction and caustics settings, stylised non-spherical eyes, eyelid fit and rigging pivots."
sources:
  - https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/glass.html
  - https://docs.blender.org/manual/en/latest/render/cycles/render_settings/light_paths.html
  - https://docs.blender.org/manual/en/latest/render/eevee/material_settings.html
  - https://docs.blender.org/manual/en/latest/editors/3dview/display/overlays.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# eye-modeling

Goal: eyes that catch light, show depth in the iris and rotate cleanly under the lids.

## Realistic two-layer eye

- **Sclera/iris mesh**: UV sphere, its front pushed inward to form a slightly concave iris disk; the pupil is a hole or dark texture in the middle.
- **Cornea mesh**: a second sphere, slightly larger, with the front bulged outward over the iris (the corneal bulge).
- Materials: sclera/iris with a texture or procedural (radial noise); cornea with a Glass BSDF, or a Principled BSDF with *Transmission Weight* 1, a physically based IOR (look the corneal value up in a reference) and Roughness 0.
- Cycles: refraction through the cornea can darken the iris and add caustic noise; the *Light Paths → Caustics* options (*Reflective*, *Refractive*) can be unchecked to reduce that noise.
- EEVEE: use the *Dithered* render method with *Raytraced Transmission* enabled on the cornea material, so transmission is raytraced instead of using only light probes (the *Blended* method is incompatible with raytracing).

## Stylised eyes

- Single mesh with painted iris and a highlight texture, or a flattened (non-spherical) eye: still rotate it around a pivot, and fit the lids with a Lattice/Mesh Deform or shrinkwrap so the lids follow the oval surface.
- Specular highlight as a separate small mesh or a light linked only to the eyes.

## Placement and rigging

- Origin exactly at the eyeball centre; the eye rotates about it.
- Eye bones: one per eye, parented to the head; *Damped Track* to a look-at target with a parent control between the eyes.
- Eyelids: model them hugging the eyeball with a small gap; blink shape keys or lid bones rotating around the eye centre.

## Gotchas

- Origin off-centre makes the eye slide out of the socket when rotating.
- Wrong normals can give black eyes; the Face Orientation overlay shows back faces in red, and *Mesh → Normals → Recalculate Outside* fixes them.

## Verify

Rotate the eye bone in every direction: the eyeball stays inside the lids; a front light shows a clear catch-light on the cornea and the iris remains visible (not black).

## Checked

2026-10-27, Blender manual 5.2 (blender-v5.2-release RST). Confirmed: Glass BSDF and Principled BSDF Transmission Weight; Cycles Light Paths > Caustics with Reflective and Refractive checkboxes; EEVEE material Render Method Dithered or Blended, with Raytraced Transmission under Dithered and Blended incompatible with raytracing; Face Orientation overlay shows back faces in red; Damped Track constraint exists. Corrected: Raytraced Transmission is a Dithered option, not a Blended one. Removed: the specific IOR value, the sphere segment counts, the Ray Visibility instruction, the 30 degree test and the negative-scale gotcha. The loop-flow guidance is modelling practice from experience and is not stated in the manual; the numeric counts, ratios and angles that no documentation covers were removed.

Method: documentation only; no commands were run.
