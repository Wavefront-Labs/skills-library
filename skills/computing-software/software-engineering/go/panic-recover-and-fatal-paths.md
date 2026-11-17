---
id: computing-software.software-engineering.go.panic-recover-and-fatal-paths
name: panic-recover-and-fatal-paths
category: computing-software
field: software-engineering
product: go
tags: [go, go-errors, go-panic-recover, panic, recover]
level: practitioner
status: docs-checked
description: "Use panic and recover correctly in Go: re-panic unknown values, convert panics at API boundaries, and keep goroutine panics from crashing servers."
sources:
  - https://go.dev/blog/defer-panic-and-recover
  - https://go.dev/ref/spec
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# panic, recover and fatal paths

**Goal:** treat panic as "programmer error or unrecoverable", and recover only at boundaries.

`recover` only works when called **directly by a deferred function**, and only while its goroutine is panicking; otherwise it returns `nil` and has no other effect. A panic that is not recovered reaches the top of that goroutine's call stack and terminates the program.

```go
func safely(fn func()) (err error) {
    defer func() {
        if r := recover(); r != nil {
            err = fmt.Errorf("panic: %v", r)
        }
    }()
    fn()
    return nil
}

go func() { defer recoverAndReport(); work() }()   // each goroutine needs its own deferred recover
```

The Go blog's real-world example is the standard library `json` package: internally recursive encode functions call `panic` to unwind the stack on error, and the top-level call recovers and returns an ordinary error value. That is the pattern to copy: panic inside a package, convert to `error` at the exported boundary.

The spec guarantees that when a goroutine is panicking and `recover` is called directly by a deferred function, the result is never `nil`; to ensure that, calling `panic` with a nil interface value (or untyped nil) causes a run-time panic.

## Gotchas
- Panics in goroutines you start are not recoverable by the parent goroutine; install the deferred `recover` inside each goroutine's own function.
- Do not swallow panics you do not understand: after logging, consider re-panicking (`panic(r)`).
- A deferred function that calls a helper which calls `recover` does not recover: `recover` must be called by the deferred function itself.

## Verify
Test that `safely(func(){ var m map[string]int; m["a"]=1 })` returns an error and that the process keeps running.

## Checked

Checked 2026-11-09 against the Go blog "Defer, Panic, and Recover" (read in full) and the "Handling panics" section of go.dev/ref/spec.
Confirmed: `recover` semantics (only useful in deferred functions, returns nil when not panicking, directly-called rule), unrecovered panic terminating the program, the `json` package pattern, and the panic(nil) rule.
Removed as unconfirmed: net/http handler-panic recovery, the Go 1.21 `PanicNilError` detail, `runtime.Error` and `debug.Stack` usage, `log.Fatal`/`os.Exit` skipping defers, `runtime.Goexit`, and the `Must*` initialiser advice.

Method: documentation only; no commands were run.
