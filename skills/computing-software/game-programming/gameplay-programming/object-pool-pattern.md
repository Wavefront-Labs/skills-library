---
id: computing-software.game-programming.gameplay-programming.object-pool-pattern
name: object-pool-pattern
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, game-programming-patterns, object-pool-pattern, object-pooling, free-list, allocation, unity-objectpool, game-programming]
level: practitioner
status: draft
description: "Apply the Object Pool pattern: fixed vs growing pools, free lists, reset-on-acquire discipline, Unity's ObjectPool<T>, and the stale-reference bugs pooling introduces."
sources: ["https://gameprogrammingpatterns.com/object-pool.html", "https://docs.unity3d.com/ScriptReference/Pool.ObjectPool_1.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Object pool pattern

**Use when:** objects are created and destroyed frequently (bullets, particles, hit numbers, audio
voices) and allocation/instantiation cost or GC spikes show in the profiler. Don't pool things that
spawn rarely; pooling adds lifetime bugs.

## Core (Nystrom's free list)
```cpp
class ParticlePool {
    static const int N = 256;
    Particle items[N];
    Particle* firstFree;
public:
    ParticlePool() {
        firstFree = &items[0];
        for (int i = 0; i < N - 1; i++) items[i].next = &items[i + 1];
        items[N - 1].next = nullptr;
    }
    Particle* acquire() {                     // O(1)
        if (!firstFree) return nullptr;       // policy: fail, steal oldest, or grow
        Particle* p = firstFree; firstFree = p->next; p->init(); return p;
    }
    void release(Particle* p) { p->next = firstFree; firstFree = p; }
};
```
The free-list `next` pointer can share storage (union) with live data since dead objects don't use it.

## Unity ObjectPool<T>
```csharp
pool = new ObjectPool<Bullet>(
    createFunc: () => Instantiate(prefab),
    actionOnGet: b => b.gameObject.SetActive(true),
    actionOnRelease: b => b.gameObject.SetActive(false),
    actionOnDestroy: b => Destroy(b.gameObject),
    collectionCheck: true,            // editor: catches double release
    defaultCapacity: 64, maxSize: 512);
var b = pool.Get(); ... pool.Release(b);
```

## Policies when empty
| Policy | Fits |
|---|---|
| Return null / skip spawn | cosmetic particles, decals |
| Recycle the oldest live object | bullet holes, footprints |
| Grow (allocate more) | gameplay-critical objects; log growth to tune size |

## Bugs pooling introduces
- **Stale state:** reset every field on acquire (`init`/`OnGet`), including timers, velocities,
  subscribed events, trail renderers (`Clear()`), and coroutines.
- **Stale references:** something holds a pointer to an object that was released and reused for a
  different entity. Use generation counters or handles, and clear references on release.
- **Double release:** corrupts the free list; enable collection checks in debug.
- Released objects still receiving physics callbacks or timers: deactivate fully.

## Verify
- [ ] Profiler shows zero instantiate/GC allocations during sustained firing after warm-up.
- [ ] Pool size high-water mark logged; capacity set just above it.
- [ ] A reused bullet never carries the previous bullet's velocity, damage or trail.
