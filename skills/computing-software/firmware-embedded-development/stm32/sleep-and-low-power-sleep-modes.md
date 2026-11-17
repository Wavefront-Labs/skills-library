---
id: computing-software.firmware-embedded-development.stm32.sleep-and-low-power-sleep-modes
name: sleep-and-low-power-sleep-modes
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-low-power, low-power-sleep, sleep-on-exit, wfi-wfe, lpsdsr, stm32, firmware-embedded-development]
level: practitioner
status: gated
description: "Use STM32 Sleep and Low-power sleep modes: WFI vs WFE, sleep-on-exit for interrupt-driven designs, clock gating in sleep, SysTick wakeups and low-power run pairing."
sources:
  - https://www.st.com/resource/en/application_note/an4621-stm32l4-and-stm32l4-ultralowpower-features-overview-stmicroelectronics.pdf
  - https://www.st.com/resource/en/programming_manual/pm0214-stm32-cortexm4-mcus-and-mpus-programming-manual-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sleep and low-power sleep

Sleep stops the CPU clock only; all peripherals, DMA and SRAM keep running, and wake latency is
a few cycles. It is the right mode whenever the CPU waits for peripherals.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Enter
```c
HAL_SuspendTick();                                        /* otherwise SysTick wakes every 1 ms */
HAL_PWR_EnterSLEEPMode(PWR_MAINREGULATOR_ON, PWR_SLEEPENTRY_WFI);
HAL_ResumeTick();
```
- **WFI**: wakes on any enabled interrupt.
- **WFE**: wakes on events (SEV, EXTI event lines, or any pending interrupt with `SEVONPEND` set),
  without needing an ISR. Executing WFE when the event register is already set returns
  immediately, so call it in a loop that re-checks the condition.

## Sleep-on-exit
For fully interrupt-driven firmware:
```c
HAL_PWR_EnableSleepOnExit();     /* SCB->SCR |= SLEEPONEXIT */
__WFI();                          /* main never continues; ISRs run, then core sleeps again */
```
Saves the exception return/entry overhead. Debugging is confusing: main appears stuck at WFI.

## Reduce sleep current
- Gate clocks of peripherals not needed during sleep: `__HAL_RCC_xxx_CLK_SLEEP_DISABLE()`
  (RCC_AHBxSMENR/APBxSMENR). Default after reset is enabled for all; disabling SRAM2, flash or
  unused peripherals in sleep saves real current.
- Lower SYSCLK before sleeping if wake latency allows.

## Low-power sleep (LPSleep)
Combination of low-power run (regulator in low-power mode, SYSCLK <= 2 MHz on L4) and sleep:
```c
HAL_PWREx_EnableLowPowerRunMode();     /* after dropping clock to MSI <= 2 MHz */
HAL_PWR_EnterSLEEPMode(PWR_LOWPOWERREGULATOR_ON, PWR_SLEEPENTRY_WFI);
```
Current in the tens of uA with peripherals running slowly. On F4-class parts `PWR_LOWPOWERREGULATOR_ON`
has no effect in Sleep; this is an L0/L1/L4/L5/U5/G0/G4 feature.

## RTOS
FreeRTOS idle hook / tickless idle uses WFI (sleep) by default; for deeper modes see Stop 2.

## Verify
- [ ] Current in sleep measured with peripheral clock gating applied vs not.
- [ ] Wake latency measured (GPIO toggle in ISR vs event).

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
