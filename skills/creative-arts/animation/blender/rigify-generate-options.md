---
id: creative-arts.animation.blender.rigify-generate-options
name: rigify-generate-options
category: creative-arts
field: animation
product: blender
tags: [blender, rigify, rigify-generate-options, rigify-regenerate, rigify-overwrite, rig-update]
level: practitioner
status: docs-checked
description: "Generate and regenerate Rigify rigs safely: Advanced options (Target Rig, Rig UI Script, Widgets Collection, Run Script), overwriting and library linking."
sources:
  - https://docs.blender.org/manual/en/latest/addons/rigify/basics.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# rigify-generate-options

Goal: iterate on the metarig and regenerate without breaking animation or custom additions.

## Generate
Metarig > Armature properties > scroll to the bottom > **Generate Rig**. Generation takes a few seconds to about a minute, and the interface does not update until it finishes. Open the **Advanced** sub-panel for:
- **Rig Name**: names a brand-new rig. If empty, `META` in the metarig name becomes `RIG`, `metarig` becomes `rig`, otherwise `RIG-` is prefixed. Ignored when overwriting.
- **Target Rig** (set automatically): the generated rig to overwrite on regeneration. If unset, Rigify creates a new rig object and stores it here, even if an object with a matching name exists.
- **Rig UI Script** (auto): the generated script datablock to overwrite; it provides the 3D Viewport panels (bone collection visibility, custom properties, IK/FK switching).
- **Widgets Collection** (auto): the collection holding generated widgets.
- **Overwrite Widget Meshes**: regenerate widgets every time; by default existing widget objects are reused so you can edit their shapes.
- **Mirror Widgets**: left and right widgets as linked duplicates with negative X scale; switching an existing character to mirrored widgets requires deleting right-side widgets or using *Force Widget Update*.
- **Run Script**: a text datablock executed after generation with the generated rig active and selected in Object Mode.

## Regenerate workflow
1. Make changes in the metarig, not by hand-editing generated bones.
2. Keep the rig and the metarig both visible, then click Generate Rig again: Rigify overwrites the existing rig, retaining modifiers and constraints and, where possible, previously generated features. Rigify tries to unhide them and aborts if it cannot.
3. Put customisations in a Run Script text. Example: `bpy.data.objects["rig"].pose.bones["MCH-spine.003"].constraints[0].influence = 0.6` (use Copy Full Data Path on the property to get the path).

## Gotchas
- Without a Target Rig, a new rig object is created, and the mesh's Armature modifier still points to the old rig.
- Do not delete the metarig after generating: later Rigify updates are provided for metarigs, not generated rigs.
- Linked rigs: link a collection with the rig and mesh (not the metarig or widgets collection), then Make Library Override. The `rig_ui_template.py` text links automatically but does not run until you run it from the Text Editor or save and restart Blender.
- Legacy face metarigs show *Upgrade Face Rig* above Generate Rig.

## Verify
After regenerating: the Armature modifier target is unchanged, the existing action plays the same, and the Rig Layers panel shows in the Item tab of the 3D Viewport sidebar when a rig bone is active.

## Checked
Date: 2026-10-27. Documentation: Blender manual, Rigify Basic Usage page, branch blender-v5.2-release. Confirmed: Generate Rig button location, all Advanced option names and behaviours, the overwrite and visibility requirements, Run Script behaviour and example, library-linking steps, and the Item tab location of the rig panels. Removed unconfirmed claims (finalize script name, hidden widget collection, info bar error text, bone-rename effects).
Method: documentation only; no commands were run.
