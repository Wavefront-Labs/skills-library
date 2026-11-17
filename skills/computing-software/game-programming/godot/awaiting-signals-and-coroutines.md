---
id: computing-software.game-programming.godot.awaiting-signals-and-coroutines
name: awaiting-signals-and-coroutines
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, gdscript, await-signal, coroutines, await, scenetreetimer, async-flow, game-programming]
level: practitioner
status: verified
description: "Use await in GDScript 4 for sequenced logic: awaiting signals, timers and other coroutines, returning values, and avoiding awaits that resume on freed nodes."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html#awaiting-signals-or-coroutines", "https://docs.godotengine.org/en/stable/classes/class_scenetreetimer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Awaiting signals with await

**Goal:** write cutscenes, telegraphed attacks and UI flows top to bottom instead of state flags and callbacks.

## Basics
```gdscript
func telegraph_attack() -> void:
    anim.play("windup")
    await anim.animation_finished                     # suspends until the signal fires
    hitbox.monitoring = true
    await get_tree().create_timer(0.2).timeout        # one-shot timer, no node needed
    hitbox.monitoring = false

func _on_boss_phase() -> void:
    await telegraph_attack()                          # await another coroutine
    print("attack done")
```
- Any function containing `await` is a coroutine; calling it as a bare statement **without** `await` returns immediately
  and the rest runs later. Using its return value without `await` is an error: `var r = coro()` is a parse error
  ("Function "coro()" is a coroutine, so it must be called with "await"."); a dynamic `call("coro")` returned a `GDScriptFunctionState`.
- Awaiting a signal with arguments returns them: one argument gives the value (run: `await one_arg` gave 42), several give an Array (run: `[7, "q"]`): `var body = await area.body_entered`.
- Return values: `func ask() -> bool: ... return await dialog.confirmed_choice`; caller `if await ask():`.
- `await get_tree().process_frame` / `physics_frame` waits one frame.

## Timers
`get_tree().create_timer(sec, process_always := true, process_in_physics := false, ignore_time_scale := false)`.
Pass `process_always = false` so the timer pauses with the game.

## Pitfalls
- **Nodes queued for deletion**: after `queue_free()` the node lives until the end of the frame, and a coroutine
  waiting on an external signal resumes if the signal fires in that window (run: it resumed with
  `is_queued_for_deletion()` true). A coroutine whose node was already freed did not resume (no output, no error)
  on 4.7.2. Guard after each await:
```gdscript
await get_tree().create_timer(1.0).timeout
if not is_instance_valid(self) or is_queued_for_deletion(): return
```
- Signals that never fire leave the coroutine suspended forever (leak). Add timeouts for external events.
- Re-entrancy: calling the coroutine again while one is in flight runs both. Track a `busy` flag or a
  generation counter to cancel stale runs.
- There's no built-in cancellation; check a token/counter after each await.

## When not to use await
Per-frame logic (movement), or logic that must be saved/restored mid-sequence (coroutine state isn't
serialisable). Use a state machine there.

## Verify
- [ ] Killing an enemy mid-windup produces no errors (guards after awaits).
- [ ] Pausing the game pauses gameplay timers.
## Checked
Ran on Godot 4.7.2 headless: `await` on a SceneTree timer, on a user signal with one and two arguments; coroutine called with `await` returns its value (5); the parse error for using a coroutine result without `await`; `create_timer(0.05, false)` did not fire while `paused = true` and fired after unpausing, `create_timer(0.05, true)` fired while paused; `create_timer` parameter list from the 4.7.2 `SceneTree` reference (`time_sec`, `process_always = true`, `process_in_physics = false`, `ignore_time_scale = false`); the freed and queued-for-deletion cases above. `AnimationPlayer.animation_finished` and `Area2D.body_entered` exist as signals (`ClassDB.class_has_signal`); the animation and hitbox bodies need a rendered scene, so only the await mechanics were exercised.
