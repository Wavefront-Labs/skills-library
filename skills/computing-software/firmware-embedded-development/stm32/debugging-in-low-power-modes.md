---
id: computing-software.firmware-embedded-development.stm32.debugging-in-low-power-modes
name: debugging-in-low-power-modes
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-low-power, dbgmcu, dbg-stop, debug-low-power, low-power-current-measurement, stm32, firmware-embedded-development]
level: practitioner
status: draft
description: "Keep a debugger attached through STM32 Sleep/Stop/Standby with DBGMCU bits, recover boards that sleep before you can connect, and avoid shipping debug settings that inflate sleep current."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4989-stm32-microcontroller-debug-toolbox-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugging in low-power modes

In Stop and Standby the core clock and debug logic are off, so the probe loses the target:
"target not responding", breakpoints never hit, IDE sessions drop.

## DBGMCU low-power debug bits
```c
HAL_DBGMCU_EnableDBGSleepMode();
HAL_DBGMCU_EnableDBGStopMode();      /* DBGMCU_CR.DBG_STOP */
HAL_DBGMCU_EnableDBGStandbyMode();   /* DBGMCU_CR.DBG_STANDBY */
```
These keep the debug clock (and in Stop, HCLK/FCLK) running so the debugger stays connected and
the device still sequences through the mode. STM32CubeIDE sets them when "Debug in low power
modes" is enabled in the debug configuration; OpenOCD/pyOCD target scripts may set them too.

Consequences:
- Current in Stop with DBG_STOP set is in the **mA** range, not uA. Never judge power with the
  debugger attached.
- The bits are typically reset only by **power-on reset**, not by NRST or software reset. A
  board debugged once keeps them until power-cycled, so "low-power current is 10x too high"
  after a debug session is normal. Power-cycle before measuring, and have production firmware
  clear them explicitly at boot:
  ```c
  #ifndef DEBUG
  HAL_DBGMCU_DisableDBGStopMode(); HAL_DBGMCU_DisableDBGStandbyMode(); HAL_DBGMCU_DisableDBGSleepMode();
  #endif
  ```

## Can't connect at all
Firmware that enters Stop/Standby (or reconfigures PA13/PA14 SWD pins) immediately after boot
leaves no window for the probe.
- **Connect under reset**: the probe holds NRST, attaches, then releases. STM32CubeProgrammer:
  `-c port=SWD mode=UR`; CubeIDE: Reset behaviour "Connect under reset"; OpenOCD:
  `reset_config srst_only srst_nogate connect_assert_srst`. Needs NRST wired to the probe.
- **BOOT0 high** to start the system bootloader instead of the app, then mass-erase.
- Add a 1-2 s delay or a "stay awake" GPIO check at boot in development builds before the first
  sleep entry.
- Never repurpose SWDIO/SWCLK as GPIO without such an escape hatch.

## Observing sleep without a debugger
- Toggle a spare GPIO on entry/exit and watch it with a logic analyser alongside current.
- Count sleeps/wakes in a backup register or noinit RAM and print after wake.
- ST power shield / X-NUCLEO-LPM01A, Joulescope, PPK2: current profile shows whether the mode
  is really entered.

## Watchdogs and timers while halted
Separate from low-power bits, DBGMCU freeze bits stop IWDG/WWDG/timers when the core is
halted (see freezing-watchdogs-in-debug).

## Verify
- [ ] Debug build: breakpoint after wake-up hits with DBG bits set.
- [ ] Release build clears DBG bits at boot; sleep current correct after a debug session plus power cycle.
- [ ] Connect-under-reset recovers a board whose firmware sleeps immediately.
