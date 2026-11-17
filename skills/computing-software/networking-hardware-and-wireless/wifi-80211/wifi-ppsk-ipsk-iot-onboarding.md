---
id: computing-software.networking-hardware-and-wireless.wifi-80211.wifi-ppsk-ipsk-iot-onboarding
name: wifi-ppsk-ipsk-iot-onboarding
category: computing-software
field: networking-hardware-and-wireless
product: wifi-80211
tags: [wifi-ppsk-ipsk, iot-wifi-onboarding, iot-vlan-segmentation]
level: practitioner
status: draft
description: "Use PPSK/IPSK or MAC-auth-bypass to place headless IoT devices on isolated VLANs without 802.1X."
sources:
  - https://www.wi-fi.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IoT onboarding

- Headless devices often lack 802.1X support and are 2.4 GHz-only, WPA2-PSK-only. Do not weaken the corporate SSID; give them their own.
- Private/Individual PSK (vendor features: PPSK, IPSK, Multi-PSK) issues a different key per device or group and maps each to a VLAN/role; revoking one key does not disrupt others.
- MAC authentication bypass is weak alone (MACs are spoofable and often randomised); combine with isolation and firewall rules.
- Firewall IoT VLANs to only the cloud endpoints they need; block lateral movement and inbound.
- Keep an inventory and owner for each device; patch firmware.

## Verify
- [ ] An IoT device in its VLAN reaches only its permitted destinations (tested by a scan from that VLAN).
