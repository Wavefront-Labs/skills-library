---
id: computing-software.software-engineering.cpp.fuzzing-with-libfuzzer
name: fuzzing-with-libfuzzer
category: computing-software
field: software-engineering
product: cpp
tags: [cpp, memory-safety, libfuzzer, fuzzing, coverage-guided-fuzzing, asan, oss-fuzz, corpus, afl-plus-plus, fuzz-targets]
level: advanced
status: docs-checked
description: "Find memory bugs in C/C++ parsers with libFuzzer: writing fuzz targets, building with sanitizers, seed corpora and dictionaries, minimising crashes and running in CI."
sources: ["https://llvm.org/docs/LibFuzzer.html", "https://github.com/google/fuzzing/blob/master/docs/good-fuzz-target.md", "https://google.github.io/oss-fuzz/", "https://clang.llvm.org/docs/AddressSanitizer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuzzing with libFuzzer

**Goal:** let a coverage-guided fuzzer throw millions of inputs at every function that
parses untrusted bytes, catching crashes, UB and leaks before attackers do.

## Fuzz target
```cpp
// fuzz_parse.cc
#include <cstdint>
#include <cstddef>
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    std::string_view in(reinterpret_cast<const char*>(data), size);
    auto r = myproj::parse_config(in);       // must not crash, leak or hit UB for ANY input
    if (r) (void)myproj::serialize(*r);      // round-trip paths too
    return 0;
}
```
Rules for good targets: deterministic, fast (ms per input), no global state carried
between runs, no `exit()`, no unbounded allocations based on input sizes (cap them).

## Build and run
```bash
clang++ -g -O1 -fsanitize=fuzzer,address,undefined fuzz_parse.cc parser.cc -o fuzz_parse
mkdir -p corpus && cp tests/data/*.conf corpus/        # seed with valid examples
./fuzz_parse corpus/ -dict=conf.dict -max_len=4096 -jobs=8 -workers=8   # libFuzzer plans to replace -jobs/-workers with -fork
```
- Crash artifacts are written as `crash-<sha1>` (also `leak-` and `timeout-`); reproduce with `./fuzz_parse crash-<sha1>`.
- `-minimize_crash=1 -runs=10000 crash-x` shrinks the input (`-minimize_crash` is used with `-runs` or `-max_total_time`).
- `-merge=1 newcorpus/ corpus/` minimises the corpus.
- Dictionaries (keywords, magic bytes) massively help text formats.

CMake: add a `fuzz` preset with `-fsanitize=fuzzer-no-link` on libraries and
`-fsanitize=fuzzer` on the target executable.

## Continuous fuzzing
- CI: run each target for a bounded time on PRs and longer nightly.
- Open source: OSS-Fuzz runs fuzz targets with libFuzzer, AFL++, Honggfuzz or Centipede plus sanitizers.
- Every crash fixed becomes a regression test: add the input to the corpus and a unit test.

## AFL++
A separate fuzzing engine that OSS-Fuzz also supports; see the AFL++ documentation for how to build a harness for it.

## Verify
- [ ] Target is fast and coverage keeps growing during the first minutes of a run.
- [ ] A deliberately planted bug is found.
- [ ] Corpus and dictionaries are committed or stored for reuse.

## Checked

Date: 2026-10-25. Documentation: libFuzzer reference (llvm/llvm-project llvm/docs/LibFuzzer.md, head 2026-10-25), Google fuzzing "good fuzz target" guide (google/fuzzing) and OSS-Fuzz docs (google/oss-fuzz, docs/index.md).

Confirmed: `-fsanitize=fuzzer`, `fuzzer-no-link`, `-dict`, `-max_len`, `-jobs`/`-workers` (planned replacement `-fork`), `-minimize_crash`, `-merge=1`, `crash-<sha1>` artifacts; fuzz-target rules (deterministic, fast, no `exit()`, little global state); OSS-Fuzz supports libFuzzer, AFL++, Honggfuzz and Centipede.
Removed as unconfirmed: libprotobuf-mutator and FuzzedDataProvider mentions, ClusterFuzzLite, the AFL++ `afl-clang-fast` compatibility line and the exec/s threshold.

Method: documentation only; no commands were run.
