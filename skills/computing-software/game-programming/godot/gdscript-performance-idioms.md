---
id: computing-software.game-programming.godot.gdscript-performance-idioms
name: gdscript-performance-idioms
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, gdscript-performance, optimisation, profiler, packed-arrays, game-programming]
level: advanced
status: docs-checked
description: "Speed up hot GDScript: profile first, use static typing, fewer script calls, built-in engine functions, and when to move code to another language or a thread."
sources: ["https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GDScript performance idioms

**Goal:** hot loops (hundreds of entities, grid algorithms) fast enough in GDScript, and knowing when to stop.

## Measure first
- Use the built-in profiler in the debugger. It must be started and stopped manually because recording
  timings can slow the project down significantly. Time spent waiting for built-in servers may not be
  counted (a known bug in the docs).
- Time a suspect area manually with `Time.get_ticks_usec()` before and after. The first run of a function
  can be slow because data is not in the CPU cache, so always use averages.

## Idioms
- **Static types in hot code**: the docs state typed GDScript uses optimised opcodes when operand and
  argument types are known at compile time. Prefer typed global-scope methods so lines stay type-safe.
  Stick to either typed or dynamic style per codebase for consistency.
- **Use built-in engine functions**: they run at the same speed regardless of scripting language. If your
  own code does a lot of calculation, consider a faster language.
- **Cache lookups** in `@onready` variables or arrays instead of repeating node or group queries per frame.
- **Process only what's needed**: `set_process(false)` for idle objects; use timers and signals instead of
  polling.
- **Compare squared distances** (`distance_squared_to`) when only ordering or thresholds matter.

## Before / after
```gdscript
# slow: untyped, lookup per frame
func _process(delta):
    for e in get_tree().get_nodes_in_group("enemies"):
        if e.position.distance_to($Player.position) < 100: e.alert()

# faster
@onready var player: Node2D = %Player
var enemies: Array[Enemy] = []
func _process(_delta: float) -> void:
    var p := player.global_position
    for e: Enemy in enemies:
        if e.global_position.distance_squared_to(p) < 10000.0: e.alert()
```

## When to leave GDScript
Large amounts of pure computation: the CPU optimisation page suggests a faster language, and threads for
calculations that can run in parallel. Threads risk race conditions and make debugging harder; read
"Using multiple threads" first.

## Verify
- [ ] The profiler or averaged timings show the hot function's time reduced after each change.

## Checked
2026-11-08. Read in full: CPU optimisation page (profiler, manual timing, caching effect, languages,
threads) and the typed GDScript page (optimised opcodes, typed global scope methods). Removed unconfirmed
claims: the 1.5-2x figure, the order-of-magnitude figure for C#, packed-array and allocation advice,
list of native functions, node-count and MultiMesh advice, `range` loop optimisation, and the 1 ms
frame budget. The code sample is illustrative and was not run.
Method: documentation only; no commands were run.
