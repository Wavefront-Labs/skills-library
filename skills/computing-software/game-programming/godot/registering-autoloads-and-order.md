---
id: computing-software.game-programming.godot.registering-autoloads-and-order
name: registering-autoloads-and-order
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, autoload, autoload-order, singletons, project-settings, globals, game-programming, autoload-ready]
level: intro
status: docs-checked
description: "Register autoloads in Godot 4 (scripts or scenes), control initialisation order, access them by name, and avoid dependencies between autoloads that break at startup."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.html", "https://docs.godotengine.org/en/stable/tutorials/best_practices/autoloads_versus_regular_nodes.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Registering autoloads and order

**Goal:** global services that exist before any scene loads and initialise in a predictable order.

## Register
Project > Project Settings > **Globals > Autoload**: pick a script that inherits `Node`, or a scene, and give
it a name (`GameState`); the name becomes the node's `name`. Leave the **Enable** column checked (the
default) to access it by name in GDScript.

## How they live
- Each autoload is instanced as a child of `/root`, **before** the main scene, in list order. The scene
  tree is `/root/Events`, `/root/Settings`, ..., then `/root/Main`.
- The engine reads the entries top to bottom, and autoloaded nodes always come first, so the last child
  of `/root` is the loaded main scene.
- They persist across `change_scene_*` calls; never remove them with `free()` or `queue_free()` (the
  engine crashes).
- Access: `GameState.score` (global variable) or `get_node("/root/GameState")`.

## Order rules
- Order entries with the up/down arrows in the Autoload list; put an autoload above the ones that
  depend on it.
- Don't use `_init` for setup that needs other autoloads or the tree.

## Gotchas
- Autoloads are processed like normal nodes: set `process_mode = PROCESS_MODE_ALWAYS` for ones that
  must run while paused (audio, pause menu).
- An autoload is not a true singleton: nothing stops you instantiating another copy of the node.
- Too many autoloads become hidden global state; see alternatives (static vars, resources).

## Verify
- [ ] Remote scene tree at startup shows autoloads in the intended order under /root.
- [ ] Changing scenes keeps autoload state; no autoload depends on one below it.

## Checked

2026-10-25, against godot-docs master ("latest" docs, last commit 2026-10-24). Confirmed in the autoloads tutorial (Globals > Autoload, name becomes the node name, top-to-bottom order with up/down arrows, Enable column, autoloads added before other scenes, free()/queue_free() warning, get_child(-1) is the loaded scene) and the Autoloads versus regular nodes page (not freed on change_scene_to_file, not a true singleton, get_node("/root/Name")), plus the pausing tutorial (process mode Always). Removed unconfirmed claims: the project.godot syntax, ready ordering, the class_name clash and the tool-script behaviour.

Method: documentation only; no commands were run.
