---
id: computing-software.game-programming.unity.job-system-burst-and-dots
name: job-system-burst-and-dots
category: computing-software
field: game-programming
product: unity
tags: [unity, job-system, burst, dots, entities, nativearray, ijob, ijobparallelfor, native-container, safety-system, multithreading, data-oriented-design, simd, entities-package, game-programming]
level: advanced
status: draft
description: "Move hot loops off the main thread in Unity with the C# Job System and Burst, and know when full DOTS/Entities is and isn't worth adopting."
sources: ["https://docs.unity3d.com/Manual/JobSystem.html", "https://docs.unity3d.com/Packages/com.unity.burst@latest", "https://docs.unity3d.com/Packages/com.unity.entities@latest"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Job System, Burst, and DOTS in Unity

**Goal:** get real multithreaded speedup out of Unity without data races, and know
the (narrow) line where adopting full Entities/DOTS pays for its complexity versus
where a plain Job + Burst on MonoBehaviour data is enough.

## The three layers, and which to reach for
1. **Burst alone** — compile a static/`[BurstCompile]` method with
   SIMD-friendly math. Single-threaded speedup (often 2-10x) for tight numeric
   loops, zero architectural change. Try this first.
2. **C# Job System** (`IJob`, `IJobParallelFor`) — schedule work on worker threads
   operating on `NativeArray<T>`/`NativeList<T>`, combined with Burst for the real
   win. This is the right tool for "transform 50k particle positions" or "batch
   raycasts" without rewriting your game as ECS.
3. **DOTS/Entities** — a full data-oriented rewrite (Entities, Systems, Components
   as pure data, Archetypes). Worth it only when you have thousands-to-millions of
   homogeneous simulated things (RTS units, voxel/boids/crowd sims) and have
   profiled that GameObject overhead itself (not just a specific loop) is the
   bottleneck. Mixing Entities with MonoBehaviour-heavy existing code is a real
   rewrite, not a bolt-on — do not start here for a normal gameplay-heavy project.

## Writing a job
```csharp
[BurstCompile]
struct MoveJob : IJobParallelFor {
    public NativeArray<float3> positions;
    [ReadOnly] public NativeArray<float3> velocities;
    public float deltaTime;
    public void Execute(int i) => positions[i] += velocities[i] * deltaTime;
}
...
var job = new MoveJob { positions = posArray, velocities = velArray, deltaTime = Time.deltaTime };
JobHandle handle = job.Schedule(posArray.Length, 64);   // 64 = inner batch count, tune per job
handle.Complete();   // blocks main thread until done — or Combine() and defer Complete to next frame
```
`[ReadOnly]`/`[WriteOnly]` attributes on `NativeArray` fields tell the safety
system which jobs can run concurrently on overlapping data; mark them accurately
or you lose parallelism (or get a safety exception) for no reason.

## The Job Safety System will stop you — read the error
Unity injects race-condition and lifetime checks in the Editor (stripped in
release builds). The two errors you'll hit constantly:
- **"You are trying to read/write [...] but you have not registered for read or
  write"** — you captured a `NativeArray` the job doesn't declare access to, or
  two scheduled jobs both write the same container without a dependency between
  them (fix with `JobHandle.CombineDependencies` or chain `job2.Schedule(job1Handle)`).
- **"has been deallocated"** — a `NativeArray` with `Allocator.Temp` outlived its
  frame, or you disposed it before `Complete()` ran. `Allocator.TempJob` is for
  arrays that live one or a few frames inside job scheduling; `Allocator.Persistent`
  for longer-lived data you manage and must `Dispose()` yourself — a leaked
  `NativeArray` throws a loud warning on domain reload, not a silent leak.

## Burst-specific gotchas
- No managed types, no exceptions-as-control-flow, no `string`, no boxing, no
  virtual calls inside `[BurstCompile]` code — it compiles to native code ahead of
  time; anything requiring the .NET runtime fails to compile with a (sometimes
  cryptic) Burst error pointing at the offending line.
- Burst recompiles can be slow; use the Burst Inspector (Jobs → Burst → Open
  Inspector) to check actual generated assembly/vectorization when chasing the
  last bit of performance, not before.
- Test with Burst **disabled** (Jobs → Burst → Enable Compilation off) occasionally
  — Burst-compiled and non-Burst code can behave differently on float edge cases
  (NaN, denormals) if you're not careful with `math` vs `Mathf`.

## Verify
- [ ] Every scheduled `JobHandle` either has `.Complete()` called before its data
      is touched on the main thread, or is tracked and completed before the next
      frame reads it — no "race condition" console errors in a full play session.
- [ ] All `NativeArray`/`NativeList` allocations have a matching `Dispose()` (or
      use `Allocator.Temp` correctly scoped to the frame); no leak warnings on exit.
- [ ] Profiler (Timeline view) shows the job actually running on worker threads in
      parallel with the main thread, not serialized behind `Complete()` called too early.
- [ ] DOTS/Entities was adopted only after profiling showed GameObject/Transform
      overhead itself as the bottleneck, not assumed up front.
