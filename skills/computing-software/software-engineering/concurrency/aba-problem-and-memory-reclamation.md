---
id: computing-software.software-engineering.concurrency.aba-problem-and-memory-reclamation
name: aba-problem-and-memory-reclamation
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, lock-free, atomics, aba-problem, hazard-pointers, epoch-based-reclamation, tagged-pointers, crossbeam-epoch, rcu]
level: sme
status: draft
description: "Recognise the ABA problem in CAS-based lock-free structures and fix it with tagged pointers, hazard pointers, epoch-based reclamation or RCU, or avoid hand-rolling."
sources: ["The Art of Multiprocessor Programming (Herlihy, Shavit), ch10 Concurrent Queues and the ABA Problem", "https://en.cppreference.com/w/cpp/atomic/atomic_compare_exchange", "https://docs.rs/crossbeam-epoch/latest/crossbeam_epoch/", "https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/p2530r3.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The ABA problem and safe memory reclamation

**Goal:** understand why a CAS that "succeeded" can still corrupt a lock-free structure,
and how production libraries prevent it.

## The problem
Lock-free stack pop (Treiber stack):
```cpp
Node* old = head.load();
while (old && !head.compare_exchange_weak(old, old->next)) {}
```
Thread 1 reads `head = A`, `A->next = B`, then is preempted.
Thread 2 pops A, pops B, frees B, pushes A back (A's memory reused).
Thread 1 resumes: CAS sees `head == A` (same pointer!) and sets head to `B` - a freed node.
The value went A -> B -> A, so compare-and-swap cannot tell anything changed.

ABA is tightly coupled with memory reclamation: if nodes were never freed/reused while
a thread might still hold a pointer, the address couldn't come back.

## Fixes
| Technique | Idea | Notes |
|---|---|---|
| Tagged / versioned pointers | CAS a (pointer, counter) pair; counter increments on each change | needs double-width CAS (`cmpxchg16b`) or spare pointer bits; counter wrap is theoretical |
| Hazard pointers | each thread publishes the pointers it is about to dereference; nodes are freed only when no hazard pointer references them | bounded memory; C++26 `std::hazard_pointer` (P2530), Folly |
| Epoch-based reclamation | threads pin an epoch while accessing; retired nodes are freed two epochs later | fast reads; a stalled thread delays all reclamation; crossbeam-epoch (Rust) |
| RCU | readers run in read-side critical sections; writers wait for a grace period before freeing | Linux kernel, liburcu; C++26 `std::rcu` |
| Garbage collection | GC'd runtimes (Java, Go, C#) don't reuse memory while references exist | ABA on node identity is solved; ABA on VALUES can still occur |

## Value ABA in GC languages
A CAS on an integer state (`IDLE -> BUSY -> IDLE`) can't distinguish "never changed"
from "changed and changed back". If that matters, CAS on a version/stamp too
(`AtomicStampedReference` in Java) or redesign.

## Practical advice
Don't hand-roll lock-free structures in application code. Use proven ones:
`java.util.concurrent` (ConcurrentLinkedQueue), crossbeam (Rust), Folly/Boost.Lockfree/
moodycamel ConcurrentQueue (C++), `System.Collections.Concurrent` (.NET). If you must write
one, model-check it (Rust `loom`, CDSChecker/GenMC, Relacy) and run TSan stress tests.

## Verify
- [ ] Any custom CAS loop over pointers has a reclamation scheme documented in code.
- [ ] Model checker or long TSan stress run passes for custom lock-free code.
