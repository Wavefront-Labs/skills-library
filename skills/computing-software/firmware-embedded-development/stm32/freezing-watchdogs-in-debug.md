---
id: computing-software.firmware-embedded-development.stm32.freezing-watchdogs-in-debug
name: freezing-watchdogs-in-debug
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [iwdg, watchdog-debug-freeze, dbgmcu-apb-fz, debug-halt, timer-freeze, motor-control-safety, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Stop STM32 IWDG, WWDG and timers from running while the core is halted by a debugger using DBGMCU freeze bits, so breakpoints don't reset the board or leave PWM outputs live."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4989-stm32-microcontroller-debug-toolbox-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Freezing watchdogs in debug

**Symptom:** you hit a breakpoint, look at variables for a few seconds, press continue, and
the board has reset. The IWDG kept counting while the core was halted.

## DBGMCU freeze bits
```c
DBGMCU->APB1FZR1 |= DBGMCU_APB1FZR1_DBG_IWDG_STOP;    /* L4: write the register directly */
DBGMCU->APB1FZR1 |= DBGMCU_APB1FZR1_DBG_WWDG_STOP;
DBGMCU->APB2FZR1 |= DBGMCU_APB2FZR1_DBG_TIM1_STOP;    /* timers too: see below */
```
On F4 the registers are `DBGMCU->APB1_FZ` / `APB2FZ` (`DBGMCU_APB1_FZ_DBG_IWDG_STOP`).
The bits only take effect **while the core is halted** by the debugger. In free-running
operation the watchdogs behave normally, so leaving the freeze in production code is harmless.
Put it right at the start of `main`, before the watchdog is started.

Register names vary: `DBGMCU->APB1FZR1` / `APB2FZR1` (L4, G4), `DBGMCU->APB1FZ` / `APB2FZ`
(F4), `DBGMCU->APB1LFZ1` / `APB3FZ1` / `APB4FZ1` (H7) — check the DBGMCU chapter of your
series' reference manual.

Some debugger configurations can set these bits too when the probe attaches. Doing it in
firmware makes it independent of the tool.

## Why not just disable the watchdog in debug builds?
Then the debug build never exercises the refresh logic and timing problems appear only in
release builds. Keep the watchdog enabled and freeze it on halt.

## IWDG can't be stopped
Once started (software start, or automatically when the `IWDG_SW` option bit selects hardware
watchdog), IWDG runs until reset. Freeze-on-halt is the only way to pause it. Some series also
have option bits to freeze IWDG in Stop/Standby (`IWDG_STOP`, `IWDG_STDBY`): those are about
low-power modes, not debugging.

## Timers and motor control
A halted core leaves timer outputs in their last state: a PWM output stuck high on a motor or
heater driver is a safety hazard. Freeze the timer (set its DBGMCU `DBG_TIM*_STOP` bit) **and**
configure the break/disable behaviour so outputs go to a safe level when the counter stops
(advanced timers: `MOE` cleared on break, idle states `OIS`). Also check that freezing a timer
used as the HAL timebase is what you want (time stops while halted, which keeps timeouts sane).

## Low-power debug bits are separate
`DBG_STOP`/`DBG_STANDBY` keep the debugger alive through low-power modes; they don't freeze
anything (see debugging-in-low-power-modes).

## Verify
- [ ] Halt at a breakpoint for 60 s, resume: no watchdog reset (`RCC_CSR` shows no IWDGRSTF/WWDGRSTF).
- [ ] Release build without debugger still resets on a deliberate hang.
- [ ] PWM outputs go to the safe state when halted (scope check) on motor/power designs.

## Checked

2026-10-31: Confirmed the DBGMCU freeze bits `DBGMCU_APB1FZR1_DBG_IWDG_STOP`/`_DBG_WWDG_STOP` and the timer freeze bits on L4 (stm32l476xx.h), the F4 `DBGMCU_APB1_FZ_DBG_IWDG_STOP` and `APB2FZ` registers (stm32f407xx.h), the H7 `DBGMCU_APB3FZ1`/`APB1LFZ1` registers (stm32h743xx.h), `DBGMCU_CR_DBG_STOP`/`DBG_STANDBY`, the `IWDG_SW`/`WWDG_SW` option bits, and AN4435's recommendation to freeze watchdogs at debug break. Replaced the `__HAL_DBGMCU_FREEZE_*` macro calls (these macros are not present in the fetched L4/F4 HAL headers) with direct register writes, corrected the register-name list, and removed the unverified OpenOCD/STM32CubeIDE specifics.

Method: documentation only; no commands were run.
