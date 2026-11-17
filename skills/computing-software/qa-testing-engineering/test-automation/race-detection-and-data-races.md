---
id: computing-software.qa-testing-engineering.test-automation.race-detection-and-data-races
name: race-detection-and-data-races
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [race-detection, data-race, wild-pointers, dynamic-analysis, concurrency-testing, go-race, threadsanitizer, stress-testing]
level: practitioner
status: docs-checked
description: "Detect race conditions: race detectors (Go -race, TSan), stress and repetition runs, deterministic schedulers, and designing tests that force interleavings."
sources:
  - https://go.dev/doc/articles/race_detector
  - https://clang.llvm.org/docs/ThreadSanitizer.html
  - https://github.com/tokio-rs/loom
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Race detection

**Goal:** find concurrency defects that only appear under specific interleavings.

## Tools
- **Go**: `go test -race mypkg` runs the tests with the race detector. It only finds races that happen at runtime, so code paths your tests do not execute are not covered.
- **C/C++**: ThreadSanitizer, built with `-fsanitize=thread` (add `-g` for line numbers and `-O1` or higher for reasonable speed).
- **Rust**: `loom` runs a test many times, permuting the possible concurrent executions of small concurrent components.

## Forcing interleavings
- Barriers/latches in tests so two threads hit the critical section together:
  ```java
  CountDownLatch start = new CountDownLatch(1);
  // N threads wait on start.await(), then call account.withdraw(10)
  start.countDown(); // then assert balance == initial - 10*N
  ```
- Inject delays at seams (test-only hooks) between read and write.
- At system level: fire concurrent requests at the same resource to find lost updates, double bookings and duplicate charges.

## Typical defects
Lost update (read-modify-write without lock/version), check-then-act (`if not exists: create`), non-atomic counters, unsafe lazy init, iterating a collection while another thread mutates it.

## Gotchas
- Passing once means little; race tests need repetition and stress.
- Sleeps make races appear less often, hiding them in CI.

## Verify
The concurrency test fails reliably on the unfixed code and passes many repetitions after the fix.

## Checked
2026-11-01. Confirmed: `go test -race` and its runtime-only limitation (go.dev race detector article); `-fsanitize=thread -g -O1` (Clang ThreadSanitizer page); loom description (tokio-rs/loom README). Removed: Go `-count` flag, Java/jcstress and Python free-threading/pytest advice, k6/xargs tool names, the CTAL-TTA section reference and the specific run counts, none of which those pages state.
Method: documentation only; no commands were run.
