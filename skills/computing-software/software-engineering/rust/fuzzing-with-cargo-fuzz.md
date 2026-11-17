---
id: computing-software.software-engineering.rust.fuzzing-with-cargo-fuzz
name: fuzzing-with-cargo-fuzz
category: computing-software
field: software-engineering
product: rust
tags: [rust, cargo-fuzz, libfuzzer, fuzzing, arbitrary, oss-fuzz, security-testing, parsers]
level: advanced
status: docs-checked
description: "Fuzz Rust parsers and decoders with cargo-fuzz and libFuzzer: targets, structured input via arbitrary, corpora and dictionaries, minimising crashes, and CI or OSS-Fuzz runs."
sources:
  - https://rust-fuzz.github.io/book/cargo-fuzz.html
  - https://github.com/rust-fuzz/cargo-fuzz
  - https://github.com/rust-fuzz/arbitrary
  - https://llvm.org/docs/LibFuzzer.html
  - https://github.com/google/clusterfuzzlite
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuzzing with cargo-fuzz

**Goal:** find panics, infinite loops, excessive memory use and (in unsafe code) memory errors in
code that handles untrusted input.

## Setup
```bash
cargo install cargo-fuzz          # needs a nightly compiler; x86-64/Aarch64 on Unix-like systems only (not Windows)
cargo fuzz init                   # creates fuzz/ crate with Cargo.toml and fuzz_targets/
cargo fuzz add parse_header
```
fuzz/fuzz_targets/parse_header.rs:
```rust
#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let _ = mycrate::parse_header(data);   // must never panic, whatever the input
});
```
Run:
```bash
cargo +nightly fuzz run parse_header                    # runs until a crash (Ctrl-C to stop)
cargo +nightly fuzz run parse_header -- -max_total_time=300 -max_len=4096 -jobs=8
```
AddressSanitizer is enabled by default (`--sanitizer none` for pure safe code is faster).

## Structured inputs with arbitrary
```rust
// Cargo.toml: arbitrary = { version = "1", features = ["derive"] }
#[derive(Debug, arbitrary::Arbitrary)]
enum Op { Insert(u16, Vec<u8>), Remove(u16), Get(u16) }

fuzz_target!(|ops: Vec<Op>| {
    let mut model = std::collections::BTreeMap::new();
    let mut real = mycrate::Tree::new();
    for op in ops { /* apply to both, assert they agree */ }
});
```
Differential fuzzing against a simple model (or an older implementation, or a round-trip
`decode(encode(x)) == x`) finds logic bugs, not just crashes.

## Corpus and dictionaries
- Seed `fuzz/corpus/parse_header/` with real sample files: coverage grows much faster.
- `-dict=fuzz/http.dict` with tokens (`"Content-Length:"`) helps text formats.
- `cargo fuzz cmin parse_header` minimises the corpus; commit a small corpus or keep it in storage.

## When it crashes
Crash input is saved to `fuzz/artifacts/parse_header/crash-<hash>`.
```bash
cargo +nightly fuzz run parse_header fuzz/artifacts/parse_header/crash-abc   # reproduce
cargo +nightly fuzz tmin parse_header fuzz/artifacts/parse_header/crash-abc  # minimise
cargo fuzz fmt parse_header <file>      # pretty-print an arbitrary-derived input
```
Turn every crash into a regular unit test with the minimised bytes so it stays fixed.
Timeouts (`-timeout=10`; libFuzzer's default is 1200 seconds) and out-of-memory findings are real bugs for parsers
(algorithmic complexity, unbounded allocation from length fields).

## Coverage of the fuzzer
`cargo fuzz coverage parse_header` generates coverage information for the fuzzed program; use it to find code the fuzzer never reaches, then add seeds or restructure the target.

## Continuous fuzzing
- CI: short runs (`-max_total_time=120`) on PRs touching parsers, longer nightly jobs.
- OSS-Fuzz for open-source projects; ClusterFuzzLite runs pull-request and batch fuzzing inside CI workflows.

## Verify
- [ ] Each untrusted-input entry point has a fuzz target.
- [ ] Seed corpus checked in; fuzz job runs in CI.
- [ ] All found crashes have regression tests.

## Checked

2026-10-25. Checked against the cargo-fuzz README and source (subcommands init, add, run, fmt, tmin, cmin, coverage; `--sanitizer` default `address`; nightly compiler, x86-64 and Aarch64, Unix-like only), the Rust Fuzz Book tutorial (artifacts under `fuzz/artifacts/<target>/crash-<hash>`), the arbitrary README (`derive` feature) and the LLVM libFuzzer documentation (`-max_total_time`, `-max_len`, `-jobs`, `-dict`, `-timeout` default 1200 s) and the ClusterFuzzLite README. Added the platform limits missing from the draft. Removed unconfirmed items: `-rss_limit_mb`, `llvm-cov show` workflow, OSS-Fuzz pricing and privacy claims, and the AFL/bolero alternatives.

Method: documentation only; no commands were run.
