---
id: computing-software.software-engineering.assembly.aapcs64-platform-variants
name: aapcs64-platform-variants
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, aapcs64-platform-variants, asm-abi-aapcs64]
level: sme
status: docs-checked
description: "Platform deviations from AAPCS64: the platform register X18, Windows ARM64 variadic arguments and frame pointer rules; Apple rules to be read from Apple."
sources:
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs64/aapcs64.rst
  - https://learn.microsoft.com/en-us/cpp/build/arm64-windows-abi-conventions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Platform deviations from AAPCS64
**Goal:** make AArch64 code portable or deliberately platform-specific.

- AAPCS64 leaves `x18` to the platform: a platform ABI that needs a dedicated register for inter-procedural state (for example the thread context) uses it, otherwise it is an extra caller-saved register. The platform ABI must document its use, so portable assembly avoids `x18`.
- AAPCS64 also lets each platform choose how strictly frame records are kept (always valid, with or without leaf exceptions, or the frame pointer as a general callee-saved register).
- Windows on ARM64 (Microsoft Learn): `x18` is reserved; in user mode it points to the TEB (in kernel mode to the KPCR). The frame pointer `x29` is required, for fast stack walking, and must point to the previous `{x29, x30}` pair. For non-variadic functions it follows the Arm parameter-passing rules.
- Windows variadic functions differ: all composites are treated alike (no special HFA/HVA treatment), SIMD and floating-point registers are not used, and arguments are laid out as on an imaginary stack whose first 64 bytes load `x0`-`x7`, with the rest placed on the stack normally.
- Apple platforms and Linux: not covered here. Read Apple's "Writing ARM64 code for Apple platforms" for Darwin rules; the Linux behaviour is plain AAPCS64.

## Gotchas
- Varargs assembly written for AAPCS64 reads the wrong places on Windows.
- Avoid `x18` everywhere to stay portable.

## Self-check
List the register or layout change you must make to port a variadic wrapper from AAPCS64 to Windows ARM64.

## Checked
2026-11-02. Checked against AAPCS64 (abi-aa, aapcs64.rst: r18 note, frame pointer section) and Microsoft Learn "ARM64 Windows ABI conventions" (x18, x29, variadic addendum). Removed: every Apple Darwin claim (x18, frame pointer, packed stack arguments, underscore symbol prefix) because Apple's page returned no readable text, and the armasm64/clang syntax remark and the symbol-prefix macro example.

Method: documentation only; no commands were run.
