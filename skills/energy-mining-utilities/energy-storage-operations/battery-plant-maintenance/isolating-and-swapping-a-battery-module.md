---
id: energy-mining-utilities.energy-storage-operations.battery-plant-maintenance.isolating-and-swapping-a-battery-module
name: isolating-and-swapping-a-battery-module
category: energy-mining-utilities
field: energy-storage-operations
product: battery-plant-maintenance
tags: [battery-plant-maintenance, bess, battery-maintenance, module-replacement, rack-replacement, dc-isolation, ac-isolation, lockout-tagout, loto, prove-dead, arc-flash, dc-arc-flash, ppe, insulated-tools, string-voltage, contactor, fire-suppression, aerosol-suppression, clean-agent, sprinkler, off-gas-detection, deflagration-vent, hvac-maintenance, chiller, thermal-runaway, damaged-battery, quarantine, lithium-ion, nfpa-855, ul-9540a]
level: practitioner
status: draft
description: "Maintain a BESS safely: DC and AC isolation, proving dead on high-voltage DC, module and rack replacement steps, fire suppression and HVAC upkeep, and thermal-runaway precautions."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Isolating and swapping a battery module

**Goal:** do maintenance inside a battery enclosure without electrical injury, arc flash
or a thermal-runaway event, and leave the plant healthier than you found it.

> Status: draft. Battery systems differ widely (rack voltages, connectors, suppression
> type). Use the integrator's maintenance manual, your electrical safety rules and the
> site's hazard mitigation analysis; NFPA 855 / UL 9540A-related site documents are
> common references in North America.

## 1. Before you open anything
- Check the enclosure's **gas detection and alarms** are normal; never enter if
  off-gas, smoke or abnormal temperature alarms are active. Ventilate per procedure.
- Review the permit: scope, isolations, arc-flash rating for the work, PPE category,
  rescue plan.
- Know where the **suppression system** manual release/inhibit is. Some suppression
  agents need the enclosure unoccupied — follow the lockout of the suppression
  system for entry if required (and restore it after).

## 2. Isolation
- **AC side:** open and lock the PCS/transformer breaker per the isolation list.
- **DC side:** open the rack/string disconnects and the battery contactors; lock and tag.
- **Key point:** batteries are always energised. Isolation separates a rack from the
  system but the modules themselves stay live — inside a rack, string voltage can be
  hundreds to over a thousand volts DC.
- **Prove dead** where it can be dead (bus, PCS input) with a meter rated for the DC
  voltage, tested on a known source before and after. Treat everything on the battery
  side of the disconnect as live.
- DC arcs don't self-extinguish at current zero the way AC arcs can; use insulated tools,
  insulating gloves and the PPE the arc-flash study specifies.

## 3. Module or rack replacement (generic)
1. Confirm the faulty module from BMS data (cell voltage, temperature, balancing
   history) — see energy-mining-utilities.energy-storage-operations.battery-management-systems.triaging-bms-alarms-and-cell-imbalance.
2. Isolate the rack; open the module's series links in the sequence the manual gives,
   reducing the string into lower-voltage sections. Cover exposed terminals.
3. Remove the module with the handling equipment provided (modules can weigh tens of
   kilograms).
4. Inspect the removed module for swelling, damage, heat marks, leaks. **A damaged
   module is quarantined** in a designated area or container, away from other battery
   stock, and shipped under dangerous goods rules.
5. Fit the replacement at a **matching SOC/voltage** to the rack (the manual will say
   how close) so balancing doesn't take days, then torque connections to specification
   — loose busbar joints run hot.
6. Restore the rack, let the BMS recognise the module, and monitor the first charge
   cycle closely.

## 4. Fire protection and HVAC upkeep
- Suppression: check cylinder/agent pressure or weights, discharge nozzles clear,
  detection devices tested, control panel healthy, manual releases accessible.
- Off-gas and smoke detectors: calibrate/test on schedule.
- **Deflagration vents or exhaust ventilation** clear and functional.
- HVAC/chillers: filters, coils, refrigerant charge, coolant levels and leak checks.
  Coolant leaks onto battery equipment are a real fault mode.

## 5. Thermal-runaway precautions
Signs: hissing or venting, sweet/solvent smell, white or grey vapour, rapid temperature
rise. **Leave and isolate remotely, don't fight it at close range**, raise the alarm,
and let the fire service work to the site's emergency plan. Vented battery gas is
flammable and toxic.

## Gotchas
- Never work alone in an enclosure.
- Metal jewellery and uninsulated tools across terminals cause severe burns.
- Replacing a module without investigating why it failed often repeats the failure.

## Verify
- [ ] Enclosure alarms normal before entry; permit and PPE matched to arc-flash level.
- [ ] AC and DC isolated, locked, and dead proven where possible.
- [ ] Damaged modules quarantined and documented.
- [ ] Replacement voltage matched and connections torqued.
- [ ] Suppression, detection and HVAC restored and checked.
