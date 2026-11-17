---
id: computing-software.cybersecurity-defensive.application-security.fuzzing
name: fuzzing
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [fuzzing, libfuzzer, go-fuzz, oss-fuzz, coverage-guided-fuzzing, sanitizers, cargo-fuzz]
level: advanced
status: docs-checked
description: "Add coverage-guided fuzzing to your own code: libFuzzer harnesses with sanitizers, native Go fuzz tests, cargo-fuzz, corpora and OSS-Fuzz."
sources: ["https://llvm.org/docs/LibFuzzer.html", "https://go.dev/doc/security/fuzz/", "https://google.github.io/oss-fuzz/", "https://rust-fuzz.github.io/book/cargo-fuzz/tutorial.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuzzing your own code

Coverage-guided fuzzers mutate inputs and keep those that reach new code, finding crashes and bugs in code that
handles untrusted input. Defensive goal: find them before release.

## What to fuzz
Code that parses untrusted bytes: file formats, protocols, deserialisers, decoders.

## libFuzzer (C/C++)
```c
extern "C" int LLVMFuzzerTestOneInput(const uint8_t *Data, size_t Size) {
  DoSomethingInterestingWithMyAPI(Data, Size);
  return 0;
}
```
- The target must not `exit()` on any input, should be as deterministic as possible (non-determinism makes fuzzing
  inefficient) and ideally should not modify global state.
- Build with `-fsanitize=fuzzer`, which links libFuzzer's `main()`: `clang -g -O1 -fsanitize=fuzzer mytarget.c`.
  Add sanitizers in the list: `-fsanitize=fuzzer,address` (ASan) or `-fsanitize=fuzzer,memory` (MSan).
- Run: `./my_fuzzer CORPUS_DIR`. Useful options: `-max_len`, `-timeout`, `-max_total_time` (time limit),
  `-runs` (iteration limit), `-dict=DICTIONARY_FILE`, `-jobs=N` / `-workers=N`.
- Crashes are written as `crash-<sha1>` (also `leak-<sha1>`, and others) under the `artifact_prefix`.
- Minimise a corpus with `./my_fuzzer -merge=1 NEW_CORPUS_DIR FULL_CORPUS_DIR`.

## Go (1.18+ native)
- A fuzz test is `FuzzXxx(f *testing.F)` in a `_test.go` file with exactly one fuzz target, a `(*testing.F).Fuzz`
  call whose function takes `*testing.T` then the fuzzing arguments. Seed entries via `f.Add` must match the argument
  types in order. Allowed argument types: `string`, `[]byte`, the int and uint sizes, `float32`, `float64`, `bool`.
- Plain `go test` runs the seed corpus as a unit test; `go test -fuzz=FuzzXxx` fuzzes (regex matching a single fuzz
  test). It runs until a failure unless `-fuzztime` is set. Other flags: `-fuzzminimizetime` (default 60s) and
  `-parallel`.
- Targets should be fast and deterministic and not depend on global state. An execution that takes over 1 second
  counts as a failure.
- A failing input is minimised and written to `testdata/fuzz/FuzzXxx/<hash>`; it is then run by default by
  `go test` as a regression test. Re-run it with `go test -run=FuzzXxx/<hash>`. Commit the file with the fix.
- Fuzzing needs coverage instrumentation (AMD64 and ARM64) so the corpus can grow.

## Rust (cargo-fuzz)
`cargo fuzz init` creates `fuzz/fuzz_targets/<name>.rs`; `cargo fuzz list` lists targets; `cargo fuzz run <name>`
runs it. The target body uses `fuzz_target!(|data: &[u8]| { ... })`, which libFuzzer calls repeatedly until a panic
or other error. Crashing input is saved to `fuzz/artifacts/<target>/crash-<hash>`.

## Continuous fuzzing
OSS-Fuzz runs libFuzzer, AFL++, Honggfuzz and Centipede with sanitizers for open source projects (C/C++, Rust, Go,
Python, Java/JVM, JavaScript, Lua) and privately alerts developers. Projects that do not qualify can run their own
ClusterFuzz or ClusterFuzzLite.

## Verify
A planted bug in the parser is found by the fuzzer, the saved crash input reproduces the failure, and it passes
after the fix.

## Checked
Method: docs-checked 2026-11-09 against the LibFuzzer page on llvm.org (harness rules, build flags, options, merge),
the Go Fuzzing page on go.dev (read in full), the OSS-Fuzz home page and the cargo-fuzz tutorial. Removed
unconfirmed claims: AFL++ commands (the AFL++ docs page was a landing page only), Atheris, Jazzer, UBSan and
`-print_coverage` specifics, the Go snippet and triage guidance, and the cargo-fuzz book index source.
