---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.automotive-connector-selection-and-sealing
name: automotive-connector-selection-and-sealing
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [connector-selection, connector, terminal, sealed-connector, uscar-2, fretting-corrosion, terminal-plating, tpa, cpa, hv-connector, hvil, ip-sealing]
level: practitioner
status: gated
description: "Select automotive connectors: terminal size and current, sealing class, plating and fretting, locking assurance, mating cycles and HV interlock; test per USCAR-2 style specs."
sources:
  - "SAE/USCAR-2 (electrical connector system performance; confirm revision); ISO 20653 (degrees of protection for road vehicles); OEM HV connector specs such as LV 214 or LV 215 (existence and scope (gated: unconfirmed, source is paywalled or blocked); confirm with the OEM)"
  - "Navet and Simonot-Lion, Automotive Embedded Systems Handbook (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Automotive connector selection and sealing

## 1. Starting questions
Where does it live (engine bay, cabin, door, underbody), what current and voltage per contact, how many circuits, signal or power or both, expected temperature range, vibration level, mating cycles, serviceability, and which wire gauges?

## 2. Terminal and housing
- **Terminal size** (blade width in mm, for example 0.64, 1.5, 2.8, 6.3 and larger (gated: unconfirmed, source is paywalled or blocked)) sets current capacity, which depends on contact material, plating, temperature class and wire gauge; use the supplier's derating curves.
- **Sealed vs unsealed:** use sealed connectors (individual wire seals plus interface seal) in wet zones. Required degree of protection per ISO 20653 (for example IP67 and IP6K9K for high-pressure wash zones (gated: unconfirmed, source is paywalled or blocked)); confirm per location.
- **Plating:** tin is common and economical; silver or gold for low-level signal contacts and high-vibration areas where fretting would raise resistance. Do not mate dissimilar platings (tin to gold) because of fretting and corrosion risk.
- **Material:** copper alloys (phosphor bronze, brass or high-strength alloys) with spring force for contact normal force.

## 3. Assurance features
- **TPA (terminal position assurance)** secondary lock to ensure all terminals are fully seated.
- **CPA (connector position assurance)** to indicate the connector is fully mated.
- **Polarisation and keying** by colour and mechanical coding to prevent cross-mating.
- **Strain relief** and back-shell for shielded circuits.

## 4. Specification and test
Typical validation per consortium or OEM specifications (SAE/USCAR-2 style): insertion and extraction forces, terminal retention, contact resistance, temperature and humidity cycling, vibration with current monitoring, thermal shock, fluid exposure, mating cycles, dust/water ingress. Confirm which test group and revision your customer requires.

## 5. High-voltage connectors
HV connectors carry touch-safe shrouding (finger-proof), HVIL (high-voltage interlock loop) pins so power opens before the connector separates, shield termination 360 degrees for EMC, locking and CPA, and high-current derating. They are specified by OEM standards and regulation; defer to HV safety engineers.

## 6. Harness integration
Wire seal outer diameter vs insulation, crimp height and pull tests, assembly line process (insertion tools), connector orientation for routing, sealing plugs for unused cavities.

## Verify
- [ ] Terminal current capacity at worst-case temperature exceeds the load.
- [ ] Sealing class chosen for the location and tested.
- [ ] Plating combinations compatible and fretting risk addressed.
- [ ] TPA, CPA and polarisation features in place; validation per customer specification.
