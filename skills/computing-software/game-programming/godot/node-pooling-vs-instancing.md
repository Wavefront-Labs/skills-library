---
id: computing-software.game-programming.godot.node-pooling-vs-instancing
name: node-pooling-vs-instancing
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-performance, godot-object-pool, node-pool, instantiate-cost, game-programming]
level: practitioner
status: docs-checked
description: "Choose between instantiate/queue_free and pooling in Godot: measure instancing cost, detach idle nodes from the tree, reset state, reuse physics objects."
sources: ["https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html", "https://docs.godotengine.org/en/stable/classes/class_packedscene.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node pooling vs instancing

**Goal:** bullets, hit effects and pickups spawn without frame spikes, with pooling only where it helps.

## Measure first
The CPU optimization guide starts from the bottleneck: use a profiler. Godot's built-in profiler must be
started and stopped manually because recording can slow the project significantly. After finding a hot
function, time it manually: in GDScript wrap the call in `Time.get_ticks_usec()` reads and run it many times
(the guide suggests 1,000 or more) because timers have limited accuracy and CPU caches skew single runs.

`PackedScene.instantiate()` instantiates the scene's node hierarchy, triggers child scene instantiation, and
sends `NOTIFICATION_SCENE_INSTANTIATED` to the root node, so cost scales with what the scene contains.
The guide says every node has a cost (`_process()` and `_physics_process()` propagate through the tree) and that
fewer nodes with more in each can perform better.

## What the docs recommend for reuse
- Removing a node from the SceneTree can give much better performance than pausing or hiding it. You do not have
  to delete it: keep a reference, call `Node.remove_child(node)`, and later `Node.add_child(node)` to reattach.
- For physics: remove objects from physics when they are out of view or outside the current area, or reuse
  physics objects (the guide's example is allowing 8 monsters per area and reusing them).
- In C#, garbage collection pauses can happen during gameplay; the guide names object pooling as a common
  workaround (it does not cover it in detail).

## Pool sketch (detached idle nodes)
```gdscript
class_name NodePool extends Node
@export var scene: PackedScene
var _free: Array[Node] = []

func acquire(parent: Node) -> Node:
    var n: Node = _free.pop_back() if _free.size() > 0 else scene.instantiate()
    parent.add_child(n)
    n.call("reset")          # your own method: pooled node restores its own state
    return n

func release(n: Node) -> void:
    if n.get_parent():
        n.get_parent().remove_child(n)
    _free.append(n)
```
A pooled node is not freed, so nothing resets for you: velocities, timers, tweens, animation state and signal
connections made in the previous life are yours to restore.

## Verify
- [ ] Profile before and after; keep pooling only if the measured spikes go away.
- [ ] Reused objects behave identically to fresh ones (automated reuse test).

## Checked
Date 2026-11-09. Read in full as fetched text: Godot CPU optimization guide (stable, 4.7 docs) and the
PackedScene class reference. Confirmed the profiler behaviour, manual timing advice, per-node cost, remove_child
and add_child reattachment, physics reuse advice, C# GC and pooling note, and `instantiate()` behaviour.
Removed as unconfirmed: the claim that spawn cost comes from shader compilation, `process_mode` disabling, the
`set_deferred` collision handling, Area2D monitoring notes, the warm-up advice and the pool-size note. The
Godot docs do not specify exact thresholds for when pooling pays.
Method: documentation only; no commands were run.
