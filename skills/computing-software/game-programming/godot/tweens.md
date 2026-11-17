---
id: computing-software.game-programming.godot.tweens
name: tweens
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-animation, godot-tween, create-tween, tween-property, easing, transitions, ui-animation, juice, game-programming]
level: intro
status: verified
description: "Animate properties procedurally with Godot 4 Tweens: create_tween, chaining and parallel steps, easing/transition types, callbacks, killing tweens and binding them to nodes."
sources: ["https://docs.godotengine.org/en/stable/classes/class_tween.html", "https://docs.godotengine.org/en/stable/classes/class_propertytweener.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tweens

**Goal:** quick code-driven animations (UI pops, damage numbers, door slides, camera punches) without
creating AnimationPlayer clips.

## Basics
```gdscript
func pop_in(node: Control) -> void:
    node.scale = Vector2.ZERO
    var tw := create_tween()                           # bound to this node: dies with it
    tw.tween_property(node, "scale", Vector2.ONE, 0.25)\
      .set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
    tw.tween_property(node, "modulate:a", 1.0, 0.1).from(0.0)
    tw.tween_callback(func(): print("done"))
```
- Steps run **sequentially** by default. `tw.set_parallel(true)` or `tw.parallel().tween_property(...)`
  to run together; `tw.chain()` to go back to sequential after parallel.
- Sub-properties: `"position:x"`, `"modulate:a"`.
- `as_relative()` to add to the current value; `from(value)` to set the start.
- `tween_interval(seconds)` for waits; `tween_method(callable, from, to, duration)` for custom setters
  (shader parameters).

## Easing
`set_trans` (curve family: LINEAR, SINE, QUAD, CUBIC, QUART, QUINT, EXPO, CIRC, ELASTIC, BACK, BOUNCE,
SPRING) + `set_ease` (IN, OUT, IN_OUT, OUT_IN). UI usually wants EASE_OUT (fast start, soft stop);
BACK/ELASTIC for playful overshoot.

## Lifetime and control
- `create_tween()` on a Node binds the tween to that node: it halts while the node is outside the tree and is killed when the node is freed (class reference; run: `is_valid()` false after the bound node was freed). `get_tree().create_tween()`
  is unbound and keeps running until it finishes or is killed; when its target object is freed the tween ends silently (run: no error, `is_valid()` false shortly after), per the docs' "all the animated objects have been freed" note.
- Store the tween to stop it before starting another on the same property, otherwise both fight:
```gdscript
var hover_tw: Tween
func on_hover(on: bool) -> void:
    if hover_tw: hover_tw.kill()
    hover_tw = create_tween()
    hover_tw.tween_property(self, "scale", Vector2.ONE * (1.1 if on else 1.0), 0.1)
```
- `set_loops(n)` (0 = infinite), `set_speed_scale`, `pause()/play()`, `await tw.finished`.
- `set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)` so UI tweens run while the game is paused (and the node
  must also process while paused).
- `set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)` for tweens moving physics objects.

## Gotchas
- Tweens start automatically on the next frame; an empty tween (no steps) logs `started with no Tweeners.`
- Tweening `position` of a CharacterBody bypasses collision (run: a body tweened from x=0 to x=100 ended at 100 through a wall at x=50); animate kinematic bodies via velocity or
  use AnimatableBody for moving platforms.

## Verify
- [ ] Rapid hover in/out never leaves a button stuck at the wrong scale (old tween killed).
- [ ] Freeing a node mid-tween produces no errors.
- [ ] Pause menu animations run while the game is paused.
## Checked
Ran on Godot 4.7.2 headless: the `pop_in` pattern (`tween_property` with `TRANS_BACK`/`EASE_OUT`, `modulate:a` with `.from(0.0)`, `tween_callback`, `await tw.finished`; final scale (1, 1) and alpha 0.5); empty tween error text; bound tween killed on free; unbound tween ending on freed target; tween moving a `CharacterBody2D` through a wall; constants `TWEEN_PAUSE_PROCESS`, `TWEEN_PROCESS_PHYSICS`, `TRANS_SPRING` exist. Method names (`set_pause_mode`, `set_process_mode`, `set_loops`, `set_speed_scale`, `pause`, `play`, `kill`, `tween_method`, `tween_interval`, `tween_callback`, `parallel`, `chain`, `set_parallel`, `finished`) and `set_loops` 0 = infinite are from the 4.7.2 `Tween` class reference; `as_relative()` is on `PropertyTweener`. Rapid-hover and pause-menu checklist items are procedures for your own project.
