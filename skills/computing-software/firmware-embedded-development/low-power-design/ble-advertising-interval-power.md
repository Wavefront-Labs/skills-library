---
id: computing-software.firmware-embedded-development.low-power-design.ble-advertising-interval-power
name: ble-advertising-interval-power
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [radio-power, ble-advertising-interval, advertising-power-budget, tx-power, discovery-latency, apple-recommended-intervals, advertising-payload-size, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Choose BLE advertising interval, TX power and payload to hit a battery target while keeping discovery fast: energy per advertising event and staged fast/slow advertising."
sources:
  - https://developer.apple.com/accessories/Accessory-Design-Guidelines.pdf
  - https://docs.zephyrproject.org/latest/connectivity/bluetooth/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BLE advertising interval and power

**Goal:** a beacon or connectable peripheral that is discovered quickly when someone looks
for it and costs microamps the rest of the time.

## Energy per advertising event
One legacy advertising event = up to 3 packets (channels 37/38/39) + radio ramp-up.
```
I_avg ~ I_sleep + E_event / T_interval
```
Get `E_event` for your chip and settings from the vendor's power profiler or by measuring, then
solve for the interval that meets the battery budget.

## Levers
- **Interval**: the dominant factor, since `E_event` is paid once per interval.
- **Payload length**: airtime scales with bytes; trim to essentials, use scan response for the
  rest (sent only when a scanner asks).
- **Channels**: advertising on fewer channels saves energy but hurts discovery; keep all three
  unless you control the scanners.
- **TX power**: use the lowest power that meets range.
- **Non-connectable** advertising if no connection is needed.

## Staged advertising
Fast after a trigger, slow otherwise. Apple's Accessory Design Guidelines: advertise at **20 ms for
at least 30 s**, then fall back to one of 152.5, 211.25, 318.75, 417.5, 546.25, 760, 852.5,
1022.5 or 1285 ms.
```c
/* Zephyr */
struct bt_le_adv_param fast = BT_LE_ADV_PARAM_INIT(BT_LE_ADV_OPT_CONN,
        BT_GAP_ADV_FAST_INT_MIN_1, BT_GAP_ADV_FAST_INT_MAX_1, NULL);   /* 30-60 ms */
/* after 30 s: bt_le_adv_update_param / stop + restart with 1022.5 ms (1636 units of 0.625 ms) */
```

## Discovery latency trade-off
Expected discovery time depends on the scanner's duty cycle, so test with the real phone apps.

## Verify
- [ ] Average current measured at each stage matches the budget.
- [ ] Discovery time from a phone (foreground and background) measured at the slow interval.

## Checked
2026-11-01. Confirmed: Apple Accessory Design Guidelines PDF, advertising section (20 ms for at least 30 seconds,
then 152.5, 211.25, 318.75, 417.5, 546.25, 760, 852.5, 1022.5 or 1285 ms); Zephyr gap.h (`BT_GAP_ADV_FAST_INT_MIN_1`
0x0030 and `BT_GAP_ADV_FAST_INT_MAX_1` 0x0060, i.e. 30-60 ms at 0.625 ms units). Removed: per-event charge and
average-current figures, spec random-delay detail, TX power ratios, RX-window and phone scan claims, and the
extended advertising airtime figures.
Method: documentation only; no commands were run.

