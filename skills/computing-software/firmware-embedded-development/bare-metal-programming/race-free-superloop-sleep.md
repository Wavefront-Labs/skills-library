---
id: computing-software.firmware-embedded-development.bare-metal-programming.race-free-superloop-sleep
name: race-free-superloop-sleep
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [event-driven-superloop, superloop, wfi-race, low-power-main-loop, primask-wfi, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Sleep in a bare-metal event loop without missing the event that arrives between the 'anything to do?' check and WFI, using the PRIMASK-masked WFI idiom."
sources:
  - https://www.state-machine.com/doc/AN_QP_and_ARM-Cortex-M-GNU.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Race-free sleep in an event-driven superloop

## The race
```c
for (;;) {
    if (g_events) process();
    __WFI();           /* event set by an ISR right after the check: we sleep anyway */
}
```
If the ISR fires after `if (g_events)` evaluates false and before `WFI`, the event waits until
the *next* interrupt, which may be a 1 s tick or never (in a pure event design).

## The idiom: check with interrupts masked, WFI wakes anyway
```c
for (;;) {
    __disable_irq();                    /* PRIMASK = 1 */
    if (g_events == 0) {
        __WFI();                        /* an interrupt still wakes the core while PRIMASK = 1 */
        __enable_irq();                 /* now the ISR runs */
    } else {
        __enable_irq();
    }
    process_events();
}
```
The Quantum Leaps application note "QP and ARM Cortex-M with GNU" describes this design for the
QP cooperative Vanilla kernel. The kernel calls its idle callback (`QF_onIdle()` in that note)
with interrupts disabled "to avoid race condition with interrupts that can post events to
active objects and thus invalidate the idle condition". Its `QF_CPU_SLEEP()` macro then stops the
CPU with WFI and re-enables interrupts afterwards, "possible, because the ARM Cortex-M CPU can
be woken up by an interrupt, even though PRIMASK is set". So an event arriving after the check
still wakes the core, and its ISR runs when interrupts are re-enabled.

## Do not use BASEPRI for this
On ARMv7-M the same application note sets PRIMASK first, then clears BASEPRI, and only then
executes WFI, because "the ARM Cortex-M3/M4 cores cannot be woken up by any interrupt blocked by
the BASEPRI register". Masking with BASEPRI alone before WFI can therefore sleep through masked
events. Use the PRIMASK sequence above.

## Debugging note
The application note uses sleep only in non-debug configurations, because sleep mode stops the
CPU clock, which can interfere with debugging. Check your MCU's reference manual for a
debug-in-sleep setting, and expect it to raise sleep current.

## Verify
- [ ] Test: an ISR fires from a timer at random phase relative to the loop; measure latency from ISR to `process_events` with a scope: never a full tick period.
- [ ] Current measurement shows the core actually sleeps between events.

## Checked
Method: docs-checked 2026-11-09 against the Quantum Leaps application note "QP and ARM Cortex-M with GNU" (downloaded, converted with pdftotext; read the QF_CPU_SLEEP descriptions for ARMv6-M and ARMv7-M and the QF_onIdle() discussion).
Removed as unconfirmed: the ARMv7-M "B1.5.19" architecture citation, the `__DSB()` and `__ISB()` barriers, the WFE with SEVONPEND alternative, the deep-sleep (SLEEPDEEP) paragraph, the STM32 DBGMCU register names, and the claim that the pattern lives in a function named `QV_onIdle()`. The Arm user guide and architecture manual sources were unreadable and were dropped.
