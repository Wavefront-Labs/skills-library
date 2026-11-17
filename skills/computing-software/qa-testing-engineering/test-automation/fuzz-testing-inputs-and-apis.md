---
id: computing-software.qa-testing-engineering.test-automation.fuzz-testing-inputs-and-apis
name: fuzz-testing-inputs-and-apis
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [fuzz-testing, fuzzing, security-testing, atheris, libfuzzer, restler, api-fuzzing]
level: advanced
status: gated
description: "Fuzz parsers and APIs: coverage-guided fuzzing (libFuzzer, Atheris, Go native fuzz), schema-based API fuzzing, corpus seeding, crash triage and CI runs."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta
  - https://go.dev/doc/security/fuzz/
  - https://github.com/google/atheris
  - https://llvm.org/docs/LibFuzzer.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuzz testing inputs and APIs

**Goal:** feed huge numbers of malformed or unexpected inputs to find crashes, hangs, memory errors and unhandled exceptions.

## Choose the fuzzer
- **Coverage-guided, in-process** (best for parsers, decoders, validators): libFuzzer/AFL++ (C/C++/Rust `cargo fuzz`), Go native fuzzing, Atheris (Python), Jazzer (Java).
- **Schema/grammar-based API fuzzing:** Schemathesis (OpenAPI/GraphQL), RESTler (stateful REST sequences), ZAP active scan fuzzer.
- **Dumb mutation** of captured requests: Burp Intruder or ffuf with payload lists for quick wins.

## Go native example

```go
func FuzzParseAmount(f *testing.F) {
    f.Add("10.00"); f.Add("-0"); f.Add("1e309")
    f.Fuzz(func(t *testing.T, s string) {
        v, err := ParseAmount(s)
        if err == nil && v.String() != Normalise(s) { t.Errorf("round-trip %q", s) }
    })
}
```
Run `go test -fuzz=FuzzParseAmount -fuzztime=5m`; failing inputs are saved under `testdata/fuzz/FuzzParseAmount/` and replay as normal tests. Run on Go 1.22.5: the example (with a stub `ParseAmount`) fuzzed about 1.4 million inputs in 10 s and passed; after making `Normalise` disagree it failed with `round-trip " 1"`, wrote `testdata/fuzz/FuzzParseAmount/<hash>` (shown with backslashes on Windows), and a plain `go test` then replayed that input as a failing subtest.

## Python Atheris

```python
import atheris, sys
with atheris.instrument_imports():
    import mylib
def TestOneInput(data):
    try: mylib.parse(data)
    except mylib.ParseError: pass   # expected rejection
atheris.Setup(sys.argv, TestOneInput); atheris.Fuzz()
```
The calls match the Atheris README (`instrument_imports`, `Setup`, `Fuzz`), but `pip install atheris` failed to build a wheel on Windows here, so the snippet was not run (gated: unconfirmed, source is paywalled or blocked). Atheris needs a compiler and clang on Linux or macOS; use WSL or a Linux CI job.

## Practice
- **Seed corpus** with real valid samples; fuzzers mutate far better from good seeds.
- **Oracles beyond crashes:** round-trip properties, differential comparison with a reference parser, sanitizers (ASan, UBSan) to turn silent corruption into crashes.
- **Triage:** minimise the crashing input (`-minimize_crash=1`, listed in the LibFuzzer docs), deduplicate by stack trace, add the minimised input as a regression test.
- **CI:** short runs per PR (minutes), long runs nightly or via OSS-Fuzz/ClusterFuzzLite.

## Verify
Fuzz targets run in CI, the corpus grows over time, and each found crash has a committed regression input that now passes.
