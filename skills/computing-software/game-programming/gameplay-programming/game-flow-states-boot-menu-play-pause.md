---
id: computing-software.game-programming.gameplay-programming.game-flow-states-boot-menu-play-pause
name: game-flow-states-boot-menu-play-pause
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-flow-states, pause-menu, game-state-machine, boot-flow, time-scale, loading-screen, game-programming]
level: practitioner
status: draft
description: "Structure top-level game flow as a state machine (boot, title, loading, playing, paused, game over) with correct pause semantics, time scale, input focus and loading transitions."
sources: ["https://gameprogrammingpatterns.com/state.html", "https://docs.unity3d.com/ScriptReference/Time-timeScale.html", "https://docs.godotengine.org/en/stable/tutorials/scripting/pausing_games.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Game flow states: boot, menu, play, pause

**Goal:** one authority decides what the whole game is doing, so "pause during loading" or "game over
while paused" cannot happen.

## Typical states
`Boot` (init services, load settings, platform login) -> `Title` -> `Loading(target)` -> `Playing`
<-> `Paused` -> `GameOver` / `Results` -> `Title` or `Loading(next)`. Use a state stack for Paused and
overlays (see `pushdown-automaton-state-stack`).

Transitions are requests (`flow.Request(Paused)`) checked against a table; illegal ones are logged
and ignored, so a stray pause input on the loading screen does nothing.

## Pause done right
- **Gameplay time stops, real time does not.** Engine switches: Unity `Time.timeScale = 0` (stops
  `FixedUpdate` and scaled `deltaTime`; UI tweens must use `unscaledDeltaTime`; Animator
  `UpdateMode.UnscaledTime` for menu animations). Godot `get_tree().paused = true` with
  `process_mode = PROCESS_MODE_ALWAYS` on the pause menu, `PROCESS_MODE_PAUSABLE` on gameplay.
  Unreal `UGameplayStatics::SetGamePaused` with `bTickEvenWhenPaused` on UI-driving actors.
- Audio: duck or pause gameplay buses, keep the UI bus live.
- Input: switch the action map to UI (Unity `PlayerInput.SwitchCurrentActionMap("UI")`, Unreal
  remove the gameplay Input Mapping Context, set `SetInputMode(FInputModeUIOnly)`) and show the cursor.
- Auto-pause on focus loss / controller disconnect / platform overlay (console certification requirement).
- Online games cannot pause the simulation: "pause" opens a menu but the world continues.

## Loading state
- Show the loading UI first, then start async loading next frame (so the screen renders).
- Keep a minimum display time (~0.5 s) to avoid flicker; fade out only once the level reports ready
  (streaming done, shaders warmed, player spawned), not when the scene file finished loading.
- Gate gameplay input until `Playing.enter`.

## Game over and restart
Restart = `Loading(sameLevel)` through the normal path, which guarantees a clean reset, rather than
"reset every object in place", which leaks state.

## Verify
- [ ] Pause during: combat, a cutscene, a loading screen, a level transition: only legal ones take effect.
- [ ] While paused, physics, AI and timers freeze; menu animations and audio still play.
- [ ] Alt-tab / unplugging the controller auto-pauses.
- [ ] Restarting 20 times shows no growth in memory or duplicate managers.
