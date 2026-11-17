---
id: computing-software.systems-network-administration.network-design.copper-cable-tracing-and-poe-faults
name: copper-cable-tracing-and-poe-faults
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, physical-troubleshooting, cable-tester, toner-probe, wire-map, split-pair, crossed-pair, cable-certifier, link-tester, poe-troubleshooting, poe-budget, attenuation, crosstalk, next]
level: practitioner
status: draft
description: "Find copper cabling faults: tone and probe tracing, wire-map errors including split pairs, qualifier vs certifier testers, and PoE devices that will not power up."
sources:
  - https://www.flukenetworks.com/knowledge-base/applications-standards-articles/wiremap-faults
  - https://www.comptia.org/certifications/network
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Copper cable tracing and PoE faults

## Tracing an unlabelled run
- **Toner and probe**: clip the tone generator to the jack (or plug in), wave the inductive
  probe over the patch panel/bundle in the comms room to find the loudest port. Digital/
  "smart" toners avoid bleed-over on live PoE switches.
- Switch-side alternative: plug a laptop into the outlet and find its MAC on the switch
  (trace-host-to-switch-port), or use LLDP/CDP from a link tester (shows switch name, port, VLAN).
- Label immediately at both ends.

## Wire-map faults
| Fault | Effect |
|---|---|
| Open | no link or 100 Mb only (if pair 3 or 4 open, gigabit fails) |
| Short | no link on that pair |
| Reversed pair (tip/ring swapped within a pair) | usually no link on that pair |
| Crossed pairs (e.g. 1-2 to 3-6 at one end, T568A vs B mix) | works via Auto-MDIX but fails certification |
| **Split pair** (wires from different pairs twisted together) | wire-map continuity passes on a cheap tester, but crosstalk kills gigabit: errors, link at 100 Mb |
Cheap continuity testers miss split pairs; qualifiers/certifiers catch them (NEXT failure).

## Tester classes
| Class | Answers |
|---|---|
| Continuity / wire-map tester | wired correctly? (pins) |
| Qualifier (e.g. LinkIQ, CableIQ) | will it run 1G/2.5G/10G? PoE load test, switch info |
| Certifier (DSX) | meets TIA category limits (insertion loss, NEXT, return loss): needed for warranty/handover |
| Switch TDR | distance to open/short (see tdr-cable-diagnostics) |

## PoE device will not power or keeps rebooting
1. `show power inline Gi1/0/x` (or vendor equivalent): is power allocated? Oper status faulty
   = short or classification failure; "denied" = budget exhausted.
2. Device class vs port capability (bt device on an at port boots in reduced mode or not at all).
3. Cable: a high-resistance joint or a damaged pair passes data but fails under PoE load; use a
   qualifier with PoE load test. 4-pair bt devices need all four pairs good.
4. Long runs near 100 m plus thin patch cords (28 AWG) increase voltage drop.
5. Inline couplers, cheap keystones, and passive splitters cause intermittent PoE failures.
6. Switch budget/PSU redundancy mode (see poe-standards-and-power-budget).

## Verify
- [ ] Run traced and labelled at both ends.
- [ ] Qualifier/certifier pass at the required speed, including PoE load if powered.
- [ ] Device negotiates full power and stays up through a load period.
