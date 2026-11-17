---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.pack-ip-rating-and-sealing
name: pack-ip-rating-and-sealing
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [pack-sealing, ip-rating, ip67, ip6k9k, iso-20653, breather-valve, pressure-equalisation, leak-test, helium-leak-test, pack-mechanical, gasket]
level: practitioner
status: verified
description: "Design and test pack sealing: IP degree of protection, gasket compression, pressure-equalisation breather, leak test method, condensation and thermal-cycle pumping."
sources:
  - "ISO 20653 (degrees of protection for road vehicles; confirm edition); IEC 60529 (IP code)"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design (chapter list)"
  - "UN Regulation 100 (REESS safety; confirm current revision at https://unece.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Pack IP rating and sealing

## 1. Target
Define the required degree of protection from use and mounting: underfloor packs normally need dust-tight and temporary immersion capability plus high-pressure and steam-jet exposure typical of road vehicles. ISO 20653 (road vehicles; the K-letter codes are defined there and not in IEC 60529, per Wikipedia IP Code) defines codes such as IP6K9K; IEC 60529 defines the general IP code. Confirm the exact requirement with your OEM specification.

## 2. Seal design
- **Gasket:** select material (EPDM, silicone, formed-in-place liquid gasket) for temperature, glycol and road-salt exposure; check compression set and creep over life.
- **Compression control:** metal stops set the compressed gasket height; bolt pitch short enough that lid stiffness holds compression between bolts.
- **Penetrations:** HV connectors, coolant fittings and vent must be rated for the code; avoid screws that penetrate the sealed cavity, or use sealed fasteners.
- **Lid flange stiffness:** large aluminium lids deflect under pressure and thermal loads; check by FEA.

## 3. Pressure equalisation
Temperature and altitude changes make the pack breathe. Use a membrane breather (typically ePTFE) that equalises pressure but blocks liquid; locate it high, away from splash, protected from direct jet. A thermal-runaway event needs a separate burst vent (see pack enclosure and venting); never rely on the breather alone.

## 4. Condensation
Breathing brings humid air; condensation on cold surfaces can cause isolation faults. Mitigate with desiccant, breather position, drainage paths, conformal coating of electronics, and isolation-monitoring diagnostics.

## 5. Testing
- **End-of-line leak test:** air-decay (pressure or flow) with a calibrated limit, or helium tracer for fine leaks, on every pack within the cycle-time budget.
- **Type tests:** dust, immersion (including thermal shock of a hot pack into cold water), spray jet, salt spray and thermal cycling, then check isolation resistance and internal moisture.
- **Correlation:** relate the air-decay limit to water-ingress pass by experiment, not by theory alone.

## Verify
- [ ] Code and test conditions agreed with the OEM specification.
- [ ] Flange compression and stiffness analysed.
- [ ] Breather size and location validated; separate burst vent exists.
- [ ] End-of-line leak limit correlated to the immersion test.
