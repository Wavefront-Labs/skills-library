---
id: computing-software.firmware-embedded-development.bare-metal-programming.device-vs-normal-memory-ordering
name: device-vs-normal-memory-ordering
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [device-memory-type, mmio, strongly-ordered, memory-attributes, mpu-attributes, firmware-embedded-development]
level: advanced
status: draft
description: "Understand ARMv7-M/v8-M memory types (Normal, Device, Strongly-ordered) and how they decide access ordering and merging between buffers in RAM and peripheral registers."
sources:
  - https://developer.arm.com/documentation/ddi0403/latest/
  - https://developer.arm.com/documentation/ddi0553/latest/
  - https://developer.arm.com/documentation/dai0321/latest/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Device vs Normal memory types and access ordering

The default memory map assigns attributes by address region (ARMv7-M ARM B3.1):
| Region | Default type | Notes |
|---|---|---|
| 0x0000_0000 Code | Normal, WT cacheable | flash |
| 0x2000_0000 SRAM | Normal, WBWA cacheable | |
| 0x4000_0000 Peripheral | Device, XN | |
| 0x6000_0000 / 0x8000_0000 External RAM | Normal | FMC/SDRAM |
| 0xA000_0000 / 0xC000_0000 External device | Device | FMC NOR/LCD |
| 0xE000_0000 PPB | Strongly-ordered | NVIC, SCB, SysTick |

## What the types guarantee
- **Normal:** accesses may be reordered, merged, speculatively read, and cached. Fine for RAM.
- **Device** (ARMv8-M: Device-nGnRE etc.): accesses to the same device are in program order and
  not merged or speculated, but writes may be **buffered**: the core continues before the write
  reaches the peripheral.
- **Strongly-ordered** (ARMv8-M: Device-nGnRnE): no buffering, each access completes before the
  next.
ARMv8-M names: G = gathering, R = reordering, E = early write acknowledge; `nGnRnE` is the
strongest.

## Where it bites
1. **RAM buffer then peripheral kick (DMA):** writing a descriptor in Normal memory and then
   writing the DMA enable register (Device): the two are different types, so ordering between
   them is not guaranteed. Insert `__DMB()` (or `__DSB()` on M7 with caches) between them.
2. **Write buffer vs interrupt flag clear:** Device writes are buffered, so a clear at the end of
   an ISR can complete after exception return (see spurious interrupts).
3. **LCD on FMC at 0x6000_0000:** that region is Normal by default, so on Cortex-M7 writes to
   the LCD command/data addresses can be merged or reordered and speculative reads hit the bus.
   Remap the bank (`FMC_BCR1.BMAP`) to 0xC000_0000 or set the MPU region to Device/Strongly-ordered.
4. **Speculative reads of Normal external memory** on M7: an MPU region with Device or
   XN + non-cacheable stops the core touching memory that is not present.

## Changing attributes
Use the MPU: ARMv7-M via TEX/C/B/S bits (`TEX=0,C=0,B=1` Shared Device; `TEX=0,C=0,B=0`
Strongly-ordered); ARMv8-M via `MAIR0/1` attribute indexes (`0x00` = Device-nGnRnE,
`0x04` = Device-nGnRE).

## Verify
- [ ] DMA descriptor writes are followed by a barrier before the enable write.
- [ ] External LCD/FPGA regions have a Device MPU region; reads of status registers return fresh values.
