---
id: computing-software.game-programming.godot.animationtree-oneshot-and-blend-tree
name: animationtree-oneshot-and-blend-tree
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-animation, animationnodeoneshot, animation-blend-tree, animationtree-parameters, game-programming]
level: practitioner
status: docs-checked
description: "Play attacks and reactions over locomotion in Godot AnimationTree: BlendTree with OneShot, Blend2/Add2 nodes, filters for upper body, and setting parameters from code."
sources: ["https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html", "https://docs.godotengine.org/en/stable/classes/class_animationnodeoneshot.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AnimationTree OneShot and BlendTree

**Goal:** fire one-off animations (attack, hit react, reload) layered over locomotion with blending
and optional upper-body masking.

## Structure
AnimationTree `tree_root` = **AnimationNodeBlendTree** containing:
- `Locomotion` (a StateMachine or BlendSpace2D),
- `OneShot` node: input "in" = locomotion, input "shot" = the action animation (or another state
  machine),
- output.
For upper body only, enable **Filters** on the OneShot and tick the spine/arms bones.

## OneShot parameters
- Fade In/Out time, Auto Restart (with delay), Mix Mode Blend or Add.
- Request: `parameters/<NodeName>/request` with `AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE`,
  `..._ABORT`, `..._FADE_OUT`.
- Status: `parameters/<NodeName>/active` (bool, read-only), `internal_active`.
```gdscript
@onready var tree: AnimationTree = $AnimationTree
func attack():
    tree.set("parameters/AttackShot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)
func is_attacking() -> bool:
    return tree.get("parameters/AttackShot/active")
# or with the shorthand: tree["parameters/AttackShot/request"] = ...
```
To pick which attack plays, put a `Transition` node in the shot input and set
`parameters/AttackType/transition_request = "slash"` (the state name).

## Other blend nodes
- `Blend2` / `Blend3` blend two or three inputs by a blend value (`parameters/<node>/blend_amount`) and can
  use filters; `TimeScale` multiplies speed by `scale` (0 pauses, negative plays backwards); `TimeSeek`
  (`seek_request`, in seconds); `Transition` (a simplified state machine, `transition_request`).
- Parameters are per-node under `parameters/<node>/...`; get the exact path by hovering a parameter in
  the inspector.

## Callbacks
`animation_finished(anim_name)` (declared on AnimationMixer, which AnimationTree inherits; not emitted
for looping animations); for gameplay events use method call tracks in the action animation (hit frame).

## Gotchas
- AnimationTree must have `active = true` and its `anim_player` set.
- When the tree drives the skeleton, set `root_motion_track` on the AnimationTree (an AnimationMixer
  property) to use root motion.
- A OneShot clears its `request` itself on the next process frame; set FIRE once per action.

## Verify
- [ ] Attack while running: legs keep running, arms attack (filter works).
- [ ] `active` returns false exactly when the attack ends (for combo windows).

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: `AnimationNodeOneShot` properties (`fadein_time`, `fadeout_time`, `autorestart`, `autorestart_delay`, `mix_mode` with BLEND and ADD, `abort_on_reset`, `break_loop_at_end`), request constants NONE, FIRE, ABORT and FADE_OUT, the `parameters/<node>/request`, `active` and `internal_active` paths, the "shot" port, filters on OneShot and Blend2/Blend3, `TimeScale` (`scale`), `TimeSeek` (`seek_request`), `Transition` (`transition_request`), AnimationTree inherits AnimationMixer and has `anim_player`, `animation_finished` is not emitted for looping animations. Removed the unconfirmed Blend3 range, Add2/Add3, right-click copy-path and version-gated claims.

Method: documentation only; no commands were run.
