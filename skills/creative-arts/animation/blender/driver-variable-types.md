---
id: creative-arts.animation.blender.driver-variable-types
name: driver-variable-types
category: creative-arts
field: animation
product: blender
tags: [blender, drivers, driver-variable-types, single-property, rotational-difference, distance-variable, transform-channel-driver, transform-channel, context-property]
level: practitioner
status: verified
description: "Choose the right Blender driver variable: Single Property paths, Transform Channel (space, rotation mode), Rotational Difference, Distance and Context Property."
sources:
  - https://docs.blender.org/manual/en/5.2/animation/drivers/drivers_panel.html
  - https://docs.blender.org/manual/en/5.2/animation/drivers/usage.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# driver-variable-types

Goal: each driver input reads exactly the value you mean, in the right space. General driver setup is in `drivers`/`rig-ui-controls`.

## Types

Variable names must start with a letter and contain only letters, digits or underscores (run: `DriverVariable.is_name_valid` is False for `1bad` and `a b`, True for `good_1`). API `DriverVariable.type` values: `SINGLE_PROP`, `TRANSFORMS`, `ROTATION_DIFF`, `LOC_DIFF` (Distance), `CONTEXT_PROP`; target fields `id`, `data_path`, `bone_target`, `transform_type`, `rotation_mode`, `transform_space`, `context_property`, `use_fallback_value`, `fallback_value`. Read drivers should access data through variables, not direct references in the expression, so dependencies are tracked.

- **Single Property**: the value of an RNA property given by ID Type, ID and RNA Path (for example `location.x`, `location[0]` or `["prop_name"]` for a custom property). For transform properties it returns the exact UI value, whereas Transform Channel takes parenting and constraints into account. **Fallback** gives a value to use if the path cannot be resolved. The easiest way to make one is Copy As New Driver on the input property, then Paste Driver Variables.
- **Transform Channel**: the value of an object or bone transform channel (ID, Bone, Type such as X Location, X Rotation, X Scale or Average Scale), with a **Mode** for rotation channels and a **Space** (World Space, Transform Space, Local Space). Rotation modes: Auto Euler, explicit Euler orders, Quaternion, and Swing and X/Y/Z Twist. Swing and Twist is often necessary for corrective shape keys and bones on organic joints; for Swing and Y Twist, Y Rotation is the twist angle, W Rotation the swing angle, and X/Z Rotation weighted swing angles.
- **Rotational Difference**: the rotational difference between two objects or bones, in radians.
- **Distance**: the distance between two objects or bones, with a Space per target.
- **Context Property**: a property of the active scene or active view layer of the evaluating animation system (Context = Active Scene or Active View Layer, then an RNA Path such as `camera.location.x`). It is a weak reference, so linking a character does not link the scene; with Fallback it suits scene-global options.

## Choosing

| Need | Variable |
|---|---|
| Slider value | Single Property |
| Elbow bend → corrective | Transform Channel with a Swing and Twist mode; or Rotational Difference |
| Proximity effect | Distance |
| Camera focal length into a shader | Single Property on camera data |

## Gotchas

- Single Property reads the UI value of a transform (before parenting and constraints); use Transform Channel when parenting or constraints should be included. Run: a child at local x 1 under a parent at x 5 scaled 2 reads 1 through Single Property and 7 through Transform Channel in World Space.
- For corrective shapes driven by joint rotation, prefer Swing and Twist modes or Rotational Difference over a single Euler channel.

## Verify

Drivers editor shows the variable's live value next to it; rotate the bone and watch the value change smoothly without jumps.

## Checked

2026-10-27, Blender 5.2 manual (blender-v5.2-release). Confirmed on the Drivers panel page: variable types and their fields, Single Property versus Transform Channel behaviour, Fallback, Context Property contexts and example path, rotation channel modes and Swing and Y Twist channels, Rotational Difference in radians. Removed the 0..pi range, Context Property version tag, Transform/Local Space definitions and Euler flip claims, none of which the manual states.

Run check, 2026-11-01, Blender 4.5.14 LTS headless (bpy, factory settings): variable type and target enums (transform types X/Y/Z Location, X/Y/Z/W Rotation, X/Y/Z Scale, Average Scale; rotation modes Auto Euler, six Euler orders, Quaternion, Swing and X/Y/Z Twist; spaces World, Transform, Local; contexts Active Scene and Active View Layer); numerical drivers: Single Property 1.0 versus Transform Channel world 7.0 versus local 1.0; Rotational Difference of a 90 degree rotation 1.5708; Distance 7.0711; fallback value 7.0 used when the path does not resolve (is_fallback_used True). Not run (confirmed from the manual only): the Swing and Twist channel meanings, Copy As New Driver, and how Context Property behaves when a character is linked.

Method: manual text and shipped UI scripts confirmed from documentation; the listed behaviour run headless in Blender 4.5.14.
