---
id: computing-software.software-engineering.refactoring.split-loop
name: split-loop
category: computing-software
field: software-engineering
product: refactoring
tags: [refactoring, moving-features, split-loop, loops, single-responsibility, extract-function, fowler-catalog]
level: practitioner
status: draft
description: "Split Loop: separate a loop doing two jobs into two loops so each can be extracted or replaced by a pipeline; performance concerns and how to measure them."
sources:
  - https://refactoring.com/catalog/splitLoop.html
  - https://refactoring.guru/refactoring/catalog
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Split Loop

**Smell:** one loop computes several unrelated results, so you cannot extract either calculation without touching the other.

## Before / after
```python
total_salary = 0
youngest = math.inf
for p in people:
    youngest = min(youngest, p.age)
    total_salary += p.salary
# after (step 1: split)
youngest = math.inf
for p in people:
    youngest = min(youngest, p.age)
total_salary = 0
for p in people:
    total_salary += p.salary
# after (step 2: extract / replace with pipeline)
youngest = min((p.age for p in people), default=math.inf)
total_salary = sum(p.salary for p in people)
```

## Mechanics
1. Copy the loop.
2. Remove the duplicated side effects from each copy so each does one job (watch for statements both loops need).
3. Test.
4. Slide each accumulator's initialisation next to its loop, then Extract Function or Replace Loop with Pipeline.

## Performance
Iterating twice is rarely the bottleneck for in-memory collections; clarity first, then profile. Keep a single pass when:
- the source is a one-shot iterator or stream (generator, network cursor, file read) - materialise it or keep one pass,
- the data is huge and memory bandwidth bound (measured),
- each iteration does expensive I/O.
If you must re-fuse later, do it after profiling, with a comment pointing at the benchmark.

## Gotchas
- Loops with `break`/`return` inside: splitting changes how far each half iterates. Check early-exit semantics.
- Order-dependent side effects (logging, writes) across the two jobs.

## Verify
- [ ] Tests green; each new loop/pipeline assigns one result.
- [ ] Benchmark only if the loop is on a measured hot path.
