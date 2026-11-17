---
id: computing-software.firmware-embedded-development.low-power-design.sleep-on-exit-interrupt-driven
name: sleep-on-exit-interrupt-driven
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [sleep-on-exit, sleeponexit, scb-scr, wfi, interrupt-driven-firmware, sleepdeep, low-power, firmware-embedded-development]
level: practitioner
status: draft
description: "Build fully interrupt-driven Cortex-M firmware with SCB->SCR SLEEPONEXIT: the core sleeps on ISR return without unstacking, saving cycles and energy; pitfalls and debugging."
sources:
  - https://developer.arm.com/documentation/dui0552/a/cortex-m3-peripherals/system-control-block/system-control-register
  - https://developer.arm.com/documentation/dui0552/a/the-cortex-m3-processor/power-management/entering-sleep-mode
  - https://www.st.com/resource/en/programming_manual/pm0214-stm32-cortexm4-mcus-and-mpus-programming-manual-stmicroelectronics.pdf
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sleep-on-exit

With `SCB->SCR.SLEEPONEXIT = 1`, when the last active exception returns to Thread mode the core
goes straight back to sleep instead of unstacking and running `main`. The next interrupt starts
without stacking again (the context is already saved). Saves ~2 x 12 cycles per event and all the
main-loop instructions in between.

## Pattern
```c
int main(void) {
    hw_init();                         /* clocks, peripherals, NVIC */
    SCB->SCR |= SCB_SCR_SLEEPDEEP_Msk; /* optional: deep sleep (Stop) instead of Sleep */
    SCB->SCR |= SCB_SCR_SLEEPONEXIT_Msk;
    __DSB();
    __WFI();                           /* never returns while SLEEPONEXIT is set */
    for (;;) { }                       /* reached only if an ISR clears SLEEPONEXIT */
}
void LPTIM1_IRQHandler(void) { LPTIM1->ICR = LPTIM_ICR_ARRMCF; sample_and_store(); }
```
All application work happens in ISRs. Typical fit: sensor nodes woken by RTC/LPTIM, simple
controllers, bootloaders waiting for UART.

## Getting back to main
An ISR can clear the bit to make `main` run once more (e.g. for a heavy job you do not want in an
ISR):
```c
SCB->SCR &= ~SCB_SCR_SLEEPONEXIT_Msk;   /* main continues after the WFI */
```

## Pitfalls
- Everything lives in ISRs, so priorities and ISR durations define the whole system; long work in
  a high-priority ISR blocks others.
- Not compatible with an RTOS (the idle task handles sleep there); bare-metal only.
- Stop-mode wake on STM32 restarts on MSI/HSI: an ISR running after deep sleep must restore the PLL
  before timing-sensitive work, or the system runs on the wake clock.
- Clear the peripheral interrupt flag *before* returning; otherwise the ISR re-enters immediately
  and the device never sleeps (visible as full active current).
- Debugging: the debugger sees the core "running" in the ISR context; breakpoints in `main` after
  WFI never hit. DBGMCU low-power bits needed to keep the probe connected.

## Verify
- [ ] Current profile shows sleep between events with no main-loop activity.
- [ ] GPIO marker in the ISR confirms each event is handled once.
