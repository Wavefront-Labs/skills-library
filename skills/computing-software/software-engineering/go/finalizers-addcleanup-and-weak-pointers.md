---
id: computing-software.software-engineering.go.finalizers-addcleanup-and-weak-pointers
name: finalizers-addcleanup-and-weak-pointers
category: computing-software
field: software-engineering
product: go
tags: [go, go-runtime-gc, go-addcleanup, finalizers, runtime-addcleanup, weak-pointer]
level: advanced
status: docs-checked
description: "Attach cleanup to Go objects with runtime.AddCleanup (1.24), understand why SetFinalizer is discouraged, and use weak pointers for caches."
sources:
  - https://pkg.go.dev/runtime#AddCleanup
  - https://pkg.go.dev/weak
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Finalizers, AddCleanup and weak pointers

**Goal:** release non-memory resources as a safety net, never as the primary mechanism.

`runtime.SetFinalizer` runs `finalizer(obj)` when the collector finds the object unreachable; that makes the object reachable again, and it is freed only the next time the collector finds it unreachable. A cyclic structure that includes a block with a finalizer is not guaranteed to be collected, and a single goroutine runs all finalizers sequentially. The docs say new code should consider `AddCleanup`, which is much less error-prone. `runtime.AddCleanup(ptr, fn, arg)` (added in Go 1.24) calls `cleanup(arg)` in a separate goroutine some time after `ptr` is unreachable; the cleanup does not receive the object, multiple cleanups may be attached to one pointer, and cleanups may run concurrently with one another.

```go
type File struct{ fd int }
func Open(path string) *File {
    f := &File{fd: openFD(path)}
    runtime.AddCleanup(f, func(fd int) { closeFD(fd) }, f.fd) // arg must not reference f
    return f
}
```

`weak.Pointer[T]` (create with `weak.Make(ptr)`) refers to an object without keeping it reachable; `wp.Value()` returns nil once the object was reclaimed. The package lists caches and canonicalisation maps as primary uses. `Value` is not guaranteed to eventually return nil, and it may return nil as soon as the object is unreachable; pass the object to `runtime.KeepAlive` after the last point it must stay reachable.

## Gotchas
- There is no specified order in which cleanups run, and a cleanup is not guaranteed to run before program exit; always provide an explicit `Close`.
- If `ptr` is reachable from the cleanup or its arg, `ptr` is never collected and the cleanup never runs; `AddCleanup` panics if `arg` equals `ptr`.
- A long-running cleanup should start a new goroutine so it does not block other cleanups.
- Cleanups are not guaranteed to run for zero-size types, for objects allocated in package-level variable initialisers, or for tiny pointer-free objects batched with live ones.

## Checked
2026-11-09. Confirmed on pkg.go.dev/runtime (`AddCleanup` added go1.24.0, `SetFinalizer` behaviour and the advice to prefer `AddCleanup`) and pkg.go.dev/weak (`Make`, `Value`, use cases, KeepAlive note). Removed: "weak.Pointer is Go 1.24" (version not on the weak page), "does not delay collection", "interior pointers" and "works with cycles" wording, and the go.dev/doc/gc-guide source, which was not read.
Method: documentation only; no commands were run.

## Verify
In a test, drop the last reference, call `runtime.GC()` in a short retry loop, and wait on a channel closed by the cleanup with a timeout (cleanups are not guaranteed to run, so keep the test tolerant).
