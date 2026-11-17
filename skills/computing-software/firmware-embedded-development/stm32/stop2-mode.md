---
id: computing-software.firmware-embedded-development.stm32.stop2-mode
name: stop2-mode
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-low-power, stop2-mode, hal-pwrex-enterstop2mode, stopwuck, wakeup-clock-restore, systick-suspend, stm32, firmware-embedded-development, stop-mode-clock-restore]
level: advanced
status: draft
description: "Enter and leave STM32 Stop 2 mode correctly (L4/L4+/U5/WB/WL): which peripherals keep running, wake sources, clock restore after wake-up, and the details that keep current at ~1-2 uA."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stop 2 mode

Stop 2 is the deepest mode that keeps **all SRAM and register contents** and resumes execution
after the WFI instruction. On STM32L4 it draws about 1-2 uA with the RTC running (datasheet
values depend on part and temperature), versus several uA for Stop 1.

## What runs in Stop 2
Only a subset of peripherals can work or wake the device: RTC, LPTIM1, LPUART1, I2C3 (address
match wake), comparators, IWDG, and EXTI lines (GPIO, PVD). Everything else is clock-gated.
Plan wake sources around this list (see low-power-timer-lptim, lpuart-wakeup-on-receive).

## Entry sequence
```c
void enter_stop2(void)
{
    /* 1. peripherals and pins ready for sleep (see gpio-leakage-and-floating-pin-elimination) */
    HAL_SuspendTick();                                 /* SysTick would wake us every 1 ms */
    __HAL_PWR_CLEAR_FLAG(PWR_FLAG_WU);                /* stale wake flags */
    /* 2. Stop 2 can't be entered from Low-power run: exit LPR first if used */
    if (READ_BIT(PWR->CR1, PWR_CR1_LPR)) HAL_PWREx_DisableLowPowerRunMode();

    HAL_PWREx_EnterSTOP2Mode(PWR_STOPENTRY_WFI);      /* sleeps here */

    /* 3. woke up: running on MSI or HSI (per RCC_CFGR STOPWUCK), PLL off */
    SystemClock_Config();                              /* restore HSE/PLL as at boot */
    HAL_ResumeTick();
}
```
Choose the wake-up clock: `__HAL_RCC_WAKEUPSTOP_CLK_CONFIG(RCC_STOP_WAKEUPCLOCK_HSI)` gives
16 MHz immediately (faster to resume UART/I2C); MSI is lower power. Peripherals clocked from
the PLL (USB, SDMMC) must not be active when entering.

## Things that ruin the current
- **Debugger**: `DBGMCU` low-power debug bits keep clocks running (see
  debugging-in-low-power-modes). Measure with the probe disconnected and after a power cycle.
- Floating GPIOs and pins driving loads. Set unused pins to analog mode.
- Pending interrupt flags: WFI returns immediately if any enabled interrupt is pending; the
  device appears to never sleep. Clear peripheral flags and EXTI pending bits before entry.
- Internal reference/regulators left on (VREFBUF, comparators, PVD) if not needed.
- Flash in Stop: power-down option (`HAL_PWREx_EnableFlashPowerDown` style on some series)
  trades wake latency for current.

## Interrupts and RTOS
With FreeRTOS tickless idle, implement `configPRE_SLEEP_PROCESSING`/`portSUPPRESS_TICKS_AND_SLEEP`
around this sequence using LPTIM as the timebase, since SysTick stops in Stop modes
(see software-timers-and-tickless-idle). Zephyr's STM32 PM support uses Stop 2 as a
`suspend-to-idle` substate defined in devicetree.

## Wake latency
Roughly a few microseconds to resume on MSI/HSI, plus time to relock HSE/PLL in
`SystemClock_Config` (HSE crystal startup can be ms). Use HSI as system clock if wake latency
matters more than clock accuracy.

## Verify
- [ ] Current measured with a power analyser (debugger disconnected) matches the datasheet class.
- [ ] Each wake source (RTC, LPTIM, LPUART, GPIO) wakes the device and the app resumes with correct clocks (UART baud check).
- [ ] 10,000 sleep/wake cycles without hang.
