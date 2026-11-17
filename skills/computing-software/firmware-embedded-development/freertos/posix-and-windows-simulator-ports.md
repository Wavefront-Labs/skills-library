---
id: computing-software.firmware-embedded-development.freertos.posix-and-windows-simulator-ports
name: posix-and-windows-simulator-ports
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-posix-port, msvc-mingw-port, host-simulation, freertos-simulator, unit-testing, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Run FreeRTOS applications on a PC with the POSIX (Linux/macOS) or Windows simulator ports for fast logic testing, and know where simulated timing and interrupts lie."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Linux/FreeRTOS-simulator-for-Linux
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/04-Demos/03-Emulation-and-simulation/Windows/FreeRTOS-Windows-Simulator-emulator-for-Visual-Studio-and-Eclipse-MingW
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# POSIX and Windows simulator ports

**Goal:** run application tasks, queues and state machines on a workstation for fast iteration
and CI, without hardware.

## Ports
- `portable/ThirdParty/GCC/Posix`: Linux and macOS, each task is a pthread; only one runs at a
  time, gated by the port.
- `portable/MSVC-MingW`: Windows, each task is a Win32 thread.

## Minimal CMake (POSIX)
```cmake
add_library(freertos_config INTERFACE)
target_include_directories(freertos_config INTERFACE config/)   # FreeRTOSConfig.h for host
set(FREERTOS_PORT GCC_POSIX CACHE STRING "")
set(FREERTOS_HEAP 3 CACHE STRING "")                             # heap_3: host malloc, ASan-friendly
add_subdirectory(FreeRTOS-Kernel)
add_executable(app_sim main_sim.c ../app/src/logic.c)
target_link_libraries(app_sim freertos_kernel freertos_config pthread)
```
Host config essentials: `configTICK_RATE_HZ 1000`, `configMINIMAL_STACK_SIZE` large (e.g.
`PTHREAD_STACK_MIN` worth), `configUSE_PREEMPTION 1`. Stack overflow checking is meaningless here.

## Structure the app for it
- Keep hardware behind a thin HAL interface; provide a `sim/` implementation (UART from stdin,
  GPIO as log lines, sensors from a file).
- "Interrupts" are simulated by a host thread or a FreeRTOS timer calling the same handler code;
  on POSIX use the documented signal-safe pattern from the demo, not arbitrary pthread calls into
  FreeRTOS APIs.

## What it is good for
- Business logic, protocol state machines, queue topologies, deadlock hunting (attach gdb, all
  tasks visible as threads).
- Sanitizers: build with `-fsanitize=address,undefined` and heap_3.
- CI: run deterministic test scenarios headless.

## Where it lies
- Timing is soft: the host OS schedules the threads; ticks jitter by milliseconds. Never validate
  deadlines or ISR latency here.
- Priority inversion and preemption points differ from the target.
- No real interrupt nesting, BASEPRI masking, or MPU faults.
- Calling blocking host functions (printf to a slow terminal, sleep) from a task stalls the whole
  simulated kernel; the POSIX port docs warn that system calls interfere with its signals.

## Verify
- [ ] Same application sources compile for target and sim (only HAL differs).
- [ ] Sim run under ASan is clean.
- [ ] Timing-sensitive requirements are verified on hardware, not the simulator.

## Checked

2026-11-01. Confirmed against FreeRTOS-Kernel: `portable/ThirdParty/GCC/Posix` and `portable/MSVC-MingW` exist, and the top-level CMakeLists.txt takes `FREERTOS_PORT` (including `GCC_POSIX`) and `FREERTOS_HEAP`. Removed demo directory names (they live in the separate FreeRTOS repo, not checked).
Method: documentation only; no commands were run.
