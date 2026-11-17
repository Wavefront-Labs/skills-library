---
id: computing-software.software-engineering.csharp-dotnet.benchmarkdotnet-microbenchmarks
name: benchmarkdotnet-microbenchmarks
category: computing-software
field: software-engineering
product: csharp-dotnet
tags: [csharp, dotnet-testing-practice, dotnet-performance, benchmarkdotnet, microbenchmarks, memorydiagnoser, baseline]
level: advanced
status: docs-checked
description: "Write trustworthy .NET micro-benchmarks with BenchmarkDotNet: Release builds, MemoryDiagnoser, params, baselines, returning results, comparing runtimes."
sources: ["https://benchmarkdotnet.org/articles/overview.html", "https://benchmarkdotnet.org/articles/guides/good-practices.html", "https://learn.microsoft.com/en-us/dotnet/core/diagnostics/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BenchmarkDotNet

```csharp
[MemoryDiagnoser]
[SimpleJob(RuntimeMoniker.Net80), SimpleJob(RuntimeMoniker.Net90)]       // stacked jobs compare runtimes
public class JoinBench
{
    [Params(10, 1000)] public int N;
    private string[] _items = default!;

    [GlobalSetup] public void Setup() => _items = Enumerable.Range(0, N).Select(i => i.ToString()).ToArray();

    [Benchmark(Baseline = true)] public string Concat() { var s = ""; foreach (var i in _items) s += i; return s; }
    [Benchmark] public string StringJoin() => string.Join("", _items);
    [Benchmark] public string Builder() { var sb = new StringBuilder(); foreach (var i in _items) sb.Append(i); return sb.ToString(); }
}
// Program.cs
BenchmarkRunner.Run<JoinBench>();      // or BenchmarkSwitcher.FromAssembly(typeof(Program).Assembly).Run(args)
```
```bash
dotnet run -c Release
```

## What the docs state
- Benchmarks run only in Release; BenchmarkDotNet reports an error otherwise. The good-practices page says never to benchmark Debug builds (it cites 10-100x slower code) and to enable optimisation with `<Optimize>true</Optimize>`.
- Avoid an attached debugger; run from the command line.
- Use each calculation's result (return it) because an unused result may let the JIT remove the code.
- Close other applications (including Visual Studio); on laptops stay plugged in with maximum performance power mode.
- Results vary across runtimes, JITs, architectures and operating systems; test each environment rather than generalising.
- `Baseline = true` adds a Ratio column relative to the baseline method.
- `[Params]` runs the benchmark for every combination of values.
- `[MemoryDiagnoser]` adds GC and allocation columns (Gen 0, Allocated). `ThreadingDiagnoser` reports lock contention and thread pool data (.NET Core 3.0+).
- Stacked `[SimpleJob(RuntimeMoniker...)]` attributes run the same benchmark on several runtimes.
- Exporters such as `MarkdownExporter`, `HtmlExporter`, `CsvExporter` are added by attribute.

## Practitioner advice (not stated on the cited pages)
- Prefer `[GlobalSetup]` over `[IterationSetup]`; benchmark realistic sizes with `[Params]`.
- Microbenchmarks mislead: confirm with a load test or trace. Shared CI runners are noisy, so allocation counts are steadier than time for regression gates.
- Keep BenchmarkDotNet in a separate console project.

## Verify
Run twice; ratios agree within error; the report shows the expected allocation drop for the optimised version.

## Checked
Method: 2026-11-08 docs-only read of the BenchmarkDotNet overview and good-practices pages. Release-build, dead-code, baseline, Params, diagnoser and runtime-job claims match. The dotnet diagnostics landing page was not used for specific claims. Dropped unsupported claims (BDN refusing debug builds is stated as an error report only; `DisassemblyDiagnoser`, `HardwareCounters`, `DOTNET_TieredPGO` and async-return notes removed). Experience-based advice is labelled as such.
