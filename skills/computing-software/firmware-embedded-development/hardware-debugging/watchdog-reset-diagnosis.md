---
id: computing-software.firmware-embedded-development.hardware-debugging.watchdog-reset-diagnosis
name: watchdog-reset-diagnosis
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [watchdog-reset-diagnosis, watchdog, iwdg, early-warning-interrupt, reset-cause, task-watchdog, dbgmcu-freeze, hang-analysis, hardware-debugging, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Find why a watchdog fired: read and clear the reset cause, a software watchdog timer that captures the stacked PC/LR, task check-ins that name the stalled task, debug freeze."
sources:
  - https://interrupt.memfault.com/blog/firmware-watchdog-best-practices
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Diagnosing watchdog resets

A watchdog reset tells you that the system hung, not where. Make it tell you where.

## 1. Know it was the watchdog
Almost every vendor exposes the last reset type in a register, and one bit indicates a watchdog
reset. The bits are typically sticky: read on boot, then clear them or you see the same value on
every boot until a power-on reset. Register names the Memfault article lists: ESP32
`RTC_CNTL_RESET_CAUSE`, MAX32 `PWRSEQ_FLAGS`, LPC `AOREG1`, nRF52 `RESETREAS`, STM32F `RCC_CSR`,
STM32H `RCC_RSR`. On the nRF52840, bit 1 of `RESETREAS` is the watchdog and you write 1 to the
bits you want to clear.

## 2. Check how your watchdog behaves
Read the datasheet for each of these:
- Is the configuration reset on each boot, or locked once enabled until a power-on reset? On the
  nRF52840 a soft reset does not reset the watchdog, so a bootloader unaware of it can be reset
  mid-update.
- What happens with a halted debugger? Many parts can pause the watchdog while halted (STM32
  DBGMCU can freeze peripheral clocks; nRF52840 `CONFIG` bit 3 controls pausing, defaulting to pause on
  halt). Disabling the watchdog entirely in debug builds hides problems until release.
- What happens at expiry? Options include immediate reset, an early-warning interrupt, or an interrupt
  followed by a few clock cycles before reset. On the nRF52840 the reset follows the TIMEOUT event
  by only two 32.768 kHz cycles, too short for real cleanup.

## 3. Capture where it was stuck
Build a software watchdog from a spare hardware timer set to expire a little before the hardware
watchdog (the article uses 7 s against a 10 s hardware timeout) and restart it on every feed.
Treat its ISR as a fault handler:
- Recover the stacked exception frame from MSP or PSP and look at the stacked PC and LR. In the
  article's polling hang they point exactly at the spin loop.
- If a debugger is attached, halt there; otherwise save a coredump and reboot. Do one last
  hardware feed first to buy cleanup time.
- Give the software watchdog the highest configurable priority, and use BASEPRI rather than
  disabling all interrupts for critical sections (not on Cortex-M0) so it can still fire inside an ISR or
  critical section.
- A software watchdog timer keeps running while the debugger halts on nRF52. The article uses GDB
  Python `gdb.events.stop` and `gdb.events.cont` handlers to stop and start the timer.

## 4. Name the stalled task
A low-priority task that feeds the watchdog misses deadlocks of higher priority tasks. Use a task
watchdog: each task registers, checks in, and the hardware watchdog is fed only when all registered
tasks have checked in. In the handler, `s_registered_tasks & ~s_fed_tasks` names the stuck task
ids. Unregister tasks that are legitimately idle waiting for work.

## 5. Common causes (from the article)
Memory corruption leading to an infinite loop, a wedged external component, mutexes taken in the wrong
order or never released, and a high-priority task starving lower ones. Avoid adding timeouts
everywhere: failing exactly where the hang happens keeps the evidence.

## Verify
- [ ] A forced hang yields a record naming that task and PC.
- [ ] Reset cause is read and cleared once per boot.

## Checked
Confirmed from the Memfault watchdog guide: sticky reset-reason registers and the vendor register
table, nRF52840 behaviour, early-warning timing, software watchdog design, task watchdog,
priority and BASEPRI advice, GDB Python pause handlers. Removed as unconfirmed: AVR MCUSR, ESP-IDF
reason enum names, STM32 WWDG EWI and SAM details, `DBGMCU->APB1FZR1` bit names, noinit RAM storage,
IWDG-cannot-be-stopped claim and the ST RM0090 source (not read).

Method: docs-checked 2026-11-09 against the Memfault Interrupt watchdog guide, read in full.
