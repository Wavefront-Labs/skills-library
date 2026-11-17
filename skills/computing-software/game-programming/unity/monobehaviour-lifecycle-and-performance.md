---
id: computing-software.game-programming.unity.monobehaviour-lifecycle-and-performance
name: monobehaviour-lifecycle-and-performance
category: computing-software
field: game-programming
product: unity
tags: [unity, unity6, csharp, monobehaviour, update, fixedupdate, lateupdate, physics, script-execution-order, object-pooling, coroutines, awaitable, game-programming]
level: practitioner
status: docs-checked
description: "Where Unity runs physics, animation, rendering and coroutine callbacks relative to MonoBehaviour events, what order is not guaranteed, and how ObjectPool<T> reuses instances."
sources: ["https://docs.unity3d.com/Manual/execution-order.html", "https://docs.unity3d.com/ScriptReference/Pool.ObjectPool_1.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MonoBehaviour event order and ObjectPool

**Goal:** know when Unity runs each kind of callback, and reuse frequently spawned objects. Unity 6000.x docs.

## Event function order
The manual's diagram (an image, not reproduced in the text) shows the key parts of the MonoBehaviour lifecycle; the full
Player loop is longer. Retrieve it with the `PlayerLoop` API, which can also remove systems, add your own, and change
order. Per-callback meaning is in the Messages section of the MonoBehaviour API reference.

- **Physics step** (collision detection, Rigidbody and joint integration, writing poses back to Transforms, and the physics
  callbacks such as `OnTriggerEnter/Stay/Exit`, `OnCollisionEnter/Stay/Exit`, `OnJointBreak`, `OnParticleCollision`,
  `OnParticleTrigger`, including the 2D versions) runs:
  - directly after `FixedUpdate` when `Physics.simulationMode` / `Physics2D.simulationMode` is `FixedUpdate`;
  - directly after `Update` in `Update` mode;
  - when you call `Physics.Simulate` / `Physics2D.Simulate` in `Script` mode.
- **Animation**: `MonoBehaviour.OnAnimatorMove` and `OnAnimatorIK` are called from the animation loop; `StateMachineBehaviour`
  adds `OnStateEnter`, `OnStateUpdate`, `OnStateExit`, `OnStateMove`, `OnStateIK`, `OnStateMachineEnter`,
  `OnStateMachineExit`. The Profiler markers show when they run.
- **Rendering** (Built-in Render Pipeline order; the SRP pipelines document their own): `OnPreCull`, `OnBecameVisible` /
  `OnBecameInvisible`, `OnWillRenderObject` (once per camera if visible), `OnPreRender`, `OnRenderObject`, `OnPostRender`,
  `OnRenderImage`, `OnGUI` (several times per frame), `OnDrawGizmos`. `OnPreCull`, `OnPreRender`, `OnPostRender` and
  `OnRenderImage` are called only on scripts on the same object as an enabled Camera; elsewhere use `Camera.onPreCull`,
  `Camera.onPreRender`, `Camera.onPostRender`. For work just before rendering see `Application.onBeforeRender`.
- **Coroutines and async**: coroutines resume at different points per yield instruction (`WaitForEndOfFrame` at end of
  frame, `WaitForFixedUpdate` at the end of the fixed update step). Regular .NET Tasks and async methods resume in the
  `Update` phase. `Awaitable` can resume at different points depending on the method awaited. The order between resuming
  coroutines and async tasks is not guaranteed.
- **Limits:** you cannot rely on the order in which the same event function runs on different GameObjects, or on different
  instances of one script (including parent and child), unless the order is documented or settable. Use Script execution
  order to order different MonoBehaviour scripts.
- With Entities, ECS system group updates are merged into the Player loop; the Entities Systems window shows their order.
- Code outside the MonoBehaviour lifecycle: `Unity.Scripting.LifecycleManagement` callbacks and Play mode entry/exit
  attributes in the `UnityEngine` and `UnityEditor.Scripting.LifecycleManagement` namespaces.

## ObjectPool<T>
`UnityEngine.Pool.ObjectPool<T>` (where T : class) is a stack-based pool that reduces the cost of frequent instantiate and
destroy. Constructor delegates: `createFunc`, `actionOnGet`, `actionOnRelease`, `actionOnDestroy`, plus `collectionCheck`
(catches double-release), `defaultCapacity`, `maxSize`.
```csharp
pool = new ObjectPool<GameObject>(
    createFunc: CreateItem, actionOnGet: OnGet, actionOnRelease: OnRelease, actionOnDestroy: OnDestroyItem,
    collectionCheck: true, defaultCapacity: 10, maxSize: 50);
var obj = pool.Get();   // creates one with createFunc if the pool is empty
pool.Release(obj);      // destroyed with actionOnDestroy if the pool is at maxSize
```
- Not safe to call from background threads; pooled instances are not physically contiguous.
- Properties: `CountActive`, `CountAll`, `CountInactive`. `Clear` and `Dispose` remove all pooled items, calling the destroy
  action for each.

## Checked
Date: 2026-11-07.
Read in full: "Event function execution order" manual page and the `ObjectPool<T>` script reference (6000.6 docs, including
its example). The Profiler manual page is only a table of contents of links, so it was dropped from sources.
Removed as unconfirmed: the Awake/OnEnable/Start/OnDisable/OnDestroy table and "touch others in Start" rule, the 0.02 s
fixed timestep default, `[DefaultExecutionOrder]`, the Rigidbody `Mover` sample, Interpolate, `MovePosition` advice, legacy
Input remarks and `linearVelocity` rename, GC-allocation lists (`GetComponent`, `Camera.main`, LINQ, `NonAlloc` physics),
Incremental GC, `[SerializeField]`/ScriptableObject/prefab variant advice, the Profiler workflow (GC Alloc sorting, frame
budgets, Deep Profile) and the invented Verify checklist.
Method: documentation only; no commands were run.
