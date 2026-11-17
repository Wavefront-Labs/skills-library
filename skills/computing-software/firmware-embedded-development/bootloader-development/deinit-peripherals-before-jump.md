---
id: computing-software.firmware-embedded-development.bootloader-development.deinit-peripherals-before-jump
name: deinit-peripherals-before-jump
category: computing-software
field: firmware-embedded-development
product: bootloader-development
tags: [peripheral-deinit, bootloader-architecture, clean-handoff, pending-interrupts, systick-disable, firmware-embedded-development]
level: advanced
status: draft
description: "Return the MCU to a near-reset state before jumping from bootloader to app: disable IRQs and SysTick, clear pending NVIC bits, reset peripherals, restore clocks, and handle DMA."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://www.st.com/resource/en/application_note/an2606-stm32-microcontroller-system-memory-boot-mode-stmicroelectronics.pdf
  - https://interrupt.memfault.com/blog/how-to-write-a-bootloader-from-scratch
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# De-initialising peripherals before the jump

The application's startup code assumes reset state. A bootloader that leaves USB, UART
interrupts, DMA or a PLL running causes faults that only appear "after an update" or "only when
booted through the bootloader".

## Checklist
```c
static void deinit_before_jump(void) {
    __disable_irq();

    SysTick->CTRL = 0; SysTick->LOAD = 0; SysTick->VAL = 0;        /* else SysTick fires into the app's vector before it is ready */

    for (uint32_t i = 0; i < 8; i++) {                              /* 8 x 32 = 240+ IRQs, size to your NVIC */
        NVIC->ICER[i] = 0xFFFFFFFFu;                                /* disable all */
        NVIC->ICPR[i] = 0xFFFFFFFFu;                                /* clear pending */
    }

    /* stop bus masters first */
    dma_abort_all();                                                /* a running DMA keeps writing into "app RAM" */
    usb_disconnect_and_stop();                                      /* soft-disconnect so the host re-enumerates the app */

    /* reset peripherals used by the bootloader */
    RCC->AHB1RSTR = 0xFFFFFFFFu;  RCC->AHB1RSTR = 0;                /* family specific: reset only what you used */
    RCC->APB1RSTR1 = 0xFFFFFFFFu; RCC->APB1RSTR1 = 0;

    HAL_RCC_DeInit();                                               /* back to MSI/HSI, PLL off, if the app expects reset clocks */

    SCB->ICSR = SCB_ICSR_PENDSTCLR_Msk | SCB_ICSR_PENDSVCLR_Msk;     /* clear pending SysTick/PendSV */
    __DSB(); __ISB();
}
```
Then set VTOR, MSP and jump (see jump-to-application). Re-enable interrupts in the app, not in the
bootloader: the app's startup/`main` does `__enable_irq()` when ready (CMSIS startup doesn't
disable them, so the app must enable them explicitly if the bootloader left PRIMASK set; document
the contract).

## Items people forget
- **MPU** enabled in the bootloader: disable it (`MPU->CTRL = 0`) unless the app expects it.
- **Caches** (Cortex-M7): clean and disable D-cache, invalidate I-cache, or the app's
  `SCB_EnableDCache()` sees stale state.
- **CONTROL register**: if the bootloader used PSP or unprivileged mode, reset CONTROL to 0 and
  `__ISB()`.
- **FPU**: clear `FPCCR`/lazy state if the bootloader used floating point (CONTROL.FPCA).
- **Watchdog**: IWDG cannot be stopped once started; the app must refresh it early (document it).
- **GPIO** in alternate function for an update interface may glitch external parts; return to
  analog/input.

## Alternative: reset into the application
Set a no-init RAM flag ("boot app directly") and `NVIC_SystemReset()`; on the next boot the
bootloader checks the flag first and jumps immediately with untouched reset-state hardware.
Simplest way to guarantee a clean handoff.

## Verify
- [ ] App behaves identically when flashed standalone at its address (with a debugger) and when started by the bootloader.
- [ ] No unexpected interrupt fires in the app before it enables that peripheral.
