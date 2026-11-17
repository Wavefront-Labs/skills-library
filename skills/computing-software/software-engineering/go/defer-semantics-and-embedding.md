---
id: computing-software.software-engineering.go.defer-semantics-and-embedding
name: defer-semantics-and-embedding
category: computing-software
field: software-engineering
product: go
tags: [go, golang, go-defer, struct-embedding, named-results, defer-in-loop, close-errors, promotion, composition, go-defer-control, go-defer-order]
level: practitioner
status: verified
description: "Use defer correctly (argument evaluation, loops, named results to capture Close errors) and struct/interface embedding without leaking unintended methods."
sources: ["https://go.dev/blog/defer-panic-and-recover", "https://go.dev/ref/spec#Defer_statements", "https://go.dev/doc/effective_go#embedding", "https://go.dev/ref/spec#Struct_types"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# defer semantics and embedding

**Goal:** cleanup that runs when and with the values you expect, and composition via
embedding that doesn't expose more API than intended.

## defer rules
1. Deferred calls run LIFO when the surrounding FUNCTION returns (not the block).
2. Arguments are evaluated when `defer` executes, not when the call runs:
   ```go
   start := time.Now()
   defer log.Printf("took %v", time.Since(start))          // WRONG: evaluated now, ~0s
   defer func() { log.Printf("took %v", time.Since(start)) }()   // right
   ```
3. Deferred closures can read and modify named results.

## Capturing Close errors on writes
Ignoring `Close()` on a written file can lose data (buffered writes fail at close):
```go
func write(path string, data []byte) (err error) {
    f, err := os.Create(path)
    if err != nil { return err }
    defer func() { err = errors.Join(err, f.Close()) }()
    _, err = f.Write(data)
    return err
}
```
For read-only files, `defer f.Close()` ignoring the error is fine.

## defer in loops
```go
for _, p := range paths {
    f, _ := os.Open(p)
    defer f.Close()     // all files stay open until the function returns: fd exhaustion
}
```
Move the body into a helper function (or a closure called per iteration) so each defer
runs per item.

## Cost
Since Go 1.14 open-coded defers are nearly free; don't avoid defer for performance
except in extremely hot loops (where it's also usually wrong per above).

## Embedding
```go
type Logger struct{ prefix string }
func (l *Logger) Log(msg string) { ... }

type Server struct {
    *Logger            // methods promoted: s.Log("x")
    mu sync.Mutex      // named field: NOT promoted (good; don't embed sync.Mutex in exported types)
}
```
- Embedding is composition with method promotion, not inheritance: inside `Log`, the
  receiver is the `*Logger`, never the Server. No virtual dispatch back to the outer type.
- Embedding an exported type in an exported struct makes all its methods part of YOUR
  API (embedding `sync.Mutex` exposes `Lock/Unlock` to callers). Prefer a named field.
- Embedding an interface in a struct (common in tests to "implement" a large interface
  partially) panics with nil-pointer if an unimplemented method is called.
- Name conflicts at the same depth are ambiguous and only error if used.

## Verify
- [ ] No `defer` inside loops over unbounded inputs.
- [ ] Write paths propagate `Close` errors.
- [ ] Exported structs don't embed types whose methods shouldn't be public.

## Checked
- Go 1.25.1: deferred closures run LIFO and `defer fmt.Println(i)` in a loop printed `2 1 0`; deferred arguments are evaluated at the `defer` statement while a deferred closure reads current values; a deferred closure modified named results (`21` became `42` with an error set); `errors.Join(err, f.Close())` pattern compiled and wrote a file; promoted methods work and `Hello` called `Logger.Who` (not `Server.Who`), so no virtual dispatch; a struct embedding an interface panicked with a nil pointer on the unimplemented method; two embedded types with the same method compile until the ambiguous selector is used (`ambiguous selector ab.Name`). The Go 1.14 notes say defer overhead is almost zero. fd exhaustion from defer in loops was not reproduced.
