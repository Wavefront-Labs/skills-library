---
id: computing-software.firmware-embedded-development.bootloader-development.jump-from-bootloader-to-application
name: jump-from-bootloader-to-application
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [bootloader-architecture, jump-to-application, vtor, msp, reset-vector, deinit-peripherals, cortex-m, systick-disable, firmware-embedded-development]
level: advanced
status: draft
description: "Hand control from a Cortex-M bootloader to the application safely: validate, de-initialise peripherals and interrupts, set VTOR and MSP, and branch."
sources:
  - https://developer.arm.com/documentation/dui0553/latest
  - https://github.com/mcu-tools/mcuboot/blob/main/boot/zephyr/main.c
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Jumping from bootloader to application

**Goal:** the application starts as if from reset, with no interrupts, clocks or DMA left
over from the bootloader.

## Sequence
```c
typedef void (*entry_t)(void);
#define APP_ADDR 0x08010200u            /* slot start + image header */

void boot_app(void) {
    const uint32_t *vt = (const uint32_t *)APP_ADDR;
    uint32_t sp = vt[0], pc = vt[1];
    if ((sp & 0x2FF00000u) != 0x20000000u) return;          /* sanity: SP in SRAM */
    if (pc < APP_ADDR || pc >= APP_END || !(pc & 1u)) return; /* Thumb bit set */

    __disable_irq();
    SysTick->CTRL = 0; SysTick->LOAD = 0; SysTick->VAL = 0;
    for (unsigned i = 0; i < 8; i++) {                        /* all NVIC lines */
        NVIC->ICER[i] = 0xFFFFFFFFu;
        NVIC->ICPR[i] = 0xFFFFFFFFu;
    }
    HAL_RCC_DeInit();                     /* back to reset clock (HSI) */
    HAL_DeInit();                         /* reset peripherals via RCC reset registers */
    SCB->VTOR = APP_ADDR;
    __DSB(); __ISB();
    __set_MSP(sp);
    __set_CONTROL(0);                     /* privileged, MSP, no FP context */
    __ISB();
    __enable_irq();                       /* PRIMASK must be clear: many apps never enable it */
    ((entry_t)pc)();
}
```
Signature/CRC validation of the image happens before this, not here.

## Gotchas
- **PRIMASK stays set** if you jump with interrupts disabled and the app's startup never calls
  `__enable_irq()` (most don't, because reset clears PRIMASK). Symptoms: app runs but no
  interrupt ever fires. Re-enable just before the jump (all sources are disabled in the NVIC
  so nothing fires early).
- **Leftover DMA** keeps writing into what is now the app's RAM. Reset DMA controllers
  (`__HAL_RCC_DMA1_FORCE_RESET()`), and USB if the bootloader used it.
- **Pending SysTick or fault exceptions** (`SCB->ICSR` PENDSTCLR) can fire on the first
  `__enable_irq`.
- **Caches (M7):** clean/invalidate D-cache and invalidate I-cache before the jump if the
  bootloader wrote the image into flash or ran with caches on.
- **Calling the jump from inside an ISR** leaves the core in handler mode: lower-priority
  interrupts never run in the app. Jump from thread mode only.
- **Alternative that avoids all of it:** set a magic word in no-init RAM, `NVIC_SystemReset()`,
  and have the bootloader jump immediately after reset before initialising anything.
  Cleanest state guarantee at the cost of a reset.

## Verify
- [ ] App's SysTick, UART and timer interrupts all work after the jump.
- [ ] `SCB->VTOR` read from the app equals its own vector table.
- [ ] Corrupted vector table (erase first app sector) keeps the bootloader in recovery.
