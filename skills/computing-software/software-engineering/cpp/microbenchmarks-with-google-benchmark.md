---
id: computing-software.software-engineering.cpp.microbenchmarks-with-google-benchmark
name: microbenchmarks-with-google-benchmark
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, c++, google-benchmark, microbenchmarks, performance, dooptimize, benchmark-compare, nanobench]
level: practitioner
status: docs-checked
description: "Write trustworthy C++ microbenchmarks with Google Benchmark: fixtures and ranges, DoNotOptimize/ClobberMemory, complexity, repetitions and stats, CPU scaling noise and compare.py."
sources: ["https://github.com/google/benchmark/blob/main/docs/user_guide.md", "https://github.com/google/benchmark/blob/main/docs/tools.md", "https://github.com/google/benchmark/blob/main/docs/reducing_variance.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Microbenchmarks with Google Benchmark

**Goal:** measure small pieces of C++ code with numbers you can trust and compare, not artefacts
of the optimiser or a noisy machine.

## Setup (CMake)
```cmake
include(FetchContent)
FetchContent_Declare(benchmark GIT_REPOSITORY https://github.com/google/benchmark.git GIT_TAG <release-tag>)
FetchContent_MakeAvailable(benchmark)
add_executable(bench bench/parse_bench.cpp)
target_link_libraries(bench PRIVATE mylib benchmark::benchmark_main)
```
Build in **Release** (optimised, with `-g` for profiling); numbers from an unoptimised build are meaningless.

## A benchmark
```cpp
#include <benchmark/benchmark.h>

static void BM_Parse(benchmark::State& state) {
    std::string input = make_input(state.range(0));      // setup outside the loop
    for (auto _ : state) {
        auto result = parse(input);
        benchmark::DoNotOptimize(result);                // keep result "used"
    }
    state.SetBytesProcessed(state.iterations() * input.size());
    state.SetComplexityN(state.range(0));
}
BENCHMARK(BM_Parse)->RangeMultiplier(4)->Range(64, 64 << 10)->Complexity(benchmark::oN);
```
- `DoNotOptimize(x)` forces x to be materialised; `ClobberMemory()` forces pending writes to
  memory. Without them the compiler may delete the work you are measuring.
- Per-iteration setup that must not be timed: `state.PauseTiming()` / `ResumeTiming()` (they have
  overhead of their own; prefer batching setup).
- `->Args({a, b})`, `->ArgsProduct(...)`, `->Unit(benchmark::kMicrosecond)`, `->UseRealTime()` for
  multithreaded or I/O work, `->Threads(4)`, `->MinTime(2.0)` (or `--benchmark_min_time=2.0`, in seconds).
- Fixtures: `class F : public benchmark::Fixture` with `SetUp`/`TearDown`, `BENCHMARK_F`.
- Counters: `state.counters["items"] = benchmark::Counter(n, benchmark::Counter::kIsRate)`.

## Running
```bash
./bench --benchmark_filter=Parse --benchmark_repetitions=10 \
        --benchmark_report_aggregates_only=true --benchmark_out=new.json --benchmark_out_format=json
```
Repetitions give aggregate statistics (mean, median, standard deviation, coefficient of variation); look at the median and the spread.

## Reduce noise
- Disable CPU frequency scaling (`sudo cpupower frequency-set --governor performance`; the library
  warns "CPU scaling is enabled").
- Pin to a fixed CPU with `taskset -c 0 ./bench`; close other workloads.
- Run on the same machine for A/B comparisons; cloud VMs are noisy - use many repetitions.
- `--benchmark_enable_random_interleaving=true` reduces ordering effects.

## Compare
```bash
pip3 install -r tools/requirements.txt    # from the google/benchmark repo
python3 tools/compare.py benchmarks old.json new.json
```
Reports per-benchmark relative change and, with repetitions, a Mann-Whitney U test p-value; trust changes
that are both large and significant.

## Pitfalls
- Benchmarking with constant inputs lets the compiler constant-fold: feed data from runtime-sized
  containers.
- Tiny data that fits in L1 hides cache effects real workloads suffer; benchmark realistic sizes.
- Microbenchmarks show local speed; confirm in the whole application with a profiler.

## Verify
- [ ] Release build and no CPU-scaling warning in the output header.
- [ ] Repetitions show a small coefficient of variation.
- [ ] compare.py result significant before claiming an improvement.

## Checked

Date: 2026-10-25. Documentation: Google Benchmark docs (google/benchmark docs/user_guide.md, tools.md, reducing_variance.md, repository head 2026-10-25).

Confirmed: `DoNotOptimize` and `ClobberMemory`; `PauseTiming`/`ResumeTiming`; `Args`, `ArgsProduct`, `RangeMultiplier`, `Range`, `Complexity` with `SetComplexityN`; `UseRealTime`, `Threads`, `MinTime` and `--benchmark_min_time` (seconds); fixtures; `Counter::kIsRate`; `--benchmark_filter`, `--benchmark_repetitions`, `--benchmark_report_aggregates_only`, `--benchmark_out`/`--benchmark_out_format`, `--benchmark_enable_random_interleaving`; `compare.py benchmarks` with Mann-Whitney U test; `cpupower` and `taskset` advice and the CPU scaling warning.
Removed as unconfirmed: the pinned GIT_TAG, `BENCHMARK_ENABLE_TESTING`, the "built as DEBUG" warning text, the `-O2/-O3` flags, the Ninja-style alternatives list and the cv threshold.

Method: documentation only; no commands were run.
