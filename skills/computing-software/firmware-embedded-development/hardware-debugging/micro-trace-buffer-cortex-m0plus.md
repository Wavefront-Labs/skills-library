---
id: computing-software.firmware-embedded-development.hardware-debugging.micro-trace-buffer-cortex-m0plus
name: micro-trace-buffer-cortex-m0plus
category: computing-software
field: firmware-embedded-development
product: hardware-debugging
tags: [micro-trace-buffer, mtb, cortex-m0plus, branch-trace, samd21, kl25z, post-mortem-trace, hardware-debugging, firmware-embedded-development]
level: advanced
status: draft
description: "Use the Cortex-M0+ Micro Trace Buffer: reserve SRAM, enable MTB_MASTER, read branch packets after a fault to see the last executed path, and tool support in J-Link/pyOCD."
sources:
  - https://developer.arm.com/documentation/ddi0486/b/
  - https://interrupt.memfault.com/blog/instruction-tracing-mtb-m33
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Micro Trace Buffer (MTB) on Cortex-M0+

M0+ has no ETM or ITM. Where the silicon vendor implemented the optional MTB (SAMD21/SAML21,
NXP Kinetis KL/MKE, some LPC8xx), it records branches into a slice of on-chip SRAM. ARMv8-M
(M23/M33) defines an optional MTB as well. Check the reference manual for the MTB register base
(SAMD21: 0x41006000; KL25: 0xF0000000).

## How it works
Each taken branch writes an 8-byte packet `{source PC, destination PC}` into the buffer at
`MTB_POSITION`. The buffer wraps, so you always have the last N/8 branches. Exceptions are recorded
too (A-bit on the source).

## Setup
1. Reserve aligned SRAM (size power of two, aligned to its size) so the linker does not use it:
   ```c
   __attribute__((section(".mtb"), aligned(1024))) volatile uint32_t mtb_buf[256];  /* 1 KB */
   ```
   On parts with a dedicated MTB SRAM window (Kinetis) it is a fixed range; do not place
   variables there.
2. Program the registers (SAMD21 offsets shown):
   ```c
   MTB->POSITION.reg = (uint32_t)mtb_buf & ~7u;   /* only address bits [AWIDTH-1:3] are kept */
   MTB->FLOW.reg     = 0;                                         /* no watermark stop */
   MTB->MASTER.reg   = MTB_MASTER_EN | MTB_MASTER_MASK(6);        /* 2^(6+4)=1 KB = mtb_buf */
   ```
   `MASK` sets the buffer size as `2^(MASK+4)` bytes; it must not exceed the reserved region.
3. Stop tracing in the HardFault handler first thing (`MTB->MASTER.reg &= ~MTB_MASTER_EN`) so the
   fault handler's own branches do not overwrite history. Alternatively use TSTOPEN with a DWT
   comparator.

## Reading it
- J-Link/Ozone and Keil MDK decode MTB natively ("Instruction trace" window).
- Manually: dump the buffer, start at `POSITION` (oldest entry once WRAP is set), pair source/dest
  and map through `addr2line -e app.elf`. Packets are back-to-back 32-bit words; bit 0 of the
  source word is the A (exception) flag, bit 0 of the destination is the S (start) flag.

## Costs
- Zero CPU overhead, but RAM taken from the application and contention on the SRAM port is
  negligible. A 1 KB buffer holds 128 branches, often enough to see the path into a fault.

## Verify
- [ ] After a deliberate fault, the last packets show the call into the faulting function.
- [ ] Buffer region excluded from `.bss`/heap in the map file.
