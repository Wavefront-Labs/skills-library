---
id: computing-software.firmware-embedded-development.freertos.xtasknotify-actions
name: xtasknotify-actions
category: computing-software
field: firmware-embedded-development
product: freertos
tags: [xtasknotify-action, enotifyaction, esetbits, eincrement, esetvaluewithoutoverwrite, freertos, firmware-embedded-development]
level: advanced
status: docs-checked
description: "Pick the right eNotifyAction for xTaskNotify (eNoAction, eSetBits, eIncrement, eSetValue with or without overwrite) to use notifications as flags, counters or mailboxes."
sources:
  - https://github.com/FreeRTOS/FreeRTOS-Kernel/blob/main/include/task.h
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# xTaskNotify actions

Each task has a 32-bit notification value plus a pending state (per index). `xTaskNotify(h,
value, action)` (and `xTaskNotifyFromISR`) updates it according to `action`:

| Action | Effect on value | Emulates | Receiver |
|---|---|---|---|
| `eNoAction` | unchanged, just marks pending | plain wake | `xTaskNotifyWait` |
| `eSetBits` | `value |= ulValue` | event group (single task) | `xTaskNotifyWait(0, bits, &v, t)` |
| `eIncrement` | `value++` (ulValue ignored) | counting semaphore | `ulTaskNotifyTake` |
| `eSetValueWithOverwrite` | `value = ulValue` always | length-1 queue with overwrite | `xTaskNotifyWait(0, ~0, &v, t)` |
| `eSetValueWithoutOverwrite` | set only if not already pending; else returns `pdFAIL` | length-1 queue | `xTaskNotifyWait` |

`xTaskNotifyGive` is shorthand for `eIncrement`.

## Event flags example
```c
#define EV_RX   (1u << 0)
#define EV_TX   (1u << 1)
#define EV_ERR  (1u << 2)

/* ISR */
xTaskNotifyFromISR(hComms, EV_RX, eSetBits, &woken);
portYIELD_FROM_ISR(woken);

/* task */
uint32_t ev;
xTaskNotifyWait(0, 0xFFFFFFFFu /*clear all on exit*/, &ev, portMAX_DELAY);
if (ev & EV_RX)  service_rx();
if (ev & EV_TX)  service_tx();
if (ev & EV_ERR) recover();
```
`ulBitsToClearOnEntry` = 0 keeps bits set before the wait began; clearing on entry loses
events that arrived just before the call.

## Mailbox example
```c
/* producer: latest ADC reading wins */
xTaskNotify(hCtl, adc_raw, eSetValueWithOverwrite);
```
Use `eSetValueWithoutOverwrite` when the producer must know the previous value was not
consumed (check for `pdFAIL`).

## Rules
- Don't mix styles on one index: incrementing and bit-setting the same value corrupts both
  meanings. Use separate indices (`xTaskNotifyIndexed`, `configTASK_NOTIFICATION_ARRAY_ENTRIES`).
- Only one task can receive; multiple producers are fine.
- `xTaskNotifyAndQuery` also returns the previous notification value through its last argument.

## Verify
- [ ] Each notification index has exactly one documented action style.
- [ ] Receivers clear bits on exit, not entry, unless deliberately discarding stale events.
- [ ] `eSetValueWithoutOverwrite` callers handle the `pdFAIL` return.

## Checked

2026-11-01. Confirmed against FreeRTOS-Kernel include/task.h: eNotifyAction values, `eSetValueWithoutOverwrite` returning pdFAIL when a notification is already pending, `eSetValueWithOverwrite` always pdPASS, `xTaskNotifyAndQuery`, `xTaskNotifyGive`, indexed notifications and `configTASK_NOTIFICATION_ARRAY_ENTRIES`. Nothing removed.
Method: documentation only; no commands were run.
