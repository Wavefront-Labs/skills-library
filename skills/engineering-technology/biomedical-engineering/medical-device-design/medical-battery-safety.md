---
id: engineering-technology.biomedical-engineering.medical-device-design.medical-battery-safety
name: medical-battery-safety
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [medical-battery, lithium-ion-safety, iec-62133, battery-protection, un-38-3]
level: practitioner
status: verified
description: "Design safe battery power for medical devices: cell choice, protection circuits, charging, thermal runaway mitigation, IEC 62133-2 and transport testing."
sources: ["IEC 62133-2 Safety requirements for portable sealed secondary lithium cells and batteries (confirm edition)", "IEC 60601-1 battery related requirements (confirm edition)", "UN Manual of Tests and Criteria, section 38.3 (confirm edition)", "https://www.iec.ch"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Medical battery safety

**Goal:** prevent fire, venting and unsafe output from batteries in devices used near patients, including after a single fault.

## Practice
- Buy cells and packs with evidence of IEC 62133-2 compliance and traceable lots; qualify second sources.
- **Protection:** overvoltage, undervoltage, overcurrent and short-circuit protection, cell balancing for multi-cell packs, temperature sensing in charging; independent hardware protection where software failure would be hazardous.
- **Charging:** charge only within the cell's temperature window; limit charge current; consider charger single-fault behaviour per IEC 60601-1 single fault conditions.
- **Thermal runaway:** gaps, venting path, material choices, and propagation barriers; battery position away from patient contact.
- **Fuel gauge and indication:** state-of-charge accuracy affects essential performance (device stopping unexpectedly during therapy).
- **Transport and storage:** UN 38.3 (UN Manual of Tests and Criteria, section 38.3) testing for lithium cells and batteries; dangerous goods labelling by mode of transport.
- **Environment:** home use brings drops, liquids and charging with non-original chargers.
- **Ageing:** capacity fade and swelling over life; define replacement and disposal.

## Verify
- [ ] Cell and pack compliance documents on file.
- [ ] Single-fault tests on charger and protection circuit.
- [ ] Abuse and drop tests per risk analysis.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
