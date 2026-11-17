---
id: computing-software.game-programming.godot.changing-scenes-and-loading-screens
name: changing-scenes-and-loading-screens
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, change-scene, resourceloader-threaded, loading-screen, scene-transitions, game-programming]
level: practitioner
status: docs-checked
description: "Switch scenes in Godot 4: change_scene_to_file/packed, deferred manual swaps, threaded background loading with ResourceLoader.load_threaded_request and fade transitions."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/change_scenes_manually.html", "https://docs.godotengine.org/en/stable/tutorials/io/background_loading.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Changing scenes and loading screens

**Goal:** level transitions with a fade and progress bar, without freezing the window or losing state.

## Simple switch
```gdscript
get_tree().change_scene_to_file("res://levels/level_2.tscn")
get_tree().change_scene_to_packed(LEVEL_2)          # already loaded PackedScene
```
The current scene is freed at the end of the frame; the new one is added next frame. Code after the
call still runs in the old scene. Autoloads persist across changes; put persistent state there.

## Threaded loading with progress
```gdscript
# LoadingScreen autoload (CanvasLayer with a ProgressBar and fade ColorRect)
var _path := ""
func goto(path: String) -> void:
    _path = path
    await fade_out()
    ResourceLoader.load_threaded_request(path)
    set_process(true)

func _process(_d: float) -> void:
    if _path.is_empty(): return
    var progress := []
    var status := ResourceLoader.load_threaded_get_status(_path, progress)
    match status:
        ResourceLoader.THREAD_LOAD_IN_PROGRESS:
            bar.value = progress[0] * 100.0
        ResourceLoader.THREAD_LOAD_LOADED:
            var scene := ResourceLoader.load_threaded_get(_path) as PackedScene
            _path = ""; set_process(false)
            get_tree().change_scene_to_packed(scene)
            await get_tree().process_frame
            fade_in()
        ResourceLoader.THREAD_LOAD_FAILED, ResourceLoader.THREAD_LOAD_INVALID_RESOURCE:
            push_error("load failed: %s" % _path); _path = ""
```
- Progress is coarse (per sub-resource), often jumps; animate the bar smoothly toward the value.
- `use_sub_threads` argument speeds big loads at the cost of more threads.

## Manual swap (keep some nodes alive)
```gdscript
func swap_level(new_scene: PackedScene) -> void:
    var old := level_root.get_child(0)
    level_root.remove_child(old); old.queue_free()
    level_root.add_child(new_scene.instantiate())
```
Use a persistent "Main" scene that owns HUD/music and swaps level children: no autoload needed and
full control over what persists.

## Passing data
Store in an autoload (`GameState.spawn_point = "door_b"`) before changing, read it in the new level's `_ready`.

## Gotchas
- First-time shader compilation can stutter after load; warm up by showing materials during the loading screen.

## Verify
- [ ] The window stays responsive (animated spinner) while a large level loads.
- [ ] Player state (health, inventory) survives the transition.

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: change_scene_to_file/packed, ResourceLoader.load_threaded_request/get_status/get, the THREAD_LOAD_* statuses and `use_sub_threads` (background loading tutorial and ResourceLoader XML); `LEVEL_2` in the example is a user constant.
Removed: the physics-callback call_deferred rule and the ubershader/pipeline cache remark (not on the fetched pages).
Method: documentation only; no commands were run.
