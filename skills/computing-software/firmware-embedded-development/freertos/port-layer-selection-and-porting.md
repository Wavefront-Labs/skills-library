---
id: computing-software.firmware-embedded-development.freertos.port-layer-selection-and-porting
name: port-layer-selection-and-porting
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertosconfig-h, freertos-port, portable-layer, gcc-arm-cm4f, arm-cm33-ntz, port-c, portmacro-h, vector-handler-mapping, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Pick the right FreeRTOS portable layer for a core/compiler (CM0, CM3, CM4F, CM7 r0p1, CM33 TrustZone or not), wire its handlers, and port to a new core when none fits."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/01-FreeRTOS-ports
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/tree/main/portable
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FreeRTOS port layer selection and porting

**Goal:** the kernel source plus exactly one correct `portable/<compiler>/<arch>` directory
and one heap file, with the port's exception handlers actually installed.

## Choosing the directory (GCC examples)
| Core | Port dir |
|---|---|
| Cortex-M0/M0+ | `GCC/ARM_CM0` |
| Cortex-M3 | `GCC/ARM_CM3` |
| Cortex-M4F / M7 with FPU | `GCC/ARM_CM4F` |
| Cortex-M7 **r0p1** silicon | `GCC/ARM_CM7/r0p1` (erratum 837070 workaround) |
| Cortex-M33 without TrustZone | `GCC/ARM_CM33_NTZ/non_secure` |
| Cortex-M33 with TrustZone | `GCC/ARM_CM33/non_secure` + `secure` (secure-side context mgmt) |
| Cortex-M with MPU | `GCC/ARM_CM4_MPU` etc. |
| RISC-V | `GCC/RISC-V` + chip-specific extensions header |
Other compilers have their own trees under `portable/` (`IAR/...`, `RVDS/...`, `ARMClang/...`). Using `ARM_CM3` on
an M4F with FPU enabled corrupts floating-point registers across task switches.

## Wiring the handlers
The port implements `vPortSVCHandler`, `xPortPendSVHandler`, `xPortSysTickHandler`. Either:
```c
/* FreeRTOSConfig.h */
#define vPortSVCHandler    SVC_Handler
#define xPortPendSVHandler PendSV_Handler
#define xPortSysTickHandler SysTick_Handler
```
or call them from your own handlers. CubeMX-generated projects already do the mapping and
move HAL's tick to another timer. Forgetting this: the first task never starts (stuck in
`vTaskStartScheduler` / prvStartFirstTask).

## Required config for Cortex-M
- `configPRIO_BITS` = the device's `__NVIC_PRIO_BITS` (see the vendor header).
- `configKERNEL_INTERRUPT_PRIORITY` = the lowest priority (shifted into the top bits) and
  `configMAX_SYSCALL_INTERRUPT_PRIORITY` (e.g. 5 << (8 - configPRIO_BITS)).
- M33/M55: `configENABLE_FPU`, `configENABLE_MPU`, `configENABLE_TRUSTZONE`,
  `configRUN_FREERTOS_SECURE_ONLY` must match how you build.

## Porting to a new core (summary of port.c duties)
1. `pxPortInitialiseStack`: build the initial stack frame the context restore expects.
2. `xPortStartScheduler`: set kernel interrupt priorities, start tick timer, launch first task.
3. Context switch: save/restore registers in a lowest-priority software interrupt (PendSV on
   Cortex-M, a software trap elsewhere).
4. Critical sections (`portENTER_CRITICAL`) with nesting count; `portYIELD`.
5. `portmacro.h`: types (`StackType_t`, `BaseType_t`), stack growth, tick type, barriers.
Start from the closest existing port and run the FreeRTOS demo's register-test tasks, which detect
register corruption.

## Verify
- [ ] The demo's register-test tasks run for hours without error.
- [ ] Floating-point tasks on two priorities don't corrupt each other's results (FPU ports).

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel `portable/`: `GCC/ARM_CM0`, `CM3`, `CM4F`, `CM4_MPU`, `CM7/r0p1` (errata 837070
in port.c), `CM33/{non_secure,secure}`, `CM33_NTZ/non_secure`, `RISC-V` with `chip_specific_extensions`, IAR/RVDS/ARMClang
trees; `vPortSVCHandler`, `xPortPendSVHandler`, `xPortSysTickHandler`, `pxPortInitialiseStack`, `xPortStartScheduler`,
`portYIELD`, `portENTER_CRITICAL`; `configENABLE_FPU/MPU/TRUSTZONE` and `configRUN_FREERTOS_SECURE_ONLY`. Removed: per-vendor
NVIC priority bit counts and the `Demo/Common` path.
Method: documentation only; no commands were run.
