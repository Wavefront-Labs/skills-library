---
id: creative-arts.animation.blender.pose-asset-creation
name: pose-asset-creation
category: creative-arts
field: animation
product: blender
tags: [blender, pose-library, pose-asset-creation, create-pose-asset, pose-asset-thumbnails, pose-thumbnail, asset-shelf, pose-assets]
level: practitioner
status: docs-checked
description: "Create pose assets in Blender: Create Pose Asset from selected bones, library and catalog choice, modifying assets, scene-camera thumbnails (Workbench) and naming."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/posing/editing/pose_library.html
  - https://docs.blender.org/manual/en/5.2/editors/asset_browser.html
  - https://docs.blender.org/api/current/bpy.ops.poselib.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# pose-asset-creation

Goal: a reusable library of hand shapes, mouth shapes and full-body poses. Applying/blending is in `pose-blend-paste-flipped`; broader library workflow in `pose-library`.

## What a pose asset is

An action marked as an asset that contains exactly one frame of animation data; each pose is its own action data-block with its own name, preview and catalog. The pose library works in Pose Mode only and is implemented by an add-on that is enabled by default (disabling it removes the pose library UI).

## Creating

1. Pose Mode, pose the character (animated or not), **select only the bones that belong to the pose** (a hand pose is the finger bones only, so applying it leaves the arm alone).
2. **Create Pose Asset** (Pose menu in the 3D Viewport, or the button in the Action Editor). Options include the pose name, the **Library** (Current File or another asset library) and the **Catalog**. Python: `bpy.ops.poselib.create_pose_asset(pose_name, asset_library_reference, catalog_path)`.
3. The action contains keys for the current location, rotation, scale and Bendy Bone properties of the selected bones.
4. Current File: the action is created in the open file and marked as an asset (rename it in the Asset Browser). Another library: the pose is extracted into a new `.asset.blend` file holding just that asset, which cannot be opened as a normal blend file to modify it.
5. Bones from several armatures in Pose Mode produce one action with a slot per armature. For generic poses use single-slot actions so the first slot is always used.

## Modifying (right-click a pose asset; current file or `.asset.blend` only)

Modes: **Adjust Pose** (update existing channels only), **Replace** (all channels), **Add** (add or update channels of the selected bones), **Remove**. It works on the active object only.

## Thumbnails

- Previews are rendered with the active **scene camera** using the **Workbench** engine; switch the scene to Workbench to see the look options (MatCap, lighting; settings can be animated).
- Select a pose asset and press **Generate Preview** to re-render. Pose library files are meant to hold poses and the camera and character used for previews.
- Use one camera framing for a whole set (for example all hand poses) so the shelf reads consistently.

## Organisation

- Catalogs such as `Character/Hands`, `Character/Mouth`, `Character/Body`.
- Names with a side, for example `hand_fist.L`; Apply Pose Flipped mirrors left and right, so one side is enough.
- The Asset Browser sidebar has optional Description and Author fields.

## Gotchas

- To copy a pose from another file, use Copy Pose as Asset (Action Editor), open the target library with Open Blend File, then Paste as New Asset.
- Poses in the current file are only available in that file unless it sits in an asset library.

## Verify

In a new file with the character linked, the asset shelf shows the catalog; applying a hand pose moves only the finger bones.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release source) and Python API reference: pose asset definition, Create Pose Asset locations and options, `.asset.blend` behaviour, multi-armature slots, Modify modes, Workbench scene-camera previews and Generate Preview, Copy Pose as Asset workflow, `create_pose_asset` signature. Corrected: thumbnails use the scene camera, not the viewport; custom properties are not listed as stored. Removed as unconfirmed: Load Custom Preview, Overlays advice, 4.2 version gate, bone-rename breakage, tags field.
Method: documentation only; no commands were run.
