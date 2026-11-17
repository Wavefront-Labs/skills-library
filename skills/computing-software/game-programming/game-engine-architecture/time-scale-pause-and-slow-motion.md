---
id: computing-software.game-programming.game-engine-architecture.time-scale-pause-and-slow-motion
name: time-scale-pause-and-slow-motion
category: computing-software
field: game-programming
product: game-engine-architecture
tags: [game-engine-architecture, game-loop, slow-motion, time-scale, pause, hit-stop, multiple-clocks, godot, game-programming]
level: practitioner
status: docs-checked
description: "Implement time scale, pause and slow motion with separate scaled and unscaled clocks, using Godot's Engine.time_scale behaviour as the documented reference."
sources: ["https://docs.godotengine.org/en/stable/classes/class_engine.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time scale, pause and slow motion

## What Godot's Engine.time_scale documents
From the Godot Engine class reference (`time_scale`, default 1.0):
- It is the speed multiplier at which the in-game clock updates compared to real time: 2.0 runs
  the game twice as fast, 0.5 half as fast.
- It affects Timer, SceneTreeTimer and every simulation that uses `delta` (including
  `Node._process()` and `Node._physics_process()`).
- Keep it above 0.0; the game may behave unexpectedly otherwise. So do not use a zero scale as
  pause there; use the engine's pause mechanism instead.
- It does not affect audio playback speed. Use `AudioServer.playback_speed_scale` to adjust audio
  independently.
- It does not adjust `physics_ticks_per_second`. At values above 1.0 each physics tick stretches
  over more engine time and physics may become less precise; for large speed-ups consider
  raising physics ticks per second.

## Multiple clocks (design pattern, own advice)
Keep separate clocks advanced from the real frame delta: a game clock (scaled, paused with the
game) for gameplay, physics, AI and animation; a UI clock for menus and HUD tweens that must
keep running while paused; real time for profiling and network timeouts. Gameplay reads only the
game clock's delta.

## Effects (own advice)
- Hit-stop: drop the game scale briefly on heavy hits, timed on the real clock so duration is
  the same at 30 and 144 fps.
- Slow motion: ease the scale rather than snapping it.
- Audio: change audio speed or filtering explicitly, since scale alone does not (Godot).
- Timers or coroutines on scaled time stall while paused; menus need unscaled waits.

## Verify
- [ ] The pause menu animates and responds while gameplay and physics freeze.
- [ ] Slow motion shows smooth motion; hit-stop duration is the same at different frame rates.
- [ ] Audio behaviour under scale changes is set deliberately.

## Checked
Method: docs-checked 2026-11-09 against the Godot Engine class reference page (downloaded HTML, read the time_scale property description and notes). Removed the Unity, Unreal and gameenginebook.com sources and their API details: the Unity page downloaded as a JavaScript shell without the property text, and the others were not read. The clock and effects sections are the skill author's design advice, not source claims.
