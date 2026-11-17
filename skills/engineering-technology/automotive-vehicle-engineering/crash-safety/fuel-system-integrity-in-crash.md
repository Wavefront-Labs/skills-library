---
id: engineering-technology.automotive-vehicle-engineering.crash-safety.fuel-system-integrity-in-crash
name: fuel-system-integrity-in-crash
category: engineering-technology
field: automotive-vehicle-engineering
product: crash-safety
tags: [fuel-integrity, fuel-system, fmvss-301, fuel-leakage, fuel-tank, rollover-valve, fuel-pump-cutoff, post-crash, rear-impact, ice-fuel-safety]
level: practitioner
status: gated
description: "Protect ICE fuel systems in crash: tank location and shielding, filler and line breakaway, valves, pump cut-off, and FMVSS 301 and UN test context. Civil vehicles."
sources:
  - "Kramer, Passive Safety of Vehicles (chapter list)"
  - "FMVSS 301 (fuel system integrity) and UN Regulation 34 and UN Regulation 94/95 fuel leakage provisions; confirm current texts"
  - "https://www.law.cornell.edu/cfr/text/49/571.301"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

Safety-critical, regulated work. This is professional practice guidance: confirm the current regulation, edition and market, and defer sign-off to qualified safety and homologation engineers.

# Fuel system integrity in crash

## 1. Regulatory context (confirm current)
FMVSS 301 limits fuel leakage in frontal, side and rear crash tests and in a rollover sequence, with maximum permitted loss during and after the test (49 CFR 571.301 S5.5-S5.6: spillage not above 142 g in the 5 minutes after motion stops and not above 28 g in any 1-minute interval in the following 25 minutes; rollover spillage not above 142 g in the first 5 minutes from the onset of rotation and 28 g per minute during later holds. Checked in eCFR). In UN-regulation markets, fuel leakage criteria appear in the frontal (R94) and side (R95) tests (gated: unconfirmed, source is paywalled or blocked), and in other regulations for the fuel system itself. Hydrogen and gaseous-fuel vehicles have separate regulations.

## 2. Design principles
- **Tank location:** place the tank in a protected zone (ahead of the rear axle and inside the wheelbase, within the structure), away from crush zones and deformable zones in rear and side impact; keep clearance to deforming members and sharp edges.
- **Tank structure:** multi-layer plastic (HDPE with barrier) or steel; shields and straps; design the straps to release without puncturing; avoid contact with rear cross-member deformation.
- **Filler neck and lines:** flexible, routed in protected areas, with breakaway or weak-link points so a displaced component does not tear the tank; fuel line fittings rated for crash loads.
- **Valves:** rollover valve (vent and fill limit valves) to seal in a rollover; check valves to stop liquid leaving through vent lines.
- **Pump cut-off:** fuel pump stops on crash signal (inertia switch or airbag ECU) to limit spillage.
- **Ignition sources:** keep tank and lines away from hot exhaust, high-voltage components and battery terminals; fuse and battery cable protection.

## 3. CAE and test
Rear-impact model with fuel sloshing (fluid or equivalent mass), tank deformation limits and strain failure criteria for plastic; rollover (quarter-turn steps) to check leakage; verification by regulation crash tests with water or approved fuel substitute as the standard specifies.

## 4. Post-crash behaviour
Fire risk checks, fuel smell, leak path analysis; instructions in the rescue sheet (see rescue sheet).

## Verify
- [ ] Applicable test requirements and leakage limits confirmed for each market.
- [ ] Tank and lines protected from deformation and from sharp edges.
- [ ] Pump cut-off and rollover valve operation verified.
- [ ] CAE and test evidence of spillage within limits.
