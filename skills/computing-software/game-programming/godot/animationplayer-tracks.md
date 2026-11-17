---
id: computing-software.game-programming.godot.animationplayer-tracks
name: animationplayer-tracks
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-animation, animationplayer, call-method-track, property-track, animation-library, reset-track, animation-finished, game-programming]
level: practitioner
status: docs-checked
description: "Animate anything in Godot with AnimationPlayer: property, method-call and audio tracks, RESET tracks, animation libraries, blending, and reacting to animation_finished."
sources: ["https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html", "https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html", "https://docs.godotengine.org/en/stable/classes/class_animationplayer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AnimationPlayer tracks

**Goal:** use AnimationPlayer as a general timeline for character moves, UI transitions, doors and
cutscene beats, with gameplay hooks at exact frames.

## Track types
| Track | Use |
|---|---|
| Property (Value) | Animate any property: `position`, `modulate`, `frame`, shader params. Update mode Continuous/Discrete/Capture. |
| 3D Position/Rotation/Scale | Efficient transform tracks for 3D nodes/bones. |
| Blend Shape | Mesh morph targets. |
| **Call Method** | Call a function at a time: spawn hitbox, play footstep, emit signal. |
| Bezier Curve | Per-component curves with handles for precise easing. |
| Audio Playback | Play streams on an AudioStreamPlayer. |
| Animation Playback | Trigger animations of another AnimationPlayer (nested). |
Keys are added with the key icon next to any inspector property while the Animation panel is open.

## Gameplay hooks with method tracks
```gdscript
# Attack animation has Call Method keys: _hitbox_on() at 0.15 s, _hitbox_off() at 0.30 s
func _hitbox_on() -> void:  $Hitbox/CollisionShape2D.set_deferred("disabled", false)
func _hitbox_off() -> void: $Hitbox/CollisionShape2D.set_deferred("disabled", true)
```
Call Method keys are not executed when the animation is previewed in the editor (a safety measure); they
run during playback in the game. A key can also be created in code with `Animation.track_insert_key()`
passing a dictionary with `"method"` and `"args"`.

## Playing and chaining
```gdscript
@onready var anim: AnimationPlayer = $AnimationPlayer

func attack() -> void:
    anim.play("attack", 0.1)                     # custom blend time
    await anim.animation_finished                # resumes when this animation ends
    anim.play("idle")

func _ready() -> void:
    anim.animation_finished.connect(func(name): if name == "die": queue_free())
```
`queue("idle")` plays next; `play_backwards`, `speed_scale`, `seek(t, true)`. Looping animations
never emit `animation_finished`.

## RESET track and libraries
- Add an animation named `RESET` (case-sensitive) with one key at time 0 per property. With
  AnimationPlayer's **Reset On Save** enabled, the scene is saved as if seeked to 0.0 (only the saved file
  changes). **Edit > Apply Reset** resets the tracks in the editor, and keying a property from the inspector
  offers to create the RESET track. RESET values are also reference values for blending.
- **Animation libraries** (`AnimationLibrary` resources) group animations; `play("library/anim")`.
  Share a library between several players (e.g. same humanoid set).

## When to use AnimationTree instead
For characters with locomotion blending, state machines and many transitions, drive animations with
an `AnimationTree` that references the AnimationPlayer's animations (see godot animationtree). Use
plain AnimationPlayer for linear, one-shot timelines.

## Verify
- [ ] Hitbox enables/disables exactly at the keyed frames (debug draw collision shapes).
- [ ] Saving a scene mid-preview does not save animated values (RESET track present).
- [ ] No `animation_finished` waits on looping animations.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: track types (Property, Position/Rotation/Scale 3D, Blend Shape, Call Method, Bezier, Audio Playback, Animation Playback); property track update modes Continuous, Discrete and Capture; Call Method keys are not run in the editor preview; `AnimationPlayer.play(name, custom_blend, custom_speed, from_end)`, `play_backwards`, `queue`, `seek(seconds, update)`, `speed_scale`; `animation_finished(anim_name)` is not emitted for looping animations; library keys use `library/animation`; RESET track behaviour and Reset On Save. Removed the unconfirmed claim about long frames skipping method keys.

Method: documentation only; no commands were run.
