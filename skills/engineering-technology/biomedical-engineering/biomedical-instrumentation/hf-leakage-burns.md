---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.hf-leakage-burns
name: hf-leakage-burns
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [hf-leakage, electrosurgery-burns, capacitive-coupling, hf-current, active-electrode-monitoring]
level: advanced
status: draft
description: "Prevent burns from high-frequency leakage and capacitive coupling in electrosurgery: leakage paths, insulation faults, laparoscopic coupling and active electrode monitoring."
sources: ["IEC 60601-2-2 High frequency surgical equipment and accessories (confirm edition)", "Clinical safety literature on electrosurgery burns (confirm citations)", "https://www.iec.ch"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# HF leakage and burns

**Goal:** prevent unintended heating from RF current leaving the intended path.

## Mechanisms
- **Capacitive coupling:** HF current couples across insulation (for example between the active electrode and the metal cannula of a laparoscope) into adjacent conductors and tissue; coupling rises with frequency, voltage and insulation area.
- **Direct insulation failure:** pinholes, cracks or wear in instrument insulation expose conductor to tissue.
- **Alternate pathways:** return through electrodes, supports or jewellery.
- **High-voltage modes:** coagulation waveforms have high crest voltage and increase capacitive leakage.

## Design controls
1. Insulation thickness and dielectric integrity for peak voltage; production test of instrument insulation (for example HF voltage test).
2. Leakage current measurement: HF leakage limits from the particular standard, tested to measure active electrode, return electrode and enclosures (confirm numbers).
3. **Active electrode monitoring (AEM)** systems detect insulation defects and shut down the output.
4. Use all-metal cannulas, not mixed metal-plastic, and instructions on cannula selection; limit power and voltage to what is needed.
5. Verify generator output waveform and maximum voltage against rated accessories (rated accessory voltage).

## Verify
- [ ] Insulation tested to rated accessory voltage.
- [ ] HF leakage measured under defined load and mode.
- [ ] Inspection instructions for reusable instruments in the IFU.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
