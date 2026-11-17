---
id: engineering-technology.biomedical-engineering.medical-device-design.implantable-battery-selection
name: implantable-battery-selection
category: engineering-technology
field: biomedical-engineering
product: medical-device-design
tags: [implantable-battery, aimd, battery-chemistry, rechargeable-implant, elective-replacement]
level: advanced
status: gated
description: "Select the power source for an active implant: primary lithium chemistries versus rechargeable cells, capacity budgeting, depletion indicators and safety."
sources: ["ISO 14708-1 Implants for surgery - Active implantable medical devices - General requirements (confirm edition)", "Manufacturer and review literature on implantable battery chemistry", "https://www.iso.org"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Implantable battery selection

**Goal:** enough energy for the target service life with a predictable end-of-life, and no battery hazard to the patient.

## Chemistry choices
- Chemistry and application claims in this list are textbook, not confirmed (gated: unconfirmed, source is paywalled or blocked).
- **Lithium-iodine** (historic pacemaker standard), **lithium-manganese dioxide, lithium-carbon monofluoride and lithium silver vanadium oxide** (high-rate for defibrillators): primary cells with low self-discharge and predictable depletion curves.
- **Rechargeable lithium-ion type cells:** used in higher-power neurostimulators; add charging electronics, thermal limits during charge and cycle-life fade.
- Wireless power can replace or supplement the cell (see implant-telemetry-wireless-power).

## Sizing
1. Build a power budget by mode: sensing, stimulation (pulse amplitude, width, rate, load impedance), telemetry, standby.
2. Add self-discharge, a margin for therapy changes and the capacity not usable below cutoff voltage.
3. Define indicators: elective replacement and end-of-service thresholds with device behaviour at each.
4. Account for ageing, temperature (body about 37 C) and voltage droop at high-pulse loads (internal impedance).

## Safety
- Hermetic case and feedthrough integrity (see hermetic-feedthrough-packaging); short-circuit and overdischarge protection; qualification and shipping rules for lithium cells.

## Verify
- [ ] Longevity predicted from measured current by mode, with margin.
- [ ] Depletion behaviour verified on accelerated discharge.
- [ ] Failure analysis plan for premature depletion.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
