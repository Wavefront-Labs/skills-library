---
id: computing-software.software-engineering.zig.test-blocks
name: test-blocks
category: computing-software
field: software-engineering
product: zig
tags: [zig, test-blocks, zig-testing, zig-test, std-testing, expect-equal, expecterror, test-block]
level: intro
status: docs-checked
description: "Write Zig test blocks with std.testing.expect, expectEqual, expectError and expectEqualStrings and run them with zig test or zig build test."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/testing.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# test blocks, std.testing and zig test
**Goal:** unit tests in the same file as the code.

```zig
const std = @import("std");
fn add(a: i32, b: i32) i32 { return a + b; }

test "add works" {
    try std.testing.expectEqual(@as(i32, 5), add(2, 3));
    try std.testing.expect(add(1, 1) == 2);
    try std.testing.expectEqualStrings("hi", "hi");
    try std.testing.expectError(error.Bad, mayFail());
    try std.testing.expectApproxEqAbs(0.3, 0.1 + 0.2, 1e-9);
}
```
```bash
zig test src/main.zig                      # compile and run all tests reachable from this file
zig test src/main.zig --test-filter add    # only tests whose name contains "add"
zig build test                             # via build.zig (b.addTest + b.addRunArtifact), if you define that step
```
- The signature is `expectEqual(expected, actual)`; both are coerced to a common type by peer type resolution.
- A failing `try expect(false)` returns `error.TestUnexpectedResult`.
- With `std.testing.allocator` the default test runner reports leaks.
- Tests in imported files only run if referenced: `test { std.testing.refAllDecls(@This()); }` or `_ = @import("x.zig");`.
- Returning `error.SkipZigTest` makes the default test runner count the test as skipped.
- `@import("builtin").is_test` is true when compiling tests.

## Gotchas
- Tests are compiled in Debug unless you pass an optimize mode, so also run them in other modes (`-Doptimize=...` through `zig build`).
- Compare slices with `expectEqualSlices(T, expected, actual)` or `expectEqualStrings`; `expectEqualDeep` compares pointed-to values.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: `expectEqual` (peer type resolution), `expectEqualDeep`, `expectEqualSlices`, `expectEqualStrings`, `expectError`, `expectApproxEqAbs`, `refAllDecls`, `TestUnexpectedResult`, and the language reference text on `--test-filter`, `error.SkipZigTest`, `std.testing.allocator` and `is_test`. Fixed: the expected value does not determine the coerced type. Removed: the `zig test -O` flag, the leak report wording.

Method: documentation only; no commands were run.

## Self-check
Write a deliberately leaking test with `std.testing.allocator` and read the leak report.
