---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.charge-injection-limits
name: charge-injection-limits
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [charge-injection, neurostimulation, stimulator-design, shannon-criterion, charge-density, water-window, safe-charge-injection-capacity, electrode-materials]
level: advanced
status: gated
description: "Set safe stimulation charge limits: Shannon criterion, charge density per phase, water window, electrode materials and charge injection capacity, with testing methods."
sources: ["Shannon, A model of safe levels for electrical stimulation (IEEE Trans Biomed Eng 1992)", "Cogan, Neural stimulation and recording electrodes (Annu Rev Biomed Eng 2008)", "McCreery et al., Charge density and charge per phase as cofactors in neural injury induced by electrical stimulation (IEEE Trans Biomed Eng 1990)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Charge injection limits

**Goal:** keep stimulation below levels that damage tissue or the electrode.

Safety-critical; limits depend on electrode, tissue and waveform, and must be justified in a risk file. Values below are literature guides, not design limits. Every figure in this skill (Shannon k, 30 uC/cm2, water window, CIC values other than IrOx) is (gated: unconfirmed, source is paywalled or blocked); the IrOx range 1-5 mC/cm2 is cited for sputtered iridium oxide films in the open-access PMC8293704.

## Tissue damage: the Shannon criterion
log10(D) = k - log10(Q), where D is charge density (microcoulombs per cm2 per phase), Q charge per phase (microcoulombs) and k a constant. Stimulation at k of about 1.5-2 or below is considered to be at lower risk for chronic cortical stimulation with the data available. This relationship was derived from limited animal data; it does not account for pulse frequency or long-term chronic effects, and is a screening guide.
A common conservative charge density guideline for surface cortical Pt electrodes is about 30 microcoulombs per cm2 per phase (from McCreery and others), with many devices operating below this.

## Electrode damage: the water window
Safe operation keeps electrode potential within the **water window** (about -0.6 V to +0.8 V versus Ag/AgCl for Pt in saline) so that hydrolysis and irreversible reactions are limited.
- **Charge injection capacity (CIC)** = the charge density that drives the electrode to the water-window limits, measured with cyclic voltammetry and voltage transients.
- Typical CIC values (approximate; check measured data): smooth Pt 0.05-0.15 mC/cm2; TiN about 1 mC/cm2; iridium oxide (sputtered or activated) about 1-5 mC/cm2; conductive polymers like PEDOT:PSS a few mC/cm2.

## Procedure
1. Choose electrode material and geometric area from the target charge per phase.
2. Measure CV (charge storage capacity) and voltage transients in saline at 37 C with the intended waveform (pulse width, interphase gap) and compute the maximum polarisation without exceeding the water window.
3. Set maximum charge density below the CIC with a safety margin (commonly 50% or less) and below tissue limits.
4. Verify long term with accelerated pulsing tests (for example 10^8-10^9 pulses) and monitor impedance and CIC drift.
5. Include the electrode area as the **geometric** area and note that current density is non-uniform (higher at edges), which raises local density above the average.

## Verify
- [ ] Voltage transient shows the electrode stays inside the water window with margin.
- [ ] Charge density per phase and charge per phase computed and below limits.
- [ ] Post-pulsing electrode checked by SEM and impedance.
