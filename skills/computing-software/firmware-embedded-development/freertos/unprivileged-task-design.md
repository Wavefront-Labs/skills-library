---
id: computing-software.firmware-embedded-development.freertos.unprivileged-task-design
name: unprivileged-task-design
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-smp, unprivileged-task, portprivilege-bit, privilege-drop, control-npriv, svc-system-call, least-privilege, freertos, firmware-embedded-development]
level: advanced
status: gated
description: "Design FreeRTOS applications with unprivileged tasks: Cortex-M privilege levels, which work needs privilege, driver-task patterns, and handling faults without system reset."
sources:
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/FreeRTOS.h
  - https://raw.githubusercontent.com/FreeRTOS/FreeRTOS-Kernel/main/include/task.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unprivileged task design

**Goal:** most application code runs unprivileged (least privilege), with a small privileged
core of drivers and the kernel, so bugs and exploits in application code are contained.

## Cortex-M privilege
- Thread mode can run privileged or unprivileged (`CONTROL.nPRIV`). Handler mode (ISRs) is
  always privileged. (gated: unconfirmed, source is paywalled or blocked)
- Unprivileged code **cannot**: access the System Control Space (NVIC, SysTick, SCB, MPU),
  execute `CPS`/`MSR` to mask interrupts, change CONTROL back, or access memory the MPU marks
  privileged-only.
- Going back up requires an exception (SVC) whose handler decides: that's how FreeRTOS-MPU
  system calls work.

## Creating tasks
- `xTaskCreate(..., priority | portPRIVILEGE_BIT, ...)`: privileged task.
- Without the bit (on MPU ports) the task is unprivileged. Restricted tasks
  (`xTaskCreateRestricted`) add per-task memory regions.

## Architecture pattern
- **Driver/service tasks (privileged):** own peripherals and their interrupts, expose
  functionality through queues/stream buffers.
- **Application tasks (unprivileged):** business logic, protocol parsing, third-party code;
  communicate only through granted kernel objects and their own regions.
- No shared global variables between them: data goes through queues (copy semantics) or
  explicitly granted shared regions (read-only where possible).

## What breaks when you drop privilege
- Code calling `__disable_irq()`, `NVIC_*`, `SysTick`, HAL functions that touch SCB/NVIC: faults.
  Move these into privileged drivers.
- `printf`/logging writing directly to a UART register: route through a logging task.

## Fault handling
A MemManage/UsageFault from an unprivileged task: the handler identifies the task
(`xTaskGetCurrentTaskHandle`), logs it, and the system can delete/restart that task instead of
resetting. Keep a supervisor (privileged) task that monitors and restarts application tasks.

## Verify
- [ ] Inventory of tasks with privilege level and justification for each privileged one.
- [ ] An unprivileged task attempting `NVIC_DisableIRQ` faults and is restarted by the supervisor.

## Checked

2026-10-28: confirmed against the FreeRTOS-Kernel sources and headers read this batch: `portPRIVILEGE_BIT` and `xTaskCreateRestricted` exist and are tied to `portUSING_MPU_WRAPPERS` (FreeRTOS.h, task.h). Removed or rewritten: `portSWITCH_TO_USER_MODE()`, the pvPortMalloc-wrapper claim and the DWT claim (not in the fetched pages). Cortex-M privilege behaviour (`CONTROL.nPRIV`, SCS/CPS access) is not confirmed: the Arm reference page returned no text (gated).
Method: documentation only; no commands were run.
