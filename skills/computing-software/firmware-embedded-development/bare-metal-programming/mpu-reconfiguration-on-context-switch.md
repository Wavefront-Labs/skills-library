---
id: computing-software.firmware-embedded-development.bare-metal-programming.mpu-reconfiguration-on-context-switch
name: mpu-reconfiguration-on-context-switch
category: computing-software
field: firmware-embedded-development
product: bare-metal-programming
tags: [mpu-context-switch, mpu, pendsv, per-task-regions, privilege-separation, firmware-embedded-development]
level: sme
status: draft
description: "Swap per-task MPU regions inside PendSV for task isolation: static vs dynamic regions, fast RBAR/RASR alias writes, barriers, and the cost per switch."
sources:
  - https://developer.arm.com/documentation/dui0553/latest/
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/ARM-Cortex/FreeRTOS-MPU-memory-protection-unit
  - https://docs.zephyrproject.org/latest/kernel/usermode/memory_domain.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Reprogramming MPU regions on context switch

**Goal:** each task (or partition) sees only its own stack and data. Static regions (flash
read-only, peripherals for the kernel) stay fixed; a few **dynamic regions** are rewritten on
every context switch.

## Region plan (8-region ARMv7-M MPU example)
| Region | Content | Changes per task |
|---|---|---|
| 0 | Flash: RO + exec, all | no |
| 1 | Kernel RAM: priv only | no |
| 2 | Peripherals: priv only, XN, Device | no |
| 3 | Shared RO data | no |
| 4 | Task stack: RW, XN | yes |
| 5-7 | Task data/peripheral grants | yes |

## Fast switch in PendSV
Precompute each task's `RBAR`/`RASR` values when the task is created (store them in the TCB), so
PendSV only copies words. Use the `RBAR` with `VALID` bit + region number, or the alias registers
(`MPU_RBAR_A1..A3`, `MPU_RASR_A1..A3` on ARMv7-M) to write 4 regions with a single `STM`:
```asm
    ldr   r1, [r0, #TCB_MPU_OFFSET]   @ r1 -> {rbar4, rasr4, rbar5, rasr5, ...}
    ldr   r2, =0xE000ED9C              @ MPU->RBAR
    ldmia r1!, {r4-r11}
    stmia r2, {r4-r11}                 @ RBAR, RASR, RBAR_A1, RASR_A1, ... (RBAR has VALID|REGION set)
    dsb
    isb
```
On ARMv8-M use `MPU->RNR` + `RBAR`/`RLAR` and the `RBAR_A1..A3` aliases the same way; attributes
come from shared `MAIR` indexes so they need no per-task reload.

## Rules
- Disable the dynamic regions or the whole MPU only if unavoidable; with `PRIVDEFENA` set,
  privileged PendSV keeps running during the update anyway.
- `DSB` + `ISB` after the last write, before returning to the task.
- ARMv7-M region alignment: task stacks must be power-of-two sized and aligned to their size;
  allocate them from aligned pools (FreeRTOS-MPU requires this for `xTaskCreateRestricted`
  stacks on v7-M). ARMv8-M only needs 32-byte alignment.
- Keep ISRs privileged: interrupts preempting a task run with the task's dynamic regions still
  loaded but under the privileged default map.

## Cost
4 regions with STM: roughly 20-40 cycles plus barriers. Region count, not region size, sets the
cost. Measure with DWT CYCCNT around the PendSV body.

## Verify
- [ ] Task A writing into task B's stack triggers MemManage with MMFAR in B's stack.
- [ ] Context switch time with and without MPU, measured via GPIO or CYCCNT, is within budget.
