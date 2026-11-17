---
id: computing-software.systems-network-administration.network-design.identity-psk-for-iot
name: identity-psk-for-iot
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wireless-design, ipsk, mpsk, ppsk, iot-onboarding, dynamic-vlan]
level: practitioner
status: docs-checked
description: "Onboard headless IoT devices with Identity/Multi PSK: one SSID, a unique key per device or group, RADIUS or controller key mapping to VLAN and policy, and rotation."
sources:
  - https://www.cisco.com/c/en/us/td/docs/wireless/controller/9800/config-guide/b_wl_17_9_cg/m_ipsk.html
  - https://documentation.meraki.com/MR/Encryption_and_Authentication/IPSK_with_RADIUS_Authentication
  - https://www.arubanetworks.com/techdocs/central/latest/content/access-points/cfg/security/mpsk.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity PSK (iPSK / MPSK / PPSK)

## Problem
Printers, sensors, TVs and medical devices cannot do 802.1X, but one shared PSK for all of them
means a leaked key exposes everything and changing it means touching every device.

## Approach
One WPA2-Personal SSID (Meraki states iPSK with RADIUS authentication does not support WPA3); the controller holds **many PSKs**. During
the 4-way handshake the AP tries keys tied to the client MAC (RADIUS lookup returning a
`Tunnel-Password` attribute in the Access-Accept, per Meraki).
The matched key determines VLAN, role and ACL.

Vendor names: Cisco iPSK, Meraki iPSK (with RADIUS, or Easy PSK on MR 32.1.3 and newer), Aruba MPSK; other vendors use their own names.

## Design
- Key per device class or per device for high-risk items; key-to-VLAN mapping (IoT-cameras,
  IoT-building, guests' own devices).
- MAC-based lookup needs MAC addresses up front; key-only modes do not but are limited in count
 .
- Client isolation inside IoT VLANs; firewall policy allows only required destinations.
- Store keys in a vault/NAC with owner and device; rotate on staff exit or compromise of one group.
- Self-service portals (NAC platforms) let users register devices and get
  personal keys in residence halls / BYOD.

## Verify
- [ ] Two devices with different keys land in different VLANs; revoking one key disconnects only that device.

## Checked

- Date: 2026-10-28
- Confirmed: Meraki iPSK-with-RADIUS article: RADIUS lookup by client MAC, PSK returned in Tunnel-Password in the Access-Accept, no WPA3 support, Easy PSK from MR 32.1.3, per-device PSK SSIDs can bridge clients onto different VLANs.
- Removed: cisco-avpair psk syntax, MPSK try-every-key behaviour, Ruckus DPSK and Extreme PPSK names, WPA3-SAE claims, portal product names (Cisco and Aruba pages were missing or blocked).
Method: documentation only; no commands were run.
