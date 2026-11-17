---
id: computing-software.firmware-embedded-development.low-power-design.lorawan-duty-cycle-and-airtime
name: lorawan-duty-cycle-and-airtime
category: computing-software
field: firmware-embedded-development
product: low-power-design
tags: [radio-power, lorawan-duty-cycle, airtime, spreading-factor, adr, eu868-1-percent, class-a, fair-use-policy, firmware-embedded-development]
level: advanced
status: draft
description: "Budget LoRaWAN uplinks against regional duty-cycle limits and battery: airtime per spreading factor, ADR, payload sizing, confirmed vs unconfirmed and class A timing."
sources:
  - https://resources.lora-alliance.org/technical-specifications/rp002-1-0-4-regional-parameters
  - https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/
  - https://www.semtech.com/design-support/lora-calculator
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# LoRaWAN duty cycle and airtime

**Goal:** an uplink schedule that is legal in the region, fair to the network, and fits the
battery budget over years.

## Airtime drives everything
Airtime depends on spreading factor (SF7-SF12), bandwidth (125 kHz typical) and payload. For a
10-byte application payload (+13 bytes LoRaWAN overhead) at 125 kHz, roughly:
| SF | Airtime | |
|---|---|---|
| SF7 | ~60 ms | |
| SF9 | ~190 ms | |
| SF12 | ~1.3-1.5 s | 20x+ SF7 |
TX current at 14 dBm is ~25-45 mA (radio dependent); energy per uplink at SF12 is ~20x SF7.
Use the Semtech LoRa calculator or TTN airtime calculator for exact values.

## Regional limits
- **EU868**: 1 % duty cycle per sub-band for most channels (0.1 % or 10 % on some): after a
  1.5 s SF12 uplink, that sub-band is unavailable for ~148 s. The LoRaWAN stack (LoRaMac-node,
  LBM, Zephyr's LoRaWAN) enforces it and returns busy/duty-cycle errors.
- **US915**: no duty cycle but 400 ms max dwell time per transmission (SF10 at 125 kHz max for
  small payloads).
- Network fair use: TTN community allows **30 s airtime per device per day** and 10 downlinks.

## Levers
- **ADR** (adaptive data rate): network lowers SF for well-placed devices; enable for static
  devices, disable or use conservative SF for mobile ones.
- **Payload**: binary-pack data (no JSON), batch several readings per uplink, send deltas.
- **Unconfirmed uplinks** by default; confirmed uplinks cost a downlink (gateway airtime, also
  duty-cycle limited) and retries at higher SF.
- **Class A**: two receive windows after each uplink (RX1 at 1 s, RX2 at 2 s); the radio
  listens briefly in each: include RX energy in budgets. Class B/C cost far more.

## Battery budget example
Uplink every 15 min at SF9, ~190 ms TX at 40 mA + RX windows ~2 x 20 ms at 12 mA + MCU wake
~50 ms at 5 mA = ~9 mC per uplink: 96/day ~ 0.86 C/day ~ 0.24 mAh/day. Plus sleep current
(2 uA x 24 h = 0.048 mAh/day). Then derate the battery for temperature and self-discharge.

## Verify
- [ ] Airtime per uplink computed for worst-case SF and checked against regional limits.
- [ ] Device behaviour when the stack reports duty-cycle busy (queue or drop, never spin).
- [ ] Measured charge per uplink matches the calculation.
