---
id: computing-software.firmware-embedded-development.hardware-debugging.pc-sampling-profiling
name: pc-sampling-profiling
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [pc-sampling, statistical-profiling, dwt-pcsr, swo-pc-sample, gmon, hotspot, cpu-load, hardware-debugging, firmware-embedded-development]
level: advanced
status: draft
description: "Profile firmware statistically by sampling the PC: DWT PC sampling over SWO, polling DWT_PCSR from the probe, timer-ISR sampling, and mapping samples to functions."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://github.com/orbcode/orbuculum
  - https://www.segger.com/products/development-tools/ozone-j-link-debugger/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Statistical PC sampling profiling

Sample the program counter thousands of times per second, histogram by function: cheap,
non-intrusive, and good enough to find where the cycles go.

## Option 1: DWT PC sampling over SWO
DWT emits a periodic PC packet every `(POSTPRESET+1) x 64` (CYCTAP=0) or `x 1024` (CYCTAP=1) CPU
cycles. Enable `DWT_CTRL.PCSAMPLENA`, `CYCCNTENA`, ITM `DWTENA`, TPIU/SWO. Tools that decode it:
Orbuculum `orbtop -e app.elf`, Segger Ozone/SystemView, Keil "Performance Analyzer", Cortex-Debug
(SWO "pcsample" decoder not built in; use orbuculum). Sleep is reported as a special packet so you
also get idle percentage.

Budget: each sample ~5 bytes. At 168 MHz with 1024-cycle period = 164k samples/s = 820 kB/s, too
much for a 2 Mbit SWO; use a larger POSTPRESET (e.g. period 16384 cycles ~ 10k samples/s).

## Option 2: probe polls DWT_PCSR
`DWT_PCSR` (0xE000101C) returns a recent PC on each read without halting. J-Link and pyOCD can
poll it; OpenOCD: `profile 10 out.gmon` (OpenOCD halts briefly unless PCSR is available) then
`arm-none-eabi-gprof app.elf out.gmon`. Works on M3/M4/M7 (not M0/M0+, which lack PCSR).

## Option 3: firmware self-sampling
A high-priority timer ISR reads the stacked PC (`((uint32_t*)__get_PSP_or_MSP())[6]`) and bins it
into an array indexed by `(pc - FLASH_BASE) >> 4`; dump over UART and map bins via the ELF.
Works on M0+, costs CPU, and cannot see code with higher priority than the sampling ISR.

## Mapping samples
`addr2line -f -e app.elf` per address, or `nm --size-sort -S -n` to build function ranges and bin.
Attribute samples in inlined code to the caller unless the tool reads DWARF inline info.

## Interpreting
- Expect ~1/sqrt(N) noise; 10k samples is enough for a top-10 list.
- Periodic code synchronised with the sample period aliases; vary the period or use a prime.
- Time in WFI shows as idle; high idle with missed deadlines means latency, not throughput, is the
  problem.

## Verify
- [ ] Busy-loop test function shows up as the dominant hotspot.
- [ ] Optimisation of the top function reduces its sample share proportionally.
