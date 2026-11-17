---
id: computing-software.firmware-embedded-development.bootloader-development.flash-unlock-sequences-and-error-flags
name: flash-unlock-sequences-and-error-flags
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [flash-unlock, flash-programming, flash-keyr, pgserr, flash-error-flags, firmware-embedded-development]
level: practitioner
status: draft
description: "Program internal flash at register level: KEYR unlock keys, relocking, clearing stale error flags (PGSERR, PGAERR, WRPERR), BSY polling, wrong-key lockout."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/user_manual/um1884-description-of-stm32l4l4-hal-and-lowlayer-drivers-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flash unlock sequences and error flags

## Unlock and lock
```c
static void flash_unlock(void) {
    if (FLASH->CR & FLASH_CR_LOCK) {
        FLASH->KEYR = 0x45670123u;          /* KEY1 */
        FLASH->KEYR = 0xCDEF89ABu;          /* KEY2 */
    }
}
static void flash_lock(void) { FLASH->CR |= FLASH_CR_LOCK; }
```
- A wrong key or wrong order locks the flash controller **until the next reset**, and on many
  families raises a bus error/HardFault. Never retry with a different sequence.
- Option bytes have a separate lock (`OPTKEYR`: 0x08192A3B, 0x4C5D6E7F) after unlocking `CR`.
- Lock again as soon as the operation is done: runaway code then can't corrupt flash.

## Before every operation
```c
while (FLASH->SR & FLASH_SR_BSY) {}
FLASH->SR = FLASH_SR_OPERR | FLASH_SR_PROGERR | FLASH_SR_WRPERR | FLASH_SR_PGAERR |
            FLASH_SR_SIZERR | FLASH_SR_PGSERR | FLASH_SR_MISERR | FLASH_SR_FASTERR | FLASH_SR_EOP;  /* W1C */
```
Stale error flags from a previous operation (or from the debugger, or from a failed write before
a reset) make the next operation fail immediately. A common symptom: "first write after boot
fails, retry works". `PGSERR` (programming sequence error) is often set after reset on some parts
when a debugger has accessed flash.

## Error flags (STM32L4 naming)
| Flag | Meaning | Usual cause |
|---|---|---|
| PROGERR | programming a non-erased double word | rewriting without erase (ECC flash) |
| WRPERR | write protection | WRP/PCROP area or RDP level |
| PGAERR | alignment | not 8-byte aligned or not a full double word |
| SIZERR | size | wrong access size during programming |
| PGSERR | sequence | PG bit not set, flags not cleared, mixing operations |
| MISERR / FASTERR | fast programming errors | fast-mode row rules violated |
| OPERR | operation error | generic; check others |

## Execution context
Code running from the same bank stalls during erase (tens of ms per page) and programming; ISRs
in that bank stall too (missed deadlines, watchdog). Run flash routines and critical ISRs from
RAM, or use the other bank on dual-bank parts. Disable the flash data cache during programming if
the family requires it, and reset caches afterwards.

## HAL equivalents
`HAL_FLASH_Unlock`, `__HAL_FLASH_CLEAR_FLAG(FLASH_FLAG_ALL_ERRORS)`, `HAL_FLASHEx_Erase`,
`HAL_FLASH_Program(FLASH_TYPEPROGRAM_DOUBLEWORD, addr, data)`, `HAL_FLASH_Lock`; check
`HAL_FLASH_GetError()` after failures.

## Verify
- [ ] Every write path clears error flags before starting and locks afterwards.
- [ ] Read-back verification after each programmed block.
