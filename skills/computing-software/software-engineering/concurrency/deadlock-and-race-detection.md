---
id: computing-software.software-engineering.concurrency.deadlock-and-race-detection
name: deadlock-and-race-detection
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, deadlock, data-race, race-detector, lock-ordering, happens-before, threadsanitizer, go-race-detector, mutex, livelock, thread-dump]
level: advanced
status: docs-checked
description: "Find and fix deadlocks (lock ordering, thread dumps) and data races (ThreadSanitizer, go -race) by reasoning about happens-before, not by adding sleeps."
sources: ["https://go.dev/doc/articles/race_detector", "https://go.dev/ref/mem", "https://clang.llvm.org/docs/ThreadSanitizer.html", "https://sourceware.org/gdb/current/onlinedocs/gdb.html/Threads.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deadlock and race detection — reason about happens-before, don't guess with sleeps

**Goal:** diagnose a hang (deadlock/livelock) or a flaky-only-under-load bug (data
race) with a tool that shows the ordering violation, instead of adding `sleep()`
until the symptom disappears.

## 1. Deadlock: capture where every thread is stuck, find the cycle
- **Native code (gdb)**: attach to the hung process and dump every thread's stack with
  `thread apply all bt`; `info threads` lists the threads (gdb manual, Threads).
  For each thread blocked on a lock, work out which lock it already holds from its own
  earlier frames; a cycle (`A waits for B's lock`, `B waits for A's lock`) is the deadlock.
- **Other runtimes**: use your runtime's thread or goroutine dump facility (check its
  documentation) and read each blocked stack.

The usual fix for a confirmed lock cycle is a **global lock ordering**: define one order
for acquiring any two locks and follow it everywhere, or collapse to a single lock if the
critical sections are small enough that contention doesn't matter.

## 2. Livelock and starvation look like deadlock but aren't
Threads are running, not blocked, but no forward progress happens (both repeatedly back
off and retry into each other). A stack dump shows them active rather than parked in a
lock call, which distinguishes this from a true deadlock. Fix by removing the
mutual-retry pattern or by randomising backoff.

## 3. Data races: use a race detector, don't rely on intuition
```
go test -race mypkg                            # Go built-in race detector
clang -fsanitize=thread -g -O1 tiny_race.c     # ThreadSanitizer (Clang)
```
- **Go**: add `-race` to `go test`, `go run`, `go build` or `go install`. The detector
  only finds races that happen at runtime, so it cannot see code paths that are not
  executed: run tests with good coverage, or a `-race` binary under a realistic workload.
  The Go docs give typical costs of memory and execution-time increase; plan CI
  capacity accordingly.
- **ThreadSanitizer**: compile and link with `-fsanitize=thread`; add `-O1` or higher for
  reasonable performance and `-g` for file names and line numbers in reports. It reports
  `ThreadSanitizer: data race` with the stacks of the conflicting accesses. It
  generally needs all code compiled with the flag; uninstrumented libraries can cause
  missed races or false positives.

A tool report that shows both racing accesses is stronger evidence than "we ran it a
lot and it was fine", because races depend on timing.

## 4. Reasoning with happens-before
The Go memory model defines happens-before as the transitive closure of the sequenced-before
and synchronized-before relations, and guarantees sequentially consistent behaviour only for
data-race-free programs. Without a synchronisation edge between two threads (mutex
unlock/lock, channel operation, atomic operation, thread join), do not assume ordering
or visibility, however the code reads top to bottom.

## Verify
- [ ] Any reported hang has a captured thread/goroutine dump showing the actual lock
      cycle, not just "it froze".
- [ ] CI runs `go test -race` (Go) or a ThreadSanitizer build on concurrent code.
- [ ] Every cross-thread shared value has an identified synchronisation edge, named in a
      comment if it's not obvious.
- [ ] A fixed race was re-run under the detector and confirmed clean.

## Checked
2026-11-01. Confirmed: Go "Data Race Detector" article (`-race` on test/run/build/install,
runtime-only detection, coverage advice); Go memory model (happens-before definition,
data-race-free guarantee); Clang ThreadSanitizer page (`-fsanitize=thread`, `-g`, `-O1`,
data-race warning, need for full instrumentation); gdb manual Threads page (`thread apply
all`, `info threads`). Removed unconfirmed claims: jstack and `kill -3` details and the
exact JVM deadlock message, the Go all-goroutines-asleep panic text, helgrind, `-Xcheck:jni`
and error-prone advice, `volatile`/`AtomicInteger` rules, and the exact overhead figures
(see the pages for current numbers).
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.concurrency.profiling-before-optimising,
computing-software.software-engineering.go.goroutines-channels-and-context
