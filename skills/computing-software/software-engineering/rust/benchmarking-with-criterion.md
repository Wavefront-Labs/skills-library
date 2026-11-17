---
id: computing-software.software-engineering.rust.benchmarking-with-criterion
name: benchmarking-with-criterion
category: computing-software
field: software-engineering
product: rust
tags: [rust, rust-testing, rust-criterion, criterion, benchmarks, black-box, divan]
level: practitioner
status: docs-checked
description: "Benchmark Rust code with criterion: benches layout, black_box, input sweeps, throughput, baselines and iter_batched."
sources:
  - https://bheisler.github.io/criterion.rs/book/getting_started.html
  - https://bheisler.github.io/criterion.rs/book/user_guide/command_line_options.html
  - https://bheisler.github.io/criterion.rs/book/user_guide/benchmarking_with_inputs.html
  - https://bheisler.github.io/criterion.rs/book/user_guide/timing_loops.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Benchmarking with criterion

**Goal:** trustworthy, comparable micro-benchmarks.

```toml
[dev-dependencies]
criterion = "0.3"          # use the current release; the book's example shows 0.3
[[bench]]
name = "parse"
harness = false            # disable the standard harness; criterion supplies main
```
```rust
// benches/parse.rs
use criterion::{black_box, criterion_group, criterion_main, BenchmarkId, Criterion, Throughput};

fn bench(c: &mut Criterion) {
    let mut g = c.benchmark_group("parse");
    for size in [64usize, 1024, 65536] {
        let input = make_input(size);
        g.throughput(Throughput::Bytes(size as u64));
        g.bench_with_input(BenchmarkId::from_parameter(size), &input, |b, i| {
            b.iter(|| parse(black_box(i)))              // black_box stops constant folding
        });
    }
    g.finish();
}
criterion_group!(benches, bench);
criterion_main!(benches);
```

- Run `cargo bench`. Plots and saved data land under `target/criterion/$BENCHMARK_NAME/`.
- Benchmarks in `benches/` compile as separate crates, so only public functions can be benchmarked and the library is imported as an external crate.
- `bench_with_input` passes the input through `black_box` automatically and puts it in the benchmark name. A `BenchmarkGroup` lets you sweep inputs and gives extra summary pages; call `finish` (it is called on drop if forgotten). `throughput` is only available through `BenchmarkGroup`.
- By default each run is compared with the previous run. `cargo bench -- --save-baseline name` compares then overwrites the named baseline; `--baseline name` compares without overwriting; `--load-baseline name` loads a named baseline as the new data set.
- `cargo bench -- <regex>` filters benchmarks by ID; `--noplot` disables plots; `--profile-time <seconds>` runs each benchmark for a fixed time without analysis, for use with a profiler; `cargo test --benches` checks the benchmarks run without measuring (for CI).
- `iter_batched` (with `SmallInput`) is for benchmarks that need fresh setup input each iteration, with the setup excluded from timing. `PerIteration` batch size adds more overhead than larger batches.

## Gotchas
- Without `black_box` the compiler can fold the whole function to a constant; the book's example shows an optimised result in picoseconds.
- The benchmark name should be unique among all benchmarks in the project.
- Read the reported confidence interval and the change line (with p-value) rather than only the mean.

## Verify
Run twice with no code change and check that the comparison does not report a change.

## Checked
Method: docs-checked 2026-11-09 against the criterion.rs book getting started, command-line options, benchmarking with inputs and timing loops pages. Dropped unconfirmed claims about the html_reports feature, divan, the unstable #[bench] attribute, bench-profile debug settings and machine-noise advice.
