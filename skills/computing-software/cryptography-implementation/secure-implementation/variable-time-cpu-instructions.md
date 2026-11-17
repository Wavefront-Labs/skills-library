---
id: computing-software.cryptography-implementation.secure-implementation.variable-time-cpu-instructions
name: variable-time-cpu-instructions
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, variable-time-instructions, constant-time, division, side-channel, timing-attack]
level: advanced
status: docs-checked
description: "Avoid variable-time CPU instructions on secrets: integer division (KyberSlash) and early-terminating multiplies such as Cortex-M3 umull, with Intel DOIT as a partial mitigation."
sources: ["https://www.bearssl.org/ctmul.html", "https://kyberslash.cr.yp.to/", "https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/data-operand-independent-timing-isa-guidance.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Variable-time CPU instructions

Constant-time code avoids secret-dependent branches and memory indices, and also instructions whose latency depends
on operand values.

## Known offenders
| Instruction | Where it varies |
|---|---|
| Integer division by a public value of a secret numerator | KyberSlash: cycle counts for division vary with the inputs in various environments, and Kyber libraries divided a secret numerator by a public denominator |
| Multiplication | ARM Cortex-M3 `umull` takes 3 to 5 cycles, the short counts being documented for operands below 65536; measurements also showed short counts for zero or power-of-two operands. Thumb-mode ARM without Thumb-2, ARM9T and some PowerPC cores can exit early or need software multiply routines (BearSSL ctmul page) |

## Mitigation
- Do not divide secret values; restructure so the division becomes a multiplication and shift on a constant.
- Where multiplies are variable-time, BearSSL forces high operand bits to 1 (`MUL31`, `MUL15` macros enabled by
  `BR_CT_MUL31` / `BR_CT_MUL15`). Its author notes this does not fully fix the Cortex-M3, whose short cycle counts
  also occur for zero operands; avoid that core for secrets. 15-bit limbs with `MUL15` are the more general strategy.
- Compilers may call software routines for multiplies wider than the hardware offers (for example 64-bit operands
  on a 32-bit CPU); keep operands within 32 bits so the direct 32 to 64 opcode is used.
- On Intel cores that enumerate DOITM (`IA32_ARCH_CAPABILITIES[12]`), the listed instructions run with data
  operand independent timing when `IA32_UARCH_MISC_CTL[DOITM]` is set. Intel does not recommend enabling it
  globally, and it covers only the listed instructions.

## Detect
Disassemble the shipped objects for each target and optimisation level and check where division and multiply
instructions touch secret data. Compiler output differs between targets, so check each one you ship.

## Verify
- [ ] No secret-dependent division in crypto code on any shipped target; multiply behaviour of embedded cores checked
  against the vendor manual and the BearSSL ctmul page.

## Checked
2026-11-01. Confirmed: KyberSlash division-timing description (kyberslash.cr.yp.to); Cortex-M3 `umull` cycles,
zero-operand short counts, `MUL31`/`MUL15`, `BR_CT_MUL31`/`BR_CT_MUL15`, Thumb, ARM9T and PowerPC early exits, 32-bit
operand advice (bearssl.org ctmul); DOITM enumeration bit and MSR, not-global advice (Intel DOIT guidance). Removed:
floating-point and shift claims, "most x86 and ARM" division claim, `-Os` compiler claim, objdump command, tool names.
Method: documentation only; no commands were run.
