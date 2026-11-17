---
id: computing-software.game-programming.gameplay-programming.acceleration-and-friction-curves
name: acceleration-and-friction-curves
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, character-controller, game-feel, acceleration-curves, deceleration, turnaround, movement-tuning, frame-rate-independence, move-towards, game-programming]
level: practitioner
status: gated
description: "Tune movement feel with acceleration, deceleration and turnaround rates: frame-rate independent formulas, time-to-max-speed parameters, ground vs air values."
sources: ["https://docs.unity3d.com/ScriptReference/Vector3.MoveTowards.html", "https://www.gdcvault.com/play/1023559/Math-for-Game-Programmers-Building", "https://www.routledge.com/Game-Feel-A-Game-Designers-Guide-to-Virtual-Sensation/Swink/p/book/9780123743282"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Acceleration and friction curves

**Goal:** movement that feels responsive or weighty on purpose, tuned in designer-friendly units and
identical at any frame rate (Swink, Game Feel: input response and simulated space).

## Parameterise in time, not magic numbers
Designers think "reaches full speed in 0.1 s, stops in 0.05 s":
```
accel     = maxSpeed / timeToMax        # units/s^2
decel     = maxSpeed / timeToStop
turnAccel = maxSpeed / timeToTurn       # used when input opposes current velocity
```

## Update (per axis or on the velocity vector)
```
target = input * maxSpeed
if |input| > 0:
    rate = (dot(velocity, target) < 0) ? turnAccel : accel
else:
    rate = decel
velocity = move_towards(velocity, target, rate * dt)     # linear approach, same speed ramp at any dt
```
`move_towards` (Unity `Vector3.MoveTowards`, Godot `Vector2.move_toward`, Unreal
`FMath::VInterpConstantTo` (gated: unconfirmed, source is paywalled or blocked)) gives frame-rate independent linear acceleration. Simulated here with maxSpeed 10 and timeToMax 0.1 s, the time to reach full speed was 0.100 s at 30 and 60 fps and 0.104 s at 144 fps (within one frame, because the last step is clamped to the frame grid).
Avoid `velocity = lerp(velocity, target, 0.1)` per frame: it depends on frame rate and never quite
arrives (simulated: reaching 99.9% of target took 66 frames, so 2.2 s at 30 fps, 1.1 s at 60 fps and 0.46 s at 144 fps). If you want exponential smoothing, use `lerp(v, target, 1 - exp(-k * dt))` (simulated with k = 10: after 0.2 s the value is 0.8647 at 30 and 60 fps, matching 1 - exp(-2) = 0.8647, and 0.8569 at 144 fps only because 0.2 s is not a whole number of 144 Hz frames).

## Typical profiles
| Feel | timeToMax | timeToStop | turnaround |
|---|---|---|---|
| Snappy platformer (Celeste-like) | ~0.05-0.1 s | ~0.03-0.06 s | faster than accel |
| Weighty action hero | 0.2-0.4 s | 0.2-0.3 s | slow, with a skid animation |
| Ice level | 0.5 s+ | 1 s+ | very slow |
| Top-down shooter | ~0.05 s | ~0.05 s | instant |
Separate **air** values (usually lower accel, much lower decel) to control air steering.

## Curves
For more character, accelerate by an AnimationCurve over normalized speed (fast initial push, slower
near max): `rate = accel * curve.Evaluate(|v| / maxSpeed)`. Keep the curve's effect testable by
graphing speed over time.

## Tuning workflow
- Expose all parameters live (inspector, ImGui) and tune while playing.
- Plot velocity over time in a debug graph; compare against a reference game capture.
- Lock tuning per character in data assets; note frame-rate independence tests at 30/60/144 fps.

## Verify
- [ ] Time to max speed measured in game matches the parameter (+-1 frame) at 30, 60 and 144 fps.
- [ ] Reversing direction uses turnaround rate (visible skid/turn timing).
- [ ] Air control values differ from ground and feel intentional in playtests.
