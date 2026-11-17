---
id: computing-software.game-programming.godot.animationtree-state-machines-and-blend-spaces
name: animationtree-state-machines-and-blend-spaces
category: computing-software
field: game-programming
product: godot
tags: [godot, godot4, godot-animation, animationtree, animationnodestatemachine, blendspace2d, blendspace1d, oneshot, travel, conditions, game-programming]
level: practitioner
status: docs-checked
description: "Drive Godot character animation with AnimationTree: state machine travel and conditions, BlendSpace1D/2D locomotion, OneShot and Blend2 nodes, and setting parameters from code."
sources: ["https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html", "https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachineplayback.html", "https://docs.godotengine.org/en/stable/classes/class_animationtree.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AnimationTree: state machines and blend spaces

**Goal:** smooth locomotion blending and responsive action states for characters, controlled by a
few parameters from gameplay code.

## Setup
`AnimationTree` node with `anim_player` pointing at the AnimationPlayer holding clips, `tree_root` set
to an `AnimationNodeStateMachine` (or a BlendTree containing one), `active = true`.

## Locomotion blend space
Inside a state `Locomotion`, use `AnimationNodeBlendSpace2D`: points idle (0,0), walk (0,0.5), run
(0,1), strafe left/right (-1,0)/(1,0), with the default Continuous blend mode (`BLEND_MODE_INTERPOLATED`;
Discrete and Carry suit frame-by-frame animation). Or `BlendSpace1D` on speed for non-strafing characters
(it works with fewer than three points).

## State machine
States: `Locomotion`, `Jump`, `Fall`, `Land`, `Attack`, `Hit`, `Death`. Transitions have:
- **Switch mode**: Immediate, Sync (switch immediately but seek to the old state's position), At End
  (wait for the current state to finish).
- **Advance mode**: Disabled (transition unused), Enabled (used only by `travel()`), Auto (taken
  automatically when its advance condition and advance expression are true).
- An **advance condition** only tests that a variable is true (it cannot test falseness; use two
  opposite conditions) and is set through `parameters/conditions/<name>`; an **advance expression**
  (`velocity.y < 0`) is evaluated against the AnimationTree's `advance_expression_base_node` (default:
  the tree itself) and is case-sensitive.
- `xfade_time` for blend duration; transition priority steers `travel()` (lower is preferred).

## Code
```gdscript
@onready var tree: AnimationTree = $AnimationTree
@onready var sm: AnimationNodeStateMachinePlayback = tree.get("parameters/playback")

func _physics_process(_d: float) -> void:
    var local_vel := global_basis.inverse() * velocity
    tree.set("parameters/Locomotion/blend_position", Vector2(local_vel.x, -local_vel.z) / run_speed)
    tree.set("parameters/conditions/is_falling", not is_on_floor() and velocity.y < 0)
    tree.set("parameters/conditions/on_floor", is_on_floor())

func attack() -> void:
    sm.travel("Attack")          # A* over the transitions; teleports if no path exists. start() jumps directly
```
Parameter paths are shown in the AnimationTree inspector under Parameters (copy them exactly).

## OneShot and layering (BlendTree)
For upper-body actions while moving: a BlendTree with the state machine as input, a `OneShot` node fed
by the attack clip and a `Blend2` with a filter (enable filters, tick upper-body bones):
`tree.set("parameters/AttackShot/request", AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE)`.
`TimeScale` nodes for speed changes.

## Gotchas
- `travel()` follows the transition graph; if no path of transitions leads to the target the state
  machine teleports to it instead. The state machine must be running (call `start()` or connect a node
  to Start) before you can travel.
- Root motion: set `root_motion_track` and apply `get_root_motion_position()` yourself (see godot
  root-motion-in-godot).
- Use `callback_mode_process = PHYSICS` when animation must sync with physics-driven movement.

## Verify
- [ ] Locomotion blends smoothly from idle to run and strafes without foot sliding beyond tolerance.
- [ ] Attack plays via travel from any locomotion state and returns automatically.
- [ ] Parameters panel shows expected values live while playing.

## Checked

Checked 2026-10-25 against the Godot 4.7 documentation (godot-docs stable branch, last commit 2026-10-24; latest engine release 4.7.2). Confirmed: transition switch modes (Immediate, Sync, At End) and advance modes (Disabled, Enabled only during `travel()`, Auto); advance conditions only test true, advance expressions use `advance_expression_base_node` (default the tree) and are case-sensitive; the `parameters/conditions/<name>` and `parameters/playback` paths; `AnimationNodeStateMachinePlayback.travel(to_node, reset_on_teleport)` and `start(node, reset)`; `travel()` uses A* and teleports when no path exists (the earlier text said unreachable states do nothing); BlendSpace blend modes (Interpolated shown as Continuous, Discrete, Carry); BlendSpace1D needs fewer than three points; OneShot, Blend2 filters, `TimeScale`; `callback_mode_process` and `root_motion_track` exist on AnimationMixer. Removed the unconfirmed Add2 and "active tree overrides the player" claims.

Method: documentation only; no commands were run.
