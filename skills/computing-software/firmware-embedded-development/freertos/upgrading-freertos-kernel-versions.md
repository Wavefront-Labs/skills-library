---
id: computing-software.firmware-embedded-development.freertos.upgrading-freertos-kernel-versions
name: upgrading-freertos-kernel-versions
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertos-upgrade, kernel-migration, freertos-v11, configenable-backward-compatibility, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Upgrade a project's FreeRTOS kernel (e.g. 9.x or 10.x to 11.x): diff the config, renamed APIs, hook signature changes, port selection, and a regression plan."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/History.txt
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization
  - https://github.com/FreeRTOS/FreeRTOS-Kernel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading kernel versions

## Get the source cleanly
Use the standalone kernel repo (`FreeRTOS/FreeRTOS-Kernel`) as a git submodule or a vendored
copy pinned to a tag (e.g. `V11.1.0`), not a vendor SDK's modified copy. Diff vendor copies
against the matching upstream tag first; local patches must be re-applied consciously.

## Read History.txt for every version you cross
`History.txt` in the kernel repo lists the changes per release (V10.6.x to V11.0.0 and the 11.x releases are separate
entries). Settings that exist in current `FreeRTOS.h` and are worth searching for when you cross into 11.x:
`configNUMBER_OF_CORES` (SMP), `configKERNEL_PROVIDED_STATIC_MEMORY`, `configTICK_TYPE_WIDTH_IN_BITS`,
`configUSE_SB_COMPLETED_CALLBACK`.

`configENABLE_BACKWARD_COMPATIBILITY 1` (default) keeps old names (`xTaskHandle`, `portTickType`, `eTaskStateGet`)
mapped to the new ones. Turn it to 0 after migrating so stale names show.

## Procedure
1. Upgrade on a branch; build with the old `FreeRTOSConfig.h` and fix compile errors only.
2. Compare your config with the new kernel's reference config/demos for your port; look for
   new required settings (`FreeRTOS.h` stops with an `#error` unless one of `configUSE_16_BIT_TICKS` and
   `configTICK_TYPE_WIDTH_IN_BITS` is defined; `configCHECK_HANDLER_INSTALLATION` defaults to 1 and is used by
   the Cortex-M0/M23/ARMv8-M ports).
3. Switch to the matching port directory (`portable/GCC/ARM_CM4F`, or `ARM_CM33_NTZ` etc.) from the
   **new** tree. Never mix an old `port.c` with a new kernel.
4. Fix hook signatures (`vApplicationGetIdleTaskMemory`, stack overflow hook) against the declarations in `task.h`.
5. Enable `configASSERT` and stack checking for the first test runs.
6. Run the regression set: timing tests, stress tests, low-power/tickless paths, every ISR that
   calls FromISR APIs.

## Things that bite
- Vendor HAL timebase: if Cube uses SysTick for HAL and FreeRTOS, ports that check handler
  installation can assert. Move HAL tick to a TIM.
- Trace recorders (Percepio, SystemView) need versions matching the kernel's trace macros.
- Third-party code using private kernel structures (`tskTCB` fields) breaks; replace with
  `vTaskGetInfo`.
- Changed defaults: compare `FreeRTOS.h` default values between versions for macros you omit.

## Verify
- [ ] Kernel and port both from the same upstream tag, recorded in the repo.
- [ ] Backward-compatibility off builds cleanly (or a ticket exists to finish migration).
- [ ] Full regression and a 24 h soak pass with asserts enabled.

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel (FreeRTOS.h, History.txt, portable/): the config macros named above, the
backward-compatibility mappings, the tick-type `#error`, the `ARM_CM33_NTZ` port directory, the handler-installation
check in the M0/M23/ARMv8-M ports, the V11.1.0 tag in History.txt. Removed the per-version breaking-change table
and the `vTaskDelayUntil` macro claim, which History.txt and FreeRTOS.h do not confirm.
Method: documentation only; no commands were run.
