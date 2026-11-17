---
id: computing-software.firmware-embedded-development.hardware-debugging.rtos-aware-gdb-debugging
name: rtos-aware-gdb-debugging
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [gdb, openocd, rtos-awareness, freertos-gdb, thread-apply-all, info-threads, hardware-breakpoint, flash-breakpoint, watchpoint, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Debug an RTOS target with GDB/OpenOCD thread awareness: enabling -rtos, required symbols, helper files, hardware breakpoint limits and watchpoints."
sources:
  - https://openocd.org/doc/html/GDB-and-OpenOCD.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTOS-aware GDB debugging

**Goal:** debug a FreeRTOS/Zephyr target where the question is which task did what, not just what the current PC is.
Builds on the probe setup in
`computing-software.firmware-embedded-development.hardware-debugging.jtag-swd-probe-setup-and-troubleshooting` and the
fault-decoding method in
`computing-software.firmware-embedded-development.hardware-debugging.cortex-m-hardfault-analysis`.

## Enabling RTOS thread awareness
OpenOCD includes RTOS support, but it defaults to disabled. Enable it per target in the config:
```tcl
$_TARGETNAME configure -rtos auto      ;# auto-detect, or name the RTOS (for example FreeRTOS)
$_TARGETNAME configure -rtos none      ;# drop it again
```
The `-rtos` types listed in the manual include `auto`, `none`, `eCos`, `ThreadX`, `FreeRTOS`, `linux`, `ChibiOS`,
`embKernel`, `mqx`, `uCOS-III`, `nuttx`, `RIOT`, `Zephyr` and `rtkernel`. GDB then shows the RTOS tasks as threads;
for the GDB commands see "Debugging Programs with Multiple Threads" in the GDB manual.

Before an RTOS can be detected, the firmware must export certain symbols. For FreeRTOS the manual lists
`pxCurrentTCB`, `pxReadyTasksLists`, `xDelayedTaskList1`, `xDelayedTaskList2`, `pxDelayedTaskList`,
`pxOverflowDelayedTaskList`, `xPendingReadyList`, `uxCurrentNumberOfTasks`, `uxTopUsedPriority` and
`xSchedulerRunning`. Most are exported by default, but some RTOSes need extra steps:
- Zephyr must be built with `DEBUG_THREAD_INFO` so the symbols for the thread list exist.
- FreeRTOS and uC/OS-III may need an OpenOCD-specific helper file linked into the project
  (`contrib/rtos-helpers/FreeRTOS-openocd.c`, `contrib/rtos-helpers/uCOS-III-openocd.c` in the OpenOCD sources).

If the thread list looks wrong, check the symbols and helper above first.

## Hardware breakpoint and watchpoint limits
OpenOCD prints how many the target has, for example `hardware has 6 breakpoints, 4 watchpoints`. Tell GDB with:
```gdb
set remote hardware-breakpoint-limit 6
set remote hardware-watchpoint-limit 4
```
(use the numbers your own OpenOCD log reports). The manual notes that on the Cortex-M3 example hardware, hardware
breakpoints only work for code running from flash; most other ARM systems do not have this restriction.
Informing GDB of the memory map lets it protect flash areas and use hardware breakpoints by default, so
`gdb breakpoint_override` is then not required (it can force `hard`, `soft` or `disable` for GUIs that do not
distinguish).

## Watchpoints for a suspected race
`watch <variable>` stops when a memory location changes, whichever task or ISR wrote it, which a breakpoint alone
cannot show when you do not know where the write happens. Watchpoints use the limited hardware comparators counted
above, so keep the number of suspects within the reported limit.

## Verify
- [ ] The thread list shows task names that match what the firmware created, cross-checked rather than assumed.
- [ ] Breakpoint and watchpoint counts stay within what OpenOCD reported for the target.
- [ ] Watchdogs and timers were considered: peripherals may keep running while the core is halted.

## Checked
Method: docs-checked 2026-11-09 against the OpenOCD manual page GDB and OpenOCD (read in full: sections on hardware limits, memory map and RTOS Support), plus Server Configuration (gdb breakpoint_override) and CPU Configuration (-rtos types). Removed unconfirmed claims: struct-layout version mismatch behaviour, `thread apply all bt` advice, Cortex-M comparator counts, ISR single-step side effects, ESP-IDF cross-reference.
