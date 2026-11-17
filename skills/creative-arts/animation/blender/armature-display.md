---
id: creative-arts.animation.blender.armature-display
name: armature-display
category: creative-arts
field: animation
product: blender
tags: [blender, rigging, armature-display, bone-axes, in-front, bone-shapes-display, bone-colors, octahedral, stick]
level: practitioner
status: verified
description: "Make Blender armatures readable: display as Octahedral/Stick/B-Bone/Envelope/Wire, In Front, axes and names, custom shapes toggle, bone colours, and per-bone wire width/hide."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/armatures/properties/display.html
  - https://docs.blender.org/manual/en/5.2/animation/armatures/bones/properties/display.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# armature-display

Goal: a rig animators can read and click easily, and a debug view riggers can trust.

## Armature (Object Data > Viewport Display)

- **Display As**: *Octahedral* (default; shows root and tip, size and roll, suited to most editing), *Stick* (constant thin sticks, no root/tip, size or roll), *B-Bone* (shows curves of multi-segment bones), *Envelope* (deformation influence), *Wire*. Individual bones can override this with their own Display As.
- **Show**: *Names*, *Axes*, *Shapes* (replace the bone shape with a chosen object in Object and Pose Mode), *Bone Colors* (draw bones in their configured colours; off uses the default colour), **In Front** (bones always drawn over solid objects, so visible and selectable; same option as in the Object Data Display panel).

## Per bone (Bone Properties > Viewport Display)

- **Hide**, **Display As** (including Armature Defined), **Bone Color** (stored on the armature data; palette sets or a custom set with regular, selected and active colours) and **Pose Bone Color** (Pose Mode override stored on the pose bone). Bone colours replace the old bone groups (see `bone-collections-management`).
- **Custom Shape**: Custom Object, Translation/Rotation/Scale offsets, **Override Transform**, **Scale to Bone Length** (the 5.2 manual also lists Affect Gizmo and Use As Pivot; Blender 4.5.14 has no such property on Bone or PoseBone), **Wireframe**, **Wire Width**. Custom shapes are never rendered; the template object's own transforms are ignored; the shape's Y axis lies along the bone, and with Scale to Bone Length a template 1 unit long on Y matches the bone.

## Gotchas

- Turn Shapes off in the armature's Viewport Display panel to see the real bones when debugging custom shapes.
- Axes display helps check bone roll on left/right pairs.

## Verify

Animator view: In Front, Stick/Shapes, colours readable; rigging view: Octahedral + Axes show consistent roll on left/right pairs.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Armature and Bone Viewport Display pages: Display As types and the Octahedral default, Show Names/Axes/Shapes/Bone Colors/In Front, per-bone Hide, Display As, Bone Color, Pose Bone Color and Custom Shape options. Removed the unconfirmed colour conventions, X-ray and Pose Mode shape remarks, and version tags.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): Armature.display_type is OCTAHEDRAL (default), STICK, BBONE, ENVELOPE, WIRE; Armature has show_names, show_axes, show_bone_custom_shapes, show_bone_colors; Object.show_in_front exists; Bone has display_type (default ARMATURE_DEFINED), show_wire, color, hide; PoseBone has color, custom_shape, custom_shape_translation, custom_shape_rotation_euler, custom_shape_scale_xyz, custom_shape_transform, use_custom_shape_bone_size, custom_shape_wire_width; there is no gizmo or pivot property; Bone Color palette enum is DEFAULT, THEME01 to THEME20, CUSTOM. Not run (confirmed from the manual only): what each display type looks like, the custom shape axis rules, and Affect Gizmo and Use As Pivot (5.x only).

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
