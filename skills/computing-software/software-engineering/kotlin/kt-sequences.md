---
id: computing-software.software-engineering.kotlin.kt-sequences
name: kt-sequences
category: computing-software
field: software-engineering
product: kotlin
tags: [kotlin, kt-collections, sequences]
level: practitioner
status: docs-checked
description: "Choose between eager collection chains and lazy Sequence pipelines."
sources: ["https://kotlinlang.org/docs/sequences.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequences and lazy evaluation
- Collection operators (`map`, `filter`) run eagerly and return an intermediate collection at each step; sequences process lazily, element by element, until a terminal operation (`toList()`, `sum()`) runs.
- Sequences avoid building intermediate results, which helps long chains; their lazy nature adds overhead that can matter for small collections or simple operations.
- `generateSequence(seed) { next }` builds a sequence from a function. Sequences can be iterated multiple times, but some implementations may allow only one iteration (documented per implementation).
Verify: benchmark with JMH or kotlinx-benchmark rather than guessing.

## Checked

Date: 2026-11-02. Confirmed on kotlinlang.org docs (sequences.html): eager vs lazy processing, intermediate vs terminal operations, generateSequence, multiple iteration caveat, small-collection overhead. Removed as not stated there: claims about first{}/take(n) early stopping and 'infinite' sequences (not read on the page).

Method: documentation only; no commands were run.
