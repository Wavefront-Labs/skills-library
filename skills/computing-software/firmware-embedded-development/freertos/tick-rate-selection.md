---
id: computing-software.firmware-embedded-development.freertos.tick-rate-selection
name: tick-rate-selection
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [freertosconfig-h, configtick-rate-hz, tick-rate, pdms-to-ticks, timing-resolution, tick-overhead, vtaskdelay, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose configTICK_RATE_HZ by trading timing resolution against overhead and power, and write delay code that stays correct when the tick rate changes."
sources:
  - https://www.freertos.org/Documentation/02-Kernel/03-Supported-devices/02-Customization#configtick_rate_hz
  - https://www.freertos.org/Documentation/02-Kernel/04-API-references/02-Task-control/01-vTaskDelay
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing configTICK_RATE_HZ

**Goal:** a tick rate that gives the timing resolution tasks need, without wasting CPU and
battery, and code that doesn't break when someone changes it.

## Trade-offs
| Rate | Resolution | Overhead |
|---|---|---|
| 100 Hz | 10 ms | low; good for battery devices with tickless idle |
| 1000 Hz | 1 ms | a common choice; measure the CPU cost on your part |
| > 1000 Hz | < 1 ms | rarely justified; use a hardware timer for fine timing |
Each tick runs the tick ISR plus a context switch when a higher-priority task unblocks. Time
slicing between equal-priority tasks also happens per tick.

## Rules for code
- **Never write raw tick counts.** `vTaskDelay(10)` means 10 ms at 1 kHz and 100 ms at
  100 Hz. Use `pdMS_TO_TICKS(10)`.
- `pdMS_TO_TICKS` truncates: at 100 Hz, `pdMS_TO_TICKS(5)` is **0**, which means "don't block"
  for most APIs. Assert non-zero for short waits or round up yourself.
- `vTaskDelay(n)` has a resolution of one tick period and is relative to the call, so it drifts in
  periodic loops. For periodic tasks use `xTaskDelayUntil` (needs `INCLUDE_xTaskDelayUntil`).
- Timeouts shorter than one tick need a hardware timer or a busy-wait.
- `configTICK_TYPE_WIDTH_IN_BITS` (or `configUSE_16_BIT_TICKS` in older kernels): use 32-bit
  ticks; 16-bit ticks wrap in 65 s at 1 kHz.

## Choosing
1. List the shortest software timing requirement handled by the scheduler (not by a
   peripheral). If it's 10 ms, 1 kHz gives 10 % jitter and 100 Hz gives 100 %.
2. If the device is battery-powered, combine a modest rate with
   `configUSE_TICKLESS_IDLE`; the tick rate then only matters while busy.
3. Keep `configCPU_CLOCK_HZ` correct (SystemCoreClock) or the tick period itself is wrong.

## Verify
- [ ] `grep -rn "vTaskDelay([0-9]" src/` returns nothing (no raw ticks).
- [ ] A task toggling a pin with `xTaskDelayUntil(&t, pdMS_TO_TICKS(10))` shows a 10.0 ms
      period on a logic analyser.
- [ ] No `pdMS_TO_TICKS(x)` evaluates to 0 for blocking calls (static assert or review).

## Checked
2026-11-01. Confirmed in FreeRTOS-Kernel source: `pdMS_TO_TICKS` is integer division (truncates), `configTICK_TYPE_WIDTH_IN_BITS`
or `configUSE_16_BIT_TICKS` required in FreeRTOS.h, `configUSE_TICKLESS_IDLE`, `xTaskDelayUntil` and `vTaskDelay` header
docs (resolution of one tick, relative to call), `configCPU_CLOCK_HZ` used for the tick timer. Removed: CPU overhead and
ISR timing figures and the n-1 to n delay claim.
Method: documentation only; no commands were run.
