---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.dry-textile-electrodes
name: dry-textile-electrodes
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [dry-electrodes, textile-electrodes, capacitive-electrodes, wearable-ecg, skin-electrode-interface]
level: advanced
status: draft
description: "Design dry and textile biopotential electrodes: contact impedance, motion artefact, conductive materials, pressure, moisture, wash durability and input amplifier needs."
sources: ["Journal literature on dry and textile electrodes for ECG and EMG (confirm citations)", "Webster (ed.), Medical Instrumentation: Application and Design", "https://www.ieee.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Dry and textile electrodes

**Goal:** record biopotentials without gel for comfort and long wear, controlling the higher and less stable skin-electrode impedance.

## Types
- **Dry metal or conductive polymer contact electrodes:** pressed against the skin; rely on sweat or stratum corneum hydration.
- **Textile electrodes:** conductive yarn (silver-coated or stainless steel) knitted into garments.
- **Capacitive (insulated) electrodes:** no galvanic contact; couple through a dielectric layer; need very high input impedance.
- **Microneedle or comb electrodes:** penetrate the stratum corneum for stable contact in hair, with comfort and infection considerations.

## Design issues
- **Impedance** is orders of magnitude higher and variable at first; it falls as the skin hydrates. Impedance imbalance between electrodes converts common-mode interference into differential noise, so use a high-impedance, high-CMRR front end, active shielding and driven-right-leg design (see ecg-front-end-design-and-patient-isolation).
- **Motion artefact:** pressure and relative motion change the contact; use mechanical design (spring loading, elastic bands) and adaptive filters.
- **Wash durability and ageing** of conductive coatings; resistance drift.
- **Moisture and sweat** improve contact but corrode and shift offset.
- **Skin safety:** pressure, allergy and nickel exposure.

## Verify
- [ ] Impedance versus time measured on a range of subjects and skin conditions.
- [ ] Signal quality (SNR, QRS detection rate) compared to gel electrodes in motion.
- [ ] Washing or wear cycles tested.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
