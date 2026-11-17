---
id: computing-software.firmware-embedded-development.freertos.amp-vs-smp-architectures
name: amp-vs-smp-architectures
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [amp-architecture, smp-architecture, multicore-design, heterogeneous-cores, openamp, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Choose between AMP (separate FreeRTOS per core) and SMP (one kernel over identical cores) for multicore MCUs, by core symmetry, isolation, and communication cost."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
  - https://www.openampproject.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMP vs SMP architectures

## Definitions
- **AMP** (asymmetric multiprocessing): each core runs its own OS image (FreeRTOS, bare metal,
  Zephyr, Linux), with its own scheduler, heap and objects. Cores talk through shared memory plus
  doorbell interrupts.
- **SMP** (symmetric multiprocessing): one FreeRTOS kernel schedules tasks across all cores,
  which share memory and kernel objects. Merged into the mainline kernel in V11.0.0 (`configNUMBER_OF_CORES` greater than 1).

## Decision guide
| Factor | AMP | SMP |
|---|---|---|
| Cores differ (M7 + M4, A53 + M4, app + network core) | Required | Not possible |
| Identical cores (RP2040, ESP32, dual M33) | Possible | Natural fit |
| Load balancing | Manual, fixed partition | Automatic |
| Communication cost | Copy through shared RAM + interrupt | Normal queues, notifications |
| Debugging | Two images, two debug sessions | One image, RTOS-aware debugger |

## AMP building blocks
- FreeRTOS message buffers in shared RAM with `sbSEND_COMPLETED` doorbells (simple, FreeRTOS
  on both sides; see amp-message-buffers-between-cores).
- A hardware inter-core mailbox or semaphore peripheral for the doorbell, and a messaging
  framework such as OpenAMP when the other core runs a different OS.
- Boot: usually the primary core loads/starts the secondary (release from reset, set its vector
  table). Plan the memory map (separate flash/RAM regions, shared window) up front in both linker
  scripts.

## SMP considerations
- `configRUN_MULTIPLE_PRIORITIES` defaults to 0: only tasks of the highest ready priority run at
  once. Setting 1 lets tasks of different priorities run in parallel on different cores, which
  can break code that relied on a lower-priority task never running alongside a higher one.
- `vTaskCoreAffinitySet` (needs `configUSE_CORE_AFFINITY 1`, default 0) pins latency-critical
  tasks to chosen cores.
- Shared data needs SMP-safe critical sections or mutexes.

## Common pattern
A dedicated function on one core (AMP) and the application on the other; or SMP for throughput
on identical cores with a few pinned tasks.

## Verify
- [ ] Architecture choice recorded with the deciding factors (core symmetry, isolation, IPC).
- [ ] For AMP: memory map shared by both linker scripts reviewed; IPC soak-tested.
- [ ] For SMP: concurrency audit of code that assumed single-core priority exclusion.

## Checked

Checked 2026-10-25 against FreeRTOS-Kernel V11.3.2 (History.txt, released 16 October 2026, current main) and the FreeRTOS Kernel Book source. Confirmed: SMP merged into the mainline kernel in V11.0.0 (History.txt); configNUMBER_OF_CORES, configRUN_MULTIPLE_PRIORITIES (default 0) and configUSE_CORE_AFFINITY (default 0) in FreeRTOS.h; vTaskCoreAffinitySet in task.h. Removed the isolation, certification and device-specific IPC claims and the ESP32 example that no fetched documentation covers. 
Method: documentation only; no commands were run.
