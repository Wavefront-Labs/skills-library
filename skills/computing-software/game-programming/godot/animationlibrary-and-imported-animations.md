---
id: computing-software.game-programming.godot.animationlibrary-and-imported-animations
name: animationlibrary-and-imported-animations
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, animationlibrary, animationplayer, gltf-import, animation-import, game-programming]
level: practitioner
status: docs-checked
description: "Organise Godot 4 animations in AnimationLibrary resources: library prefixes, saving imported glTF animations to files, sharing libraries and editing imported clips."
sources: ["https://docs.godotengine.org/en/stable/classes/class_animationlibrary.html", "https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/import_configuration.html", "https://docs.godotengine.org/en/stable/classes/class_animationmixer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AnimationLibrary and imported animations

**Goal:** animations shared across characters, editable, and not lost on reimport.

## Libraries
In Godot 4 an AnimationPlayer (AnimationMixer) holds one or more `AnimationLibrary` resources. The
default library has an empty name; others prefix names: `play("locomotion/run")`.
```gdscript
var lib: AnimationLibrary = load("res://anim/locomotion.res")
$AnimationPlayer.add_animation_library("locomotion", lib)
$AnimationPlayer.play("locomotion/walk")
```
The Animation panel's Animation menu manages libraries.

## Imported glTF/FBX animations
Imported scenes embed animations; editing them in the scene is not allowed (they are read-only and
would be overwritten on reimport). Options in the **Advanced Import Settings** (double-click the
model):
- Save an animation to a file from the Advanced Import Settings so you can edit it without losing changes on reimport (see the import configuration page for the exact options).
- Import as **Animation Library** (root type) for animation-only files to produce a library resource
  directly.

## Sharing between characters
Same skeleton/bone names: reuse the library in each character's AnimationPlayer; tracks use node
paths relative to the player's `root_node`, so keep the hierarchy identical (`Skeleton3D` path). For
different skeletons, retarget with BoneMap at import first.

## Gotchas
- Track paths break if the model's root node name differs; set root node consistently or use
  Root Type/Name options on import.
- A library shared between players is edited in one place; duplicate it if one character needs its own changes.

## Verify
- [ ] Reimporting the model keeps custom tracks; two characters share one library correctly.

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: AnimationLibrary and AnimationMixer classes (`add_animation_library`, `library/animation` play names) and the import configuration page (Animation Library root type).
Removed: menu item names (Manage Animations, Make Unique), the Slices and Keep Custom Tracks options, and the .res/.tres size and speed comparison (not found on fetched pages).
Method: documentation only; no commands were run.
