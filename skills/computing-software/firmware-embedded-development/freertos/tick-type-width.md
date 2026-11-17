---
id: computing-software.firmware-embedded-development.freertos.tick-type-width
name: tick-type-width
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [configtick-type-width, configtick-type-width-in-bits, ticktype-t, tick-overflow, freertos, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose the FreeRTOS TickType_t width (16, 32 or 64 bit) via configTICK_TYPE_WIDTH_IN_BITS: maximum delays, the legacy configUSE_16_BIT_TICKS, and wrap-safe time comparisons."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/FreeRTOS.h
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tick type width

```c
/* FreeRTOSConfig.h */
#define configTICK_TYPE_WIDTH_IN_BITS  TICK_TYPE_WIDTH_32_BITS
/* options: TICK_TYPE_WIDTH_16_BITS, TICK_TYPE_WIDTH_32_BITS, TICK_TYPE_WIDTH_64_BITS */
```
`FreeRTOS.h` requires exactly one of `configUSE_16_BIT_TICKS` and
`configTICK_TYPE_WIDTH_IN_BITS` to be defined (it raises an `#error` if neither or both are
set) and rejects any other width value. For backward compatibility, a config that sets only
`configUSE_16_BIT_TICKS` gets 16-bit ticks when it is 1 and 32-bit ticks otherwise.

## Consequences
Maximum delay is the largest value of `TickType_t` divided by the tick rate (`configTICK_RATE_HZ`):

| Width | Largest value | Max delay at 1 kHz |
|---|---|---|
| 16 | 65535 | about 65.5 s |
| 32 | 4294967295 | about 49.7 days |
| 64 | 2^64 - 1 | effectively unlimited |

Check that your port supports the width you choose. A narrower tick type changes which delays
fit in `TickType_t`, so re-check every long timeout when changing the width.

## Overflow is normal
The tick counter wraps, so your code must compare elapsed time by subtraction:
```c
TickType_t start = xTaskGetTickCount();
...
if ((TickType_t)(xTaskGetTickCount() - start) >= pdMS_TO_TICKS(500)) timeout();  /* wrap-safe */
/* WRONG: if (xTaskGetTickCount() >= start + pdMS_TO_TICKS(500)) */
```
Or use `vTaskSetTimeOutState` / `xTaskCheckForTimeOut`, which exist in `task.h` for this
purpose.

To test wrap early, define `configINITIAL_TICK_COUNT` (it defaults to 0 in `FreeRTOS.h`) near
the maximum of the tick type in a test build.

## Gotchas
- With 16-bit ticks at 1 kHz, any timeout above about 65 s does not fit in `TickType_t`:
  check every long delay.

## Verify
- [ ] Tick width chosen deliberately and documented next to `configTICK_RATE_HZ`.
- [ ] All elapsed-time comparisons use subtraction or `xTaskCheckForTimeOut`.
- [ ] A wrap test with `configINITIAL_TICK_COUNT` near the maximum passes.

## Checked
2026-10-31. Confirmed in the FreeRTOS-Kernel `FreeRTOS.h` and `task.h` headers: the
`TICK_TYPE_WIDTH_*` names, the exactly-one-of rule and legacy mapping, `configINITIAL_TICK_COUNT`
default, and the presence of the timeout functions. The delay table is arithmetic from the
type sizes. Removed: kernel-11 version gate, event group bit counts, atomicity and critical
section claims, `portMAX_DELAY`/`INCLUDE_vTaskSuspend` semantics, the internal wrap handling
description and the `pdMS_TO_TICKS` overflow figure, which the headers fetched did not
confirm. The freertos.org pages could not be read (JavaScript only).
Method: documentation only; no commands were run.
