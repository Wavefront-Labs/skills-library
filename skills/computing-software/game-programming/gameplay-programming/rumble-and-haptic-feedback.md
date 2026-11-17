---
id: computing-software.game-programming.gameplay-programming.rumble-and-haptic-feedback
name: rumble-and-haptic-feedback
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, input-system, rumble, haptics, force-feedback, dualsense, adaptive-triggers, vibration, game-feel, accessibility, game-programming]
level: practitioner
status: draft
description: "Design and implement controller rumble: low/high-frequency motors, layered effect mixing, priorities, engine APIs, DualSense haptics and an intensity accessibility slider."
sources: ["https://docs.unity3d.com/Packages/com.unity.inputsystem@1.11/manual/Gamepad.html", "https://dev.epicgames.com/documentation/en-us/unreal-engine/force-feedback-in-unreal-engine", "https://docs.godotengine.org/en/stable/classes/class_input.html#class-input-method-start-joy-vibration"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rumble and haptic feedback

**Goal:** vibration that communicates (hit taken, engine revving, gun recoil), never buzzes forever,
and respects player settings.

## Hardware model
Classic gamepads have two eccentric-mass motors: **low frequency** (left, heavy, "thud") and **high
frequency** (right, light, "buzz"). Values 0..1 each. DualSense/Switch HD rumble are voice-coil
actuators driven by audio-like waveforms; DualSense also has adaptive trigger resistance.

## Effect design
| Event | Low | High | Duration |
|---|---|---|---|
| Light hit / footstep on landing | 0.2 | 0.4 | 60-100 ms |
| Heavy hit / explosion nearby | 0.8-1.0 | 0.5 | 200-400 ms with decay |
| Gun shot (automatic) | 0.1 | 0.6 | 40 ms per shot |
| Engine idle | 0.1 | 0.05 | continuous, scaled by RPM |
Use envelopes (attack/decay curves) rather than flat on/off; scale distance-based events by falloff.

## Mixer, not direct calls
Many systems request rumble at once. Keep a small mixer per player:
```
effects: list of {curveLow, curveHigh, start, duration, priority, loop}
each frame:
  low  = max over active effects of curveLow(elapsed/duration)   # max, not sum, avoids saturation
  high = max over ... curveHigh(...)
  apply(low * settings.intensity, high * settings.intensity)
  remove finished effects
on pause / focus lost / controller disconnect: apply(0,0)
```
The pause/focus reset is critical: an un-stopped rumble keeps going while the game is paused or
tabbed out.

## Engine APIs
- **Unity Input System:** `Gamepad.current.SetMotorSpeeds(low, high)`; `PauseHaptics()`,
  `ResumeHaptics()`, `ResetHaptics()`. Per-player: `playerInput.GetDevice<Gamepad>()`.
- **Unreal:** Force Feedback Effect asset (curves per motor: Large/Small Left/Right),
  `PlayerController->ClientPlayForceFeedback(Effect, Params)`; Force Feedback Component for
  world-positioned, attenuated effects. DualSense trigger effects via platform plugins.
- **Godot:** `Input.start_joy_vibration(device, weak, strong, duration)`;
  `Input.stop_joy_vibration(device)`. Mobile: `Input.vibrate_handheld(ms)`.

## Accessibility and platform rules
- Options: vibration on/off and an intensity slider (0-100%). Some players need it off entirely.
- Console certification requirements commonly include stopping vibration when the game pauses or the
  system menu opens; check the platform's current requirements.
- Do not encode critical information only in haptics.

## Verify
- [ ] Pause during a long rumble: motors stop immediately.
- [ ] Two overlapping effects never exceed 1.0 and the stronger dominates.
- [ ] Intensity 0 produces no vibration from any system.
- [ ] Unplug the controller mid-effect: no errors, effect state cleared.
