---
id: computing-software.cryptography-implementation.secure-implementation.compiler-optimisations-breaking-constant-time
name: compiler-optimisations-breaking-constant-time
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, constant-time, timing-attack, compiler-constant-time, value-barrier, optimization-barrier, clang, llvm, assembly-review, dit]
level: sme
status: draft
description: "Stop compilers turning constant-time source into branchy binaries: value barriers, inline asm and volatile tricks, checking assembly, -O levels, and CPU DIT/DOIT modes."
sources: ["https://www.bearssl.org/constanttime.html", "https://eprint.iacr.org/2024/1060", "https://developer.arm.com/documentation/ddi0601/latest/AArch64-Registers/DIT--Data-Independent-Timing", "https://www.intel.com/content/www/us/en/developer/articles/technical/software-security-guidance/best-practices/data-operand-independent-timing-isa-guidance.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Compiler optimisations breaking constant time

C and Rust have no notion of "constant time". Optimisers recognise mask
idioms and turn them back into branches or conditional jumps: clang has
been shown to convert `(a & m) | (b & ~m)` with a 0/1-derived mask into a
branch when it can prove `m` is all-zeros or all-ones. Code that was
constant time at -O0 can leak at -O2, and a compiler upgrade can break code
that was fine for years.

## Value barriers

Hide the mask's provenance from the optimiser so it cannot reason about it:

```c
static inline uint32_t value_barrier_u32(uint32_t x) {
#if defined(__GNUC__) || defined(__clang__)
    __asm__("" : "+r"(x) : /* no inputs */);   /* compiler forgets what x is */
#else
    volatile uint32_t v = x; x = v;
#endif
    return x;
}
static inline uint32_t ct_mask(uint32_t bit) { return value_barrier_u32(0u - bit); }
```

BoringSSL (`value_barrier_w`), libsodium, and Rust's `subtle` crate
(`black_box`-style `Choice` with `core::hint::black_box` / volatile reads)
use this approach. In Rust use `subtle::ConditionallySelectable` and
`ConstantTimeEq` rather than hand-written masks.

## Check the output

- Inspect assembly for the critical functions after every compiler or flag
  change: `objdump -d --no-show-raw-insn lib.o | less`, Compiler Explorer, or
  `cargo asm`. Look for `j*` conditional jumps, `cmov` is usually fine (still
  verify per CPU guidance).
- Automated: ctgrind/`valgrind --tool=memcheck` with secrets marked
  undefined (`VALGRIND_MAKE_MEM_UNDEFINED`), `timecop`, binary-level tools
  such as `dudect` (statistical) and research tools (Binsec/Rel, ct-verif).
- Run checks in CI on release builds with production flags (LTO and PGO can
  change things).

## Hardware modes

- **ARM DIT** (Data Independent Timing, Armv8.4+): set PSTATE.DIT so listed
  instructions run in data-independent time; Apple and Linux expose it
  (`__builtin_arm_wsr("dit", 1)` style or OS APIs). Go and BoringSSL enable it
  around crypto on supporting CPUs.
- **Intel DOIT** (Data Operand Independent Timing, MSR bit) on newer Intel
  CPUs: OS-controlled; Linux has support to enable it.
Without these modes, even "constant-time" instructions like multiply may be
variable on some cores.

## Verify

- [ ] Masks pass through a value barrier or a vetted constant-time library.
- [ ] Assembly of release builds checked for secret-dependent branches.
- [ ] Constant-time checks re-run on compiler upgrades.
