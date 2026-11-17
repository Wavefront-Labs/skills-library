---
id: computing-software.software-engineering.zig.optimize-modes
name: optimize-modes
category: computing-software
field: software-engineering
product: zig
tags: [zig, optimize-modes, zig-performance, releasefast, releasesafe, releasesmall, optimize-mode, build-mode]
level: practitioner
status: gated
description: "Choose Zig optimisation modes, understand which safety checks each keeps, and set defaults per project and per scope."
sources:
  - https://ziglang.org/documentation/0.15.2/
  - https://ziglang.org/learn/build-system/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Debug, ReleaseSafe, ReleaseFast and ReleaseSmall
**Goal:** pick the right mode for each situation.

| Mode | Safety checks | Speed | Size | Compile time |
|---|---|---|---|---|
| Debug | on | slow | big | fast |
| ReleaseSafe | on | fast | medium | slow |
| ReleaseFast | off | fastest | medium | slow |
| ReleaseSmall | off | fast | smallest | slow |

- Select with `-Doptimize=<mode>` (build.zig using `standardOptimizeOption`) or `-O <mode>` for `zig build-exe/run/test`.
- Default for local development is Debug; ship ReleaseSafe for services where a panic is better than silent corruption, ReleaseFast for compute kernels, ReleaseSmall for embedded and wasm.
- Per-scope: `@setRuntimeSafety(false)` in a hot function, `@setFloatMode(.optimized)` for relaxed float math.
- Dependencies can have independent optimize modes: pass `.optimize = .ReleaseFast` to `b.dependency` for a hot library while keeping your code Debug. (gated: unconfirmed, source is paywalled or blocked)
- Compare modes by running benchmarks and the test-suite in each.

## Gotchas
- Benchmarking a Debug build is meaningless.
- Behavior that relies on overflow/UB differs across modes; test at least Debug and ReleaseSafe.

## Self-check
Build the same program in all four modes, compare binary sizes and benchmark time.

## Checked
- 2026-11-02: compared with the Zig 0.15.2 language reference (ziglang.org/documentation/0.15.2/).
- Confirmed: Debug/ReleaseSafe/ReleaseFast/ReleaseSmall, -O <mode>, standardOptimizeOption, @setRuntimeSafety, @setFloatMode (language reference).
- Removed or changed: the version hedge on @setFloatMode.
- Gated: library (std) names not covered by the language reference stay marked in the text.
Method: documentation only; no commands were run.
