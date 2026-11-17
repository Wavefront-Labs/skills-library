---
id: computing-software.game-programming.godot.profiler-and-performance-monitors
name: profiler-and-performance-monitors
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-performance, godot-profiler, monitors, visual-profiler, custom-monitors, frame-time, draw-calls, game-programming, custom-monitor]
level: practitioner
status: docs-checked
description: "Find Godot performance problems: the Debugger Profiler and Visual Profiler, Monitors for draw calls and objects, custom monitors, and profiling exported builds."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/debug/debugger_panel.html", "https://docs.godotengine.org/en/stable/classes/class_performance.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Godot profiler and performance monitors

**Goal:** know whether a slow frame is script, physics, rendering CPU or GPU, and which function or
node is responsible.

## Debugger > Profiler (CPU, scripts)
- Start profiling, play the slow section, stop. Graph shows frame time split into Physics Time,
  Process Time, and per-script function costs.
- Select a frame; the table lists functions with **Self** and **Total** (inclusive) time; sort by
  Self to find hot functions. Enable "Measure: Frame Time / Average Time" as needed.
- Profiling adds overhead; compare relative numbers.

## Debugger > Visual Profiler (rendering CPU/GPU)
Per-frame breakdown of rendering passes on CPU and GPU (e.g. depth prepass, opaque, shadows,
transparency, post). GPU-bound frames show GPU time above the frame budget while CPU idles.

## Debugger > Monitors
Time (FPS, Process, Physics), Memory, Object (including **orphan nodes**), Raster (including
**draw calls**), Physics and more; see the debugger panel page for the full list.
- Orphan nodes rising = nodes removed from the tree but never freed (`remove_child` without
  `queue_free`): a leak.
- Draw calls in the thousands: merge meshes, use MultiMesh, atlas textures, fewer materials.

## Custom monitors
```gdscript
func _ready() -> void:
    Performance.add_custom_monitor("game/enemies", func(): return get_tree().get_nodes_in_group("enemy").size())
    Performance.add_custom_monitor("game/pathfinding_ms", func(): return last_path_ms)
```
They appear in the Monitors tab and can be graphed alongside engine metrics. Read engine values in
code with `Performance.get_monitor(Performance.TIME_PROCESS)`, e.g. for an in-game overlay.

## Exported builds and native profiling
- Remote debug an exported build: export with "Export With Debug" and run with
  the remote-debug option, or use one-click deploy; see the debugger panel docs for the exact flag.
- For engine-level/native hot spots, use a native profiler such as perf, Visual Studio profiler, Xcode Instruments, or RenderDoc for GPU frames.

## Typical findings and fixes
| Finding | Fix |
|---|---|
| `_process` on hundreds of nodes | Disable processing when idle (`set_process(false)`), central manager loops. |
| Many `get_node` calls per frame | Cache with `@onready`. |
| Physics time high | Simpler shapes, fewer active bodies, collision layers to cut pairs, Jolt. |
| Draw calls high | MultiMesh, merge static meshes, fewer lights casting shadows. |

## Verify
- [ ] Profile shows frame time under budget (about 16.7 ms at 60 fps) on target hardware.
- [ ] Orphan node count stays stable over a long session.
- [ ] Custom monitors for key game systems exist for ongoing tracking.

## Checked
Godot docs (stable) pages and godotengine/godot master doc/classes XML fetched 2026-10-28.
Confirmed: Performance class (`add_custom_monitor`, `get_monitor`, `TIME_PROCESS`, orphan node monitor) and the debugger panel page (Visual Profiler, Monitors tab).
Removed: the specific `--remote-debug tcp://...:6007` argument, Tracy build-option claim, the long monitor list, and the 10-minute figure; 60 fps frame time corrected to about 16.7 ms.
Method: documentation only; no commands were run.
