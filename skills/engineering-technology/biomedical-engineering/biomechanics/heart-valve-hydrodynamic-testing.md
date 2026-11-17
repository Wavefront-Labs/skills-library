---
id: engineering-technology.biomedical-engineering.biomechanics.heart-valve-hydrodynamic-testing
name: heart-valve-hydrodynamic-testing
category: engineering-technology
field: biomedical-engineering
product: biomechanics
tags: [heart-valve-testing, pulse-duplicator, effective-orifice-area, regurgitation, iso-5840]
level: advanced
status: gated
description: "Test prosthetic heart valves in a pulse duplicator: steady and pulsatile flow, effective orifice area, regurgitant fraction, setup and accelerated wear context."
sources: ["ISO 5840-1:2021 General requirements (https://www.iso.org/standard/77033.html)", "ISO 5840-2:2021 Surgically implanted heart valve substitutes (https://www.iso.org/standard/77034.html)", "ISO 5840-3:2021 Transcatheter heart valve substitutes (https://www.iso.org/standard/67606.html)", "FDA guidance on heart valve submissions (confirm current version)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Heart valve hydrodynamic testing

**Goal:** measure valve opening performance and leakage under physiological pulsatile conditions and report them comparably.

## Setup
- **Pulse duplicator:** a pump generates ventricular flow, with a compliance and resistance (Windkessel, see windkessel-models) giving aortic pressure; the test valve is mounted in an annulus with test fluid (saline typically), at room or body temperature as specified; pressures upstream and downstream and flow rate recorded.
- **Conditions:** heart rate (for example 70 beats per minute), cardiac output ranges, mean aortic pressure about 100 mmHg, and additional stress conditions from the standard (values per ISO 5840 (gated: unconfirmed, source is paywalled or blocked)).

## Measures
- **Pressure drop and effective orifice area (EOA):** the formula used in the standard form is EOA = q_rms / (51.6 times the square root of (mean pressure difference / fluid density)), with q_rms in mL/s, pressure in mmHg and density in g/cm^3, giving EOA in cm^2 (formula seen in pulse-duplicator literature and patents, not the ISO text; q_rms is taken over the positive-pressure interval; confirm in your edition (gated: unconfirmed, source is paywalled or blocked)). Low-gradient valves make this formula very sensitive to test execution (Springer Cardiovasc Eng Technol 2021, doi 10.1007/s13239-021-00548-5).
- **Regurgitant fraction:** closing volume (valve closing displacement) plus leakage volume divided by forward stroke volume.
- **Steady forward flow test:** pressure drop at constant flows.
- **Other:** high-speed video of leaflet motion, closing velocities and cavitation concerns for mechanical valves, flow visualisation.
- **Minimum performance** for EOA and regurgitation is set by size and type in the standard; confirm.

## Durability
- Accelerated wear testing runs hundreds of millions of cycles (required number and conditions per the standard (gated: unconfirmed, source is paywalled or blocked)) and inspection for leaflet damage.

## Verify
- [ ] Test fluid, temperature, rate and pressure conditions recorded.
- [ ] Sensors calibrated; repeat valves tested for repeatability.
- [ ] Results compared to the minimum performance requirements and a reference valve.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
