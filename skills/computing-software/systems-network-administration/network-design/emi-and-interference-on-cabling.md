---
id: computing-software.systems-network-administration.network-design.emi-and-interference-on-cabling
name: emi-and-interference-on-cabling
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, troubleshooting-physical, emi, crosstalk, shielded-cabling, grounding, alien-crosstalk]
level: practitioner
status: docs-checked
description: "Diagnose and avoid electromagnetic interference on copper cabling: separation from power, shielding and grounding, crosstalk types, and symptoms in interface error counters."
sources:
  - https://tiaonline.org/products-and-services/standards/
  - https://www.flukenetworks.com/knowledge-base/applications-standards-articles-copper/what-alien-crosstalk
  - https://www.cisco.com/c/en/us/support/docs/interfaces-modules/port-adapters/12768-eth-collisions.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# EMI and interference on cabling

## Sources
Motors, elevators, VFDs, fluorescent ballasts and LED drivers, welding, transformers, power
cables run in parallel, radio transmitters.

## Separation from power
Keep UTP away from power cabling: follow the separation distances in your cabling standard; cross power cables at 90 degrees; use
grounded metal trays or dividers when parallel runs are unavoidable.

## Crosstalk terms
- **NEXT/FEXT**: coupling between pairs inside a cable (bad termination, untwisting).
- **Alien crosstalk (ANEXT)**: coupling between adjacent cables.
- Measured by certification testers; failing NEXT at one end often points to that termination.

## Shielding and grounding
- Shielded cable (F/UTP, S/FTP) helps in high-EMI areas only if the shield is continuous and the
  panel is bonded to the telecom grounding busbar. A shield grounded badly or at only some
  points can make things worse.
- Industrial sites: shielded cable or fibre near drives/welders; fibre is immune to EMI.

## Symptoms
- CRC/FCS errors, runts, input errors increasing on specific ports, often at certain times (machines
  running): `show interfaces` error counters.
- Speed downshift (1G to 100M), link flaps.
- Errors move with the cable route, not with the port or device.

## Verify
- [ ] Error counters stay flat after rerouting/shielding/fibre replacement during the machinery's operating hours.

## Checked

- Date: 2026-10-28
- Confirmed: Cisco Ethernet troubleshooting page shows the runts, CRC, input-error and frame counters used as symptoms.
- Removed: separation distances (5 in / 12 in), 10GBASE-T and Cat6A statements, TIA-607 reference, exact show command (Fluke and TIA pages unreadable).
Method: documentation only; no commands were run.
