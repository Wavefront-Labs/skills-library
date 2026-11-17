---
id: computing-software.firmware-embedded-development.stm32.iwdg-freeze-in-stop-and-standby
name: iwdg-freeze-in-stop-and-standby
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-watchdog, iwdg-stop, iwdg-stdby, watchdog-low-power, option-bytes-iwdg, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Keep the STM32 IWDG from resetting a device in Stop or Standby using IWDG_STOP and IWDG_STDBY option bytes, or design periodic wake-ups to refresh it on series without them."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Freezing IWDG in Stop and Standby

The IWDG keeps counting in Stop and Standby (it runs from LSI). A device that sleeps for 10 min
with a 1 s watchdog resets every second. Two solutions.

## 1. Option bytes freeze (L4, L5, U5, G0, G4, WB, WL, H7)
`IWDG_STOP = 0` freezes the counter in Stop modes; `IWDG_STDBY = 0` freezes it in Standby.
(Bit value 1 = running, the default.)
Program them with STM32CubeProgrammer's option-byte commands (display the option bytes,
then set IWDG_STOP=0 and IWDG_STDBY=0; the CLI syntax is in UM2237).
From firmware:
```c
FLASH_OBProgramInitTypeDef ob = {0};
HAL_FLASHEx_OBGetConfig(&ob);
if (ob.USERConfig & OB_IWDG_STOP_RUN) {               /* still running in stop */
    HAL_FLASH_Unlock(); HAL_FLASH_OB_Unlock();
    ob.OptionType = OPTIONBYTE_USER;
    ob.USERType = OB_USER_IWDG_STOP | OB_USER_IWDG_STDBY;
    ob.USERConfig = OB_IWDG_STOP_FREEZE | OB_IWDG_STDBY_FREEZE;
    HAL_FLASHEx_OBProgram(&ob);
    HAL_FLASH_OB_Launch();                             /* reloads option bytes: system reset */
}
```
Do it in production programming rather than at runtime: an OB write that loses power midway can
corrupt option bytes. Field names per series differ (`OB_IWDG_STOP_FREEZE` on L4/G4).

## 2. Periodic wake (F2/F4/F7 and others without the bits)
F4 has no freeze option: the IWDG always runs in Stop/Standby. Wake periodically (RTC wake-up
timer) shorter than the IWDG timeout, refresh, sleep again. Use the longest timeout (PR=/256,
RLR=4095: ~32 s at 32 kHz) and RTC wake-up at, e.g., 20 s. Costs a little energy per wake.
Standby + IWDG on F4 means the device resets out of Standby: design the wake-up path to treat
an IWDG reset as a normal periodic wake (check `RCC_CSR_IWDGRSTF`) only if that is intentional.

## Trade-off
Freezing means a hang **during** Stop can't be detected (rare: the core isn't running). Hangs
in run mode are still caught.

## Verify
- [ ] Device sleeps longer than the IWDG timeout without reset (check RCC_CSR flags after wake).
- [ ] Option byte values verified in production test (STM32CubeProgrammer option-byte display).

## Checked

2026-10-31: Confirmed the `FLASH_OPTR_IWDG_STOP`/`IWDG_STDBY`/`IWDG_SW` option bits (stm32l476xx.h), the HAL `OB_IWDG_STOP_FREEZE`/`OB_IWDG_STDBY_FREEZE`/`OB_IWDG_STOP_RUN`/`OB_USER_IWDG_STOP`/`OB_USER_IWDG_STDBY`/`OPTIONBYTE_USER` constants (stm32l4xx_hal_flash.h), `HAL_FLASHEx_OBGetConfig`/`OBProgram`/`OB_Launch` and the L4 IWDG/low-power behaviour (AN4621: in all modes except Shutdown the BOR and IWDG can stay active). Rewrote the STM32_Programmer_CLI lines to point at UM2237 (the tool's PDF now redirects to a JS-only docs site, so the CLI syntax could not be read this batch).

Method: documentation only; no commands were run.
