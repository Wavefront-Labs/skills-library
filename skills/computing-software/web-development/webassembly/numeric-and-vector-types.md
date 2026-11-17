---
id: computing-software.web-development.webassembly.numeric-and-vector-types
name: numeric-and-vector-types
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, wasm-numeric-types, v128-simd-type, wasm-integer-semantics, wasm-value-types, i32-i64-f32-f64, wasm-reference-types, wasm]
level: practitioner
status: docs-checked
description: "i32/i64/f32/f64/v128"
sources: ["https://webassembly.github.io/spec/core/syntax/types.html", "https://webassembly.github.io/spec/core/syntax/instructions.html", "https://webassembly.github.io/spec/core/exec/numerics.html", "https://webassembly.github.io/spec/core/exec/instructions.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric and vector value types

Goal: reason about Wasm values.
- Value types: i32, i64, f32, f64, v128, funcref, externref; integers carry no sign; signed and unsigned variants are separate ops (`i32.div_s` vs `i32.div_u`).
- Floats follow IEEE 754 with canonical and arithmetic NaN rules; `i32.trunc_f32_s` has no result for a NaN or out-of-range input (a trap), and the `trunc_sat` forms (`i32.trunc_sat_f32_s`) are the saturating variants.
- No dedicated boolean type: tests and comparisons produce a Boolean integer result (i32 0 or 1).
Verify: a small module exercising div/trunc traps as expected.

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: value types; `sx` signed/unsigned variants; `div_sx`, `trunc_sx`, `trunc_sat_sx` naming; NaN rules; boolean integer results.
Removed or reworded as unconfirmed: the exact saturation semantics were not read in full, so only 'saturating variants' is kept.
Method: documentation only; no commands were run.
