---
id: computing-software.game-programming.unity.runtime-prefab-spawning
name: runtime-prefab-spawning
category: computing-software
field: game-programming
product: unity
tags: [unity, prefab, instantiate, instantiateasync, objectpool, object-pooling, runtime-spawning, game-programming]
level: practitioner
status: docs-checked
description: "Spawn Unity prefabs at runtime from serialized references: typed Instantiate overloads, InstantiateAsync batches and the ObjectPool class."
sources: ["https://docs.unity3d.com/ScriptReference/Object.Instantiate.html", "https://docs.unity3d.com/ScriptReference/Object.InstantiateAsync.html", "https://docs.unity3d.com/ScriptReference/Pool.ObjectPool_1.html", "https://docs.unity3d.com/Manual/instantiating-prefabs.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Runtime prefab spawning

**Goal:** spawn enemies, projectiles and pickups from prefab references at runtime.

## Reference the prefab by its component type
```csharp
[SerializeField] Enemy enemyPrefab;   // drag the prefab asset in the Inspector
Enemy e = Instantiate(enemyPrefab, spawnPoint.position, spawnPoint.rotation, enemiesRoot);
```
- `Instantiate` clones script instances directly: Unity clones the whole GameObject hierarchy and returns the cloned
  script instance. The generic form `Instantiate<T>(T original, ...)` returns `T`, so no `GetComponent` call is needed.
- Overloads exist for: nothing extra; a `Transform` parent (with or without keeping world position); a position and
  rotation (world space, no parent); position, rotation and parent; a `Scene`; and `InstantiateParameters`.
- The plain overload gives the clone no parent even if the original had one. The clone keeps the original's active
  state. `Awake` and `OnEnable` run on the clone and its hierarchy only if the object is active in the hierarchy when you
  call `Instantiate`.
- `Instantiate` does not create a prefab connection (that is `PrefabUtility.InstantiatePrefab`, Editor only).
- Cloning deep hierarchies is limited to avoid a stack overflow; beyond half the stack size Unity throws
  `InsufficientExecutionStackException`.

## Async instantiation
```csharp
var op = InstantiateAsync(enemyPrefab, 50, positions, rotations);   // AsyncInstantiateOperation<Enemy>
```
`InstantiateAsync<T>` returns an `AsyncInstantiateOperation<T>` holding the resulting objects. Overloads take a count, an
optional parent, `ReadOnlySpan<Vector3>` positions and `ReadOnlySpan<Quaternion>` rotations, and some take
`InstantiateParameters` and a `CancellationToken`. The operation is mainly asynchronous, but the last stage (integration
and awake calls) runs on the main thread. It can be cancelled, or the integration stage delayed with
`allowSceneActivation`.

## Pooling with ObjectPool<T>
`UnityEngine.Pool.ObjectPool<T>` is a stack-based pool for reusing instances to reduce the overhead of frequent
instantiating and destroying.
```csharp
pool = new ObjectPool<Projectile>(
    createFunc: () => Instantiate(projectilePrefab),
    actionOnGet: p => p.gameObject.SetActive(true),
    actionOnRelease: p => p.gameObject.SetActive(false),
    actionOnDestroy: p => Destroy(p.gameObject),
    collectionCheck: true, defaultCapacity: 64, maxSize: 512);
```
- `Get()` returns an instance, calling `createFunc` if the pool is empty. `Release(item)` returns it; if the pool has
  reached `maxSize` the item is destroyed through `actionOnDestroy`.
- `collectionCheck` makes the pool catch double-release mistakes when returning an item.
- Do not call `ObjectPool<T>` from background threads; do not assume pooled objects are contiguous in memory.
- Counters: `CountActive`, `CountInactive`, `CountAll`.

## Verify
- [ ] Spawned objects appear at the right pose (position and rotation passed in the `Instantiate` call).
- [ ] Every `Get()` is matched by a `Release()`.

## Checked
Date: 2026-11-09. Read in full: Script Reference Object.Instantiate (overload list and remarks), Object.InstantiateAsync
(overload list and remarks) and Pool.ObjectPool_1; the manual page "Instantiating prefabs at runtime" is only an index of
topics. Removed as not confirmed on those pages: the "Unity 2022.3.20+/Unity 6" availability claim, Rigidbody pop and
second-move advice, the claim that copying runs off the main thread, GC.Alloc claims, `Resources.Load` and Addressables
advice, deep-parent transform cost, and the pre-warm and Profiler advice.
Method: docs-checked 2026-11-09 against the four Unity pages named above.
