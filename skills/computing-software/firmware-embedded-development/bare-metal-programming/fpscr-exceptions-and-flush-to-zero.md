---
id: computing-software.firmware-embedded-development.bare-metal-programming.fpscr-exceptions-and-flush-to-zero
name: fpscr-exceptions-and-flush-to-zero
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [fpscr, fpu, flush-to-zero, denormals, fpu-exception-flags, nan-handling, firmware-embedded-development]
level: advanced
status: draft
description: "Read and control the Cortex-M FPSCR: sticky exception flags (IOC, DZC, OFC), flush-to-zero and default-NaN modes, rounding, and the FPU interrupt line on STM32."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://www.st.com/resource/en/application_note/an4044-floatingpoint-unit-demonstration-on-stm32-microcontrollers-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# FPSCR exception flags and flush-to-zero

The Cortex-M4F/M7/M33 FPU never traps on floating-point exceptions. It sets **sticky** flags in
FPSCR and returns IEEE results (inf, NaN, denormal). If you want to know a NaN appeared, you must
look.

## FPSCR fields
| Bits | Field | Meaning |
|---|---|---|
| 0 IOC | invalid operation (0/0, sqrt(-1), inf-inf) -> NaN | sticky |
| 1 DZC | divide by zero -> inf | sticky |
| 2 OFC / 3 UFC | overflow / underflow | sticky |
| 4 IXC | inexact (happens constantly) | sticky |
| 7 IDC | input denormal (only when FZ=1) | sticky |
| 22:23 RMode | rounding: 00 nearest, 01 +inf, 10 -inf, 11 zero | |
| 24 FZ | flush-to-zero: denormals treated as 0 | |
| 25 DN | default NaN: all NaN results are the canonical quiet NaN | |
| 26 AHP | alternative half-precision | |

```c
uint32_t f = __get_FPSCR();
if (f & 0x3u) log_fp_error(f);          /* IOC or DZC */
__set_FPSCR(f & ~0x9Fu);                /* clear sticky flags */
```

## Flush-to-zero
Cortex-M4 FPU handles denormals in hardware at full speed (unlike some application cores), so FZ
is rarely a performance win on M4/M7. Use FZ+DN when you need deterministic results matching a
reference (e.g. CMSIS-DSP or a MATLAB model run with FTZ). Set default values for all contexts
via `FPU->FPDSCR` (the value loaded into FPSCR on exception entry):
```c
FPU->FPDSCR |= FPU_FPDSCR_FZ_Msk | FPU_FPDSCR_DN_Msk;
__set_FPSCR(__get_FPSCR() | (1u << 24) | (1u << 25));   /* current context too */
```
Exception handlers get FPSCR from FPDSCR, not from the interrupted code.

## FPU interrupt line (STM32 `FPU_IRQn`)
Some SoCs OR the FPSCR cumulative flags into an NVIC interrupt. Enable it to catch NaN or
divide-by-zero events as they happen. Inside the handler the flags are in the **stacked FPSCR**
of the interrupted context (lazy stacking): read via `FPU->FPCAR + 0x40`, clear it there, or
the flags reappear on return. AN4044 shows the sequence.

## Gotchas
- Compiler `-ffast-math` assumes no NaN/inf and may remove your `isnan()` checks.
- `float` comparisons with NaN are false both ways: `if (x > limit)` won't trip on NaN; use
  `if (!(x <= limit))` for safety checks.
- Sticky flags are per context only if the RTOS saves FPSCR (it does when it saves FP context).

## Verify
- [ ] A deliberate `0.0f/0.0f` sets IOC and your monitoring logs it.
- [ ] `FPU->FPDSCR` has the intended FZ/DN bits and an ISR reading FPSCR sees them.
