---
id: computing-software.game-programming.godot.signal-disconnect-and-object-lifetime
name: signal-disconnect-and-object-lifetime
category: computing-software
field: game-programming
product: godot
tags: [godot, signals, signal-disconnect, is_connected, callable-lifetime, game-programming]
level: practitioner
status: verified
description: "Manage Godot signal connections over time: disconnect and is_connected, automatic cleanup when targets are freed, lambda pitfalls and reconnect-on-reuse bugs with pooling."
sources: ["https://docs.godotengine.org/en/stable/classes/class_object.html#class-object-method-disconnect", "https://docs.godotengine.org/en/stable/classes/class_signal.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disconnecting signals and object lifetime

**Goal:** no duplicated handlers, no errors from freed listeners, no leaks through lambdas.

## API
```gdscript
health.died.connect(_on_died)
if health.died.is_connected(_on_died): health.died.disconnect(_on_died)
# Object-level equivalents: connect("died", callable), disconnect(...), is_connected(...)
for c in health.died.get_connections(): print(c.callable)
```
Connecting the same Callable twice errors ("already connected") unless `CONNECT_REFERENCE_COUNTED`
is used (then it counts and needs matching disconnects; run: one disconnect left it connected).

## Automatic cleanup
When the **target object** of a method Callable is freed, Godot removes the connection. When the
**emitter** is freed, its connections go with it. So for `node.method` callables you rarely need
manual disconnects on free.

## Lambdas don't auto-clean the way you think
```gdscript
enemy.died.connect(func(): score += 10)   # lambda bound to self (the script instance)
```
A lambda connection is **not** removed when the script instance that created it is freed (run on 4.7.2: a lambda
connected from a node's method, then that node `free()`d, left the connection count unchanged and the lambda still ran
on the next emit). Captured variables (other nodes) can also be freed independently, and accessing them errors
(`Lambda capture at index 0 was freed. Passed "null" instead.`). And you cannot easily disconnect an anonymous lambda:
store it in a variable if you'll need to, and disconnect it in `_exit_tree`.

## Pooling pitfall
Reused (pooled) nodes keep connections from their previous life. Connect once at creation, or
disconnect in a `reset()`; otherwise each reuse adds duplicates (or errors).

## Common patterns
- Temporary listening: `CONNECT_ONE_SHOT` flag disconnects after first emit.
- Listening to a global bus from a node: connect in `_ready`/`_enter_tree`, disconnect in
  `_exit_tree` (the bus outlives the node; auto-cleanup only happens when freed, not when removed from
  the tree and kept).

## Gotchas
- `disconnect` on a non-connected callable errors (`Attempt to disconnect a nonexistent connection`) — check `is_connected` first.

## Verify
- [ ] Reuse a pooled enemy 50 times: died handler runs once per death.
- [ ] Free listeners during gameplay: no "Attempt to call function on a previously freed instance".
## Checked
Ran on Godot 4.7.2 headless: auto-removal for a freed target's method (1 to 0); lambda from a freed owner stays connected and runs; freed capture error text; double connect error; REFERENCE_COUNTED counting; disconnect of a missing connection; `get_connections()` entries expose `callable`. The pooling pitfall follows from the double-connect and persistence results above. The editor-reconnect and C# bullets were removed because they were not checked here.
