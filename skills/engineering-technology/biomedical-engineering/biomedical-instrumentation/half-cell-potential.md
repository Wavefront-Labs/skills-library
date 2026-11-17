---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.half-cell-potential
name: half-cell-potential
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [half-cell-potential, electrode-offset, polarization, dc-offset, electrode-potential]
level: practitioner
status: draft
description: "Understand half-cell potential and electrode offset in biopotential measurement: dissimilar metals, polarisable versus non-polarisable electrodes, drift and amplifier design."
sources: ["Webster (ed.), Medical Instrumentation: Application and Design (biopotential electrodes chapter)", "Neuman, in Bronzino (ed.), The Biomedical Engineering Handbook (electrodes chapter; confirm)", "https://www.ieee.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Half-cell potential and offset

**Goal:** predict electrode DC offsets, and design amplifier inputs that tolerate them.

## Concepts
- A metal in an electrolyte develops a **half-cell potential** set by its redox reaction; for common electrode metals it ranges from tens of mV (Ag/AgCl) to hundreds of mV (stainless steel, gold).
- A measurement uses two electrodes: the **offset voltage** is the difference of the half-cell potentials plus any skin potential difference; it appears as DC at the amplifier input.
- **Non-polarizable (Ag/AgCl)** electrodes pass current by a reversible reaction and have stable low offset. **Polarizable (platinum, stainless steel)** electrodes behave like a capacitor at the interface; their offset drifts and noise is higher, but they are robust and used in dry electrodes.
- Offset varies with temperature, current history and chloride concentration, so it drifts for minutes after application.

## Design implications
1. Use the same electrode material and lot in a pair to cancel offset.
2. AC-couple or use a DC servo or high-pass in the front end; keep gain stages from saturating on offset (typical front ends tolerate hundreds of mV; verify for dry electrodes).
3. Provide a bias current path for amplifier inputs (a leaky path to ground) to avoid drifting to the rail.
4. For ECG diagnostics, high-pass cutoff (for example 0.05 Hz in diagnostic mode) affects ST measurement, so offset removal must preserve ST accuracy (see baseline-wander-removal).
5. Limit DC current through electrodes to avoid polarisation and skin damage (patient currents are limited in the safety standard).

## Verify
- [ ] Measured pair offset against specification across lots.
- [ ] Settling time after application characterised.
- [ ] Amplifier input range margin verified at worst offset.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
