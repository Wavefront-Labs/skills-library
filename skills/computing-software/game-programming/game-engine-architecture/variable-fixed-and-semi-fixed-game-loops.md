---
id: computing-software.game-programming.game-engine-architecture.variable-fixed-and-semi-fixed-game-loops
name: variable-fixed-and-semi-fixed-game-loops
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, game-loop, semi-fixed-timestep, fixed-timestep, variable-timestep, accumulator, interpolation, spiral-of-death, game-programming, delta-time-clamp]
level: practitioner
status: docs-checked
description: "Choose and implement a game loop: fixed, variable, semi-fixed and accumulator-with-interpolation timesteps, avoiding the spiral of death, and Unity FixedUpdate catch-up."
sources: ["https://gafferongames.com/post/fix_your_timestep/", "https://gameprogrammingpatterns.com/game-loop.html", "https://docs.unity3d.com/Manual/fixed-updates.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Variable, fixed and semi-fixed game loops

**Goal:** a loop whose simulation is stable and reproducible while rendering runs as fast as the display allows
(Gaffer "Fix Your Timestep", Nystrom "Game Loop").

## The options
| Loop | Code shape | Pros | Cons |
|---|---|---|---|
| Fixed delta time | `integrate(dt); render();` | ideal if dt matches the display refresh and the update fits in a frame | runs faster or slower than intended on other machines or with VSYNC off |
| Variable | `integrate(frameTime)` | tracks real time | behaviour depends on dt: different "feel", springs exploding, tunnelling, falling through floors; physics damping is tuned to one step |
| **Semi-fixed** | `while (frameTime > 0) { d = min(frameTime, dt); integrate(d); frameTime -= d; }` | dt never exceeds the maximum | several steps per frame plus a remainder step, so risk of the spiral of death; not exactly reproducible (floating point) |
| **Fixed + accumulator (+ interpolation)** | below | simulation only uses fixed dt, reproducible, rendering decoupled | leftover time must be interpolated or the picture stutters |

Gaffer's view: a simulation is realistically well behaved only if delta time is at or below some maximum.

## Accumulator with interpolation
```cpp
const double dt = 0.01;
double t = 0.0, accumulator = 0.0, currentTime = now();
State previous, current;
while (!quit) {
    double newTime = now();
    double frameTime = newTime - currentTime;
    if (frameTime > 0.25) frameTime = 0.25;       // clamp after a hitch
    currentTime = newTime;
    accumulator += frameTime;
    while (accumulator >= dt) {
        previous = current;
        integrate(current, t, dt);
        t += dt;  accumulator -= dt;
    }
    const double alpha = accumulator / dt;         // 0..1
    render(current * alpha + previous * (1.0 - alpha));
}
```
- The renderer produces time and the simulation consumes it in dt-sized steps; leftover time carries to the next frame.
- Without interpolation the displayed state differs slightly from render time, causing visible stutter. alpha is the
  blend between previous and current state. For 3D rigid bodies store orientation as a quaternion and use slerp.

## Spiral of death
If the simulation takes longer in real time to run X seconds of physics than X (Y > X), it falls behind, so it simulates
more steps to catch up, which makes it fall further behind. Defences from Gaffer: leave headroom (updating X seconds of
physics must take significantly less than X seconds), or clamp the maximum number of steps per frame so the simulation
appears to slow down under load. Nystrom: the fixed time step must be greater than the time one `update()` takes
on the slowest hardware, otherwise the game cannot catch up.

## Nystrom's version
Fixed update step with a `lag` accumulator: add elapsed time, run `update()` while `lag >= MS_PER_UPDATE`, then
render. A shorter step costs more processing to catch up; a longer one is choppier. Residual lag (`lag` after the
loop) is how far into the next frame you are; pass it to `render()` to extrapolate.

## Unity
- Physics runs on a fixed timestep; read or change it with `Time.fixedDeltaTime` or Project Settings > Time > Fixed
  Timestep (seconds). Code goes in `MonoBehaviour.FixedUpdate`.
- Fixed updates need a frame to run in: with a high frame rate a frame has one fixed update or none; with a low frame
  rate a backlog accumulates and several run in the next frame.
- There is a maximum timestep beyond which Unity does not try to catch up (see Unity's "Handling variation in
  time"). A smaller timestep means more precise simulation and higher CPU load.

## Verify
- [ ] Simulation results identical at different render frame rates.
- [ ] A forced multi-second hitch does not lock the game.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on Gaffer, Game Programming Patterns and the Unity fixed updates manual page. Removed because none of
the pages state them: the Unity default maximum timestep of 1/3 s, Unreal "Max Substeps", Godot physics
interpolation versions, the table of which systems run in fixed versus per-frame loops, input latching advice and
the "one frame of visual latency" claim.
