---
id: computing-software.game-programming.godot.csharp-async-await-with-tosignal
name: csharp-async-await-with-tosignal
category: computing-software
field: game-programming
product: godot
tags: [godot, godot-csharp, tosignal, csharp-async, signal-awaiter, game-programming]
level: practitioner
status: docs-checked
description: "Use async/await in Godot C# with ToSignal: awaiting signals, SceneTreeTimer and process frames, timer pause behaviour, and a sequence-id cancellation pattern."
sources: ["https://docs.godotengine.org/en/stable/tutorials/scripting/c_sharp/c_sharp_signals.html", "https://docs.godotengine.org/en/stable/classes/class_scenetree.html#class-scenetree-method-create-timer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# async/await with ToSignal in Godot C#

**Goal:** sequential gameplay code (cutscenes, ability sequences) in C# without callback spaghetti.

## Basics
```csharp
public async void PlayIntro() {
    _anim.Play("intro");
    await ToSignal(_anim, AnimationPlayer.SignalName.AnimationFinished);
    await ToSignal(GetTree().CreateTimer(0.5), SceneTreeTimer.SignalName.Timeout);
    await ToSignal(GetTree(), SceneTree.SignalName.ProcessFrame);   // next frame
    _ui.Show();
}
```
Use the nested `SignalName` class of a node type to get signal names for `ToSignal` (documented on the C# signals
page; the `ProcessFrame` and `SceneTreeTimer.SignalName.Timeout` forms appear in the docs). Prefer
`SceneTreeTimer` waits for gameplay delays.

## SceneTreeTimer behaviour
`SceneTree.CreateTimer(timeSec, processAlways = true, processInPhysics = false, ignoreTimeScale = false)`:
- With the default `processAlways = true` the timer keeps running while the tree is paused; pass `false` to make it
  pause when `paused` is set.
- With `ignoreTimeScale = true` it ignores `Engine.TimeScale` and uses real elapsed time.

## Cancellation
`ToSignal` takes no cancellation token. A simple pattern is a sequence id checked after each await:
```csharp
int _seq;
async void Sequence() { int id = ++_seq; await ToSignal(...); if (id != _seq) return; ... }
void Cancel() => _seq++;
```
Before using nodes after an await, check `IsInstanceValid` on any object that may have been freed meanwhile.
Test what happens when the awaiting or emitting node is freed mid-sequence in your Godot version; the docs fetched
for this skill do not specify it.

## Gotchas
- Do not block the main thread with `.Result` or `.Wait()` on tasks that need the main thread to complete.
- Wrap fire-and-forget `async void` entry points in try/catch so failures are logged where you can see them.

## Verify
- [ ] Free the actor mid-sequence: no exceptions and no further steps run (test in your version).
- [ ] Pause the game during a timer await created with `processAlways = false`: the timer pauses.

## Checked
2026-10-28. Confirmed on the C# signals page and the SceneTree.create_timer reference: `ToSignal`/`SignalName` use,
ProcessFrame and timer-timeout awaits, `create_timer` parameters and defaults. Corrected: the old verify step claimed
timers pause with the game by default; per the reference they do not (process_always defaults to true). Removed (not
documented on the pages): synchronization-context and main-thread resume claims, freed-object behaviour in "recent
4.x", `Task.Delay` thread-pool claim, and `CallDeferred` advice.
Method: documentation only; no commands were run.
