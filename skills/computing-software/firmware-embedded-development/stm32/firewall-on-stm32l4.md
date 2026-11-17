---
id: computing-software.firmware-embedded-development.stm32.firewall-on-stm32l4
name: firewall-on-stm32l4
category: computing-software
field: firmware-embedded-development
product: stm32
tags: [stm32-security, stm32-firewall, firewall-call-gate, code-segment-protection, volatile-data-segment, stm32, firmware-embedded-development]
level: advanced
status: gated
description: "Isolate sensitive code and data on STM32L0/L4 with the Firewall peripheral: code, non-volatile and volatile data segments, call gate entry, and reset-on-violation behaviour."
sources:
  - https://www.st.com/resource/en/application_note/an4729-stm32l0l4-firewall-overview-stmicroelectronics.pdf
  - https://www.st.com/resource/en/reference_manual/rm0351-stm32l47xxx-stm32l48xxx-stm32l49xxx-and-stm32l4axxx-advanced-armbased-32bit-mcus-stmicroelectronics.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Firewall on STM32L4

The Firewall (L0, L4, L4+; superseded by TrustZone on L5/U5) protects up to three segments:
code (flash), non-volatile data (flash), volatile data (SRAM1). Once enabled, any access to a
protected segment from outside the "open" state resets the device.

Claims in this skill were not verified against primary documentation (gated: unconfirmed, source is paywalled or blocked).

## Segments
```c
FIREWALL_InitTypeDef fw = {0};
fw.CodeSegmentStartAddress = 0x08070000; fw.CodeSegmentLength = 0x8000;
fw.NonVDataSegmentStartAddress = 0x08078000; fw.NonVDataSegmentLength = 0x800;
fw.VDataSegmentStartAddress = 0x2000F000; fw.VDataSegmentLength = 0x1000;
fw.VolatileDataExecution = FIREWALL_VOLATILEDATA_NOT_EXECUTABLE;
fw.VolatileDataShared = FIREWALL_VOLATILEDATA_NOT_SHARED;
__HAL_RCC_FIREWALL_CLK_ENABLE();
HAL_FIREWALL_Config(&fw);
HAL_FIREWALL_EnableFirewall();      /* cannot be disabled until reset */
```
Granularity: 256 bytes (code/NV data), 64 bytes (volatile data).

## Call gate
The only legal entry into the protected code is the **call gate** at the code segment base
address + 4 bytes. Calling it opens the firewall; execution inside can
access all segments. Leaving the code segment closes it. Implement a single dispatcher at the
call gate:
```c
__attribute__((section(".fw_callgate"))) uint32_t fw_entry(uint32_t fn, void *in, void *out) {
    __HAL_FIREWALL_PREARM_ENABLE();      /* allow the next exit to re-close cleanly */
    /* validate fn and pointer ranges (out must not point into protected RAM) */
    ...
}
```
Jumping anywhere else inside the segment, or reading it as data from outside, resets the chip
(`RCC_CSR.FWRSTF`).

## Interrupts
An interrupt taken while the firewall is open runs ISR code that can access protected data,
and leaving the segment for the ISR closes the firewall (returning resets the chip unless
pre-armed). Disable interrupts inside protected functions, or keep the vector table and ISRs
non-sensitive. The volatile data segment can be marked shared/executable
to support specific patterns.

## Pair with
PCROP over the code segment (execute-only), RDP level 1/2, WRP. The Firewall alone does not stop a
debugger at RDP 0.

## Verify
- [ ] Read of protected code from the app causes reset with FWRSTF set.
- [ ] Call gate API works; out-of-range pointer arguments are rejected.

## Checked

- Date: 2026-11-01. Reason: every cited source is paywalled, login-gated or blocked to automated readers (st.com); no readable alternative was found.

Method: documentation only; no commands were run.
