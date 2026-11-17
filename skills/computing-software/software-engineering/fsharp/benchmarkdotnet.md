---
id: computing-software.software-engineering.fsharp.benchmarkdotnet
name: benchmarkdotnet
category: computing-software
field: software-engineering
product: fsharp
tags: [fsharp, benchmarkdotnet, fsharp-perf-measure, benchmarks, memory-diagnoser]
level: advanced
status: draft
description: "Benchmark F# code with BenchmarkDotNet including MemoryDiagnoser, Release builds and fair baselines."
sources:
  - https://benchmarkdotnet.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# BenchmarkDotNet
**Goal:** measure, do not guess.

```fsharp
open BenchmarkDotNet.Attributes
open BenchmarkDotNet.Running

[<MemoryDiagnoser>]
type Sums() =
    let data = Array.init 10_000 id

    [<Benchmark(Baseline = true)>]
    member _.Loop() =
        let mutable acc = 0
        for x in data do acc <- acc + x
        acc

    [<Benchmark>]
    member _.Seq() = data |> Seq.sum

    [<Benchmark>]
    member _.Array() = data |> Array.sum

[<EntryPoint>]
let main _ = BenchmarkRunner.Run<Sums>() |> ignore; 0
```
```bash
dotnet run -c Release
```
- Always run in Release without a debugger attached; BenchmarkDotNet refuses unoptimised builds by default.
- Benchmark classes are classes with `[<Benchmark>]` members; `[<GlobalSetup>]` initialises data.
- `[<MemoryDiagnoser>]` adds allocation columns; look at Gen0 and Allocated.
- Return results (or use `Consumer`) so the JIT cannot eliminate the work.
- `[<Params(10, 100)>]` parameterises runs.

## Gotchas
- Benchmarks of `let mutable` captured in closures are not comparable to their allocation-free form.
- Results vary with machine state; close other apps, fix the power plan.

## Self-check
Run it and confirm the table lists mean, error and allocated bytes per method.
