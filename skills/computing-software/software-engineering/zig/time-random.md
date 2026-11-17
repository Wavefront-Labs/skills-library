---
id: computing-software.software-engineering.zig.time-random
name: time-random
category: computing-software
field: software-engineering
product: zig
tags: [zig, time-random, zig-std-time-random, timer, nanotimestamp, defaultprng, crypto-random]
level: practitioner
status: docs-checked
description: "Measure time with std.time.Timer, get timestamps, sleep, and generate pseudo-random and cryptographic random numbers in Zig."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/time.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Random.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Thread.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/mem.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Clocks, timers and random numbers
**Goal:** benchmark and randomise correctly.

```zig
var t = try std.time.Timer.start();
doWork();
const ns = t.read();                                  // monotonic nanoseconds
const ms = std.time.milliTimestamp();                 // wall clock, i64
std.Thread.sleep(10 * std.time.ns_per_ms);

var prng = std.Random.DefaultPrng.init(12345);
const r = prng.random();
const dice = r.intRangeAtMost(u8, 1, 6);
const f = r.float(f64);
r.shuffle(u32, items);

var seed: u64 = undefined;
std.crypto.random.bytes(std.mem.asBytes(&seed));      // CSPRNG from the OS
```
- Seed `DefaultPrng` from `std.crypto.random` for non-reproducible runs; a fixed seed makes tests reproducible.
- `std.time.Instant.now()` and `.since(other)` for monotonic instants.
- Sleeping is `std.Thread.sleep(ns)` in 0.15.1; `std.time` has no `sleep`.
- `std.time.epoch` converts seconds to year/month/day.

## Gotchas
- Wall-clock (`timestamp`) can go backwards; benchmark with `Timer`.
- PRNGs are not secure for tokens or keys; use `std.crypto.random`.
- Compilers may optimise away benchmarked work: use `std.mem.doNotOptimizeAway(&x)`.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference and the 0.15.1 standard-library source (tag 0.15.1). Confirmed: `Timer.start/read`, `milliTimestamp`, `Instant.now/since`, `ns_per_ms`, `time.epoch` in time.zig; `Random.DefaultPrng` (alias of Xoshiro256), `intRangeAtMost`, `float`, `shuffle`; `Thread.sleep`; `mem.doNotOptimizeAway`. Fixed: `std.time.sleep` does not exist in 0.15.1 (the example now uses `std.Thread.sleep`). Removed: the time-zone claim.

Method: documentation only; no commands were run.

## Self-check
Time a 1M-iteration loop with `Timer` and use `doNotOptimizeAway` so ReleaseFast does not delete it.
