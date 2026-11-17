---
id: computing-software.software-engineering.concurrency.lock-free-and-atomic-patterns
name: lock-free-and-atomic-patterns
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, atomics, lock-free, compare-and-swap, cas, memory-ordering, memory-barrier, acquire-release, sequential-consistency, abi-problem, wait-free]
level: sme
status: docs-checked
description: "Use atomics correctly: memory ordering (acquire/release vs relaxed vs seq_cst), CAS loops, Go sync/atomic semantics, and why a mutex is usually the right answer anyway."
sources: ["https://en.cppreference.com/cpp/atomic/memory_order", "https://pkg.go.dev/sync/atomic", "https://go.dev/ref/mem", "https://clang.llvm.org/docs/ThreadSanitizer.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Lock-free and atomic patterns — and why a mutex is usually still correct

**Goal:** know when lock-free code earns its complexity, and the memory-ordering rules
that make it correct instead of a hard-to-reproduce bug.

## 0. Default to a mutex
Lock-free code is much harder to verify than a lock. Justify it with profiling evidence of
lock contention (computing-software.software-engineering.concurrency.profiling-before-optimising),
not intuition, and reach for it only on a specific measured hot path.

## 1. Memory orders in C++
`std::memory_order` values are `relaxed`, `consume`, `acquire`, `release`, `acq_rel` and
`seq_cst`. From cppreference:
- **Default**: all atomic operations in the library are sequentially consistent unless you
  pass a `std::memory_order` argument; the page notes the default can hurt performance.
- **`memory_order_relaxed`**: only the operation's atomicity is guaranteed, with no
  synchronisation or ordering constraints on other reads or writes.
- **`memory_order_acquire`** (load) and **`memory_order_release`** (store): no reads or
  writes in the current thread can be reordered before the acquire load or after the
  release store, and all writes the releasing thread made are visible to a thread that
  acquires the same atomic variable. Publishing an object through an atomic pointer with
  release-store and acquire-load is the standard use. A mutex `lock()` is an acquire
  operation and `unlock()` a release operation.
- **`memory_order_seq_cst`**: acquire for loads, release for stores, both for
  read-modify-write, plus a single total order in which all threads observe all
  modifications in the same order.

Choose weaker orders only where you can state what each one synchronises with, and
document it.

## 2. Go's `sync/atomic`
The package docs say that if the effect of an atomic operation A is observed by atomic
operation B, then A "synchronizes before" B, and that all atomic operations in a program
behave as though executed in some sequentially consistent order, matching C++
sequentially consistent atomics and Java `volatile`. The package provides
`CompareAndSwap` functions per type (for example `CompareAndSwapInt32`) and an
`atomic.Value` type. A hand-rolled spinlock built on CAS reimplements `sync.Mutex`;
prefer the mutex unless measurement says otherwise.

## 3. The ABA problem
A CAS succeeds because the value matches, but the object may have been freed and a
different one given the same address in between, so the CAS wrongly believes nothing
changed. It is classic in lock-free structures using raw pointers. Use an established
mitigation (version-tagged pointers, hazard pointers, epoch-based reclamation) rather than
hand-rolling one; see the ABA and memory-reclamation skill in this library.

## 4. Testing
Unit tests rarely catch ordering bugs. Run concurrent code under ThreadSanitizer (Clang
`-fsanitize=thread`) or the Go race detector, which report data races with both stacks.
Memory models differ between C++, Java and Go, so port the reasoning of a published
algorithm, not the code, and verify it against the target language's own model.

## Verify
- [ ] Profiling data justifies skipping a mutex for this path.
- [ ] Every atomic's memory order is deliberate and documented with what it synchronises
      with.
- [ ] Any pointer-based lock-free structure has an explicit ABA mitigation.
- [ ] The code was run under a race detector or sanitizer.

## Checked
2026-11-01. Confirmed: cppreference `std::memory_order` (list of orders, seq_cst default
and its performance note, relaxed/acquire/release/seq_cst semantics, mutex lock/unlock as
acquire/release); Go `sync/atomic` package docs (synchronizes-before, sequentially
consistent order, CompareAndSwap functions, `Value`); Go memory model; Clang
ThreadSanitizer. Removed unconfirmed claims: `compare_exchange_weak` spurious failure
and `fetch_add` advice, x86-versus-ARM failure behaviour, false-sharing section
(`alignas(64)`), `atomic.Pointer[T]` version note, specific library names for
reclamation, and the performance comparison of mutex versus CAS loops.
Method: documentation only; no commands were run.

Related: computing-software.software-engineering.concurrency.deadlock-and-race-detection,
computing-software.software-engineering.concurrency.profiling-before-optimising
