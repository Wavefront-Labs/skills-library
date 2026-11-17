---
id: engineering-technology.biomedical-engineering.biomaterials.cyclic-polarization-astm-f2129
name: cyclic-polarization-astm-f2129
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [cyclic-polarization, implant-corrosion, fretting-corrosion, astm-f2129, breakdown-potential, repassivation-potential, pitting-corrosion, nitinol-corrosion]
level: advanced
status: draft
description: "Run ASTM F2129 cyclic potentiodynamic polarisation on implants: cell setup, deaeration, scan rate, breakdown and repassivation potentials, acceptance practice and pitfalls."
sources: ["ASTM F2129 Standard test method for conducting cyclic potentiodynamic polarization measurements to determine the corrosion susceptibility of small implant devices (confirm current edition)", "ASTM G5 and G61 (potentiostatic and cyclic polarisation reference methods)", "FDA guidance on non-clinical engineering tests and recommended labelling for intravascular stents (corrosion section; confirm)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# ASTM F2129 cyclic polarisation

**Goal:** assess the susceptibility of an implant device to pitting and crevice corrosion by finding its breakdown potential.

## Setup
- Electrochemical cell with the device as the working electrode, a platinum or graphite counter electrode and a reference electrode (saturated calomel or Ag/AgCl; state which).
- Electrolyte: deaerated 0.9% sodium chloride solution or phosphate-buffered saline (per standard) at 37 C.
- Test the **finished device** (after sterilisation, passivation and any heat treatment), mounted so crevices are not introduced by the fixture, with exposed area known.

## Procedure (outline)
1. Purge the electrolyte with nitrogen for at least 30 minutes before and during the test.
2. Monitor open-circuit potential (OCP) for about an hour until stable.
3. Scan the potential from slightly below OCP in the anodic direction at the specified slow scan rate (about 0.167 mV/s) until the current density reaches a defined limit (for example 1 mA/cm2), then reverse the scan.
4. Record the **breakdown potential Eb** (potential at which current rises sharply) and the **repassivation (protection) potential Er** (where the reverse scan returns to the passive current).
5. Repeat on multiple samples (typically 3-6).

## Interpretation
- A device is resistant to pitting if Eb is well above the potentials expected in vivo and Er is above OCP. Commonly cited acceptance practice for nitinol stents is a breakdown potential of at least roughly 600 mV versus SCE with Er above OCP, but the numbers must be justified for the device and regulatory context; confirm current guidance.
- Compare results with controls of the same material in a known good condition.

## Pitfalls
- Crevices at mounting leads cause early breakdown unrelated to the device.
- Scan rate and solution deaeration changes results; follow the standard.
- Surface condition (oxide, passivation) dominates; test the final surface.
- Cyclic polarisation does not capture fretting or galvanic corrosion (see galvanic-corrosion and taper-corrosion).

## Verify
- [ ] OCP stable and recorded; blank and control runs acceptable.
- [ ] Eb and Er reported for each sample with potential reference stated.
- [ ] Post-test visual or SEM confirmation of pitting site.
