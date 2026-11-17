---
id: computing-software.firmware-embedded-development.bare-metal-programming.float-abi-selection
name: float-abi-selection
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [fpu, float-abi, mfloat-abi-hard, softfp, mfpu, fpv4-sp-d16, single-precision-literals, double-promotion, abi-mismatch-link-error, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose GCC -mfloat-abi and -mfpu for Cortex-M, avoid hard/soft ABI link errors with vendor libraries, and keep single-precision code from silently using double."
sources:
  - https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Optimize-Options.html
  - https://gcc.gnu.org/onlinedocs/gcc-14.2.0/gcc/Warning-Options.html
  - https://github.com/ARM-software/abi-aa/blob/main/aapcs32/aapcs32.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Float ABI selection

**Goal:** compiler flags that use the FPU the core actually has, link with every library,
and keep float math single-precision on single-precision FPUs.

## Flags
Three GCC options decide this: `-mcpu=` (the core), `-mfpu=` (what floating-point hardware
exists) and `-mfloat-abi=` (`soft`, `softfp` or `hard`).
- `-mfpu=` accepts, among others, `fpv4-sp-d16`, `fpv5-sp-d16`, `fpv5-d16`, `vfpv4-d16`, `auto`
  and `vfpv3-d16` (the full list is on the GCC ARM Options page). The `sp` names are the
  single-precision-only variants.
- Which name matches your part comes from the core's technical reference manual or the
  vendor reference manual, which this review could not read; look it up there. With no FPU,
  use `-mfloat-abi=soft`.
- Use identical `-mcpu`, `-mfpu` and `-mfloat-abi` for every object and for the final link, so
  that every piece agrees on the calling convention (below).
- GCC's `-mcpu=` description lists extension suffixes for newer cores (for example turning off
  DSP or MVE parts on `cortex-m55`); read it for your core.

## hard vs softfp vs soft
- `soft`: GCC generates library calls for floating-point operations.
- `softfp`: may generate hardware floating-point instructions but still uses the soft-float
  calling conventions, so it stays call-compatible with soft-float code.
- `hard`: generates FPU instructions and uses FPU-specific calling conventions. The AAPCS VFP
  variant passes floating-point arguments in `s0`-`s15` (`d0`-`d7`), and `s16`-`s31` are
  callee-saved.
- Because the calling conventions differ, objects built for `hard` cannot simply be mixed with
  `soft`/`softfp` objects; the linker rejects the mismatch. Usual cause: a vendor's
  precompiled `.a` (DSP, BLE stack, sensor fusion) built for a different ABI. Pick the library
  variant that matches your setting, or build everything with the same ABI. Check the vendor's
  library names for the variant they encode.

## Keeping it single precision
GCC's `-Wdouble-promotion` text: CPUs with a 32-bit single-precision unit implement `float` in
hardware but emulate `double` in software, so `double` computation is much more expensive,
and floating-point literals are implicitly `double`.
- Literals: `x * 0.5` is double; write `0.5f`. `-fsingle-precision-constant` treats
  floating-point constants as single precision instead of implicitly converting them to double
  (it changes semantics: use knowingly).
- Math functions: `sinf`, `sqrtf`, `fabsf`, not `sin`, `sqrt`.
- `printf("%f", x)` takes a `double` through varargs; avoid in hot paths.
- Enable `-Wdouble-promotion` (warns when a `float` is implicitly promoted to `double`) and
  `-Wfloat-conversion` (warns for implicit conversions that reduce the precision of a real
  value; also enabled by `-Wconversion`).
- Check the map/disassembly for soft-float helper calls: their presence means software
  floating-point is linked.

## Other knobs
- `-ffast-math` is shorthand for `-fno-math-errno`, `-funsafe-math-optimizations`,
  `-ffinite-math-only`, `-fno-rounding-math`, `-fno-signaling-nans`, `-fcx-limited-range` and
  `-fexcess-precision=fast`, and defines `__FAST_MATH__`. Read what each option relaxes before
  using it on code that tests for NaN or infinity.
- `-ffp-contract=fast` allows forming fused multiply-add operations if the target has native
  support (it is the default outside strict ISO modes such as `-std=c11`, where the default is
  `off`).

## Verify
- [ ] `arm-none-eabi-readelf -A firmware.elf` shows the floating-point build attributes you expect for the ABI you chose.
- [ ] `nm firmware.elf` shows no unexpected soft-float helper symbols (or each hit is justified) on single-precision-FPU parts.

## Checked
Checked 2026-11-08 against the GCC ARM Options page (`-mfloat-abi`, `-mfpu` names, `-mcpu`
extensions), GCC 14.2 Optimize Options (`-ffast-math`, `-ffp-contract`,
`-fsingle-precision-constant`) and Warning Options (`-Wdouble-promotion`, `-Wfloat-conversion`),
and the AAPCS32 document (VFP argument registers `s0`-`s15`, `s16`-`s31` preserved). Removed
because no readable page states them: the core-to-flags table (the Arm technical reference
manuals were unreadable), the "100x slower" figure, the exact linker error text and the Arm
library file name, the `__aeabi_d*` helper names, `FPSCR.FZ` behaviour, and the multilib
selection remark.
Method: documentation only; no commands were run.
