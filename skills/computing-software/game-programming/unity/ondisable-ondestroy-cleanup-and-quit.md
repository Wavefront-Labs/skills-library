---
id: computing-software.game-programming.unity.ondisable-ondestroy-cleanup-and-quit
name: ondisable-ondestroy-cleanup-and-quit
category: computing-software
field: game-programming
product: unity
tags: [unity, monobehaviour, ondestroy-cleanup, onapplicationquit, ondisable, event-unsubscribe, application-quitting, onapplicationpause, game-programming, onapplicationfocus]
level: practitioner
status: docs-checked
description: "Clean up correctly in Unity: OnEnable/OnDisable event pairing, when OnDestroy runs, and OnApplicationPause, quitting and wantsToQuit by platform."
sources: ["https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnDisable.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnDestroy.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnApplicationQuit.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.OnApplicationPause.html", "https://docs.unity3d.com/ScriptReference/Application-quitting.html", "https://docs.unity3d.com/ScriptReference/Application-wantsToQuit.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# OnDisable, OnDestroy cleanup and quitting

**Goal:** no leaked event subscriptions and saves that actually happen on mobile.

## Pair subscriptions with enable state
```csharp
void OnEnable()  { GameEvents.PlayerDied += HandleDeath; health.Changed += UpdateBar; }
void OnDisable() { GameEvents.PlayerDied -= HandleDeath; health.Changed -= UpdateBar; }
```
`OnDisable` is called when:
- a component of an active GameObject is disabled in code or the Inspector;
- an enabled component's parent GameObject is deactivated;
- the component or its parent is destroyed with `Object.Destroy`;
- the scene is unloaded;
- scripts are reloaded as part of a domain reload.

So a symmetric `OnEnable/OnDisable` pair covers disable, destroy, unload and domain reload. `OnDisable`
cannot be a coroutine.

## OnDestroy
`OnDestroy` is called when:
- a component or its parent GameObject is destroyed with `Object.Destroy`;
- a scene ends or is unloaded (all GameObjects not preserved with `Object.DontDestroyOnLoad` are
  destroyed), including closing and opening scenes in the Editor;
- the runtime application quits or Play mode exits.

It is only called on GameObjects that have previously been active, and it cannot be a coroutine.
On mobile, if the OS quits a suspended app, Unity might be unable to call it, so do not rely on it to
save state.

## Quitting and backgrounding
| Callback | Behaviour per the docs |
|---|---|
| `OnApplicationQuit` | Sent to all active GameObjects before quitting, including disabled components (not inactive GameObjects). Called when exiting Play mode. Not called on iOS (apps suspend) or Web. |
| `Application.quitting` (static event) | Raised when the quit cannot be cancelled. Not raised on forced quit or crash. Raised when exiting Play mode. Not detected on Android pause. |
| `Application.wantsToQuit` (static `Func<bool>`) | Raised when quit has started but can still be cancelled: return false to cancel, true to continue. Return value ignored when exiting Play mode and has no effect on iOS or iPadOS. Not always raised on Android. |
| `OnApplicationPause(bool)` | true when the app pauses on losing focus, false on resume. Also called with false after `Awake` on first entering Play mode. Not called by the Editor Pause button. |
| `OnApplicationFocus(bool)` | Called when focus is lost or gained. |

For mobile saving, the docs say to treat every loss of application focus as an exit and use
`OnApplicationFocus` to save data. For Android pause, they recommend `OnApplicationFocus` or
`OnApplicationPause` instead of `quitting`/`wantsToQuit`. On Windows Store/UWP apps there is no quit
event, so use `OnApplicationFocus`.

## Verify
- [ ] Load and unload a scene repeatedly: event subscriber counts do not grow.
- [ ] Mobile: background the app, kill it from the task switcher, relaunch: progress saved.

## Checked

Method: docs-checked 2026-11-09 against the Unity script reference pages MonoBehaviour.OnDisable, MonoBehaviour.OnDestroy, MonoBehaviour.OnApplicationQuit, MonoBehaviour.OnApplicationPause, Application.quitting and Application.wantsToQuit (all read in full).
Removed as unconfirmed: "OnDisable always runs before OnDestroy", destroy order being undefined, the "Some objects were not cleaned up" error and the spawn-in-OnDestroy advice, the quitting-flag code sample, the "static events are the most common leak" claim, the resource-release list (NativeArray, Addressables, InputAction, materials), the 20-load verify figure, and the execution-order source.
