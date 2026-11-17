---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.isolation-monitoring
name: isolation-monitoring
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [isolation-monitoring, isolation-resistance, insulation-monitoring, imd, un-r100, y-capacitance, ground-fault]
level: practitioner
status: verified
description: "Implement HV isolation monitoring: requirements per ohm per volt, measurement methods, response times, Y-capacitance effects and fault handling."
sources:
  - "https://www.ecfr.gov/current/title-49/part-571/section-571.305"
  - "UN Regulation 100 and ISO 6469-3 isolation requirements; confirm current editions"
  - "Bender IMD application notes"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Isolation monitoring

1. Requirement basis: UN R100 / ISO 6469-3 specify minimum isolation resistance in ohms per volt of the working voltage (FMVSS 305 in eCFR: 100 ohm/V for DC and 500 ohm/V for AC high voltage sources; the UN R100 and ISO 6469-3 values and continuous-monitoring variants are (gated: unconfirmed, source is paywalled or blocked)); confirm the edition and the market's rule.
2. Example: 400 V DC bus at 100 ohm/V = 40 kohm minimum; 500 ohm/V = 200 kohm.
3. Measurement: either a dedicated insulation monitor (injects a low-frequency test signal between HV and chassis) or a measurement circuit with switched resistors comparing voltages of HV+ and HV- to chassis; the regulation gives a reference method.
4. Y-capacitors (HV to chassis EMC capacitors) slow the response of active monitors and must be considered, along with the stored energy and touch current at isolation faults.
5. Fault handling: warn the driver at the warning threshold, and if the fault is severe disconnect or restrict operation; separate threshold for the charging situation.
6. Include the charger: monitoring while plugged in, and DC fast-charging insulation test at start.
7. Test: insert known resistances from HV+ and HV- to chassis and check measured values and thresholds.

**Gotchas:** wet connectors and coolant leaks cause intermittent isolation faults; log events.

## Verify
- [ ] Insert 100 ohm/V and 500 ohm/V equivalent resistors; monitor reads within tolerance and flags correctly.
- [ ] Response time to a step fault recorded.
