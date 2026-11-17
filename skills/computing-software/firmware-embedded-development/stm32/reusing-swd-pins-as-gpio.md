---
id: computing-software.firmware-embedded-development.stm32.reusing-swd-pins-as-gpio
name: reusing-swd-pins-as-gpio
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-gpio, swd-pin-reuse, pa13-pa14, connect-under-reset, debug-pin-recovery, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Reuse STM32 SWDIO/SWCLK (PA13/PA14) and SWO pins as GPIO without bricking debug access: delayed reconfiguration, connect-under-reset recovery and boot-pin fallbacks."
sources:
  - https://www.st.com/resource/en/application_note/an4989-stm32-microcontroller-debug-toolbox-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um2237-stm32cubeprogrammer-software-description-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reusing SWD pins as GPIO

On small packages (TSSOP20, SO8 STM32G0/C0) PA13/PA14 may be needed as GPIO. Once firmware
reconfigures them, the debugger can't connect while the firmware runs.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Make it recoverable
1. **Delay** the reconfiguration by 1-2 s after reset (or until a condition, e.g. no debugger
   detected), giving a window to attach:
   ```c
   HAL_Delay(2000);                       /* debug window */
   if (!(CoreDebug->DHCSR & CoreDebug_DHCSR_C_DEBUGEN_Msk))   /* no debugger attached */
       MX_GPIO_ReuseSWD_Init();
   ```
   `C_DEBUGEN` is set while a debugger is connected (not readable by the core on Cortex-M0+ on
   some parts; test).
2. Wire **NRST** to the debug header: connect-under-reset holds the chip in reset, attaches, and
   halts before firmware runs (CubeProgrammer `mode=UR`, CubeIDE "Connect under reset").
3. Keep a **BOOT0** path: booting the system bootloader (BOOT0 high or nBOOT_SEL option bytes on
   G0) leaves SWD in its default state, so you can mass erase.

## Hardware considerations
- SWDIO has an internal pull-up and SWCLK a pull-down after reset; external circuits on those
  pins must tolerate that and must not drive the lines during debug.
- Use these pins for low-importance outputs (LED) or inputs that are idle during programming.
- SWO (PB3) reuse only removes trace output.

## F1 specifics
On STM32F1 you release JTAG/SWD with `AFIO_MAPR SWJ_CFG`; `SWJ_DISABLE` frees PA13/PA14. Same
recovery rules apply.

## Recovery when locked out
```bash
STM32_Programmer_CLI -c port=SWD mode=UR reset=HWrst -e all
```
If NRST isn't connected: power-cycle while holding BOOT0 high (system bootloader), then
connect over SWD or UART and erase.

## Verify
- [ ] Production firmware on a board: debugger connects under reset and erases.
- [ ] Delayed-switch firmware: attach works within the window.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
