---
id: computing-software.it-support-helpdesk.troubleshooting-methodology.cable-and-port-testing
name: cable-and-port-testing
category: computing-software
field: it-support-helpdesk
product: troubleshooting-methodology
tags: [it-support-helpdesk, troubleshooting-methodology, networking, network-troubleshooting, cable-testing, toner-probe, cable-tester, link-lights, patch-panel, poe, loopback-plug, speed-duplex, comptia-a-plus]
level: intro
status: draft
description: "Test wired connections physically: link lights and speed, swap tests, cable testers and toner/probe to trace ports, loopback plugs, PoE and duplex mismatch."
sources:
  - "https://www.comptia.org/certifications/a"
  - "https://learn.microsoft.com/en-us/powershell/module/netadapter/get-netadapter"
  - "https://www.flukenetworks.com/knowledge-base"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# cable-and-port-testing

Goal: prove or eliminate the physical layer quickly for a wired desk
(A+ 220-1201 2.x network tools and 5.7 wired troubleshooting).

## Quick checks
- **Link lights** on NIC/dock and switch: off = no link; amber/orange often
  = lower speed or fault (vendor-specific).
- Negotiated speed:
  ```powershell
  Get-NetAdapter | Select Name, Status, LinkSpeed, MediaConnectionState
  ```
  100 Mbps on a gigabit network = bad pair in the cable/jack (gigabit needs
  all 4 pairs) or old patch lead.
- **Swap tests**: known-good patch lead; another wall port; another device
  on the same port; direct to laptop NIC instead of dock.

## Tools
| Tool | Use |
|---|---|
| **Cable tester** (continuity/wiremap) | opens, shorts, miswires, split pairs; certifiers measure performance for Cat6/6A |
| **Toner and probe** | find which patch-panel port a wall jack connects to (label it while there) |
| **Loopback plug** | test a NIC or switch port in isolation |
| **Link/PoE tester** | shows switch port speed, VLAN (via CDP/LLDP), PoE wattage |
| **Punchdown tool** | re-terminate a jack or panel (110/Krone) |
| **Crimper** | make/replace patch leads — buy moulded leads where possible |

## Common faults
- Damaged lead under a chair wheel; RJ45 clip broken (intermittent).
- Wall jack wired to a dead or unpatched panel port → patch it (with
  network team approval) and label.
- Switch port disabled, wrong VLAN, port security/MAC limit or 802.1X →
  network team checks the switch.
- PoE phone/AP not powering: switch PoE budget exceeded or port not PoE.
- Duplex mismatch (one end forced full, other auto → half): slow and
  errors; `Get-NetAdapterAdvancedProperty` shows Speed & Duplex — set both
  to auto.

## Safety and tidiness
Don't trace cables in ceilings/floors without authorisation; label
everything you identify; no cable runs across walkways.

## Verify
Link up at expected speed (1 Gbps+), no errors, device gets an address and
works through a file copy without drops.
