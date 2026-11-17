---
id: computing-software.cybersecurity-defensive.network-defence.mac-authentication-bypass-and-profiling
name: mac-authentication-bypass-and-profiling
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [network-access-control, mac-authentication-bypass, mab, device-profiling, iot-onboarding, mac-spoofing, endpoint-identity-groups]
level: practitioner
status: draft
description: "Use MAC Authentication Bypass safely for devices without 802.1X: profiling, restricted authorisation per device type, and detecting MAC spoofing."
sources: ["Cisco ISE Administrator Guide - MAB and profiling", "Aruba ClearPass Policy Manager documentation (device profiling)", "CompTIA Security+ SY0-701 objective 3.2 (port security)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MAC authentication bypass (MAB) and profiling

**Goal:** printers, cameras, badge readers and other headless devices can connect, but a
spoofed MAC address does not give an attacker corporate access.

## How MAB works
The switch sends the device's MAC as username/password to RADIUS. If the MAC is in an
allowed list or profiled group, the RADIUS server returns authorisation. MAC addresses are
trivially spoofed (printed on labels, visible on the wire), so MAB is identification, not authentication.

## Make it safer
1. **Profiling**: NAC classifies devices using DHCP fingerprints (option 55), CDP/LLDP, HTTP user
   agent, SNMP and NMAP probes. Authorise by profile + MAC, not MAC alone.
2. **Restricted authorisation per device type**: printers get a printer VLAN/ACL that permits only
   print servers on 9100/IPP; cameras only the NVR. A spoofer gets a printer's tiny access, not the LAN.
3. **Profile change detection**: alert and re-authorise (CoA) when a "printer" MAC suddenly looks
   like a Windows laptop (DHCP fingerprint and user agent change).
4. **Port binding**: expect each MAC on a known switch port; alert when it moves.
5. Onboarding workflow: MACs registered through a ticket with owner and device type, not added ad hoc.

## Switch side
Configure `mab` with `authentication order dot1x mab` so 802.1X-capable devices still use 802.1X;
consider `authentication order mab dot1x` only for ports dedicated to headless devices to speed connection.

## Gotchas
- Static lists of thousands of MACs rot: expire entries not seen for 90 days.
- Devices with randomised MACs (phones on Wi-Fi) do not fit MAB.
- Profiling probes (SNMP, NMAP) need network access from the NAC to devices; test with security teams so scans are expected.

## Verify
- [ ] A laptop spoofing a printer MAC is detected (profile mismatch) and restricted.
- [ ] Each MAB policy result limits access to only the services that device type needs.
