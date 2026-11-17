---
id: computing-software.game-programming.unity.defaultexecutionorder-and-script-order
name: defaultexecutionorder-and-script-order
category: computing-software
field: game-programming
product: unity
tags: [unity, monobehaviour, defaultexecutionorder, script-execution-order-settings, execution-order, game-programming]
level: practitioner
status: docs-checked
description: "Control cross-script ordering in Unity with DefaultExecutionOrder and Script Execution Order settings instead of relying on undefined Awake/Update order."
sources: ["https://docs.unity3d.com/ScriptReference/DefaultExecutionOrder.html", "https://docs.unity3d.com/Manual/class-MonoManager.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DefaultExecutionOrder and Script Execution Order

**Goal:** deterministic ordering between scripts (managers before consumers, movers before cameras)
without sprinkling `Invoke`/`yield return null` hacks.

## Facts
- Scripts with the same configured order, or all at the default order, run in a non-deterministic
  order. It may look consistent in testing but is not guaranteed across builds, machines or Unity
  versions.
- Assets imported from the Asset Store may use the same order values as your scripts; set distinct
  values after import if you rely on ordering.
- Order applies to lifecycle events Unity calls on all active GameObjects, such as `Awake()` and
  `OnEnable()`. It does not guarantee order for callbacks that can happen at any time, such as
  `OnTriggerEnter`.
- Scripts run lowest value first, highest last (for example -200, -100, -50, 50, 100, 200). Scripts not
  listed run in the Default Time slot: after negative values and before positive values.

## Two ways to set it
```csharp
[DefaultExecutionOrder(-100)]   // lower runs earlier
public class GameServices : MonoBehaviour { void Awake() => Instance = this; }
```
Edit > Project Settings > Script Execution Order: add scripts with the plus button, drag them or edit
the integer values. The Editor stores the values in the script metadata files. If the attribute and the
Project Settings give different values for the same class, Unity uses the Editor value, and the
attribute order does not show in that window.

## Suggested bands (a convention, not an Unity rule)
| Order | Use |
|---|---|
| -1000 | bootstrap / service registration |
| -100 | input gathering |
| 0 | gameplay |
| 100 | cameras following gameplay |
| 200 | UI that reads camera / gameplay |

Leave gaps between values so adding a script does not force edits to the others.

## Better than ordering
- For managers, lazy accessors or explicit init from a single bootstrap script remove the dependency
  entirely.
- A single update manager that calls systems in a fixed list is the most explicit order.

## Verify
- [ ] Log `Time.frameCount` and script name in each Awake; order matches the table in a player build.
- [ ] Removing a `yield return null` workaround still works after ordering is set.

## Checked
2026-11-01. Confirmed against the DefaultExecutionOrder script reference and the Script Execution
Order project settings page: lowest-first ordering, Default Time slot, non-deterministic ties, the
Editor value winning over the attribute, metadata storage, and lifecycle versus event callbacks.
Removed unconfirmed claims: Update/LateUpdate/FixedUpdate ordering, loaded-together Awake behaviour,
Awake-before-Start and additive-scene rules, plugin extreme orders and subclass inheritance of the
attribute. The suggested bands are a labelled convention.
Method: documentation only; no commands were run.
