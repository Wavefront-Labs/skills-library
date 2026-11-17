---
id: computing-software.firmware-embedded-development.low-power-design.debugger-attached-current-measurement-pitfalls
name: debugger-attached-current-measurement-pitfalls
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [debugger-current-draw, dbgmcu, debug-in-sleep, sleep-current-measurement, power-on-reset-after-debug, swd-leakage, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Avoid false sleep-current readings with a debugger attached: debug-in-stop bits keeping clocks on, probe leakage through SWD/UART, and power-cycling after a debug session."
sources:
  - https://www.st.com/resource/en/application_note/an4445-stm32l0x1-ultralow-power-features-overview-stmicroelectronics.pdf
  - https://docs.nordicsemi.com/bundle/ps_nrf52840/page/power.html
  - https://www.segger.com/products/debug-probes/j-link/technology/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Debugger-attached measurement pitfalls

The most common "our sleep current is 1.5 mA instead of 2 uA" cause is the debug setup.

## How the debugger inflates current
- **Debug in low-power modes:** STM32 `DBGMCU_CR` DBG_SLEEP/DBG_STOP/DBG_STANDBY keep HCLK and
  the debug domain powered so the probe can stay connected; IDEs and HAL debug configs often set
  them. Stop mode then draws hundreds of uA to mA.
- **Debug power-up request:** once a debugger has set `CDBGPWRUPREQ` (any connection), many parts
  keep the debug domain on until a power-on reset. nRF52: entering System OFF with debug attached
  enters "emulated System OFF" with much higher current. A pin reset does not clear it.
- **Probe I/O paths:** SWDIO/SWCLK pulls, the probe's level shifters back-feeding through VTref,
  and a USB-UART adapter's TX line (idle high) powering the MCU through its RX pin ESD diode.
- **Probe supplying power:** J-Link/ST-LINK 3.3 V supply in the measurement path.

## Correct procedure
1. Flash and debug as normal.
2. Physically disconnect the probe (and UART adapters), or use a probe with isolated/switchable
   I/O (J-Link with `power off`, PPK2's own digital inputs for logic markers).
3. **Power cycle** the board (remove supply, not just reset) so the debug domain powers down.
4. Measure with the profiler supplying the board.
5. Release builds must clear DBGMCU bits explicitly (`HAL_DBGMCU_DisableDBGStopMode()`), because
   the register survives non-POR resets.

## If you must debug sleep current
- Keep the probe attached but disable low-power debug bits; accept that the debugger loses the
  target in Stop and reconnects under reset.
- Use GPIO markers and the profiler's logic inputs instead of breakpoints.
- Nordic: verify with `NRF_POWER->RESETREAS` that the wake was from System OFF, not emulated.

## Gotchas
- Some debuggers keep SWCLK toggling in background polling (live watch, RTT) which wakes or keeps
  the core from sleeping. Turn off live features.
- USB connected boards (Nucleo, DK) power the target from the onboard debugger; use the board's
  "IDD" jumper or cut the solder bridge to measure only the MCU.

## Verify
- [ ] Sleep current identical with probe disconnected and with probe never connected since POR.
- [ ] Release firmware leaves DBGMCU low-power debug bits cleared.
