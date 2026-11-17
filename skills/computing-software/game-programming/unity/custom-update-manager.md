---
id: computing-software.game-programming.unity.custom-update-manager
name: custom-update-manager
category: computing-software
field: game-programming
product: unity
tags: [unity, unity-update-manager, monobehaviour, update-loop, performance, game-programming]
level: practitioner
status: docs-checked
description: "Replace thousands of per-object Unity Update calls with one manager that ticks registered behaviours, cutting native-to-managed call overhead and fixing order."
sources: ["https://unity.com/blog/engine-platform/10000-update-calls", "https://docs.unity3d.com/Manual/ExecutionOrder.html", "https://docs.unity3d.com/ScriptReference/MonoBehaviour.Update.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom update manager

**Goal:** thousands of agents, bullets or props tick from one `Update` instead of one magic method each.

## Why it pays
Unity does not use reflection on every call: the first time a MonoBehaviour type is accessed, the script is inspected
for magic methods and the result is cached in per-method lists (an `Update` script joins the every-frame list). Each
call from that list is still a call from native C++ into managed C#, preceded by validity checks (active GameObject,
initialised, `Start` called), and it has a cost. In Unity's own test (a 2015 post, Unity 5.2.2, two iOS devices, 10,000
behaviours) a manager that looped over an array calling a custom `UpdateMe` method was about 5 times faster than
10,000 individual `Update` methods on IL2CPP. The author notes the test is not fair: the manager skips the checks Unity
does, and a real manager would be more complex and slower. Treat the figure as direction, and profile your own game.

## Pattern
```csharp
public interface ITickable { void Tick(float dt); }

public sealed class UpdateManager : MonoBehaviour {
    static readonly List<ITickable> items = new(1024);
    static readonly List<ITickable> pendingRemove = new();
    static bool iterating;
    public static void Register(ITickable t)   => items.Add(t);
    public static void Unregister(ITickable t) { if (iterating) pendingRemove.Add(t); else items.Remove(t); }
    void Update() {
        float dt = Time.deltaTime; iterating = true;
        for (int i = 0; i < items.Count; i++) items[i].Tick(dt);
        iterating = false;
        foreach (var t in pendingRemove) items.Remove(t);
        pendingRemove.Clear();
    }
}

public class Mover : MonoBehaviour, ITickable {
    void OnEnable()  => UpdateManager.Register(this);
    void OnDisable() => UpdateManager.Unregister(this);
    public void Tick(float dt) => transform.position += Vector3.forward * dt;
}
```
- Register in `OnEnable`, unregister in `OnDisable` so disabled objects stop ticking like a real `Update`.
- The manager must handle what Unity's loop handles for you (destroyed objects, objects created mid-loop); the deferred
  removal above is one such case.
- The blog post's manager iterated an array rather than a `List<T>` and measured it faster for 10,000 elements.

## Order
The order of `Update` between different objects of the same script is not something you can set. To order different
scripts, use Script Execution Order (Edit > Project Settings > Script Execution Order, per the blog post; the manual
page "Script execution order" covers it). One manager with an explicit list gives you an explicit order.

## Variants
- Separate lists for Update, LateUpdate and fixed-step so order is explicit.
- When the work is pure data, move to Jobs/Burst or ECS instead; the manager is the step before.

## Gotchas
- Keep empty magic methods out of every script: the blog shows a `BaseMonoBehaviour` base class with empty virtual
  `Awake`, `Start`, `OnEnable`, `OnDisable`, `Update`, `LateUpdate`, `FixedUpdate` puts every behaviour in all the lists,
  so each is called every frame doing nothing.
- A static list outlives a stopped play session if domain reload is disabled; clear it at startup yourself.

## Checked
Date: 2026-11-07.
Read in full: the "10000 Update() calls" Unity blog post (How Update is called, execution order, empty-method base
class, the 10,000-behaviour test, array vs List, the "not completely fair" caveat); the Event function execution order
manual page (Limitations: no control over order between instances of the same script; Script execution order for
different scripts); the MonoBehaviour.Update script reference page (short).
Removed as unconfirmed: "found by reflection at load" (the blog says the opposite), "several times faster" (now the
blog's 5x with its caveats), the "under ~200 / above ~1,000" thresholds, the `BehaviourUpdate` profiler marker name,
`[DefaultExecutionOrder]`, the `[RuntimeInitializeOnLoadMethod]` clear, the exception-aborts-loop remark, the O(n)
remove advice, and the invented Verify checklist.
Method: documentation only; no commands were run.
