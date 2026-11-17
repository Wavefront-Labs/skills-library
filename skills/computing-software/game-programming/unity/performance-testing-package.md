---
id: computing-software.game-programming.unity.performance-testing-package
name: performance-testing-package
category: computing-software
field: game-programming
product: unity
tags: [unity, performance-testing-extension, performance-tests, unity-test-framework, benchmarking, game-programming]
level: practitioner
status: draft
description: "Write Unity Performance Testing package tests: Measure.Method, Measure.Frames, ProfilerMarkers sampling, warmup and iteration counts, and comparing results across runs in CI."
sources: ["https://docs.unity3d.com/Packages/com.unity.test-framework.performance@3.0/manual/index.html", "https://docs.unity3d.com/Packages/com.unity.test-framework.performance@3.0/manual/measure-method.html", "https://docs.unity3d.com/Packages/com.unity.test-framework.performance@3.0/manual/measure-frames.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Performance Testing package

**Goal:** automated, repeatable performance measurements that fail CI on regressions.

## Install
`com.unity.test-framework.performance`; reference `Unity.PerformanceTesting` in the test asmdef.

## Method benchmarks (edit or play mode)
```csharp
[Test, Performance]
public void Pathfinding_100x100() {
    var grid = TestGrids.Open(100, 100);
    Measure.Method(() => AStar.Find(grid, start, goal))
        .WarmupCount(5).MeasurementCount(20).IterationsPerMeasurement(10)
        .GC()                      // also record GC allocations
        .Run();
}
```

## Frame measurements (play mode)
```csharp
[UnityTest, Performance]
public IEnumerator CombatScene_FrameTime() {
    yield return SceneManager.LoadSceneAsync("PerfCombat");
    yield return Measure.Frames().WarmupCount(30).MeasurementCount(300)
        .ProfilerMarkers("PlayerLoop", "Physics.Simulate", "Camera.Render").Run();
}
```
`Measure.Scope()` measures a code block; `Measure.Custom(new SampleGroup("Memory", SampleUnit.Megabyte), value)`
records anything.

## Results
Run via Test Runner or command line (`-runTests -testPlatform PlayMode -perfTestResults results.json`).
Results JSON holds median, min, max, std dev per sample group. Compare against a baseline in CI with
your own script or the Performance Benchmark Reporter tool, flagging median regressions beyond a
threshold (5-10%).

## Gotchas
- Editor measurements are noisy; run perf suites in players on dedicated hardware, same device every
  run, VSync off, fixed resolution.
- Use medians and enough measurements; single runs swing with thermal throttling.
- Keep fixtures deterministic (fixed seeds, scripted camera path).

## Verify
- [ ] Perf suite produces a JSON per build; dashboard or CI step shows trend and fails on regression.
