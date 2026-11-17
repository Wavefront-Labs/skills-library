---
id: computing-software.software-engineering.code-review.reviewing-concurrent-code
name: reviewing-concurrent-code
category: computing-software
field: software-engineering
product: code-review
tags: [code-review, specialised-review, concurrency-review, thread-safety, race-conditions, check-then-act, lock-ordering, async-review]
level: advanced
status: draft
description: "Review concurrent and async code for races, check-then-act, unsafe publication, lock ordering, blocking in async contexts, cancellation and shared-state leaks."
sources: ["Java Concurrency in Practice (Goetz et al.), ch2-3 and ch10", "https://google.github.io/eng-practices/review/reviewer/looking-for.html#functionality", "https://go.dev/ref/mem"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reviewing concurrent code

**Goal:** catch concurrency bugs in review, where they're cheap; in production they are
intermittent, unreproducible and expensive.

## First: map the shared state
For each piece of mutable state touched by the change, ask: which threads/tasks/requests
can access it, and what protects it (lock, confinement, immutability, atomic)?
Document the answer in a comment (`// guarded by mu`) if it isn't obvious; Java's
`@GuardedBy` / Clang `-Wthread-safety` annotations make it checkable.

## Checklist
- **Check-then-act / read-modify-write** without a lock: `if (!map.containsKey(k)) map.put(...)`,
  `count = count + 1`, lazy init `if (instance == null)`. Ask for atomic ops or a lock
  around the whole sequence.
- **Compound invariants**: two fields that must change together, protected by
  different locks or one unprotected.
- **Unsafe publication**: objects shared before construction completes; non-volatile
  flags polled by another thread.
- **Lock ordering**: multiple locks acquired in different orders on different paths;
  calling unknown code (callbacks, listeners, virtual methods) while holding a lock.
- **Holding locks during I/O** or long work: contention and latency.
- **Async**: blocking calls on event loops (`time.sleep`, sync DB driver in asyncio,
  `.Result`/`.Wait()` in C#, blocking in tokio tasks); missing awaits (floating promises);
  locks held across `await`.
- **Cancellation and shutdown**: are tasks/goroutines stopped? Leaks of goroutines blocked
  on channels nobody reads; executors never shut down.
- **Shared mutable state across requests**: singletons/static fields holding
  request-specific data (cross-user data leaks).
- **Thread-unsafe library objects** shared (SimpleDateFormat, HashMap, some HTTP
  clients/DB connections).
- **Tests**: is there a stress test or race-detector run (`go test -race`, TSan,
  jcstress)? "It passed once" proves nothing.

## Asking for simpler designs
Often the best review comment is "can we avoid sharing this at all?": confine state to
one goroutine/actor, use immutable snapshots, or message passing.

## Verify
- [ ] Every new shared mutable field has a documented protection mechanism.
- [ ] CI runs the race detector / sanitizer for the affected packages.
