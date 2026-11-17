---
id: computing-software.software-engineering.go.testing-with-table-tests-and-benchmarks
name: testing-with-table-tests-and-benchmarks
category: computing-software
field: software-engineering
product: go
tags: [go, golang, testing, table-driven-tests, subtests, benchmarks, fuzzing, go-test, testify, race-detector, httptest, golden-files, go-fuzzing, go-benchmarks, go-testing, go-subtests, go-benchmarks-profiling, go-benchstat]
level: practitioner
status: docs-checked
description: "Write idiomatic Go tests: table-driven subtests, benchmarks with b.ResetTimer, fuzzing, and catching races with -race."
sources:
  - https://pkg.go.dev/testing
  - https://go.dev/doc/security/fuzz/
  - https://pkg.go.dev/net/http/httptest
  - https://pkg.go.dev/golang.org/x/perf/cmd/benchstat
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Go testing — table-driven tests, real benchmarks, and the race detector

**Goal:** a test suite that reads as a spec (each case is one row), catches data races
before production, and benchmarks that measure what you think they measure.

## 1. Table-driven tests with named subtests
```go
func TestParse(t *testing.T) {
    cases := []struct {
        name string
        in   string
        want int
        wantErr bool
    }{
        {"simple", "42", 42, false},
        {"negative", "-1", -1, false},
        {"empty", "", 0, true},
    }
    for _, tc := range cases {
        t.Run(tc.name, func(t *testing.T) {
            got, err := Parse(tc.in)
            if tc.wantErr {
                if err == nil { t.Fatalf("expected error") }
                return
            }
            if err != nil { t.Fatalf("unexpected error: %v", err) }
            if got != tc.want { t.Errorf("got %d, want %d", got, tc.want) }
        })
    }
}
```
`t.Run` gives each case an independently-reportable name (`TestParse/negative`) and
lets `go test -run TestParse/negative` isolate one failing case. Pre-1.22, the classic
loop-variable-capture bug applies here too if subtests run in goroutines or `t.Parallel()`
is used — capture `tc := tc` inside the loop body (or rely on Go 1.22+'s per-iteration
variable semantics).

## 2. `t.Parallel()` changes failure isolation
Marking subtests parallel speeds up I/O-bound suites but means shared mutable
fixtures (a package-level variable) now race. `t.Setenv` and `t.Chdir` cannot be used
in parallel tests because they affect the whole process. Always run with `-race` when adding parallelism.

## 3. Benchmarks: reset the timer after setup
```go
func BenchmarkParse(b *testing.B) {
    data := loadFixture()   // setup cost shouldn't count
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Parse(data)
    }
}
```
Forgetting `b.ResetTimer()` after expensive setup inflates the per-op number. Since Go 1.24, `for b.Loop() { ... }`
resets the timer on its first call, runs the benchmark function once per measurement and keeps call arguments and
results alive; do not mix it with a `b.N` loop. Run with
`-benchmem` to catch unexpected allocations (`b.ReportAllocs()` in code, or the flag):
an allocation inside a hot loop that shows up only here, not in a normal test, is
often the actual perf bug. Compare before/after with `benchstat old.txt new.txt`
(`golang.org/x/perf/cmd/benchstat`) — it reports medians with confidence intervals and whether a difference is statistically significant.

## 4. Fuzzing (Go 1.18+) for parsers and anything taking untrusted input
```go
func FuzzParse(f *testing.F) {
    f.Add("42")           // seed corpus
    f.Fuzz(func(t *testing.T, s string) {
        Parse(s)          // must not panic for any input
    })
}
```
`go test -fuzz=FuzzParse -fuzztime=60s` — crashers get saved under `testdata/fuzz/` and
automatically replayed as regression tests on every future `go test`. This is the
right tool for "does this panic on malformed input," which table tests rarely cover
exhaustively.

## 5. `httptest` for HTTP handlers without a real server
```go
req := httptest.NewRequest("GET", "/users/5", nil)
w := httptest.NewRecorder()
handler.ServeHTTP(w, req)
// assert w.Code, w.Body
```
For full round-trip tests (middleware, routing), `httptest.NewServer` starts a real
listener on a random port — use it sparingly (slower, needs cleanup via `defer
srv.Close()`) versus the no-network `NewRecorder` form for unit-level handler tests.

## Gotchas
- `go test ./...` without `-race` in CI means races are only ever found in production.
- Golden-file tests (`testdata/*.golden`) need a `-update` flag convention
  (`if *update { os.WriteFile(...) }`) or regenerating them becomes manual and error-prone.
- `testify`'s `assert` continues after a failure; `require` stops the test immediately
  — using `assert` for a precondition (e.g. "err must be nil before checking fields")
  causes a confusing nil-pointer panic on the next line instead of a clean failure.

## Verify
- [ ] `go test -race ./...` passes, not just `go test ./...`.
- [ ] Every table test case has a descriptive `name` and ran individually via `-run`.
- [ ] Benchmarks call `b.ResetTimer()` after any non-trivial setup and are compared
      with `benchstat`, not eyeballed ns/op.
- [ ] Any function parsing untrusted input has a fuzz target with a growing corpus.

Related: computing-software.software-engineering.go.error-handling-and-wrapping,
computing-software.software-engineering.concurrency.profiling-before-optimising

## Checked

2026-10-25. Checked against the Go source and docs (testing package: `t.Run`, `T.Setenv` and `T.Chdir` denied in parallel tests, `B.ResetTimer`, `B.ReportAllocs`, `B.Loop` since Go 1.24; Go 1.22 release notes on per-iteration loop variables; httptest `NewRequest`, `NewRecorder`, `NewServer` listening on a system-chosen port; the Go fuzzing documentation: Go 1.18+, `f.Add`, `go test -fuzz=`, failing inputs under `testdata/fuzz`), the benchstat source docs (median, 95% confidence interval, significance) and the testify README (`require` terminates the test, `assert` returns a boolean). Replaced prose-title entries in `sources` with real URLs and removed a self-correction from the body. Added the Go 1.24 `b.Loop` method and removed an unsupported claim about `b.N` convergence.

Method: documentation only; no commands were run.
