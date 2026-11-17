---
id: computing-software.game-programming.gameplay-programming.seeded-rng-and-reproducible-generation
name: seeded-rng-and-reproducible-generation
category: computing-software
field: game-programming
product: gameplay-programming
tags: [gameplay-programming, seeded-rng, procedural-generation, prng, pcg, xorshift, determinism, daily-seed, game-programming, pcg32]
level: practitioner
status: gated
description: "Make procedural content reproducible: pick a portable PRNG (PCG, xoshiro, SplitMix), per-system streams, hash-derived chunk seeds, platform-independent float use and seed sharing."
sources: ["https://www.pcg-random.org/", "https://prng.di.unimi.it/", "https://en.cppreference.com/w/cpp/numeric/random/uniform_int_distribution"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Seeded RNG and reproducible generation

**Goal:** the same seed produces the same world on every machine, build and run, so players can
share seeds and testers can reproduce bugs.

## Choose a PRNG you own
- Engine/stdlib RNGs are often **not** stable across versions or platforms: C `rand()`, .NET
  `System.Random` (in current dotnet/runtime source, `new Random()` on the base type uses Xoshiro while `new Random(seed)` keeps the legacy algorithm for compatibility, so only seeded instances are stable), Unity `Random` (global state shared
  with everything), and C++ `std::uniform_int_distribution` (engines are specified, **distributions
  are not specified by the standard**, so standard libraries can give different numbers (gated: unconfirmed, source is paywalled or blocked; confirm in the [rand.dist] clauses of the C++ standard, cppreference does not state it)).
- Ship your own small generator: **PCG32**, **xoshiro128\*\*/xoshiro256\*\***, or **SplitMix64**
  (also good for seeding others). A few lines each, fast, well-tested. Test vectors (Python reimplementation run here): PCG32 with state seed 42 and stream 54 (`pcg32_srandom_r(&rng, 42u, 54u)`) must produce `0xa15c02b7 0x7b47f409 0xba1d3330 0x83d2f293 0xbfa4784b 0xcbed606e`, matching the reference pcg-c check output; SplitMix64 starting from state 0 gives `0xe220a8397b1dcdaf` first, using the constants `0x9e3779b97f4a7c15`, `0xbf58476d1ce4e5b9`, `0x94d049bb133111eb` with shifts 30, 27, 31 as in Vigna's reference `splitmix64.c`. Unity's `UnityEngine.Random` is a static class with one shared state (its docs contrast it with the instanced `System.Random`).
- Write your own range mapping (e.g. Lemire's multiply-shift or rejection sampling) instead of
  library distributions.

## Streams, not one global RNG
One global RNG means adding a single extra call anywhere (a new particle effect) changes every
subsequent level. Instead:
- Separate RNG instances per system: `worldGen`, `loot`, `combat`, `cosmetic`.
- **Derive seeds by hashing**: `chunkSeed = hash64(worldSeed, chunkX, chunkY, "trees")`. Each chunk
  regenerates identically regardless of visit order. Use a good mixer (SplitMix64 finaliser, xxHash).
- Cosmetic randomness (screen shake, particle jitter) uses its own unseeded RNG and never touches
  gameplay streams.

## Floats and ordering
- Floats are deterministic on the same binary and CPU family with the same settings; across
  compilers/platforms, `sin/cos/pow` and fused multiply-add can differ. For cross-platform
  reproducible generation, do generation logic in integers/fixed point or round before decisions.
- Iterate containers in a defined order: hash-map iteration order varies; sort keys first.
- Never seed from time in gameplay paths; log the seed at startup.

## Seed UX
Display the seed (and game version) in pause/results screens; accept text seeds via a stable string
hash; daily challenges use `hash(date)`. Note the version: generator changes break old seeds, so
version the generator and keep old versions if seeds are a feature.

## Verify
- [ ] Golden test: seed 12345 generates a map whose hash matches the committed value on every CI platform.
- [ ] Visiting chunks in different orders gives identical chunks.
- [ ] Adding a cosmetic random call does not change generated content.
