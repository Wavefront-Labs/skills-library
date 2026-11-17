---
id: computing-software.firmware-embedded-development.stm32.build-analyzer-and-static-stack-analyzer
name: build-analyzer-and-static-stack-analyzer
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-cube, build-analyzer, static-stack-analyzer, memory-regions, fstack-usage, stm32, firmware-embedded-development]
level: practitioner
status: draft
description: "Use STM32CubeIDE Build Analyzer and Static Stack Analyzer to see flash/RAM per region and symbol, and compute worst-case stack depth from -fstack-usage data."
sources:
  - https://www.st.com/resource/en/user_manual/um2609-stm32cubeide-user-guide-stmicroelectronics.pdf
  - https://gcc.gnu.org/onlinedocs/gcc/Developer-Options.html#index-fstack-usage
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build Analyzer and Static Stack Analyzer

## Build Analyzer
Opens automatically after a build (Window > Show View > Build Analyzer). Reads the `.map` and
`.elf`:
- **Memory Regions** tab: used/free per linker region (FLASH, RAM, RAM2, DTCMRAM, ITCMRAM ...).
- **Memory Details** tab: sections and symbols per region, sortable by size.
Use it to find the biggest buffers and confirm DMA buffers land in the intended RAM (e.g. D2
SRAM on H7, not DTCM which DMA1/2 can't reach).

Command-line equivalent:
```bash
arm-none-eabi-size -A build/app.elf
arm-none-eabi-nm -S --size-sort -C build/app.elf | tail -30
```

## Static Stack Analyzer
Enable `-fstack-usage` (Project Properties > C/C++ Build > Settings > MCU GCC Compiler >
Miscellaneous, or "Generate per function stack usage information"; also `-fcallgraph-info` in
newer GCC). After build, Window > Show View > Static Stack Analyzer:
- **List** view: each function's own frame (static/dynamic/bounded).
- **Call graph** view: max stack depth through each call chain.

Limits:
- Function pointers, recursion and `alloca`/VLAs show as unbounded or are excluded; add their
  worst case by hand.
- ISRs stack on the main stack (MSP) on top of whatever was running: add the deepest ISR
  chain (times nesting levels) to main's depth.
- RTOS tasks: each task's entry function depth + FreeRTOS context frame (~100+ bytes, more with FPU).

## Stack size decision
`_Min_Stack_Size` in the linker script = deepest main chain + deepest ISR nesting + margin
(25%). Confirm at runtime with stack painting (fill with 0xA5 at startup, scan for high water).

## Verify
- [ ] Every RAM region has margin in the Build Analyzer.
- [ ] Static analysis plus runtime high-water measurement agree within margin.
