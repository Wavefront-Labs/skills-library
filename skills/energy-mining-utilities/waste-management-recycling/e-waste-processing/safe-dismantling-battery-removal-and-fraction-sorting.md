---
id: energy-mining-utilities.waste-management-recycling.e-waste-processing.safe-dismantling-battery-removal-and-fraction-sorting
name: safe-dismantling-battery-removal-and-fraction-sorting
category: energy-mining-utilities
field: waste-management-recycling
product: e-waste-processing
tags: [e-waste-processing, e-waste, ewaste, weee, waste-electronics, electronics-recycling, itad, dismantling, depollution, lithium-ion, li-ion, swollen-battery, battery-removal, battery-fire, capacitor-discharge, crt, leaded-glass, lcd, ccfl, mercury-lamp, toner-cartridge, data-destruction, nist-800-88, hdd-shredding, ssd-destruction, circuit-board-grading, pcb-grades, bfr-plastics, brominated-flame-retardant, cable-recovery, r2, e-stewards]
level: practitioner
status: draft
description: "Dismantle waste electronics safely: triage for reuse, remove batteries without fires, deal with CRTs, lamps, capacitors and toner, destroy data-bearing parts, and sort fractions for value."
sources:
  - "EU WEEE Directive Annex VII selective-treatment list; NIST SP 800-88 media sanitisation categories; general e-waste depollution practice, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Safe dismantling, battery removal and fraction sorting for e-waste

**Goal:** take apart end-of-life electronics so that nobody is hurt, nothing catches
fire, no customer data escapes, and each material fraction goes to the buyer who pays
most for it. The order matters: **depollute first, then recover value.**

## 1. Triage on arrival
- **Reuse first:** working or repairable devices are worth more whole. Test, grade
  and set them aside under a data-wipe workflow.
- **Data-bearing items** (PCs, laptops, phones, tablets, drives, printers with
  disks, network gear): track by serial number in a secure, access-controlled area.
- **Hazard spot-check:** swollen, hot, leaking or damaged batteries go straight to the
  quarantine bin (below). Check for CRTs, lamps, refrigerant units and toner.

## 2. Batteries (the main fire risk)
- Remove batteries **before** any shredding or crushing. Lithium cells
  punctured or crushed go into thermal runaway.
- Use plastic spudgers, not metal screwdrivers, to prise pouch cells; warm the
  adhesive if the design allows. **Never bend or puncture a pouch.**
- **Tape terminals** or bag each battery individually; store in approved containers
  (metal bins with lids, with vermiculite or other suppressant media where required),
  away from combustibles.
- Swollen or damaged cells: quarantine container, away from the line, collected
  promptly. A smoking battery: get it outside or into a fire-resistant container if
  it's safe, otherwise evacuate and call the fire service; have the right
  extinguishing agent per your fire plan (large volumes of water are often used for
  cooling lithium fires).

## 3. Other hazardous components
- **CRTs:** implosion risk; handle by the frame, wear face shields; the funnel glass
  is leaded and the screen coated with phosphors — keep CRT glass separate.
- **Capacitors:** large electrolytics (microwaves, power supplies, CRTs) can hold a
  dangerous charge. **Discharge with a resistor tool** and verify with a meter before
  touching.
- **Backlight lamps (CCFL)** in older LCDs contain mercury; remove whole, store in
  sealed containers.
- **Toner cartridges:** fine toner dust can ignite; don't shred with other material
  or use compressed air near it.
- **Fridges and air-conditioners** need refrigerant and oil recovery by certified
  technicians and plant — separate stream.

## 4. Data destruction
Follow your contract and a recognised standard (NIST SP 800-88 calls it clear,
purge or destroy):
- **HDDs:** wipe with verified software if reused; else shred or physically destroy
  the platters (degaussing also works on magnetic drives).
- **SSDs, phones, flash:** degaussing does **not** work; use a manufacturer secure
  erase/cryptographic erase where verified, otherwise shred to a small particle size.
- Record serial numbers and issue certificates of destruction.

## 5. Fraction sorting
Typical saleable fractions: ferrous steel, aluminium (heatsinks, casings), copper
(cables, transformers, motors), **circuit boards** (graded high/medium/low by
precious-metal content — e.g. CPU/memory and phone boards high, TV/PSU boards low),
connectors and gold-plated pins, plastics (separate where possible; plastics with
brominated flame retardants often must be kept out of recycling streams),
batteries by chemistry, glass. Mixed fractions sell at the lowest-grade price.

## 6. Personal safety
Cut-resistant gloves and eye protection; dust control (local extraction, no dry sweeping
— use vacuum with suitable filters); hand washing before eating (lead and other
metals). Certifications such as R2 or e-Stewards set auditable versions of all this.

## Verify
- [ ] Reusable items triaged; data-bearing items tracked by serial.
- [ ] Every battery removed before shredding; terminals taped; swollen cells quarantined.
- [ ] Capacitors discharged and metered; CRT glass, lamps and toner segregated.
- [ ] Data destruction matches media type, with certificates.
- [ ] Fractions sorted to buyer grades; dust control and hygiene in place.
