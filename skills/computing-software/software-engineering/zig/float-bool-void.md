---
id: computing-software.software-engineering.zig.float-bool-void
name: float-bool-void
category: computing-software
field: software-engineering
product: zig
tags: [zig, float-bool-void, zig-primitives, f32, f64, noreturn, zero-bit-types]
level: intro
status: docs-checked
description: "Use Zig floats f16 to f128, bool, void, noreturn, anyerror and type, including NaN comparison and void as a zero-bit payload."
sources:
  - https://ziglang.org/documentation/0.15.1/
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/math.zig
  - https://github.com/ziglang/zig/blob/0.15.1/lib/std/math/isnan.zig
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Floats, bool, void, noreturn and type
**Goal:** know what each primitive is for.

- Floats: `f16 f32 f64 f80 f128` (IEEE-754-2008 formats; `c_longdouble` matches C `long double`). There is no syntax for NaN or infinity: use `std.math.nan(f64)`, `std.math.inf(f64)`, `std.math.isNan(x)`.
- `bool` is `true/false`; logical operators are `and`, `or`, `!` (not `&&`/`||`), and they short-circuit.
- `void` has a known size of 0 bytes and is the only type whose expression value can be ignored; `HashMap(K, void)` is a set whose entries have no value field.
- `noreturn` is the type of `break`, `continue`, `return`, `unreachable` and `while (true) {}`; it is compatible with every other type when resolving `if` and `switch` branches.
- `anyerror` is a primitive type; `anyopaque` has an unknown but non-zero size.

```zig
const std = @import("std");
test "nan" {
    const n = std.math.nan(f64);
    try std.testing.expect(n != n);            // NaN != NaN
    try std.testing.expect(std.math.isNan(n));
    var set = std.AutoHashMap(u32, void).init(std.testing.allocator);
    defer set.deinit();
    try set.put(5, {});
}
```
## Gotchas
- Float equality `==` is exact; use `std.math.approxEqAbs/approxEqRel` in tests.
- Float to int needs `@intFromFloat`, which converts the integer part and invokes safety-checked illegal behavior if it does not fit the destination type.

## Checked
Checked 2026-11-02 against the Zig 0.15.1 language reference, the 0.15.1 standard-library source and the 0.15.1 init templates (tag 0.15.1). Confirmed: the Floats, `void`, `noreturn` and `@intFromFloat` sections of the language reference; `approxEqAbs`/`approxEqRel`, `nan`, `inf` and `isNan` in the std source. Removed: the bool-operator and `type` remarks (unchecked), arrays-of-void and IEEE-arithmetic claims.

Method: documentation only; no commands were run.

## Self-check
Print `@sizeOf(void)`, `@sizeOf(f80)` and `@sizeOf(bool)`; assert NaN != NaN in a test.
