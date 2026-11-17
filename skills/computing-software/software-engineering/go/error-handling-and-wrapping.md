---
id: computing-software.software-engineering.go.error-handling-and-wrapping
name: error-handling-and-wrapping
category: computing-software
field: software-engineering
product: go
tags: [go, golang, errors, error-wrapping, errors-is, errors-as, sentinel-errors, panic, recover, fmt-errorf, errors-join, custom-error-types, multierror, go-errors, go-errors-wrapping, go-sentinel-errors, go-errors-join]
level: practitioner
status: verified
description: "Idiomatic Go error handling: wrapping with %w, errors.Is/As, sentinel vs typed errors, errors.Join, and when panic/recover is actually appropriate."
sources: ["Go blog - Working with Errors in Go 1.13", "Go docs - errors package (Is, As, Join)", "Effective Go - errors"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Go error handling — wrap with context, check with Is/As, panic rarely

**Goal:** errors that carry enough context to debug in production logs, while callers
can still programmatically detect the specific failure they care about.

## 1. Wrap with `%w`, not string concatenation
```go
if err != nil {
    return fmt.Errorf("fetching user %d: %w", id, err)
}
```
`%w` preserves the original error in the chain (`Unwrap() error`) so callers can still
match it; `%v` or string concat destroys that — `errors.Is`/`errors.As` on the result
will fail. Every layer that adds `%w` context builds a chain; the top-level log line
then shows the full path ("fetching user 5: querying db: connection refused") in one
message instead of scattered across layers.

## 2. `errors.Is` for sentinels, `errors.As` for typed errors with data
```go
var ErrNotFound = errors.New("not found")
...
if errors.Is(err, ErrNotFound) { ... }       // identity match through the wrap chain

type ValidationError struct{ Field string }
func (e *ValidationError) Error() string { return "invalid: " + e.Field }
...
var ve *ValidationError
if errors.As(err, &ve) { log.Print(ve.Field) }  // extracts typed data through the chain
```
Never compare with `==` on a wrapped error — it only works on the exact, unwrapped
sentinel. A common bug: wrapping with `fmt.Errorf("...: %v", err)` (verb `%v` not `%w`)
by accident, which silently breaks every downstream `errors.Is` check with no compiler
warning.

## 3. `errors.Join` for multiple independent failures (Go 1.20+)
```go
err := errors.Join(err1, err2, err3)   // nil entries are skipped
errors.Is(err, ErrNotFound)            // matches if ANY joined error matches
```
Use when several independent operations can each fail (closing multiple resources in
a `defer`) and the caller needs to see all of them, not just the first.

## 4. Don't over-use custom error types
A sentinel (`var ErrX = errors.New(...)`) is enough when callers only need to branch
on *which* error. Reach for a struct type only when callers need structured data back
(a field name, an HTTP status, a retry-after duration) — most Go error taxonomies over
in enterprise code are typed errors nobody ever calls `errors.As` on; a wrapped string
would have done.

## 5. panic/recover: narrow and deliberate, not a substitute for error returns
- `panic` is for programmer errors (nil pointer that should be impossible, invariant
  violated, index out of range you failed to check) — things that mean the program's
  internal state is wrong, not "the file didn't exist."
- Library code should almost never panic across its public API; if it must (e.g. a
  parser that panics internally for control flow), `recover()` at the boundary and
  convert to an `error` before returning to the caller — a panic that crosses a
  goroutine boundary to the caller that didn't spawn it cannot be recovered and kills
  the process.
- A `recover()` in a goroutine only catches panics from *that* goroutine; an unrecovered
  panic in any goroutine crashes the whole process regardless of other goroutines'
  `recover` calls — wrap every `go func(){...}()` body that can panic in its own
  `defer recover()`.

## Gotchas
- Loop variable capture in closures that return wrapped errors (`for _, item := range
  items { go func(){ errs <- fmt.Errorf("%v", item) }() }`) — pre-1.22 Go reuses the
  loop variable; pass `item` as a parameter or shadow it (`item := item`) on older Go.
- `err != nil` checks on typed-nil interfaces: a `*MyError` nil pointer boxed into an
  `error` interface is **not** `== nil` — return `nil` literally, never a nil-valued
  typed pointer, from a function returning `error`.
- Ignoring errors with `_ = f()` is sometimes correct (best-effort `Close()`) but
  should be an explicit, commented choice — `go vet`/`errcheck` linters catch the
  accidental ones.

## Verify
- [ ] Every `fmt.Errorf` that wraps an error uses `%w`, confirmed by grep (`%v.*err\)`
      near a return is a red flag).
- [ ] `errors.Is`/`errors.As` used for branching, never `==` or type-switch on a
      possibly-wrapped error.
- [ ] No exported function panics on bad *input* (as opposed to invariant violations);
      `go test` includes a case feeding it invalid input and expects an `error`, not a crash.
- [ ] Every `go func(){}()` that can panic has its own `defer recover()`.

Related: computing-software.software-engineering.go.goroutines-channels-and-context

## Checked
- Go 1.25.1: `%w` chains answer `errors.Is`/`errors.As` with the full context string, `==` on a wrapped sentinel is false, `%v` breaks `errors.Is`, `errors.Join` skips nils, matches any member and returns nil when all are nil, a nil `*MyErr` returned as `error` is not `== nil`, and a panic in a goroutine crashes the process even though `main` has a deferred `recover` (printed `panic: boom in goroutine`, `main recovered?` never ran). The pre-1.22 loop-variable note is covered by the closures skill's run.
