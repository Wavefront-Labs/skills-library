---
id: computing-software.firmware-embedded-development.bare-metal-programming.systick-clock-source-and-calib
name: systick-clock-source-and-calib
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [systick-clksource, systick-timebase, syst-calib, stcalib, reload-value, firmware-embedded-development]
level: practitioner
status: gated
description: "Choose the SysTick clock source (processor clock vs external reference such as HCLK/8), compute LOAD correctly, and read SYST_CALIB TENMS and SKEW bits."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://arm-software.github.io/CMSIS_6/latest/Core/group__SysTick__gr.html
  - https://github.com/ARM-software/CMSIS_6/blob/main/CMSIS/Core/Include/core_cm7.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SysTick clock source and calibration register

## Registers
| Register | Purpose |
|---|---|
| `SYST_CSR` (`SysTick->CTRL`) | ENABLE, TICKINT, CLKSOURCE (bit 2), COUNTFLAG (bit 16) |
| `SYST_RVR` (`LOAD`) | reload value, 24 bits (mask 0xFFFFFF) |
| `SYST_CVR` (`VAL`) | current value, 24 bits (CMSIS writes 0 to it when starting) |
| `SYST_CALIB` (`CALIB`) | TENMS (bits 23:0), SKEW (30), NOREF (31) |

## CLKSOURCE
- `1` = processor clock. `SysTick_Config()` sets this bit (CMSIS core header). (gated: unconfirmed, source is paywalled or blocked)
- `0` = an implementation-defined external reference; which clock it is, and whether one exists, is in the
  device reference manual. `CALIB.NOREF` (bit 31) set means there is no reference, so keep CLKSOURCE at 1.
  (gated: unconfirmed, source is paywalled or blocked)

Why use a slower reference: with a 24-bit counter at 480 MHz the longest period is about 35 ms; at one eighth of
that clock it is about 280 ms (useful for long single-shot delays).

## LOAD calculation
```c
SysTick->LOAD = (clk_hz / tick_hz) - 1u;   /* the counter counts LOAD..0, i.e. LOAD+1 cycles */
SysTick->VAL  = 0;
SysTick->CTRL = SysTick_CTRL_CLKSOURCE_Msk | SysTick_CTRL_TICKINT_Msk | SysTick_CTRL_ENABLE_Msk;
```
Forgetting the `-1` makes a 1 kHz tick at 64 MHz run 1/64000 slow: about 1.35 s/day.
`LOAD` must be <= 0xFFFFFF; `SysTick_Config` returns 1 if `ticks - 1` does not fit. It is left out when a
device header defines `__Vendor_SysTickConfig` as 1, in which case the vendor supplies its own.

## CALIB register
`CALIB` is read-only: `TENMS` (bits 23:0), `SKEW` (bit 30), `NOREF` (bit 31). `TENMS` is a vendor-supplied
reload value for 10 ms and `SKEW=1` means it is not exact. Treat it as a hint; compute from the known
clock frequency instead. (gated: unconfirmed, source is paywalled or blocked)

## COUNTFLAG
Bit 16 of `CTRL`. It is set when the counter reaches 0 and cleared by reading `CTRL`, which makes it usable for
polled delays without an interrupt (a debugger watch on `CTRL` can clear it). (gated: unconfirmed, source is paywalled or blocked)

## Gotchas
- After changing the system clock (PLL, low-power run), recompute LOAD or the tick rate shifts.
- SysTick may stop in deep sleep depending on the device clocking; check the reference manual before using it
  across low-power modes.

## Verify
- [ ] `SysTick->CALIB` read and NOREF checked before choosing CLKSOURCE=0.
- [ ] Toggle a GPIO each 1000 ticks: 1.000 s on a scope or frequency counter.

## Checked
2026-11-01. Confirmed in the CMSIS core header `core_cm7.h` and the CMSIS-Core SysTick page: SysTick register
names and offsets (CTRL 0x00, LOAD 0x04, VAL 0x08, CALIB 0x0C from 0xE000E010), CLKSOURCE bit 2, TICKINT bit 1,
ENABLE bit 0, COUNTFLAG bit 16, 24-bit LOAD and VAL, CALIB NOREF bit 31, SKEW bit 30, TENMS bits 23:0,
`SysTick_Config` behaviour and the `__Vendor_SysTickConfig` note. The `LOAD` and period figures are arithmetic.
Removed: STM32, nRF52 and NXP clock-source claims, the TrustZone banking claim and the claim that SysTick stops in deep sleep on most parts.
Gated: architectural meaning of CLKSOURCE, TENMS/SKEW and COUNTFLAG, because the Arm documentation pages are
JavaScript-only and could not be read.
Method: documentation only; no commands were run.
