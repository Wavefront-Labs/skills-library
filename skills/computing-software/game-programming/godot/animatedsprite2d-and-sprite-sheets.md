---
id: computing-software.game-programming.godot.animatedsprite2d-and-sprite-sheets
name: animatedsprite2d-and-sprite-sheets
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-2d, animatedsprite2d, spriteframes, sprite-sheet, pixel-art, frame-animation, animation-finished, game-programming]
level: intro
status: docs-checked
description: "Animate 2D characters with Godot AnimatedSprite2D and SpriteFrames: sprite sheet import, per-animation FPS and looping, flipping, frame signals, pixel-art settings."
sources: ["https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html", "https://docs.godotengine.org/en/stable/classes/class_animatedsprite2d.html", "https://docs.godotengine.org/en/stable/classes/class_spriteframes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AnimatedSprite2D and sprite sheets

**Goal:** frame-by-frame 2D character animation (idle, run, jump, attack) driven by gameplay state.

## Setup
1. Add `AnimatedSprite2D`; in `sprite_frames` create a new `SpriteFrames` resource.
2. In the SpriteFrames panel: add animations (`idle`, `run`, `jump`, `attack`), add frames from a
   sprite sheet (the tutorial: open the sheet, set horizontal and vertical image counts, select the
   frames, "Add N frames").
3. Per animation: speed and looping. In 4.7 looping is a `SpriteFrames.LoopMode`
   (`LOOP_NONE`, `LOOP_LINEAR`, `LOOP_PINGPONG`) via `set_animation_loop_mode()`; `set_animation_loop()` is deprecated.
4. Alternative from the tutorial: a `Sprite2D` with `hframes`/`vframes` animated by an AnimationPlayer.

## Driving from code
```gdscript
@onready var sprite: AnimatedSprite2D = $AnimatedSprite2D

func _physics_process(_d: float) -> void:
    if attacking: return                            # let the attack finish
    if not is_on_floor():
        sprite.play("jump" if velocity.y < 0 else "fall")
    elif abs(velocity.x) > 5:
        sprite.play("run")
    else:
        sprite.play("idle")
    if velocity.x != 0: sprite.flip_h = velocity.x < 0

func attack() -> void:
    attacking = true
    sprite.play("attack")
    await sprite.animation_finished                 # not emitted if the animation is looping
    attacking = false
```
`play(name, custom_speed = 1.0, from_end = false)`; `animation` defaults to `&"default"` and `frame` to 0.

## Frame events
```gdscript
sprite.frame_changed.connect(func():
    if sprite.animation == "attack" and sprite.frame == 3: enable_hitbox())
```
Other signals: `animation_changed`, `animation_looped`, `sprite_frames_changed`. For many timed events,
a `Sprite2D` with `hframes`/`vframes` driven by an AnimationPlayer keeps everything on one timeline.

## Verify
- [ ] Animations switch correctly through idle/run/jump/fall with no flicker.
- [ ] Attack completes before returning to locomotion.

## Checked
2026-10-28, Godot docs `stable` (latest release tag 4.7.2-stable). Confirmed from the 2D sprite animation tutorial and the AnimatedSprite2D and SpriteFrames class pages: sprite sheet import steps, hframes/vframes alternative, play() signature, animation/frame/flip_h defaults, animation_finished not emitted for looping animations, frame_changed and the other signals, LoopMode enum and the deprecation of set_animation_loop. Removed (not confirmed): FPS suggestions, pixel-art project settings, play()-same-name no-restart claim, flip_h-does-not-flip-children gotcha and the negative-scale advice.
Method: documentation only; no commands were run.
