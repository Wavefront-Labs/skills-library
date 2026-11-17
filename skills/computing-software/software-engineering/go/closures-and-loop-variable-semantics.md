---
id: computing-software.software-engineering.go.closures-and-loop-variable-semantics
name: closures-and-loop-variable-semantics
category: computing-software
field: software-engineering
product: go
tags: [go, loopvar, go-closures, go-1-22, goroutine-capture, loop-variable-capture, effective-go, go-functions-methods]
level: practitioner
status: verified
description: "Understand Go closures and the Go 1.22 per-iteration loop variable change: what it fixed, when old behaviour still applies via the go directive, and remaining capture pitfalls."
sources: ["https://go.dev/blog/loopvar-preview", "https://go.dev/wiki/LoopvarExperiment", "https://go.dev/ref/spec#For_statements", "https://go.dev/doc/go1.22"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Closures and loop variable semantics

**Goal:** know exactly which variable a closure or goroutine captures, before and after
Go 1.22.

## Closures capture variables, not values
```go
counter := 0
inc := func() { counter++ }     // refers to the same `counter`
inc(); inc()
fmt.Println(counter)            // 2
```

## The old bug (go directive < 1.22)
```go
for _, item := range items {
    go func() { process(item) }()       // all goroutines likely saw the LAST item
}
for i := 0; i < 3; i++ {
    funcs = append(funcs, func() { fmt.Print(i) })   // printed 333
}
```
One variable was shared across all iterations. The fix was `item := item` or passing it as an
argument.

## Go 1.22+: per-iteration variables
Each iteration of a `for` loop (both `range` and three-clause) now gets a fresh variable, so
the code above works as intended (prints 012). The behaviour is controlled by the **`go` line
in go.mod** of the module containing the loop: modules declaring `go 1.21` or lower keep the
old semantics even when built with a newer toolchain. Upgrading the `go` directive changes
semantics - run tests (and `-race`) when bumping it.

Per-file override: a `//go:build go1.22` constraint opts that file in.

Tooling: `go vet`'s `loopclosure` check reports the old bug in pre-1.22 modules;
`bisect -compile=loopvar` finds the loop responsible if the change alters behaviour (rare:
code that relied on sharing, or allocation-sensitive benchmarks).

## Pitfalls that remain
- Variables declared **outside** the loop are still shared:
```go
var err error
for _, f := range files {
    go func() { err = upload(f) }()      // data race on err
}
```
  Use `errgroup.Group` or collect results per goroutine.
- Capturing a pointer to a loop variable is now per-iteration (good), but capturing a slice
  element via `&items[i]` still aliases the slice storage.
- Deferred closures in a loop run at function end, not iteration end:
  `for ... { f, _ := os.Open(p); defer f.Close() }` keeps every file open until return -
  wrap the body in a function.
- Closures in long-lived goroutines keep captured data alive (memory leaks via capture).

## Verify
- [ ] go.mod `go` directive >= 1.22 (or loops audited if older).
- [ ] `go test -race ./...` clean after bumping the go directive.

## Checked
- Go 1.25.1 toolchain with throwaway modules: a `go 1.21` module printed `333`, a shared-variable goroutine result with a hole (`[  c]`) and three equal pointers; a `go 1.22` module printed `012`, `[a b c]` and distinct pointers; `go vet` reported `loop variable item captured by func literal` on the 1.21 module and nothing on 1.22; a file with `//go:build go1.22` inside a `go 1.21` module got per-iteration semantics. The Go wiki loopvar page describes the `bisect` tool. `go run -race` was not run: the race detector needs cgo, which this Windows setup lacks (set `CGO_ENABLED=1` with a C compiler).
