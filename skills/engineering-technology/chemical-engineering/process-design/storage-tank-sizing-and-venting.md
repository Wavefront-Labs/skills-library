---
id: engineering-technology.chemical-engineering.process-design.storage-tank-sizing-and-venting
name: storage-tank-sizing-and-venting
category: engineering-technology
field: chemical-engineering
product: process-design
tags: [chemical-engineering, process-design, pd-equipment-sizing, storage-tank-sizing-and-venting, storage-tank, tank-sizing, api-650, api-2000, tank-venting, inventory-days, tank-farm, working-volume, breather-vent]
level: practitioner
status: gated
description: "Size atmospheric and low-pressure storage tanks from inventory days and delivery size, and set the venting basis (normal and emergency) referencing API 2000 and 650/620."
sources:
  - "Towler and Sinnott Chemical Engineering Design, Turton et al. Analysis Synthesis and Design of Chemical Processes, Peters Timmerhaus and West Plant Design and Economics, Douglas Conceptual Design of Chemical Processes, NCEES FE and PE Chemical exam specifications"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Storage tank sizing and venting basis

**Goal:** tank count and working volume from the supply-chain logic, with the venting basis stated for the mechanical designer.

## Sizing
1. **Required inventory**: days of storage times daily throughput; add shipment or batch size (the tank must take a whole delivery with headroom), plus minimum heel.
2. **Working volume** = nominal volume x usable fraction (often about 85 to 95% (gated: unconfirmed, source is paywalled or blocked), after allowing for low-level heel and overfill margin).
3. **Number of tanks**: at least two when continuous service is required (one in service, one being filled/tested/cleaned), unless the process allows downtime.
4. **Diameter and height**: choose from standard sizes and foundation limits; consider tank height versus diameter for cost.
5. **Type**: fixed cone roof, internal or external floating roof for volatile liquids, or pressurised/refrigerated storage for LPG-type materials, per the applicable standards and local regulations.

## Venting basis
Atmospheric and low-pressure tanks have normal venting (pump in/out, thermal breathing) and emergency venting (external fire). API 2000 is the standard commonly used for sizing the vent capacity requirements (gated: unconfirmed, source is paywalled or blocked); confirm the edition and applicability. State: maximum fill and empty rates, fluid vapour pressure, flash point, insulation, and the set pressures and vacuum, so the tank vendor or mechanical engineer sizes the vents. Vent emissions are regulated; check with the environmental regulator.

## Gotchas
- Pump-out without vacuum relief collapses a tank.
- Containment (bund) volume and spacing are separate design tasks that depend on local regulation.
- Tank design and construction codes (API 650, API 620 or local equivalents (gated: unconfirmed, source is paywalled or blocked)) require qualified designers.

## Verify
- [ ] Inventory days and delivery size reconciled with working volume.
- [ ] Venting basis in the data sheet lists all scenarios.
