---
id: computing-software.software-engineering.zig.fuzz-property-tests
name: fuzz-property-tests
category: computing-software
field: software-engineering
product: zig
tags: [zig, fuzz-property-tests, zig-testing, std-testing-fuzz, property-testing, random-tests, corpus]
level: advanced
status: docs-checked
description: "Write randomised and fuzz tests in Zig using std.testing.fuzz, DefaultPrng loops and corpus seeds, and reproduce failures with fixed seeds."
sources:
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/testing.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/Random.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/compiler/build_runner.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Fuzzing and property-style tests
**Goal:** find edge cases beyond hand-written examples.

Property test with a deterministic PRNG:
```zig
test "roundtrip encode/decode" {
    var prng = std.Random.DefaultPrng.init(0xC0FFEE);   // fixed seed = reproducible failures
    const r = prng.random();
    var buf: [256]u8 = undefined;
    for (0..1000) |_| {
        const n = r.uintLessThan(usize, buf.len);
        r.bytes(buf[0..n]);
        const enc = try encode(std.testing.allocator, buf[0..n]);
        defer std.testing.allocator.free(enc);
        const dec = try decode(std.testing.allocator, enc);
        defer std.testing.allocator.free(dec);
        try std.testing.expectEqualSlices(u8, buf[0..n], dec);
    }
}
```
- `std.Random.DefaultPrng` is `Xoshiro256`; `Random` has `uintLessThan` and `bytes`.
- Integrated fuzzing: `std.testing.fuzz(context, comptime testOne: fn (context, input: []const u8) anyerror!void, options: FuzzInputOptions)`, where `FuzzInputOptions` has a `corpus` list of byte slices. `zig build --fuzz` continuously searches for unit test failures (implies `--webui`). The compiler flag `-ffuzz` enables fuzz instrumentation.
- `std.testing.allocator` reports leaks in tests, which also covers error paths.

## Self-check
Break `decode` to drop a byte and confirm the test fails.

## Checked
2026-11-02. Confirmed in 0.15.1 `lib/std/testing.zig` (`fuzz`, `FuzzInputOptions`, `expectEqualSlices`), `lib/std/Random.zig`, `lib/compiler/build_runner.zig` (`--fuzz` help text) and `src/main.zig` (`-ffuzz`).
Fixed: `zig build test --fuzz` replaced by `zig build --fuzz` as documented in the runner help. Removed: AFL++/libFuzzer advice, property suggestions, "print the seed" advice, ReleaseSafe throughput claim, non-determinism gotcha, "introduced around 0.14-0.15" hedge.
Method: documentation only; no commands were run.
