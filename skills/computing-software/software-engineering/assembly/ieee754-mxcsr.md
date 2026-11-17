---
id: computing-software.software-engineering.assembly.ieee754-mxcsr
name: ieee754-mxcsr
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, ieee754-mxcsr, asm-x87]
level: advanced
status: draft
description: "Control IEEE 754 behaviour in SSE code: MXCSR layout, rounding modes, flush-to-zero and denormals-are-zero, NaN compares and callee-saved control bits."
sources:
  - https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html
  - https://gitlab.com/x86-psABIs/x86-64-ABI
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# IEEE 754 handling in SSE: NaN, rounding, MXCSR
**Goal:** read and set floating-point control state correctly.

- MXCSR (32-bit): bits 0-5 sticky exception flags (IE DE ZE OE UE PE), bit 6 DAZ, bits 7-12 exception masks, bits 13-14 rounding control, bit 15 FTZ. Reset value 0x1F80 (all exceptions masked, round to nearest even).
- Rounding control: 00 nearest-even, 01 toward -inf, 10 toward +inf, 11 toward zero.
```nasm
sub     rsp, 8
stmxcsr [rsp]
or      dword [rsp], (1<<15)|(1<<6)   ; FTZ and DAZ: flush denormals
ldmxcsr [rsp]
add     rsp, 8
```
- NaN: any compare with NaN is unordered; `ucomisd` sets ZF=PF=CF=1, so test `jp` first. `x != x` is true only for NaN.
- `cvtsd2si` honours the rounding mode; `cvttsd2si` always truncates. `roundsd` (SSE4.1) rounds with an explicit mode.
- SysV: MXCSR control bits (6-15) are callee-saved; status bits (0-5) are not. A function that changes rounding must restore it.

## Gotchas
- FTZ/DAZ speed up denormal-heavy code but break strict IEEE results.
- Unmasking exceptions turns SSE faults into SIGFPE; most runtimes keep them masked.

## Self-check
Set round-toward-zero, convert 2.9 with `cvtsd2si`, expect 2, then restore MXCSR.
