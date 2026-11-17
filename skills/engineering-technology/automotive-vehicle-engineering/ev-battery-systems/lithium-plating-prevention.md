---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.lithium-plating-prevention
name: lithium-plating-prevention
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [lithium-plating, plating, fast-charging, low-temperature-charging, anode-potential, three-electrode-cell, charge-limits, battery-ageing, dvdq, coulombic-efficiency]
level: practitioner
status: gated
description: "Prevent lithium plating on graphite anodes: understand the conditions that cause it, set temperature and SoC dependent charge current limits, and detect it in tests."
sources:
  - "Plett, Battery Management Systems Vols 1 and 2"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design (chapter list)"
  - "Linden and Reddy, Handbook of Batteries (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Lithium plating prevention

Safety-relevant battery topic: plated lithium shortens life and can form dendrites that raise short-circuit risk. Use supplier limits and qualified battery engineers; this note is engineering practice, not approval.

## 1. Mechanism
During charging, lithium ions intercalate into graphite. If the anode surface potential falls to about 0 V versus Li/Li+ (gated: unconfirmed, source is paywalled or blocked), metallic lithium can deposit instead (plating raises short-circuit and degradation risk, confirmed in Wikipedia Lithium-ion battery). Risk rises with low temperature, high charge rate, high SoC, unbalanced or thick electrodes, and aged cells with higher resistance.

## 2. Prevention levers
1. **Charge limit map:** maximum charge current as a function of cell temperature and SoC from supplier data, tightened for ageing; taper at high SoC.
2. **Preconditioning:** heat the pack before fast charging and for low-temperature charging (see battery preconditioning).
3. **Regen limits:** regenerative braking at low temperature and high SoC can plate; derate regen with temperature (see current limit and derating).
4. **Model-based charging:** an electrochemical or reduced-order model (or a map calibrated with three-electrode cells) keeps anode potential above a safety margin.
5. **Cell design:** anode-to-cathode capacity ratio, graphite grade and electrolyte additives, set by the cell supplier.

## 3. Detection in development
- Three-electrode cells measure anode potential during charge.
- A voltage relaxation plateau after charge and a dV/dQ feature on discharge (stripping of plated lithium) are common indicators.
- Coulombic efficiency drop and abnormal capacity fade; post-mortem inspection (optical, SEM) of the anode.
- Compare in-vehicle charge profiles against the supplier-validated envelope.

## 4. Calibration workflow
Run a fast-charge test matrix over temperature and SoC at several C-rates for a defined number of cycles; do check-ups; tear down selected cells; set the limit just inside plating onset with margin; re-validate at aged state (end-of-life resistance).

## Verify
- [ ] Charge limit map defined for temperature, SoC and ageing.
- [ ] Plating detection method used on test cells and teardown completed.
- [ ] Regen and preconditioning limits consistent with plating margin.
- [ ] Supplier approval of the final charge profile.
