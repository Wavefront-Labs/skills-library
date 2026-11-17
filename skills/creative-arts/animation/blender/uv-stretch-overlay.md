---
id: creative-arts.animation.blender.uv-stretch-overlay
name: uv-stretch-overlay
category: creative-arts
field: animation
product: blender
tags: [blender, uv, uv-editor, uv-stretch-overlay, minimize-stretch, uv-stretch, distortion, checker-texture]
level: practitioner
status: docs-checked
description: "Measure and reduce UV distortion in Blender: Display Stretch (Angle/Area), unwrap methods, Minimize Stretch, Average Island Scale, UV Grid test image and Correct Aspect."
sources:
  - https://docs.blender.org/manual/en/latest/modeling/meshes/editing/uv.html
  - https://docs.blender.org/manual/en/latest/editors/uv/overlays.html
  - https://docs.blender.org/manual/en/latest/modeling/meshes/uv/applying_image.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# uv-stretch-overlay

Goal: UVs where a texel covers about the same surface area everywhere and squares stay square.

## Display stretch

- UV Editor > Overlays popover > UV Stretch > **Display Stretch**: compares the UV mapping to the 3D mesh; blue is little distortion, red is high. **Display Stretch Type**: *Angle* (compares face angles: shape distortion) or *Area* (compares face areas: scale differences). *Opacity* adjusts the overlay.
- 3D check: in the Image editor header press New and set *Generated Type* to UV Grid (the built-in test image), apply it to the material, and look for even squares.

## Reducing stretch

- **Unwrap method** (redo panel after `U` > Unwrap): *Angle Based* (ABF, a good 2D representation), *Conformal* (LSCM, usually less accurate than Angle Based but better on simpler objects), *Minimum Stretch* (SLIM, minimises distortion of both areas and angles; extra options *Iterations*, *No Flip*, *Importance Weights* with a vertex group and weight factor).
- Other unwrap options: *Fill Holes*, *Use Subdivision Surface*, *Original Bounds*, *Correct Aspect* (needs a material with a selected Image Texture node), *Margin Method* (Scaled, Add, Fraction) and *Margin*.
- **Minimize Stretch** (UV > Minimize Stretch): minimises the difference between angles in 3D and UV space; options *Fill Holes*, *Blend* (0 is fully minimised, 1 keeps the original UVs) and *Iterations* (more is smoother but slower). Similar to the Relax tool with the Geometry method.
- Add seams where stretch concentrates.
- **Average Island Scale** (UV > Average Island Scale): scales islands to roughly the same scale; *Non-Uniform* scales U and V independently, *Shear* shears the U axis to reduce shearing.
- Pack Islands afterwards to use the texture space.

## Gotchas

- Distortion is sometimes intentional: enlarge hero areas on purpose and accept red there.
- Non-square textures: enable Correct Aspect, otherwise results look stretched even when the UVs are right.

## Verify

Stretch overlay mostly blue; the UV Grid squares look even across the model.

## Checked

Date: 2026-10-27. Documentation release: Blender 5.2 manual (blender-v5.2-release branch, projects.blender.org/blender/blender-manual). Confirmed against the UV Operators, UV Overlays and Applying Images to UVs pages: overlay names and colours, Display Stretch Type, unwrap methods and options, Minimize Stretch options, Average Island Scale options, the generated UV Grid. Removed the unconfirmed Ctrl V and Ctrl A shortcuts, the 4.3+ version gate, 'default' label for Angle Based and the apply-scale claim.
Method: documentation only; no commands were run.
