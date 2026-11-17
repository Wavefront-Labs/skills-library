---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.lorawan-coverage-planning-for-farms
name: lorawan-coverage-planning-for-farms
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, lorawan, lora, lpwan, gateway-placement, link-budget, spreading-factor, duty-cycle, iot-coverage, farm-iot]
level: advanced
status: draft
description: "Plan LoRaWAN coverage across farmland: regional frequency plan, gateway siting, antenna height, link budget, spreading factor and ADR, duty cycle and test survey."
sources:
  - "LoRa Alliance, LoRaWAN Regional Parameters RP2 (https://lora-alliance.org/resource_hub/rp2-1-0-3-lorawan-regional-parameters/)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LoRaWAN coverage planning for farms

**Goal:** reliable low-power radio links between field sensors and a gateway, over the area needed.

## Basics
LoRaWAN is a low-power wide-area network protocol that uses LoRa radio modulation in licence-free bands. Regional frequency plans differ (for example EU868, US915, AU915, AS923, IN865, among others, as defined in the LoRa Alliance regional parameters); use the plan and the devices for your country. Rules on transmit power, duty cycle (for example limits on the share of time transmitting in some European sub-bands) and listen-before-talk differ by region; follow the national rules.

## Planning steps
1. Map the sensor locations and the terrain (use an elevation model, `elevation-and-topography-derivatives`).
2. Pick gateway sites on high points (a barn roof, grain bin, a mast) with mains or solar power and a backhaul (cellular, fibre or satellite); antenna height matters more than gateway power.
3. Estimate range: line-of-sight links can span many kilometres at low data rates; crops, trees, buildings and hills reduce this strongly; a conservative design assumes only a fraction of the theoretical range for sensors at ground level inside tall crops.
4. Link budget: transmit power plus antenna gains minus path loss and fading margin must exceed the receiver sensitivity, which improves with a higher spreading factor (SF7 is fastest; SF12 has the longest range and the highest airtime). Use the radio vendor's calculators.
5. Enable adaptive data rate (ADR) for fixed sensors; keep payloads small; use a longer reporting interval for distant nodes since airtime at high SF is long.
6. Redundancy: two gateways covering the area improve the packet delivery and allow failover.
7. Antennas: use a good outdoor antenna with the right cable and lightning protection; mount nodes at the maximum feasible height above the crop (for example on a stake).

## Survey
Test with a node placed at the real locations (a field test with a handheld node and a logger of RSSI and SNR); log packet delivery ratio for a week; adjust gateway antenna or add a gateway.

## Verify
- [ ] Packet delivery ratio at each site above your target (for example 95 percent).
- [ ] Gateway status and backhaul monitored with alerts.
- Unconfirmed: regional regulations; check the national regulator.
