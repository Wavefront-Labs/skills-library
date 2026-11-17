---
id: computing-software.firmware-embedded-development.stm32.reset-cause-decoding
name: reset-cause-decoding
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [iwdg, reset-cause, rcc-csr, rmvf, noinit-ram, fault-history, stm32, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Decode why an STM32 reset happened (watchdog, brown-out, software, pin, low-power, option-byte load) from RCC_CSR flags with the right precedence, and keep a fault history."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reset cause decoding

## The flags (RCC_CSR, L4 names; F4 is similar)
| Flag | Cause |
|---|---|
| `LPWRRSTF` | low-power reset (Stop/Standby/Shutdown exit forced to reset by the `nRST_STOP/STDBY/SHDW` option bytes) |
| `WWDGRSTF` | window watchdog |
| `IWDGRSTF` | independent watchdog |
| `SFTRSTF` | software: `NVIC_SystemReset()` (also your fault handler's reset) |
| `BORRSTF` | brown-out / power-on (F4: `PORRSTF` + `BORRSTF`) |
| `PINRSTF` | NRST pin |
| `OBLRSTF` | option byte load (`HAL_FLASH_OB_Launch`) |
| `FWRSTF` | firewall violation (L4) |

## Precedence matters
Every internal reset also drives the NRST pin low, so `PINRSTF` is set **together with** the
real cause after a watchdog or software reset. Power-on sets BOR as well. Check in priority
order and report the first match:
```c
typedef enum { RST_UNKNOWN, RST_LOWPOWER, RST_WWDG, RST_IWDG, RST_SOFTWARE,
               RST_OPTION_BYTES, RST_FIREWALL, RST_POWER, RST_PIN } reset_cause_t;

reset_cause_t reset_cause_read_and_clear(void)
{
    reset_cause_t c = RST_UNKNOWN;
    if      (__HAL_RCC_GET_FLAG(RCC_FLAG_LPWRRST)) c = RST_LOWPOWER;
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_WWDGRST)) c = RST_WWDG;
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_IWDGRST)) c = RST_IWDG;
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_SFTRST))  c = RST_SOFTWARE;
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_OBLRST))  c = RST_OPTION_BYTES;
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_FWRST))   c = RST_FIREWALL;
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_BORRST))  c = RST_POWER;
    else if (__HAL_RCC_GET_FLAG(RCC_FLAG_PINRST))  c = RST_PIN;
    __HAL_RCC_CLEAR_RESET_FLAGS();               /* RMVF: otherwise flags accumulate */
    return c;
}
```
Call it **early in `main`**, before anything that could clear the flags, and clear them so
the next boot reports only the next reset. Flags are sticky across resets until cleared.

Standby wake-ups look like resets: check `PWR_FLAG_SB` first (see standby-mode-and-wakeup-flags).

## Telling software resets apart
`SFTRSTF` covers deliberate restarts, OTA reboots, HardFault handlers that reset, and assert
failures. Record the reason before calling `NVIC_SystemReset()`:
```c
__attribute__((section(".noinit"))) static struct {
    uint32_t magic, reason, pc, lr, count;
} reset_info;

void fault_reset(uint32_t reason, uint32_t pc, uint32_t lr) {
    reset_info = (typeof(reset_info)){ 0xDEADBEEF, reason, pc, lr, reset_info.count + 1 };
    NVIC_SystemReset();
}
```
The `.noinit` section must be excluded from startup zeroing in the linker script, and the
data is only valid if `magic` matches (it's garbage after power-on). Backup registers
(`RTC->BKPxR`) also survive and are valid after power-on if VBAT is present.

## Using it
- Report reset cause and counts in telemetry; a rising IWDG count in the field is often the
  first sign of a deadlock or bus lockup.
- Boot policy: after N watchdog resets in a short time, enter safe mode or roll back firmware.

## Verify
- [ ] Trigger each cause (NRST button, `NVIC_SystemReset`, IWDG timeout, power cycle) and confirm the decoded result.
- [ ] Flags cleared each boot (two consecutive pin resets don't report the earlier watchdog).
- [ ] `.noinit` data survives software reset and is rejected after power-on.

## Checked

2026-10-31: Confirmed the L4 flag set (`RCC_FLAG_LPWRRST`, `WWDGRSTF`, `IWDGRSTF`, `SFTRSTF`, `BORRSTF`, `PINRSTF`, `OBLRSTF`, `FWRSTF` and RMVF clearing) from stm32l4xx_hal_rcc.h and stm32l476xx.h, `PORRSTF` on F4 (stm32f407xx.h), the `nRST_STOP`/`nRST_STDBY`/`nRST_SHDW` option bits (stm32l476xx.h), `__HAL_RCC_BACKUPRESET_FORCE` (stm32f4xx_hal_rcc.h, same macro family on L4), `NVIC_SystemReset` (CMSIS docs), `HAL_FLASH_OB_Launch` (stm32l4xx_hal_flash_ex.h) and the backup-register family (RTC_BKP0R.., RTC_BKP_NUMBER = 32). Reworded the LPWRRSTF table row to the reset-on-low-power-exit mechanism tied to those option bits.

Method: documentation only; no commands were run.
