---
id: engineering-technology.biomedical-engineering.medical-device-design.implant-telemetry-wireless-power
name: implant-telemetry-wireless-power
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [implant-telemetry, wireless-power, inductive-link, medradio, ble-implant]
level: advanced
status: gated
description: "Design telemetry and wireless power links for implants: inductive coupling, MedRadio and BLE links, link budget, tissue heating and security."
sources: ["https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-95/subpart-I","https://www.iso.org/standard/52804.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Telemetry and wireless power for implants

**Goal:** a reliable, secure data and power link that does not heat tissue or interfere with other devices.

## Link types
- **Inductive near-field:** coil pairs at low kHz to MHz; short range; used for power transfer and programming. Coupling coefficient falls with distance and misalignment; design with detuning margin.
- **MedRadio (MICS band; 401-406 MHz is a MedRadio band under 47 CFR Part 95 Subpart I, eCFR checked):** longer range data link regulated per region; low power.
- **2.4 GHz BLE:** convenient with smartphones; higher tissue attenuation, coexistence issues (see wireless-coexistence-medical).

## Design points
- Link budget through tissue and the can; antenna in a header outside the metal case.
- Wireless power: rectifier, regulation, foreign-object and thermal limits; implant surface temperature rise is limited by the active implant standard (confirm the figure for your edition (gated: unconfirmed, source is paywalled or blocked)).
- Programming session authentication and encryption; see device-cybersecurity.
- Telemetry-on or MRI-conditional modes interplay with battery current.
- Regulatory: radio approval by region (for example FCC rules in the US, RED in the EU), in addition to device regulation.

## Verify
- [ ] Link range and error rate tested with tissue-equivalent phantoms.
- [ ] Thermal rise measured at maximum power transfer.
- [ ] Security threat model addresses unauthorised programming.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
