---
id: creative-arts.animation.blender.multi-view-exr
name: multi-view-exr
category: creative-arts
field: animation
product: blender
tags: [blender, stereoscopy, multi-view, multi-view-exr, view-suffix, openexr]
level: practitioner
status: docs-checked
description: "Render multi-view setups: Multi-View mode with camera suffixes, individual files or multi-view OpenEXR output, the compositor Switch View node, and Image Editor checks."
sources:
  - https://docs.blender.org/manual/en/latest/render/output/properties/stereoscopy/usage.html
  - https://docs.blender.org/manual/en/latest/render/output/properties/output.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---
# multi-view-exr

Goal: render several views (stereo eyes or a camera array) in one pass and keep them together.

## Multi-View mode

Output Properties > **Stereoscopy** (enable the panel's checkbox), then choose **Multi-View** instead of Stereo 3D. The manual's description of the property: a multi-camera system where you adjust the cameras individually. Add and remove views with the + and - buttons; each view has a **Camera Suffix**, which identifies the cameras to use and is also added to the output file names for that view.

Name the scene cameras to match the suffixes (the suffix is matched against camera names), often parented to a rig.

## Output

- **Individual** (the default): each view saved as a separate file, so there are as many files as views.
- **Multi-View** with an OpenEXR Multilayer format: all views in a single file. The manual says multi-view OpenEXR is backward compatible with old OpenEXR viewers (you see only one view) and that native multi-view support exists only for OpenEXR.
- In the compositor, compositing of a view finishes before the next view starts. The **Switch View** node lets you treat the views separately before an output node. The scene's views define which views are rendered.

## Gotchas

- Render time and memory scale with the number of views, since every view is rendered. When rendering from the UI all views are rendered and then composited.
- Adaptive subdivision can have inconsistencies between views (manual limitation of the Subdivision Surface modifier).
- Viewing in Blender: the Image Editor has a View menu to inspect individual views of Viewer nodes, render results or opened images.

## Verify

Render a frame, open it in the Image Editor and switch between views: each named view should appear and differ by camera position. For a multi-view EXR, reload it in Blender with Use Multi-View on.

## Checked

Date 2026-10-27. Blender manual 5.2 (blender-v5.2-release RST) and Blender source (properties_output.py, rna_scene.cc on main).
Confirmed: Stereoscopy panel with Stereo 3D / Multi-View mode and Camera Suffix property; Individual default output; Multi-View file option for multilayer EXR; multi-view EXR statements; Switch View node; Image Editor view inspection.
Removed as unconfirmed: the exact `<camera><suffix>` naming rule and the "missing camera renders from active camera" fallback, claims about Nuke and `oiiotool`, and the OpenEXR standard link that was not opened.
Method: documentation only; no commands were run.
