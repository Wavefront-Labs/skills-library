---
id: computing-software.software-engineering.concurrency.exhaustive-concurrency-testing-loom-jcstress
name: exhaustive-concurrency-testing-loom-jcstress
category: computing-software
field: software-engineering
product: concurrency
tags: [concurrency, testing, loom, jcstress, model-checking, shuttle, interleavings]
level: sme
status: draft
description: "Test concurrent code systematically: loom permutation testing for Rust, jcstress for Java memory-model outcomes, Shuttle and other schedulers, and what each can and cannot find."
sources: ["https://github.com/tokio-rs/loom", "https://github.com/openjdk/jcstress", "https://github.com/awslabs/shuttle", "https://learn.microsoft.com/en-us/archive/msdn-magazine/2008/june/test-run-concurrency-testing-with-chess"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Testing concurrent code exhaustively (loom / jcstress)

Stress tests run the same interleavings over and over; bugs hide in the rare ones. These tools
explore interleavings or memory-model outcomes deliberately.

## loom (Rust)
Runs a test under a deterministic scheduler, exploring **all** interleavings (with bounding) and the
C++11 memory model's permitted reorderings for atomics.
```rust
#![cfg(loom)]          // tests/loom_tests.rs
use loom::sync::{Arc, atomic::{AtomicUsize, Ordering}};
use loom::thread;
#[test]
fn counter_is_atomic() {
    loom::model(|| {
        let n = Arc::new(AtomicUsize::new(0));
        let hs: Vec<_> = (0..2).map(|_| { let n = n.clone(); thread::spawn(move || {
            n.fetch_add(1, Ordering::Relaxed); }) }).collect();
        for h in hs { h.join().unwrap(); }
        assert_eq!(n.load(Ordering::Relaxed), 2);
    });
}
```
Run: `RUSTFLAGS="--cfg loom" cargo test --release --test loom_tests`. Swap `std::sync` for
`loom::sync` via a cfg-gated module. Keep models tiny (2-3 threads, few operations); state space
explodes. `LOOM_MAX_PREEMPTIONS=2` bounds it. Used by tokio, crossbeam.

## Shuttle (Rust, AWS)
Randomised/PCT scheduling instead of exhaustive: scales to bigger tests, finds bugs with high
probability, doesn't model weak memory. Good complement to loom.

## jcstress (Java)
Harness for testing JMM outcomes: runs actors concurrently millions of times and tallies results
against declared acceptable/forbidden outcomes.
```java
@JCStressTest
@Outcome(id = "1, 1", expect = ACCEPTABLE) @Outcome(id = "0, 0", expect = ACCEPTABLE_INTERESTING, desc = "reordering")
@State public class Reorder {
    int x, y;
    @Actor public void a1(II_Result r) { x = 1; r.r1 = y; }
    @Actor public void a2(II_Result r) { y = 1; r.r2 = x; }
}
```
Generate a project from the archetype (`jcstress-java-test-archetype`), `mvn clean verify`, then
`java -jar target/jcstress.jar -t Reorder`. Run on ARM too: x86's strong ordering hides many
outcomes. Validates publication, volatile semantics, custom lock-free code.

## Others
CHESS (.NET research), Coyote (.NET actor/task systematic testing), `go test -race` + `-count` and
the `testing/synctest` package (Go 1.24 experiment) for deterministic time, CDSChecker/GenMC for C/C++,
TLA+ for designs before code, Antithesis/deterministic simulation for whole systems.

## Limits
They test the code you model: assumptions about the environment (OS scheduling, I/O) and code
outside the model are untested. Combine with TSan/race detector in normal test runs.
