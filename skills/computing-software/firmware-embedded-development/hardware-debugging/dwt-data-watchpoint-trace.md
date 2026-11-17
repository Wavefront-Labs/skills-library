---
id: computing-software.firmware-embedded-development.hardware-debugging.dwt-data-watchpoint-trace
name: dwt-data-watchpoint-trace
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [dwt-data-trace, dwt, data-watchpoint, watch, rwatch, dwt-comparator, itm-data-trace, memory-corruption, hardware-debugging, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Catch memory corruption with Cortex-M DWT comparators: GDB watch/rwatch/awatch, size and alignment limits, data-value matching, and streaming data trace over SWO without halting."
sources:
  - https://github.com/ARM-software/CMSIS_6
  - https://sourceware.org/gdb/current/onlinedocs/gdb.html/Set-Watchpoints.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DWT data watchpoints and data trace

The Data Watchpoint and Trace unit has a device-specific number of comparators: read
`DWT_CTRL.NUMCOMP` (DWT base 0xE0001000, bits 31:28). Each can halt the core on an address access or
emit a trace packet instead.

## Halting watchpoints from GDB
```gdb
watch g_state                 # write
rwatch *(uint32_t*)0x20001F00 # read
awatch buf[12]                # read or write
watch -l p->len               # -location: watch the address, not the expression scope
info watchpoints
```
GDB must use hardware watchpoints (`set can-use-hw-watchpoints 1`); software watchpoints
single-step the program and are far too slow on a target. The PC shown at a hit is typically just
after the access; look back a few instructions (`x/4i $pc-8`).

## Limits
- Size: a comparator matches an address range set by its `DWT_MASK` register, so a range is a
  power-of-two size; a misaligned 6-byte struct needs a covering 8-byte range or two comparators.
- Value match: a comparator can match a data value (`DWT_FUNCTION.DATAVMATCH`, bit 8, linked to an
  address comparator); many debug probes expose it rarely.
- Watchpoints only see core accesses. **DMA writes do not trigger them**; corruption with no hit
  means a DMA/peripheral master (or another core) did it.

## Non-halting data trace
Configure a comparator for "data trace" (`FUNCTION` = PC + data value) and enable ITM/SWO with
DWTENA; every access emits a packet with value and optionally PC. Use your probe vendor's SWO
decoder. Trace bandwidth is limited, so a variable written at a high rate can saturate the SWO line.

## Corruption hunt recipe
1. Identify the corrupted variable and a reproducible trigger.
2. `watch -l` it right after it is initialised; continue.
3. On hit, `bt` and inspect: buffer overrun in a neighbour (check `nm -n app.elf` for what sits
   just below), use-after-free, stack overflow into `.bss`.
4. No hit but value changed: suspect DMA (check DMA descriptors/length), second core, or a
   bootloader writing RAM before your init.

## Verify
- [ ] Watchpoint fires on a deliberate write to the target address.
- [ ] Root cause confirmed by fixing it and running the trigger without the watchpoint.

## Checked
2026-11-01. Confirmed: CMSIS_6 core_cm4.h/core_cm7.h/core_cm33.h (`DWT_BASE` 0xE0001000, `DWT_CTRL_NUMCOMP` at bit 28
with 4-bit mask, `DWT_MASK`, `DWT_FUNCTION_DATAVMATCH` bit 8); GDB manual Setting Watchpoints (`watch`, `rwatch`, `awatch`,
`-location`, `can-use-hw-watchpoints`, `info watchpoints`). Removed: per-core comparator counts, ARMv8-M range-pair
claim, MASK size limits, tool-specific claims, SWO packet sizes and rates.
Method: documentation only; no commands were run.

