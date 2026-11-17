---
id: creative-arts.animation.blender.vr180-360-render
name: vr180-360-render
category: creative-arts
field: animation
product: blender
tags: [blender, stereoscopy, vr-render, equirectangular, vr180-360, vr180, 360-render, panoramic-camera]
level: practitioner
status: docs-checked
description: "Render 360 and VR180 in Cycles: panoramic equirectangular camera, latitude and longitude limits, spherical stereo with pole merge, cubemap alternative and spatial metadata."
sources:
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/cameras.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/stereoscopy/usage.html
  - https://docs.blender.org/manual/en/latest/render/cameras.html
  - https://github.com/google/spatial-media
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# vr180-360-render

Goal: immersive 360 or VR180 renders that players can interpret correctly.

## Camera (Cycles only)

The **Panoramic** camera type is marked Cycles Only. Panoramic cameras do not display in non-rendered viewport modes such as Solid; they only work in the final render (and Rendered view). Camera Data > Type **Panoramic** > Panorama Type **Equirectangular**:
- **Latitude Min/Max** and **Longitude Min/Max** limit the vertical and horizontal field of view. A full 360 uses the full range; VR180 keeps the front hemisphere, longitude -90 to 90 degrees (the Python API stores these in radians).
- Equirectangular matches the environment texture mapping, so it can render an environment map. For the default mapping, rotate the camera object to (90, 0, -90).
- **Equiangular Cubemap Face** has a more uniform pixel distribution (the manual recommends it for virtual reality) but no latitude or longitude limits.
- Other panorama types: Fisheye Equisolid, Fisheye Equidistant (suited to full-dome projection), Fisheye Lens Polynomial, Mirror Ball.
- Aspect ratio: use 2:1 for a full equirectangular frame and 1:1 per eye for a 180 degree hemisphere (arithmetic of the angle ranges).

## Stereo

Enable Stereoscopy (Stereo 3D) and, on the camera, Stereoscopy > **Spherical Stereo**: each pixel is rendered by rotating the camera around the middle of the interocular distance. **Use Pole Merge** fades the interocular distance to 0 between the Pole Merge Start Angle and End Angle, avoiding eye strain at the poles. Output layout comes from Views Format (Top-Bottom or Side-by-Side among others).

## Metadata

Players need spatial metadata to recognise 360 or stereo layouts. Google's spatial-media repository ("Specifications and tools for 360 video and spatial audio") provides a metadata injector; check which tool your target platform requires.

## Practice notes

- Camera at a plausible eye height, level and moving slowly; fast moves or roll risk motion sickness.
- Equirectangular renders see every direction, so expect long render times.
- Screen-space compositor effects (glare, vignette, lens distortion) do not wrap around the seam.

## Verify

Play the encoded file in a 360 or VR player: no visible seam at the back, correct up direction, comfortable depth.

## Checked

Checked 2026-10-27 against the Blender 5.2 manual (blender-v5.2-release): render/cycles/object_settings/cameras.rst (panoramic types, latitude/longitude, cubemap, rotation for default mapping, viewport limitation), render/cameras.rst (Panoramic is Cycles Only), stereoscopy/usage.rst (Spherical Stereo, Use Pole Merge); github.com/google/spatial-media description via the GitHub API. Removed: specific resolutions, eye-height figure, EEVEE statement, YouTube claim. Method: documentation only; no commands were run.
