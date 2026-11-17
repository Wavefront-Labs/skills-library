---
id: computing-software.software-engineering.concurrency.communicating-sequential-processes
name: communicating-sequential-processes
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, csp, channels, go-channels, select, message-passing]
level: advanced
status: gated
description: "Apply CSP (communicating sequential processes): share-nothing processes talking over channels, select, pipelines and fan-out/fan-in in Go, Kotlin, Rust and Clojure."
sources: ["https://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf", "https://go.dev/blog/pipelines", "https://go.dev/doc/effective_go#concurrency", "https://clojure.github.io/core.async/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Communicating sequential processes (CSP)

Hoare (1978): independent sequential processes that share no memory and interact only by sending
messages over **channels**; synchronous (rendezvous) by default. Go's motto: "Don't communicate by
sharing memory; share memory by communicating."

## CSP vs actors
| CSP | Actors |
|---|---|
| anonymous processes, named channels | named actors (addresses), anonymous messages |
| channels first-class, can be passed around | mailbox per actor |
| synchronous by default (unbuffered) | asynchronous send |
| `select`/alt over several channels | receive with pattern matching |

## Core patterns (Go)
```go
// pipeline stage with cancellation
func square(ctx context.Context, in <-chan int) <-chan int {
    out := make(chan int)
    go func() {
        defer close(out)
        for n := range in {
            select {
            case out <- n * n:
            case <-ctx.Done(): return
            }
        }
    }()
    return out
}
```
- **Fan-out**: several goroutines read from one channel to parallelise; **fan-in**: merge many
  channels into one (WaitGroup closes the output when all inputs finish).
- **select** with `default` for non-blocking ops, with `time.After` / context for timeouts.
- **Ownership rule**: the sender closes a channel, never the receiver; closing twice panics (`close of closed channel`) and sending on a closed channel panics (`send on closed channel`) (both run on Go 1.26).
- Bounded buffered channels as semaphores/backpressure (`sem := make(chan struct{}, 10)`).

## Pitfalls
- Goroutine leaks: a sender blocked forever because nobody reads (always provide a cancellation
  path; run: 10 unread senders left `runtime.NumGoroutine()` 10 higher). Detect with `goleak` in tests or the goroutine profile.
- Deadlock: all goroutines blocked; Go runtime reports `fatal error: all goroutines are asleep - deadlock!` only if
  *every* goroutine is blocked (run: main blocked on a channel with another goroutine looping on `time.Sleep` produced no report).
- Nil channels block forever (useful to disable a select case deliberately; run: a `select` with a nil-channel case and `default` took `default`).
- Channels are not always the answer: a mutex around a map is simpler for shared state; use
  channels for transferring ownership and orchestrating work.

## Other languages
Clojure `core.async` (`chan`, `go` blocks, `alts!`), Kotlin coroutines `Channel` + `select`, Rust
`crossbeam-channel` (`select!`; crate exists on crates.io) and `tokio::sync::mpsc` with `tokio::select!`, Occam (original),
Java via `SynchronousQueue` + virtual threads (Clojure, Kotlin, Rust and Java usage not run here (gated: unconfirmed, source is paywalled or blocked)).

## Reasoning
CSP has a formal algebra (FDR model checker) used to verify protocols; for everyday code, the value
is that each process is sequential and easy to reason about in isolation.
