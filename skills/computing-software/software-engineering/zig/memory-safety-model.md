---
id: computing-software.software-engineering.zig.memory-safety-model
name: memory-safety-model
category: computing-software
field: software-engineering
product: zig
tags: [zig, memory-safety-model, zig-security, memory-safety, bounds-checking, input-validation, fuzzing, hardening]
level: advanced
status: docs-checked
description: "Understand what Zig does and does not guarantee for memory safety, and apply safe modes, input validation, bounds, allocation limits and fuzzing."
sources:
  - https://ziglang.org/documentation/0.15.1/#Illegal-Behavior
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/math.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/crypto.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Zig's safety model and secure coding practice
**Goal:** write robust code in a language that is not memory safe.

- Illegal Behavior is either safety-checked (the compiler inserts a check that triggers a panic) or unchecked (anything can happen). Most Illegal Behavior is safety-checked, but safety checks are disabled by default in ReleaseFast and ReleaseSmall, and `@setRuntimeSafety` can enable or disable them per block. With checks disabled, checked cases behave like unchecked ones.
- Debug (the default) and ReleaseSafe keep safety on; `-O ReleaseSafe` optimizes for performance with safety on.
- Use `std.math.cast(T, x)`, which returns `?T`, instead of `@intCast` on untrusted values.
- Zero secrets with `std.crypto.secureZero(T, slice)`.
- `std.testing.allocator` makes tests report leaks.
- Tools against C code: `-fsanitize-c` (C undefined behavior detection), `-fsanitize-thread` (Thread Sanitizer) and `-ffuzz` are compiler flags.
- Package dependencies in `build.zig.zon` carry content hashes, and `build.zig` of a dependency is Zig code run at build time.

## Self-check
Feed random bytes to a parser in a loop under ReleaseSafe and confirm it returns errors rather than panicking.

## Checked
2026-11-02. Confirmed in the 0.15.1 language reference (Illegal Behavior), `lib/std/math.zig` (`cast`), `lib/std/crypto.zig` (`secureZero`), `src/main.zig` help text (sanitizer/fuzz flags) and `doc/build.zig.zon.md` (hashes).
Removed: the specific list of runtime checks, `readAllAlloc` caps, `errdefer` ordering, `std.crypto.random` for secrets, TOCTOU advice, CVE and DoS gotchas, ReleaseSafe-for-internet-facing recommendation.
Method: documentation only; no commands were run.
