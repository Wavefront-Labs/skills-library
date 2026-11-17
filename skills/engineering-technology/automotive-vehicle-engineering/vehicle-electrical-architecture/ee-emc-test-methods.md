---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.ee-emc-test-methods
name: ee-emc-test-methods
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [emc-testing, emc, cispr-25, iso-11452, bci, alse, iso-11451, un-r10, radiated-emissions, conducted-emissions, hv-artificial-network, emc-validation]
level: practitioner
status: gated
description: "Plan automotive EMC testing: component emissions and immunity (CISPR 25, ISO 11452), vehicle-level tests, HV artificial networks, set-up rules, and typical fixes."
sources:
  - "UN Regulation No 10 as published in the EU Official Journal (https://eur-lex.europa.eu/eli/reg/2012/10/oj); current revision at https://unece.org"
  - "ISO 11452-2:2019 (https://www.iso.org/standard/68557.html); ISO 11452-4:2020 (https://www.iso.org/standard/74108.html)"
  - "CISPR 25 (IEC webstore, https://webstore.iec.ch), ISO 11451 series, CISPR 12; confirm current editions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# E/E EMC test methods

## 1. Test families (confirm current editions)
- **Emissions:** CISPR 25 sets component and vehicle limits and methods to protect on-board receivers (radio, TV, GNSS, mobile); radiated measurement in an absorber-lined shielded enclosure (ALSE) (gated: unconfirmed, source is paywalled or blocked), conducted voltage and current methods, and for electric drives HV artificial networks (HV-AN) to separate the HV lines. CISPR 12 protects off-board receivers (vehicle-level, measured from a distance).
- **Radiated immunity (component):** ISO 11452-2 in an ALSE and ISO 11452-4 (harness excitation methods, which include **bulk current injection (BCI)**; the 2020 edition is titled "Harness excitation methods" and the old BCI-titled edition is withdrawn); field strengths per OEM spec.
- **Vehicle-level immunity:** ISO 11451 series (gated: unconfirmed, source is paywalled or blocked).
- **Transients and ESD:** see transient and ESD immunity.
- **Regulation:** UN Regulation 10 sets type-approval requirements for vehicles with regard to electromagnetic compatibility (published in the EU Official Journal as Regulation No 10 of the UN/ECE); several revisions exist, and the current revision number was not confirmed (unece.org blocked) (gated: unconfirmed, source is paywalled or blocked). Confirm the revision applicable in your market and the component approval options.

## 2. Test set-up essentials
- Test plan from the OEM EMC specification: frequency ranges, limits, antenna polarisation, dwell times, operating modes that give worst case (full load, communication active, motors running).
- Ground plane, harness length and height above ground, artificial networks (LISN, HV-AN) and load simulators per standard figures; cable routing and shielding must replicate vehicle practice.
- Functional performance status criteria for immunity tests (what must continue working).

## 3. Pre-compliance
Near-field probes, LISN and spectrum analyser in the lab, on every prototype; scan switching converters, motor drives and clocks; find sources before the formal test. Check harness and shielding concepts early.

## 4. Typical fixes
Filtering at power entry (common mode chokes, X/Y capacitors), spread-spectrum clocking, slower switching edges (gate resistors, snubbers) trading efficiency, layout (return paths, ground planes, short loops), shield termination 360 degrees, ferrites, changing PWM frequencies away from sensitive bands, shielded connectors.

## 5. Special topics
EV: inverter switching harmonics and charger noise (including emissions during charging, tested to separate standards), HV cable shielding, isolated DC-DC. Wireless charging and radar have separate rules.

## Verify
- [ ] Applicable standards, editions and limits chosen and recorded.
- [ ] Worst-case operating modes defined and tested.
- [ ] Pre-compliance scans on each design iteration.
- [ ] Fix measures verified for side effects (efficiency, thermal, cost).
