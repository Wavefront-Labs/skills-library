---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.radiation-shielding
name: radiation-shielding
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [radiation-shielding, shielding-design, ncrp-147, barrier-thickness, workload]
level: advanced
status: gated
description: "Understand shielding design for diagnostic imaging rooms: workload, use and occupancy factors, design goals, barrier thickness, secondary barriers, qualified-expert review."
sources: ["NCRP Report 147 Structural Shielding Design for Medical X-Ray Imaging Facilities (confirm current status)", "National and regional radiation protection regulations (confirm for your jurisdiction)", "https://www.ncrponline.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Radiation shielding design

**Goal:** set barrier materials and thickness so doses to staff and the public stay below design goals. The design and its verification are carried out by a qualified expert (medical physicist or radiation protection expert).

## Method (summary)
1. **Shielding design goals (P):** weekly or annual dose targets for controlled areas (staff) and uncontrolled areas (public); NCRP 147 sets P as air kerma of 0.1 mGy per week (5 mGy per year) for controlled and 0.02 mGy per week (1 mGy per year) for uncontrolled areas, tied to 5 and 1 mSv annual limits (from search of NCRP/AAPM material, report text itself paywalled (gated: unconfirmed, source is paywalled or blocked)); some state rules write the same numbers as mSv. In US federal rules, 10 CFR 20.1301(a) limits public dose to 1 mSv (0.1 rem) per year and 0.02 mSv (0.002 rem) in any one hour in unrestricted areas (fetched, eCFR).
2. **Workload (W):** the amount of radiation produced per week for the room (for example mA minutes per week for radiography, or dose-length product for CT), from the practice's data or published surveys.
3. **Use factor (U):** fraction of time the beam points at the barrier (primary barriers); **occupancy factor (T):** fraction of time an area is occupied; **distance (d)** from the source.
4. Required transmission B is about P times d squared divided by (W times U times T) (with the proper kerma units; standard form (gated: unconfirmed, source is paywalled or blocked)); thickness comes from transmission curves for lead, concrete or steel at the relevant tube potential.
5. **Secondary barriers** handle scatter and leakage radiation; CT rooms are mostly secondary shielding with scatter from the isocentre.
6. Include doors, windows, penetrations and floors and ceilings.
7. Verify after construction by survey meter measurements and inspection for gaps.

## Verify
- [ ] Design report with assumptions (W, U, T, kVp) and regulatory sign-off.
- [ ] Construction inspection of lead continuity at joints and penetrations.
- [ ] Post-install survey with documented results.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
