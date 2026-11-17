---
id: computing-software.firmware-embedded-development.hardware-debugging.etm-instruction-trace
name: etm-instruction-trace
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [trace, etm-trace, etm, tpiu, trace-port, j-trace, etb, mtb, instruction-trace, code-coverage, firmware-embedded-development]
level: sme
status: docs-checked
description: "Choose and use instruction trace on Cortex-M: streaming ETM probes like J-Trace PRO, ORBTrace with orbmortem, live coverage and profiling, and what to check first."
sources:
  - https://www.segger.com/products/debug-probes/j-trace/
  - https://github.com/orbcode/orbuculum
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ETM instruction trace

**Goal:** record executed instructions in real time so you can reconstruct the path into a hard
fault, a race or a rare state, which breakpoints and printf cannot show.

## Options
| Tool | What the vendor says |
|---|---|
| SEGGER J-Trace PRO | Captures every executed instruction non-intrusively; unlimited streaming trace with live analysis; also gives live code coverage and profiling; full J-Link Pro debug features |
| ORBTrace Mini with Orbuculum | Open-source parallel-trace hardware and tools; `orbmortem` shows the last executed instructions (ETM) |

J-Trace variants: PRO (multi-architecture), PRO Cortex-A/R/M, PRO Cortex-M, PRO RISC-V. All list
Cortex-M ETM trace and share the same features; they differ in supported architectures. Their
published limits: max trace clock 150 MHz, max TPIU frequency 300 MHz, max SWO speed 100 MHz, max
target interface speed 50 MHz. They have two connectors, a debug connector and a debug-and-trace
connector; only one can be used at a time. Check your board has the trace connector and the
target device supports trace (the J-Trace PRO is described as working out of the box with most
trace-capable devices).

## Streaming versus buffer
SEGGER distinguishes traditional buffer trace (only the last N MB of trace data is available) from
unlimited streaming trace (all data is available on the PC). Streaming enables code coverage and
CPU load analysis per function. Use buffer trace for "what led to the crash", streaming for coverage
and profiling.

## With Orbuculum (ORBTrace)
- `orbmortem` needs a parallel trace source such as ORBTrace Mini configured to stream ETM
  (the gdb `startETM` macro), and the ELF (`-e`) for symbols and source. Protocols: ETM35 (default)
  or MTB (MTB only makes sense from a file).
- It holds a post-mortem buffer (default 32 KB, `-b`). Pressing H holds the capture and decodes the
  buffer. If the stream is lost (for example the debugger takes over) it auto-holds and
  decodes, showing the last instructions executed.
- In parallel trace the TPIU framing is mandatory and must be stripped by the probe or by
  orbuculum; set the trace width on the target to match the FPGA configuration (default 4 bits).
- The README says orbmortem is not thoroughly tested. If decodes do not arrive correctly try the
  `-a` alternate address option.

## Practical steps
1. Confirm the device and board support trace and that the trace connector is present.
2. Enable trace output on the target (debugger scripts or firmware); the exact register setup is
   device specific, so use the vendor or tool documentation for your part.
3. Load the exact ELF that is running; decoding needs the code image.
4. Stop at the fault and read the last instructions, or stream for coverage and profiling.

## Verify
- [ ] A known loop appears in the trace with the right iteration count.
- [ ] Trace decodes without errors or lost sync at your chosen core clock.

## Checked
Confirmed from the SEGGER J-Trace page (features, models, limits, connectors, streaming versus
buffer note) and the Orbuculum README (orbmortem requirements, options, TPIU note). Removed as
unconfirmed: STM32 DBGMCU and GPIO pin setup, MTB register names, the trace-clock-at-half-core-clock
rule, length-matching advice, DO-178 and ISO 26262 claims, low-power TRACECLK behaviour,
non-SEGGER probe list beyond ORBTrace, and the Arm IHI0064 and OpenOCD sources (Arm page
unreadable).

Method: docs-checked 2026-11-09 against the SEGGER J-Trace product page and the Orbuculum GitHub README, both read in full.
