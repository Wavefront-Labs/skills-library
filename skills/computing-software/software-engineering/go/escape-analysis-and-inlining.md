---
id: computing-software.software-engineering.go.escape-analysis-and-inlining
name: escape-analysis-and-inlining
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-escape-analysis, gcflags, inlining, heap-allocation, performance, compiler-diagnostics]
level: advanced
status: verified
description: "Read Go compiler escape-analysis and inlining decisions with -gcflags=-m, find why values move to the heap, and cut allocations in hot paths."
sources: ["https://go.dev/doc/gc-guide#Eliminating_heap_allocations", "https://pkg.go.dev/cmd/compile", "https://go.dev/wiki/CompilerOptimizations"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Escape analysis and inlining

**Goal:** turn a profile's "too many allocations" into specific lines, and know which code
changes keep values on the stack.

## Ask the compiler
```bash
go build -gcflags='-m' ./pkg/hot 2>&1 | grep -v '^#'
go build -gcflags='-m=2' ./pkg/hot          # explains WHY (the flow that causes escape)
go build -gcflags='all=-m' ./...            # all packages including deps (noisy)
go test -gcflags='-m' -run '^$' -bench Hot ./pkg/hot
```
Typical lines:
```
./parse.go:21:6: can inline parseByte
./parse.go:40:13: inlining call to parseByte
./parse.go:55:9: &Token{...} escapes to heap
./parse.go:61:14: buf does not escape
./parse.go:70:17: ... argument does not escape     # fmt.Sprintf: the slice stays local
./parse.go:70:23: x escapes to heap                  # but the boxed value does
```

## Common reasons for escape
- Returning a pointer to a local (`return &T{}`) - fine when the object must outlive the call;
  the compiler may still keep it on the stack if the caller is inlined.
- Converting to an interface (`any`, `error`, `fmt.Println(x)`) - the value is usually boxed.
- Storing into a heap object, global, or a slice/map that escapes.
- Closures capturing variables that outlive the frame (goroutines, stored callbacks).
- A `make` whose result is returned or stored (`make([]byte, n)` returned from the function printed `escapes to heap`; the same `make` with a non-constant size used only locally did not on 1.27), or a constant size over 64 KB (`make`/`new`: 65536 stays, 65537 escapes; an explicit `var a [N]byte` moves to the heap above 128 KiB).
- Calls through interfaces or function values: the compiler cannot see the callee, so arguments
  are assumed to escape.

## Fixes that work
- Let the caller provide the buffer: `func (d *Dec) Decode(dst []byte) []byte` instead of returning
  a new slice (the `append`-style API the stdlib uses).
- Return values instead of pointers for small structs.
- Pre-size slices with a constant capacity when the max is known; reuse with `buf[:0]`.
- Avoid `fmt` in hot paths; use `strconv.AppendInt` and friends.
- `sync.Pool` for large, short-lived buffers (measure; pools add overhead).

## Inlining
- The inliner has a cost budget (about 80 nodes); `-m=2` prints "cost N exceeds budget 80".
  Small leaf functions inline; functions with `defer`, `recover` or `go` did not on 1.27
  (`cannot inline ...: unhandled op DEFER`), while `select` and closures did (rules evolve each release - check `-m` output, not folklore).
- Mid-stack inlining means non-leaf functions can inline too. Inlining enables escape analysis to
  keep the callee's allocations on the caller's stack.
- PGO (`default.pgo`) raises the budget for hot call sites.
- `//go:noinline` is for benchmarks and tests only; `-gcflags=all=-l` disables inlining globally
  (used for debugging with Delve).

## Measure, do not guess
```bash
go test -bench Hot -benchmem -count 10 ./pkg/hot > new.txt
benchstat old.txt new.txt     # allocs/op should drop
```
`testing.AllocsPerRun` can lock an allocation count into a unit test to stop regressions.

## Verify
- [ ] `-gcflags=-m` no longer reports the escaping line.
- [ ] `allocs/op` dropped in benchstat with statistical significance.
- [ ] Code is still readable; do not contort cold paths.

## Checked
2026-10-21 on Go 1.27.3 (Windows): ran `-gcflags=-m`, `-m=2`, `all=-m`, `all=-l` and `go test -gcflags=-m -run '^$' -bench` on a scratch package. Observed: variadic `fmt` argument prints `... argument does not escape` and the boxed value prints `x escapes to heap`; `make([]byte, 65536)` stays on the stack and `65537` escapes (same for `new`), an explicit `var a [N]byte` moves to the heap above 128 KiB; a non-constant `make` that does not leave the function reports no escape; `defer` and `recover` still block inlining (`unhandled op DEFER`, `call to recover`), `select` and closures do not; budget message is `function too complex: cost 110 exceeds budget 80`; `testing.AllocsPerRun` reported 2 allocs for `fmt.Sprintf`; benchstat (golang.org/x/perf) showed `Sprintf` to `strconv.Itoa` at -63% time and fewer bytes/op (p=0.002 n=6); PGO inlining text from https://go.dev/doc/pgo.
