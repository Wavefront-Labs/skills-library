---
id: computing-software.game-programming.godot.scene-based-autoloads
name: scene-based-autoloads
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, autoload, autoload-scene, canvaslayer, music-player, transitions, game-programming]
level: intro
status: docs-checked
description: "Register a .tscn as an autoload for global systems that need child nodes (music player, transition overlay, debug HUD), with process modes and layering set correctly."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html", "https://docs.godotengine.org/en/stable/tutorials/2d/canvas_layers.html", "https://docs.godotengine.org/en/stable/classes/class_control.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scene-based autoloads

**Goal:** persistent systems built visually (audio players, fade overlays, debug panels) that survive scene changes.

## Why a scene
A script autoload is a bare Node. A **scene** autoload can hold configured children: AudioStreamPlayers
with buses set, a CanvasLayer with a ColorRect and AnimationPlayer, Timers. Register the `.tscn` in
Project Settings > Globals > Autoload just like a script.

## Transition overlay
```
Transition (CanvasLayer, layer = 100, process_mode = Always)
└── Fade (ColorRect, full rect anchors, color black, mouse_filter = Ignore)
    └── AnimationPlayer ("fade_out", "fade_in")
```
```gdscript
# transition.gd on the root
extends CanvasLayer
func change_scene(path: String) -> void:
    $AnimationPlayer.play("fade_out")
    await $AnimationPlayer.animation_finished
    get_tree().change_scene_to_file(path)
    await get_tree().process_frame
    $AnimationPlayer.play("fade_in")
```
- CanvasLayer `layer` above game UI so the fade covers everything.
- `mouse_filter = Ignore` on the overlay or it blocks clicks after fading in (or toggle it during fades).

## Music player
```
Music (Node, process_mode = Always)
├── A (AudioStreamPlayer, bus = "Music")
└── B (AudioStreamPlayer, bus = "Music")
```
Crossfade by tweening `volume_db` of A down and B up; the music continues across scene changes and pause.

## Rules
- Set `process_mode` to Always on autoloads that must work during pause.
- Autoload scenes are added to the root before the main scene, so they cannot rely on main-scene nodes
  existing in their own setup.
- Keep them small: autoloads are not freed when the scene changes and live for the whole session.
- A single "Main" persistent scene that swaps level children is an alternative to several autoload scenes.

## Verify
- [ ] Music continues through scene changes and the pause menu.
- [ ] Fade overlay never blocks input when transparent.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the autoloads tutorial (a script autoload is a Node; scenes and scripts register under Globals > Autoload; autoloads are added before other scenes), the pausing tutorial (process mode Always), the CanvasLayer class page (layer default 1), the Control class page (mouse_filter default MOUSE_FILTER_STOP, MOUSE_FILTER_IGNORE), AnimationMixer.animation_finished and SceneTree.change_scene_to_file and process_frame. Removed the unsupported startup-time claim.

Method: documentation only; no commands were run.
