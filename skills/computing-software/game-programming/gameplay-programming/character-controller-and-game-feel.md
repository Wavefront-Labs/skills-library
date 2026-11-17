---
id: computing-software.game-programming.gameplay-programming.character-controller-and-game-feel
name: character-controller-and-game-feel
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, character-controller, platformer, game-feel, coyote-time, jump-buffering, variable-jump-height, acceleration, friction, air-control, state-machine, finite-state-machine, hit-stop, screen-shake, juice, camera-follow, input-buffer, kinematic-controller, unity, godot, unreal]
level: practitioner
status: draft
description: "Build a responsive character controller: acceleration curves, jump arcs from height and time, coyote time, jump buffering, a state machine, and the feedback that sells impact."
sources: ["GDC 2016, Kyle Pittman: Math for Game Programmers - Building a Better Jump", "https://gameprogrammingpatterns.com/state.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Character controller and game feel

**Goal:** a player character that does what the player meant, with tunable numbers a
designer can adjust, and feedback that makes actions feel weighty. Engine-agnostic;
pseudocode maps directly onto Unity, Godot or Unreal.

## Kinematic vs physics-driven
Most action games use a **kinematic** controller (you compute velocity and resolve
collisions with sweeps/`move_and_slide`/`CharacterController.Move`) rather than a
dynamic rigid body: you get exact control and no unwanted bouncing or sliding. Use a
rigid body when the character should be pushed around by physics (vehicles, ragdoll
games).

## Horizontal movement: accelerate, don't snap
```
target = input_x * max_speed
rate   = (abs(target) > 0.01) ? (grounded ? accel : air_accel)
                              : (grounded ? decel : air_decel)
vel.x  = move_toward(vel.x, target, rate * dt)
```
Starting numbers for a 2D platformer in "tiles" (1 tile ≈ character width): max speed
8–10 tiles/s, reach full speed in ~0.1 s (snappy) to ~0.3 s (weighty), stop in a bit
less than that. Turning around should use the higher of accel/decel so reversals feel
crisp. Air control at 50–80% of ground acceleration.

## Jumps designed from height and time
Pick **jump height h** (e.g. 3.5 tiles) and **time to apex t** (e.g. 0.4 s), derive the rest:
```
gravity        = 2 * h / t^2          // 3.5 tiles, 0.4 s → 43.75 tiles/s²
jump_velocity  = 2 * h / t            // → 17.5 tiles/s upward
```
Designers then tune in meaningful units instead of fiddling with raw gravity.
- **Falling faster** than rising (gravity × 1.5–2.5 while vel.y is downward) removes the
  floaty feel.
- **Variable jump height:** if the button is released while rising, multiply upward
  velocity by ~0.5 (or apply extra gravity) — short taps give short hops.
- Clamp fall speed (terminal velocity) so players can read and react.

## Forgiveness: the two timers that matter most
```
if grounded: coyote_timer = 0.1     else coyote_timer -= dt
if jump_pressed: buffer_timer = 0.12 else buffer_timer -= dt
if buffer_timer > 0 and coyote_timer > 0:
    vel.y = jump_velocity; buffer_timer = 0; coyote_timer = 0
```
- **Coyote time** (~0.08–0.15 s): jump still works just after running off a ledge.
- **Jump buffering** (~0.1–0.15 s): a press slightly before landing still jumps on landing.
- Also: corner correction (nudge a few pixels around a ceiling corner instead of
  bonking), and ledge-snap on the way down.
Players never notice these; they notice when they're missing ("I pressed jump!").

## Structure: a finite state machine
States like `Idle, Run, Jump, Fall, Dash, WallSlide, Hurt`, each with `enter()`,
`update(dt)`, `exit()` and explicit transitions. This stops boolean soup
(`isJumping && !isDashing && ...`) and gives clean hooks for animation and sound. Use a
state stack or hierarchical states when attacks can happen in several movement states.

## Juice: feedback that sells impact
- **Hit-stop:** freeze (or slow to ~0) both attacker and victim for 2–6 frames on a hit.
- **Screen shake:** short (0.1–0.3 s), decaying, driven by "trauma" (shake = trauma²)
  so small hits are subtle. Always offer a reduce/disable option (accessibility).
- Squash and stretch on jump/land, dust particles, a landing sound scaled by fall speed,
  controller rumble.
- Camera: smooth follow with a dead zone, look-ahead in the movement direction, and
  vertical lock until the player lands on a new platform height.

## Gotchas
- Read input every rendered frame and consume it in the fixed step, or presses get
  lost at high frame rates.
- Frame-rate dependence: multiply by `dt` everywhere and test at 30 and 240 fps (or use a
  fixed timestep — see
  computing-software.game-programming.game-physics.fixed-timestep-and-collision-detection).
- Put all tunables in one data asset so designers can iterate live.

## Verify
- [ ] Jump height and apex time match the configured values (measure in-game).
- [ ] Jumping 0.1 s after leaving a ledge and 0.1 s before landing both work.
- [ ] Identical feel at 30 and 240 fps.
- [ ] Movement states are explicit; no contradictory flag combinations possible.
- [ ] Blind playtest: new players don't report "it didn't jump".
