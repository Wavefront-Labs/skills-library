---
id: computing-software.software-engineering.nim.random-and-hashing-seeds
name: random-and-hashing-seeds
category: computing-software
field: software-engineering
product: nim
tags: [random-and-hashing-seeds, stdlib-math-random-misc, random, rand, randomize, shuffle, sample, seed, initrand, urandom, nim]
level: practitioner
status: docs-checked
description: "Generate pseudo-random numbers with std/random, seed deterministically, sample, shuffle, and know when to use a CSPRNG."
sources:
  - https://nim-lang.org/docs/random.html
  - https://nim-lang.org/docs/sysrand.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# random numbers, shuffling and seeding

Goal: use randomness appropriately.

- `import std/random`; call `randomize()` once to seed from time (global generator), or `randomize(1234)` for reproducible runs.
- `rand(10)` int 0..10 inclusive, `rand(1.0)` float, `rand(1..6)` range, `sample(seq)`, `shuffle(seq)`, `gauss(mu, sigma)`.
- Own generator state: `var r = initRand(42); r.rand(100)`; procs that take a `Rand` avoid the default generator, whose procs are not thread-safe.
- The generator is based on xoroshiro128+; do not use the module for cryptographic purposes.
- For tokens and keys use `std/sysrand`, a cryptographically secure generator: `urandom(size)` returns `seq[byte]`.

Gotchas:
- The default generator always starts in the same state, so without `randomize()` every run repeats.
- The procs that use the default generator are not thread-safe.

Verify: two runs with the same seed print identical sequences.

## Checked

2026-11-03. Confirmed against the random and sysrand pages: randomize() and randomize(seed), initRand(seed), rand, sample, shuffle, gauss, xoroshiro128+ basis, the default generator starting in a fixed state, default-generator procs not thread-safe, sysrand urandom(size). Real error fixed: the algorithm was named xoshiro128+/PCG; the page says xoroshiro128+. Removed: 'thread-local-ish' and the Nim 2.x remark.

Method: documentation only; no commands were run.
