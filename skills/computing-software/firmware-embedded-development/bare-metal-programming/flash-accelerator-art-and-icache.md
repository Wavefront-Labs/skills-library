---
id: computing-software.firmware-embedded-development.bare-metal-programming.flash-accelerator-art-and-icache
name: flash-accelerator-art-and-icache
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [art-accelerator, flash-prefetch, vendor-icache, flash-wait-state-hiding, stm32-icache, firmware-embedded-development]
level: advanced
status: draft
description: "Enable vendor flash accelerators (ST ART, prefetch, I/D caches, ICACHE on L5/U5/H5) to hide flash wait states, and handle invalidation after flash programming."
sources:
  - https://www.st.com/resource/en/reference_manual/rm0090-stm32f405415-stm32f407417-stm32f427437-and-stm32f429439-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
  - https://www.st.com/resource/en/application_note/an5212-improve-stm32-mcu-performance-with-icache-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0432-stm32l4-series-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Vendor flash accelerators (ART and ICACHE)

Cortex-M3/M4/M33 cores have no architectural cache; at 80-170 MHz flash needs 2-8 wait states.
Vendors put a cache/prefetch unit between the bus and flash. Leaving it disabled can halve
performance; leaving it enabled across flash writes can execute stale code.

## STM32F2/F4/L4/G4: ART accelerator and caches in FLASH_ACR
```c
FLASH->ACR = FLASH_ACR_LATENCY_5WS          /* set latency first (before raising clock) */
           | FLASH_ACR_PRFTEN               /* prefetch */
           | FLASH_ACR_ICEN | FLASH_ACR_DCEN;   /* instruction and data (literal) caches */
```
HAL: `__HAL_FLASH_PREFETCH_BUFFER_ENABLE(); __HAL_FLASH_INSTRUCTION_CACHE_ENABLE(); __HAL_FLASH_DATA_CACHE_ENABLE();`
(`PREFETCH_ENABLE` etc. in `stm32xxxx_hal_conf.h`).

**After programming or erasing flash** (bootloader, EEPROM emulation in the same bank): reset the
caches or the CPU may run old instructions/constants:
```c
FLASH->ACR &= ~(FLASH_ACR_ICEN | FLASH_ACR_DCEN);
FLASH->ACR |= FLASH_ACR_ICRST | FLASH_ACR_DCRST;
FLASH->ACR &= ~(FLASH_ACR_ICRST | FLASH_ACR_DCRST);
FLASH->ACR |= FLASH_ACR_ICEN | FLASH_ACR_DCEN;
```
Caches must be disabled while asserting the reset bits.

## STM32L5/U5/H5/WBA: ICACHE peripheral
A separate `ICACHE` block caches code from flash and external memory (OCTOSPI):
```c
ICACHE->CR = ICACHE_CR_WAYSEL;   /* 2-way set-associative (default on reset may be 1-way/direct) */
ICACHE->CR |= ICACHE_CR_EN;
```
Invalidate with `ICACHE_CR_CACHEINV` (wait for `BUSYF`/`BSYENDF`). Region remapping lets external
memory be cached too. Some parts also have a DCACHE for external memory.

## Other vendors
- NXP LPC55: FMC flash cache/prefetch config in `SYSCON->FMCCR`.
- Nordic nRF52: `NVMC->ICACHECNF` (cache enable and profiling hit/miss counters).
- Microchip SAM D5x: `CMCC` cache controller.

## Measuring
nRF52 and STM32 ICACHE expose hit/miss counters (ICACHE `HMONR`/`MMONR`). Use them, or DWT
CYCCNT on a benchmark loop, before and after enabling.

## Verify
- [ ] Benchmark (CoreMark or a hot loop) with accelerators on vs off: expect large gains at high wait states.
- [ ] After a bootloader writes a new image and jumps without reset, caches were reset first.
