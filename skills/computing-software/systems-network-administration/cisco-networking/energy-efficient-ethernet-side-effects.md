---
id: computing-software.systems-network-administration.cisco-networking.energy-efficient-ethernet-side-effects
name: energy-efficient-ethernet-side-effects
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, ios-xe, energy-efficient-ethernet, eee, ieee-802-3az, power-efficient-ethernet, link-flaps, latency, interface-troubleshooting]
level: practitioner
status: draft
description: "Recognise Energy Efficient Ethernet (802.3az) side effects on Catalyst ports, such as latency, link drops and NIC interop, and disable or verify it per port."
sources:
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/configuration_guide/int_hw/b_179_int_and_hw_9300_cg/configuring_eee.html
  - https://standards.ieee.org/ieee/802.3az/4270/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Energy Efficient Ethernet (802.3az) side effects

## What it does
EEE puts copper PHYs into Low Power Idle (LPI) between frames. Both ends negotiate it via
auto-negotiation. Waking from LPI costs microseconds (about 16.5 us for 1000BASE-T, 4.5 us for 10GBASE-T).

## When it bites
- **Latency- or jitter-sensitive traffic** (trading, PTP, audio-over-IP like Dante/AES67):
  wake time adds jitter. Audinate recommends disabling EEE on Dante ports.
- **NIC/PHY interop bugs**: link drops or renegotiation every few minutes, especially older
  desktop NICs and some IP phones. Symptom: `%LINK-3-UPDOWN` with no cable fault, TDR clean.
- **Wake-on-LAN or PXE oddities** on some endpoints.
- PTP boundary/transparent clock accuracy degrades.

## Commands (Catalyst 9000)
```
show eee capabilities interface Gi1/0/5
show eee status interface Gi1/0/5        ! operational state, LPI state
interface range Gi1/0/1 - 48
 no power efficient-ethernet auto         ! disable
 power efficient-ethernet auto            ! enable
```
Defaults vary by platform and release; confirm with `show eee status` rather than assuming.

## Diagnose
1. Correlate flaps with `show logging | i Gi1/0/5` and `show interfaces Gi1/0/5 | i resets`.
2. Check the endpoint NIC setting (Windows NIC Advanced tab "Energy Efficient Ethernet"/"Green Ethernet";
   Linux `ethtool --show-eee eth0`, `ethtool --set-eee eth0 eee off`).
3. Disable on one side; EEE needs both ends, so disabling either stops LPI.

## Verify
- [ ] Ports for real-time media/PTP have EEE operationally disabled.
- [ ] Flap count stable for 24 h after the change.
