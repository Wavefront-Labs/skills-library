---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.eeg-impedance-checking
name: eeg-impedance-checking
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [eeg-impedance, electrode-impedance, impedance-check, scalp-preparation, contact-quality]
level: practitioner
status: gated
description: "Check and manage EEG electrode impedance: acceptance limits, measurement frequency and current, skin preparation, high-impedance amplifier tolerance and documentation."
sources: ["IFCN, Recommended standards for EEG recording (confirm current guidance)", "Amplifier manufacturer impedance specifications (confirm for your system)", "https://www.ifcn.info"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# EEG impedance checking

**Goal:** confirm electrode contact is good enough that noise and mains pickup are acceptable.

## Practice
- Classic clinical practice keeps electrode impedances below about 5 kilohms (gated: unconfirmed, source is paywalled or blocked) and similar across electrodes; modern amplifiers with very high input impedance tolerate much higher values (tens of kilohms) with proper shielding, so follow the amplifier maker's guidance and your protocol. Confirm the numbers in current guidelines.
- **Measurement:** the system injects a small known AC current (commonly in the 10 to 30 Hz range (gated: unconfirmed, source is paywalled or blocked), or higher frequency for some systems, at microamp level well within patient-leakage limits) and reads the voltage, so the result is impedance at that frequency and does not equal DC resistance. Avoid DC measurement that polarises electrodes.
- **Skin preparation:** part hair, light abrasion and cleaning reduce stratum corneum resistance; conductive paste or gel fills the gap.
- **Imbalance** between electrodes converts common-mode mains into differential noise, so matching matters as much as low values.
- **Re-check** after setup, during long recordings and after movement; record values for the file.

## Dry and active electrodes
- Active electrodes have a buffer at the electrode and are less sensitive to impedance; follow vendor limits.

## Verify
- [ ] Impedance map recorded at start and end.
- [ ] Out-of-range electrodes corrected or documented.
- [ ] Mains noise level acceptable after hookup.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
