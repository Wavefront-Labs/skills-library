---
id: computing-software.software-engineering.d.d-inline-asm-x86-syntax
name: d-inline-asm-x86-syntax
category: computing-software
field: software-engineering
product: d
tags: [d-inline-asm-x86-syntax, inline-asm, asm, naked, x86-64, d_inlineasm_x86_64, intel-syntax, assembler, d]
level: sme
status: draft
description: "Write asm { } blocks in D: Intel-like syntax, accessing locals by name, naked functions, registers preserved by ABI, and version(D_InlineAsm_X86_64) guards."
sources:
  - https://dlang.org/spec/spec.html
  - https://dlang.org/phobos/index.html
  - https://dub.pm/
  - https://ddili.org/ders/d.en/index.html
  - https://dlang.org/articles.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# asm blocks on x86 and x86-64 (dmd syntax)

Goal: embed machine code only where needed.

```d
version (D_InlineAsm_X86_64)
ulong rotl(ulong v, ubyte n) {
    asm pure nothrow @nogc { naked; mov RCX, RSI; mov RAX, RDI; rol RAX, CL; ret; }  // SysV args in RDI, RSI
}
```
- Syntax is Intel order (destination first); labels `L1:`; `align`, `db`/`dw`/`dd`/`dq` data directives; `asm { naked; }` removes prologue/epilogue (you write `ret`).
- Locals and parameters are addressable by name in non-naked asm (`mov EAX, x;`); use `[RBP+offset]` only in naked.
- ABI: SysV (Linux/macOS) args RDI, RSI, RDX, RCX, R8, R9; Win64 RCX, RDX, R8, R9; callee-saved RBX, RBP, R12-R15 (and RDI, RSI on Win64); return in RAX/XMM0.
- Attributes after `asm` (`pure nothrow @nogc @trusted`) assert safety; asm is `@system` by default.
- Guard: `version (D_InlineAsm_X86_64) {...} else {portable fallback}` (and `D_InlineAsm_X86`).
- Prefer `core.bitop` (`bsf`, `bsr`, `bswap`, `popcnt`, `rol`, `ror`), `core.simd` and intrinsics first.

Gotchas:
- dmd asm is not available on ARM or in LDC (LDC uses `ldc.llvmasm`/`__asm`); gate every use.
- The optimizer cannot see through asm blocks.

Verify: unittest comparing asm result with the portable implementation across random inputs.
