---
id: computing-software.game-programming.unreal-engine.ftimermanager-timers
name: ftimermanager-timers
category: computing-software
field: game-programming
product: unreal-engine
tags: [unreal-engine, uclass, ftimermanager, timer-handle, settimer, game-programming]
level: practitioner
status: docs-checked
description: "Use Unreal FTimerManager timers: SetTimer, looping and first delay, handles, pause/clear, next-tick timers, per-object clearing and what the docs say about destroyed objects."
sources: ["https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-timers-in-unreal-engine", "https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/FTimerManager"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timers with FTimerManager

**Goal:** delayed and repeating gameplay logic without per-frame Tick.

## Which manager
`FTimerManager` exists on the Game Instance and on each World. `AActor::GetWorldTimerManager` reaches the
World's manager (via `UWorld::GetTimerManager`); `UGameInstance::GetTimerManager` is the global one, also the
fallback if a World has none, and suits calls that should not depend on a specific World.

## Set, repeat, clear
```cpp
// Call RepeatingFunction once per second, starting two seconds from now.
GetWorldTimerManager().SetTimer(MemberTimerHandle, this, &AMyActor::RepeatingFunction, 1.0f, true, 2.0f);
...
GetWorldTimerManager().ClearTimer(MemberTimerHandle);   // handle can now be reused
```
(The example is from the Gameplay Timers page; the arguments are handle, object, method, rate, loop, first delay.)
- `SetTimer` fills an `FTimerHandle`, used to pause, query or cancel the timer.
- `SetTimer` with a rate less than or equal to zero is identical to `ClearTimer`.
- Calling `SetTimer` with an existing handle clears that timer and replaces it with a new one.
- Setting timers inside a function called by a timer is safe, including reusing the same handle.
- `ClearAllTimersForObject(Object)` clears all timers bound to functions on that object.
- `SetTimerForNextTick` runs on the next frame. The Gameplay Timers page says it does not fill out a timer
  handle; the 5.x API page lists it as returning `FTimerHandle`, so check your engine version before relying on either.
- Callbacks may be function pointers, `TFunction` or delegates (including dynamic delegates for UFunctions).

## Pause and query
- `PauseTimer` / `UnPauseTimer`: a paused timer does not fire; elapsed and remaining times stay the same.
- `IsTimerActive` (exists and not paused), `IsTimerPaused`, `IsTimerPending`, `TimerExists`.
- `GetTimerRate`, `GetTimerElapsed`, `GetTimerRemaining` return -1 for an invalid handle; elapsed plus remaining
  should equal the rate. A timer's rate cannot be changed directly: call `SetTimer` again with the same handle.

## Lifetime and threads
- Timers are cancelled automatically if the Object they would call, such as an Actor, is destroyed first; the handle
  becomes invalid and the function is not called.
- The timer code is not thread safe and asserts if accessed outside the game thread (Known Issues).

## Verify
- [ ] Destroy the actor with a timer pending: the callback never fires and the handle is invalid.
- [ ] A repeating timer stops after `ClearTimer` and the same handle can start a new timer.

## Checked
Date: 2026-11-07.
Read in full: Gameplay Timers (Timer Management, Setting and Clearing, Pausing, Timer Information, Known Issues)
and the FTimerManager API page (class page including the Public function table), from dev.epicgames.com.
The two pages differ on whether `SetTimerForNextTick` returns a handle; both are reported above.
Removed as unconfirmed: `CreateWeakLambda` / `CreateLambda` guidance, time-dilation and pause behaviour,
looping catch-up bursts, Blueprint `Delay`/Set Timer nodes, constructor/CDO advice, replication advice.
Method: documentation only; no commands were run.
