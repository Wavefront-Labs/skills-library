---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.battery-regulations-and-test-standards
name: battery-regulations-and-test-standards
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [battery-regulations, un-38-3, un-r100, gtr-20, iec-62660, iso-12405, gb-38031, regulatory-testing, battery-safety]
level: practitioner
status: gated
description: "Map the battery regulations and test standards: transport UN 38.3, UN R100 RESS, GTR 20, IEC 62660, ISO 12405, GB 38031, and what each covers; confirm editions."
sources:
  - "UN Manual of Tests and Criteria section 38.3"
  - "UN Regulation 100"
  - "UN GTR 20"
  - "https://eur-lex.europa.eu/eli/reg/2023/1542/oj/eng"
  - "IEC 62660 series"
  - "ISO 12405 series"
  - "GB 38031"
licence: Apache-2.0
version: 4
updated: 2026-11-17
aliases: []
---

# Battery regulations and test standards

This is a map for planning, not legal advice; confirm the current edition, amendments and your market with the regulator or an approved test lab.

- **UN 38.3 (UN Manual of Tests and Criteria):** transport tests for lithium cells and batteries: altitude simulation, thermal cycling, vibration, shock, external short circuit, impact/crush (cells), overcharge, forced discharge. Required to ship cells and packs (the test list here is from the UN manual (gated: unconfirmed, source is paywalled or blocked)).
- **UN Regulation No. 100 (UNECE):** safety of battery electric vehicles: part I electric power train protection (isolation, direct and indirect contact, etc.), part II RESS tests: vibration, thermal shock and cycling, mechanical shock and integrity, fire resistance, external short circuit, overcharge, over-discharge, over-temperature protection. Applies in UNECE member states.
- **UN GTR 20 (Electric Vehicle Safety):** global technical regulation covering REESS and electric power train safety, including propagation (thermal event) provisions in later phases.
- **ISO 6469 series:** safety specifications for EVs; **ISO 12405:** test specifications for lithium-ion traction battery packs and systems; **IEC 62660:** performance and abuse tests for secondary lithium cells for EVs.
- **GB 38031 (China):** safety requirements for traction batteries including thermal-propagation criteria. The 2025 revision (GB 38031-2025, in force from 1 July 2026 per trade press (gated: unconfirmed, source is paywalled or blocked); confirm the phase-in for existing type approvals in the official text) replaces the old 5-minute alarm criterion with no fire and no explosion in thermal propagation, and adds bottom-impact and post-fast-charge tests.
- **EU Batteries Regulation (EU) 2023/1542:** applies from 18 February 2024 (Article 96, fetched from EUR-Lex 32023R1542); EV, light-means-of-transport and industrial batteries above 2 kWh need a battery passport from 18 February 2027 (Article 77, fetched; threshold is capacity greater than 2 kWh for industrial batteries). Vehicle type approval under UN R100 is separate.
- **US:** FMVSS 305 (49 CFR 571.305, electric-powered vehicles: electrolyte spillage and electrical shock protection; title fetched, and note it has a successor 571.305a that a vehicle may be certified to instead); SAE J2464/J2929 are abuse testing and safety references.
- Plan: identify the markets, check which edition applies at start of production, book the lab early, and keep samples for design verification before formal tests.

**Gotchas:** test requirements are revised often; teams design to an outdated edition.

## Verify
- [ ] Applicable regulation list with edition and date per market recorded.
- [ ] Test plan assigns each regulation test to design-verification and certification phases.
