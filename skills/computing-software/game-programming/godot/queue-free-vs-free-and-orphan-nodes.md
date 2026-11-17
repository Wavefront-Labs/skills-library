---
id: computing-software.game-programming.godot.queue-free-vs-free-and-orphan-nodes
name: queue-free-vs-free-and-orphan-nodes
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-scenes, queue_free, orphan-nodes, is_instance_valid, game-programming]
level: practitioner
status: verified
description: "Free Godot nodes safely: queue_free vs free, removing without freeing, finding orphan-node leaks, is_instance_valid checks and freeing during signals or physics callbacks."
sources: ["https://docs.godotengine.org/en/stable/classes/class_node.html#class-node-method-queue-free", "https://docs.godotengine.org/en/stable/tutorials/scripting/debug/the_profiler.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# queue_free vs free and orphan nodes

**Goal:** nodes leave the game without crashes, dangling references or slow memory leaks.

## Options
| Call | Effect |
|---|---|
| `queue_free()` | deletes at end of the current frame (after all callbacks). Safe default. |
| `free()` | deletes immediately. Errors if the object is locked by the call stack (run: freeing an emitter inside its own signal handler logged `Object is locked and can't be freed.` and the object survived); freeing a different plain node from a handler worked. |
| `remove_child(n)` / `n.get_parent().remove_child(n)` | detaches from the tree but does **not** free -> orphan unless you keep and re-add or free it later |
| `reparent(new_parent)` | move keeping global transform optionally |

`Node` is not reference-counted (unlike `RefCounted`/`Resource`): a removed node that you lose the
reference to leaks forever.

## Validity checks
```gdscript
if is_instance_valid(target) and not target.is_queued_for_deletion():
    target.take_damage(5)
```
A freed object reference becomes a "previously freed" instance; using it errors. `is_instance_valid`
returns false after free. Between `queue_free()` and the end of frame the node is still valid — check
`is_queued_for_deletion()` if others must ignore it immediately.

## Finding leaks
- `Performance.get_monitor(Performance.OBJECT_ORPHAN_NODE_COUNT)` (the same counter the debugger monitors show) rising over time = leak.
- `Node.print_orphan_nodes()` is a static method (4.7.2 prints lines like `<id> - Stray Node: orph (Type: Node) (Source:)`); `Node.get_orphan_node_ids()` returns the ids.
- Common sources: `remove_child` without free, instantiated scenes never added to the tree, pooled
  nodes discarded, `duplicate()` results unused.

## Freeing in callbacks
- In `body_entered` / `area_entered` and other physics signals, prefer `queue_free()` or
  `call_deferred("queue_free")`; changing physics state (removing collision shapes) during a physics
  callback errors with "Can't change this state while flushing queries" — use `set_deferred` /
  `call_deferred`.
- Freeing the scene root you're iterating children of: iterate a copy (`get_children()` already
  returns a new array).

## Gotchas
- `queue_free()` on a node not in the tree still works (run: freed after one frame).
- Freeing a parent frees all children; references to children become invalid too (run: child invalid after `free()` of the parent).
- Signals connected to a freed object are disconnected automatically (for Callables bound to it), but
  lambdas capturing it are not — guard them.

## Verify
- [ ] Orphan Nodes monitor stays flat across 10 level reloads.
- [ ] No "previously freed" errors in the debugger during combat stress tests.
## Checked
Ran on Godot 4.7.2 headless: `queue_free()` leaves the node valid with `is_queued_for_deletion()` true until the next frame; `remove_child` leaves a valid orphan listed by `Node.print_orphan_nodes()`; `get_children()` returns a typed `Array[Node]` copy; parent `free()` invalidates children; locked-object error; `Performance.OBJECT_ORPHAN_NODE_COUNT` monitor values 2 then 1 after freeing an orphan. `Node.print_orphan_nodes` and `get_orphan_node_ids` from the 4.7.2 Node reference. The physics-callback `set_deferred` advice was run in the connect-deferred skill. The Verify checklist items are test procedures for your own project.
