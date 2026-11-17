---
id: computing-software.software-engineering.java.jmh-microbenchmarks
name: jmh-microbenchmarks
category: computing-software
field: software-engineering
product: java
tags: [java, java-performance, jmh, microbenchmark, blackhole, benchmark-forks, gc-profiler, dead-code-elimination]
level: advanced
status: docs-checked
description: "Write trustworthy JMH benchmarks: @State, @Benchmark, Blackhole, forks, parameterisation, profilers (-prof gc), and benchmark modes."
sources: ["https://github.com/openjdk/jmh", "https://github.com/openjdk/jmh/tree/master/jmh-samples/src/main/java/org/openjdk/jmh/samples"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMH microbenchmarks

Hand-rolled `System.nanoTime()` loops mislead because of dead-code elimination, constant folding and JIT profile effects. JMH handles those.

## A benchmark
```java
@BenchmarkMode(Mode.AverageTime) @OutputTimeUnit(TimeUnit.NANOSECONDS)
@State(Scope.Thread)
@Warmup(iterations = 3, time = 1) @Measurement(iterations = 5, time = 1) @Fork(2)
public class JoinBench {
    @Param({"10", "1000"}) int n;
    List<String> items;
    @Setup public void setup() { items = IntStream.range(0, n).mapToObj(Integer::toString).toList(); }

    @Benchmark public String stringJoin() { return String.join(",", items); }                     // returned value is implicitly consumed
    @Benchmark public void builder(Blackhole bh) {                                               // or sink via Blackhole
        var sb = new StringBuilder(); for (String s : items) sb.append(s).append(','); bh.consume(sb);
    }
}
```
```bash
java -jar target/benchmarks.jar JoinBench -prof gc
```
## Rules
1. Dead-code elimination removes work whose result is unused. Returned results are implicitly consumed by Blackholes; use an explicit `Blackhole` (itself a bundled `@State` object) only when sinking several values. Do not clutter code with explicit Blackholes otherwise.
2. The flip side is constant folding: if the compiler can predict a result it can move the computation outside the JMH loop. Take inputs from `@State` fields (non-final) rather than constants.
3. Avoid loops inside benchmark methods to amortise call overhead: loops get unrolled and the measured operation is hoisted. Rely on JMH's own loop.
4. JVMs are good at profile-guided optimisation, which can skew results run in one JVM. JMH forks by default; use `@Fork` (or `-f`) so each test runs in a fresh JVM, and `Fork(0)` only to run in the same JVM.
5. Profilers are selected with `-prof <name>` (and `-prof <name>:help` lists options): examples in the samples are `stack`, `gc`, `cl`, `comp`, and on Linux `perf`, `perfnorm` and `perfasm` (Windows `xperfasm`, macOS `dtraceasm`).
6. Modes: `Throughput`, `AverageTime`, `SampleTime` (samples execution time) and `SingleShotTime` (a single invocation).

## Gotchas
- `@Param` values (the samples vary several) can change which implementation wins; test more than one size.
- A microbenchmark result rarely predicts end-to-end gain; confirm with a load test or JFR.

## Checked

Method: docs-checked 2026-11-09 against the JMH sample sources JMHSample_02 (modes), 03 (states), 08 (dead code), 09 (blackholes), 10 (constant fold), 11 (loops), 12 (forking), 27 (params) and 35 (profilers) from raw.githubusercontent.com. The repository front page was not usable. Dropped unconfirmed claims (archetype and Gradle plugin, -rf and -rff flags, specific gc.alloc counter, async profiler, error-bar interpretation, baseline timing).
