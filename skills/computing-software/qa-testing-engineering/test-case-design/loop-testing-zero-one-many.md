---
id: computing-software.qa-testing-engineering.test-case-design.loop-testing-zero-one-many
name: loop-testing-zero-one-many
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [loop-testing, white-box-testing, boundary-value-analysis, control-flow-testing, nested-loops]
level: practitioner
status: draft
description: "Test loops systematically: skip, one, two, typical, max-1, max and max+1 iterations; nested and concatenated loops; and loop exit conditions."
sources:
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loop testing (zero, one, many iterations)

**Goal:** loops hide boundary defects (off-by-one, empty input, accumulation, termination). Classic loop testing per Beizer and Pressman.

## Simple loop (max n iterations)
Test with: 0 iterations (skip), 1, 2, m (typical, m < n), n-1, n, n+1 (if the input allows trying).
Data equivalent: empty list, single item, two items, typical batch, at page/limit size, over the limit.

## Nested loops
1. Start at the innermost loop; set outer loops to minimum iterations.
2. Run simple loop tests on the inner loop; hold outer at minimum.
3. Move outward one level; inner loops at typical values.
4. Continue until all levels are tested; finish with all loops at max together (performance/overflow).

## Concatenated loops
Independent: test each as a simple loop. If the second loop uses a counter or result from the first, treat as nested.

## Unstructured loops
Jumps into/out of loop bodies: refactor before testing; they are a defect magnet.

## What to check
- Initial state before first iteration (accumulator reset, empty result).
- Exit condition at exactly the limit; `while` with a flag that is never set (infinite loop -> use a timeout in tests).
- Early `break`/`return` paths, `continue` paths.
- Resource use over many iterations (memory growth, connections opened per iteration).
- Retry loops: 0 retries needed, succeeds on last allowed attempt, exhausts retries.

## Example: batch processor, max 500 records per batch
Inputs: 0, 1, 2, 250, 499, 500, 501 (should split into two batches), 1000 (exact multiple), 1001.

## Gotchas
- Branch coverage is satisfied by 0 and 1 iterations; it misses "many" defects.
- Pagination and streaming loops depend on server data; control it with stubs.

## Verify
Each loop in the critical module has 0/1/many and limit tests, and nested loops were tested inner-first.
