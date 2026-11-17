---
id: computing-software.firmware-embedded-development.iot-protocols.lorawan-duty-cycle-airtime
name: lorawan-duty-cycle-airtime
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [lorawan-duty-cycle-airtime, lorawan, airtime, duty-cycle, time-on-air, iot-protocols]
level: practitioner
status: docs-checked
description: "LoRaWAN duty cycle and airtime: Budget messages per day within regulatory and fair-use limits."
sources:
  - https://www.thethingsnetwork.org/docs/lorawan/duty-cycle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# LoRaWAN duty cycle and airtime

**Goal:** Budget messages per day within regulatory and fair-use limits.

## Steps
1. Duty cycle is the fraction of time a resource is busy. A device sending 2 time units in every 10 on one channel has a 20% duty cycle; across 3 channels it transmits 60% of the time even though each channel is 20% busy. Regulators often set 1%, but check your local regulation.
2. In Europe duty cycle is regulated by section 4.3.3 of ETSI EN 300.220-2 V3.2.1 (2018-06), which defines sub-bands: K (863-865 MHz) 0.1%, L (865-868 MHz) 1%, M (868-868.6 MHz) 1%, N (868.7-869.2 MHz) 0.1%, P (869.4-869.65 MHz) 10%, Q (869.7-870 MHz) 1%. A transmission on one channel counts against the whole sub-band.
3. The LoRaWAN specification also sets duty cycles for the join frequencies used by OTAA; in most regions 1%.
4. The Things Stack Sandbox (The Things Network) applies a Fair Use Policy of 30 seconds of uplink airtime per node per day (24 hours) and 10 downlink messages per node per day. Private networks are not subject to it but still must meet regulatory and LoRaWAN limits.
5. Compute each message's airtime with an airtime calculator, then choose a transmit interval: maximum messages per period = allowed airtime / airtime per message. For example 1% of an hour is 36 seconds.
6. Where a sub-band is shared by several channels, one approach is to divide the sub-band duty cycle by the channel count (1% over 8 channels = 0.125% each).

## Gotcha
Some radio modules enforce duty cycle themselves; the RN2483 limits it per channel and reports `no_free_ch` when exceeded, so with a single channel configured it starts enforcing after the first message.

## Verify
- [ ] Airtime per message computed with a calculator
- [ ] Daily message count under the applicable cap
- [ ] Both nodes and gateways stay within the regulated duty cycle

## Checked
2026-11-09. Read The Things Network "Duty Cycle" page: definitions, ETSI sub-band table, join-frequency note, Fair Use Policy (30 s, 10 downlinks), RN2483 behaviour, per-channel division. Removed: time-on-air formula parameters, the 56 ms / 1.5 s figures, the 13-byte header, ADR gotcha and listen-before-talk checklist item (not on the page), and the LoRa Alliance spec source (404).
Method: documentation only; no commands were run.
