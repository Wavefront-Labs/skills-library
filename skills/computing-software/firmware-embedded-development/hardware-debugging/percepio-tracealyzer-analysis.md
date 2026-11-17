---
id: computing-software.firmware-embedded-development.hardware-debugging.percepio-tracealyzer-analysis
name: percepio-tracealyzer-analysis
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [trace, tracealyzer, percepio, tracerecorder, snapshot-mode, streaming-mode, freertos-trace, zephyr-trace, user-events, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Understand what Percepio Tracealyzer and the TraceRecorder library record, snapshot versus streaming capture, the views used for RTOS timing problems, and OS support."
sources:
  - https://percepio.com/tracealyzer/
  - https://github.com/percepio/TraceRecorderSource
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Percepio Tracealyzer

**Goal:** record RTOS kernel events with Percepio's tracing library and use Tracealyzer's views to
explain timing, blocking and resource problems.

## How it works
A software tracing library in the target extends the RTOS kernel with lightweight instrumentation
on pre-existing hooks, capturing task switches, kernel API calls, blocking and timeouts. A C API
for custom logging ("user events") records variable values and other debug events. It is a 100%
software solution: no trace port is needed, though fast probes such as IAR I-jet and SEGGER J-Link
help for continuous streaming.

The recorder source is in github.com/percepio/TraceRecorderSource (Apache-2.0). Its layout includes
`config`, `include`, `kernelports` and `streamports` folders and sources such as
`trcStreamingRecorder.c`, `trcTaskMonitor.c`, `trcStackMonitor.c` and `trcISR.c`. Follow the
getting started guide at percepio.com/gettingstarted for the actual integration steps for your
RTOS and transport.

## Capture modes
- **Streaming:** continuous live trace over a debug-probe or other transport.
- **Snapshot:** an in-memory capture of the critical moments leading up to a problem.

## Views and analysis
The vendor lists CPU load graphs, stack and heap memory usage, timing plots and event-level
detail (from a graph to the exact kernel event). Use CPU load to find bursts, timing plots to find
where execution time goes, and the event-level view to see what the kernel was doing around a
timing outlier. It is aimed at timing-sensitive bugs that vanish when a breakpoint is set.

## Supported targets
Prepackaged support for FreeRTOS, Zephyr, ThreadX, PX5 RTOS, SafeRTOS, LynxOS-178, VxWorks and
Linux, plus a Bare-Metal option for any C/C++ project. Works with GCC, Clang and IAR, with guides
for Keil uVision, IAR, SEGGER J-Link, STM32CubeIDE, ESP-IDF and Lauterbach. A TraceExporter for VS
Code exports TraceRecorder snapshots from a debug session.

## Verify
- [ ] The trace shows named tasks and ISRs for a known workload.
- [ ] A capture around a known fault shows the events leading up to it.

## Checked
Confirmed from the Percepio Tracealyzer product page and the TraceRecorderSource repository page:
operation, capture modes, views, supported systems, repository layout. Removed as unconfirmed
(no recorder documentation was read): FreeRTOSConfig and trcConfig symbol names, init and enable
call names, Zephyr Kconfig options, event sizes, buffer sizes, RTT stream-port advice, the
missed-events counter, and named view details beyond the product page.

Method: docs-checked 2026-11-09 against the Percepio Tracealyzer product page and the TraceRecorderSource GitHub page, both read in full.
