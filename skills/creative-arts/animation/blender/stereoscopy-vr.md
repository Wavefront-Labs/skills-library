---
id: creative-arts.animation.blender.stereoscopy-vr
name: stereoscopy-vr
category: creative-arts
field: animation
product: blender
tags: [blender, stereoscopy, stereo-3d, multi-view, vr-render, equirectangular, panoramic, 360-video, convergence, interocular, anaglyph, side-by-side, top-bottom, omnidirectional-stereo]
level: advanced
status: docs-checked
description: "Blender stereo 3D and 360 output: interocular, convergence, pivot, viewport preview, SBS/top-bottom/anaglyph formats, panoramic cameras."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/stereoscopy/index.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/stereoscopy/usage.html
  - https://docs.blender.org/manual/en/latest/render/cycles/object_settings/cameras.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# stereoscopy-vr

Goal: deliver a left/right pair or a 360 degree panorama that looks right in a headset or on a 3D screen, without rendering twice by hand.

## Stereoscopy setup

- Output Properties: enable *Stereoscopy* for the scene. This gives a 3D preview in the viewport and extra panels across the UI.
- Select the camera, Camera properties, Stereoscopy tab: tweak the stereo parameters; the viewport responds in real time.
- The stereo pair is created on the fly: it behaves as two cameras sharing most parameters (focal length, clipping) but offset, with their own rotation and shift.
- **Interocular Distance**: distance between the camera pair. Convergence can be changed in post, but different interocular distances give different results because different parts of the scene are occluded from each point of view.
- **Convergence Plane Distance**: the converge point of the stereo cameras (often the distance between a projector and the screen). It can be visualised in the 3D Viewport.
- **Convergence mode**: *Off-Axis* (cameras separated by the interocular distance and shifted inwards to converge at the plane; the ideal format, closest to human vision), *Parallel* (two parallel cameras that do not converge, so they must be converged manually and cannot be used for viewing; common when combining real footage with rendered elements), *Toe-in* (rotates the cameras instead of shifting the frustum; rarely used in modern 3D productions).
- **Pivot**: Center builds a new camera for each eye around the active camera; Left or Right uses the existing camera as one eye. The latter suits rendering only one eye for an existing mono project.

## Viewport preview

- 3D Viewport Sidebar, Stereoscopy panel: choose whether to see stereo 3D or which camera to see, and show *Cameras*, *Plane* and *Volume*.
- *Plane* is the convergence plane, i.e. the screen as perceived by the audience; go outside camera view to lay the scene out against your depth script.
- *Volume* is the intersection of the two camera frustums, bounded by the camera's start and end clipping distances. Areas seen by only one camera are retinal rivalry areas: tolerated in negative space (convergence plane into the image), to be avoided in positive space (convergence plane towards the camera).
- A real 3D display mode is set per window from the Window menu (Stereo 3D operator, `wm.set_stereo_3d`). Modes: Anaglyph (red-cyan, green-magenta, yellow-blue), Interlace (Row, Column, Checkerboard, with a Swap Left/Right option), Time Sequential (needs Quad Buffer support, fullscreen only), Side-by-Side (Cross-Eye option, fullscreen only) and Top-Bottom (fullscreen only). Some modes need a fullscreen editor.

## Output and image I/O

- Render Output panel, *Views Format*: individual files per view, or a stereo 3D format (top-bottom, anaglyph and so on). By default each view is saved as an individual file.
- Lossy formats: Anaglyph drops colour channels, squeezed Top-Bottom discards half the vertical resolution, Interlace mangles the data. Lossless options: Individual with PNG or OpenEXR, or Top-Bottom / Side-by-Side without the Squeezed Frame option.
- Multi-view OpenEXR stores several views in one file and stays backward compatible with old OpenEXR viewers (which show only one view). Native multi-view support exists only for OpenEXR.
- Image Editor: the View menu switches between the combined stereo result and individual views (works for Viewer nodes, render results and opened images). A dropped-in stereo-format image opens as individual images first; switch Views Format to Stereo 3D, enable *Use Multi-View* and pick the matching method.
- Compositor: each view is composited completely before the next. An Image node lacking the requested view is treated as single-view. The Switch View node combines the views before an output node. For test iterations, disable all but one view in the Scene Views panel.

## 360 panoramas

Camera Data, Lens Type Panoramic, then Panorama Type. Both Cycles and EEVEE support panoramic cameras; EEVEE has some restrictions (see its Panoramic Camera limitations in the manual).
- **Equirectangular**: renders the scene with an equirectangular projection, compatible with the world Environment Texture. To match the default mapping set the camera object rotation to (90, 0, -90) (pointing along positive X). *Latitude Min/Max* and *Longitude Min/Max* limit the field of view.
- **Central Cylindrical**: projects onto a virtual cylinder around the camera and unwraps it; *Height Min/Max*, *Longitude Min/Max* and *Cylinder Radius* control it. The poles cannot be included.
- **Equiangular Cubemap Face**: more uniform pixel distribution than equirectangular (less loss at the poles), good for VR; it has no longitude or latitude limits.
- **Fisheye Equisolid** best matches real cameras (uses lens focal length, field of view and sensor size); **Fisheye Equidistant** gives a circular fisheye using the whole sensor, good for full-dome. Field of view can go to 360 and more.
- **Fisheye Lens Polynomial**: match a real camera with a 4th degree polynomial; **Mirror Ball**: renders as a photo of a reflective ball.

## Spherical stereo

Camera Stereoscopy settings include *Spherical Stereo* (render every pixel rotating the camera around the middle of the interocular distance) and *Use Pole Merge* (fade the interocular distance to 0 after a cutoff angle), with *Pole Merge Start Angle* (where the fade starts) and *Pole Merge End Angle* (where the distance is 0).

## Verify

- Subject at the convergence distance shows no red/cyan fringe in an anaglyph preview; nearer and farther objects fringe in opposite directions.
- Both views of a rendered side-by-side frame differ only horizontally.

## Checked

2026-11-09. Confirmed against the Blender manual (raw RST of Stereoscopy usage and Cycles Cameras pages): stereoscopy setup, interocular and convergence descriptions, convergence modes, pivot, viewport Cameras/Plane/Volume, window display modes, output format and lossy/lossless notes, multi-view EXR, Image Editor, compositor notes, panorama types and their options, spherical stereo and pole merge. Removed unconfirmed claims: numeric interocular and parallax rules of thumb, file suffix details, Sequencer strip handling, render-time multipliers, resolution and aspect advice, VR180/ODS recipes, VR Scene Inspection, metadata injection, and the old claim that EEVEE has no panoramic camera (the manual says it supports them with restrictions).
Method: documentation only; no commands were run.
