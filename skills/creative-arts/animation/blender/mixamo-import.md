---
id: creative-arts.animation.blender.mixamo-import
name: mixamo-import
category: creative-arts
field: animation
product: blender
tags: [blender, motion-capture, mixamo-import, mixamo, rokoko, fbx-import, mocap]
level: practitioner
status: gated
description: "Bring Mixamo and Rokoko animation into Blender: FBX import settings (automatic bone orientation, scale), fixing the 100x armature, combining clips as actions, and retargeting to your rig."
sources:
  - https://helpx.adobe.com/creative-cloud/help/mixamo-rigging-animation.html
  - https://support.rokoko.com/hc/en-us
  - https://docs.blender.org/manual/en/latest/files/import_export/fbx.html
  - https://docs.blender.org/manual/en/latest/files/import_export/fbx_legacy.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# mixamo-import

## Mixamo download settings

- Format **FBX Binary**, Skin **With Skin** for the first clip (mesh + rig), **Without Skin** for additional clips, Frames per Second 30 (or your scene fps), Keyframe Reduction none, and the **In Place** checkbox for locomotion clips you will drive with root motion in-engine (gated: unconfirmed, source is paywalled or blocked).

## Import into Blender

- File > Import > FBX (.fbx) uses the native importer. Its options are **Scale**, custom properties, **Ignore Leaf Bones** (ignores the last bone of each chain, which only marks the previous bone's length), **Import Animation** and **Animation Offset**. It has no Automatic Bone Orientation or Bone Axis options: those exist only in the deprecated **FBX (.fbx) (Legacy)** importer, where Automatic Bone Orientation tries to align the major bone axis with the bone's children.
- Each FBX take is imported as a separate Action, with each animated object assigned its own Action Slot (importer note in the manual).
- Mixamo armatures import with object scale 0.01 and bones in cm (gated: unconfirmed, source is paywalled or blocked): if so, Ctrl A > Apply Scale on the armature *and* child mesh, or keep the 0.01 object scale consistently. Check the animation after applying scale (practice).
- Each Without-Skin import brings a new armature with an action named `Armature|mixamo.com|Layer0` (gated: unconfirmed, source is paywalled or blocked). Rename the action (`Mixamo_Run`), give it a fake user, delete the imported armature, and assign the action to the first armature (same bone names `mixamorig:...` (gated: unconfirmed, source is paywalled or blocked)).

## Rokoko

- Rokoko Studio exports FBX/BVH; the **Rokoko Studio Live** Blender add-on streams live and includes a retargeting panel (source/target bone list with auto-detection) (gated: unconfirmed, source is paywalled or blocked).
- Rokoko Studio can also retarget to a Mixamo/Unreal skeleton before export (gated: unconfirmed, source is paywalled or blocked).

## Retarget to your rig

Mixamo's skeleton names are consistent — make one bone map for `mixamorig:` → your controls and reuse it (see `bone-mapping-retarget`), or use retarget add-ons.

## Gotchas

- Mixed fps between clips → speed differences; download all at the scene fps (the scene frame rate is set under Output Properties > Format).
- Fingers missing on some characters (Mixamo "skeleton LOD") — choose the full skeleton when uploading (gated: unconfirmed, source is paywalled or blocked).
- Root motion on `mixamorig:Hips` (no separate root bone) (gated: unconfirmed, source is paywalled or blocked) — engines may need a root added (see `root-motion`).

## Verify

All clips assigned in the Action Editor play on one armature at correct scale; foot contacts stay on the ground.

## Checked

2026-10-27. Documentation release: Blender manual 5.2 (branch blender-v5.2-release) plus the bpy.ops.wm.fbx_import signature in the Python API reference and the FBX add-on source. Confirmed: the native FBX importer options (Scale, custom properties, Ignore Leaf Bones, Import Animation, Animation Offset), takes imported as Actions with Action Slots (files/import_export/fbx.rst), and that Automatic Bone Orientation and Bone Axis belong to the deprecated Legacy importer (fbx_legacy.rst and io_scene_fbx __init__.py). Wrong in the old text: the main import now has no Automatic Bone Orientation option, and the claim that Apply Properties makes animation scale is unsupported and was removed. The Mixamo and Rokoko behaviour claims are marked gated because the Adobe and Rokoko help pages answered HTTP 403 to a read-only fetch and could not be checked.

Method: documentation only; no commands were run.
