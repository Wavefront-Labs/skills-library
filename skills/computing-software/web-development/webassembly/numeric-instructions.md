---
id: computing-software.web-development.webassembly.numeric-instructions
name: numeric-instructions
category: computing-software
field: web-development
product: webassembly
tags: [webassembly, i32-add, f64-sqrt, wasm-comparisons, wasm-instructions, wasm-numeric-instructions, wasm-variable-instructions, wasm]
level: practitioner
status: docs-checked
description: "Arithmetic and bit ops"
sources: ["https://webassembly.github.io/spec/core/syntax/instructions.html", "https://webassembly.github.io/spec/core/exec/numerics.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Numeric instructions

Goal: pick the right numeric ops.
- Integer: `add`, `sub`, `mul`, `div_s`/`div_u`, `rem_s`/`rem_u`, shifts, `rotl`, `clz`, `ctz`, `popcnt`; float: `sqrt`, `min`, `max`, `nearest`, `copysign`.
- Sign-extension ops (`i32.extend8_s`) and saturating conversions (`trunc_sat`) are part of the current instruction set.
- Shift counts are taken modulo the bit width (`k = i2 mod N`).
Verify: unit test of edge cases (shift by 32).

## Checked

2026-11-02. Confirmed against the pages listed in `sources`: integer and float op lists; `extend sz _s`; `trunc_sat`; shift count taken mod N; integer divide by zero or signed overflow is undefined (a trap).
Removed or reworded as unconfirmed: the 'separate feature sets' wording.
Method: documentation only; no commands were run.
