---
id: computing-software.firmware-embedded-development.hardware-debugging.segger-systemview-rtos-tracing
name: segger-systemview-rtos-tracing
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [trace, systemview, segger, rtt, freertos-trace, task-switch, isr-timeline, cpu-load, event-recording, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Trace an RTOS or bare-metal app with SEGGER SystemView over RTT: how recording works, supported RTOSes, and fixing overflow, invalid packet and start-up problems."
sources:
  - https://www.segger.com/products/development-tools/systemview/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SEGGER SystemView tracing

**Goal:** a timeline of tasks, interrupts, timers, API calls and user events to find starvation,
priority problems, jitter and CPU load in a running system.

## How it works
A small module containing SystemView and RTT is added to the target (instrumentation code at
github.com/SEGGERMicro/SystemView). It collects events, formats them and passes them to RTT, which
stores them in a target RAM buffer. With a J-Link, continuous recording reads that buffer while the
target runs; single-shot and post-mortem modes work on any system. Debug access only: no extra pins or
hardware. SEGGER quotes under 2 KB ROM, about 600 bytes RAM for continuous recording, and under 1%
overhead at 10,000 events per second on a 200 MHz Cortex-M4. Timestamps can be as fine as one CPU
cycle.

## RTOS support (per SEGGER)
embOS (since 4.12a), ThreadX (since 6.4), FreeRTOS (V8 to V11, native from V11), uC/OS-II and
uC/OS-III, Micrium OS Kernel, Zephyr (through its tracing feature, all versions since 2019) and
NuttX (through its RTT drivers). Any other RTOS needs hooks or manual instrumentation to record task
execution. With no OS at all it still records interrupt activity and user events, which can time
module execution.

## Integration
Include the small set of SystemView and RTT files and call `SEGGER_SYSVIEW_Conf()` during start-up.
SEGGER says as little as one function call or two lines per interrupt may be needed; follow the
RTOS-specific instructions in the SystemView user manual for hook setup. Make sure about 200 bytes of stack
is available in every context that can generate SystemView events (tasks, interrupts and the
scheduler) or the application can crash when SystemView connects.

## Other features
Heap monitoring, a DataPlot window for custom samples, CPU load analysis, an event timeline, printf-style
logging with host-side formatting, and ELF-based name lookup so long text need not be sent.

## Using it with a debugger
SystemView can run in parallel with a debugger (Windows and Linux) if the debugger connection uses
a high interface speed (4 MHz or more). J-Link Ultra and J-Link Pro give the highest RTT throughput.
Older J-Links (V8 and earlier) may overflow. Continuous recording is not possible on ARM7 and ARM9;
Cortex-A and Cortex-R need an AHB-AP.

## Troubleshooting (from the FAQ)
- **Overflow events:** the RTT buffer is full because J-Link is busy with debugger activity, the
  interface speed is low, or the app produces too many events. Reduce debugger interaction
  (disable live watches), raise the speed for every tool connected to J-Link, enlarge the
  SystemView buffer (1 to 4 kB), or run stand-alone without a debugger.
- **Cannot start recording:** J-Link or target not connected; target not running (RTT control block
  not found); module not configured or `SEGGER_SYSVIEW_Conf()` not called; outdated J-Link software.
- **Control block not found:** start recording only after start-up has completed. If it lies outside
  the known RAM range for the device, enter its address or an address range in SystemView.
- **Invalid packets:** `SEGGER_SYSVIEW_LOCK()` and `SEGGER_RTT_LOCK()` not configured correctly for the
  device, or the system entering sleep or low-power mode (avoid WFI with a probe connected).

## Verify
- [ ] Tasks and ISRs appear with names for a known workload.
- [ ] A long capture shows no overflow events.

## Checked
Confirmed from the SEGGER SystemView product page: how it works, resource and overhead figures,
RTOS support list, features, FAQ troubleshooting items. Removed as unconfirmed (the user manual
UM08027 was not read): FreeRTOSConfig.h include lines, config symbol names, timestamp source
details, Cortex-M0 timestamp workaround, MarkStart/MarkStop calls, the specific buffer macro name and
interpretation rules for the timeline.

Method: docs-checked 2026-11-09 against the SEGGER SystemView product page, read in full.
