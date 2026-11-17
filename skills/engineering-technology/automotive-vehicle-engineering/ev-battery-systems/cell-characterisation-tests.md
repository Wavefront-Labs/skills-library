---
id: engineering-technology.automotive-vehicle-engineering.ev-battery-systems.cell-characterisation-tests
name: cell-characterisation-tests
category: engineering-technology
field: automotive-vehicle-engineering
product: ev-battery-systems
tags: [cell-characterisation, hppc, ocv-test, capacity-test, dcir-test, eis, cell-testing]
level: practitioner
status: draft
description: "Plan cell characterisation: capacity, OCV-SOC, HPPC pulses for resistance, temperature sweeps and EIS, with channel, thermal and data-quality practice."
sources:
  - "Plett, Battery Management Systems Vol. 1"
  - "Warner, Lithium-Ion Battery Chemistries and Pack Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Cell characterisation tests

1. Equipment: cycler with sufficient voltage/current accuracy (check the cycler specification relative to the cell's current), thermal chamber, thermocouples on cell surface, 4-wire connection.
2. **Capacity:** CC-CV charge to full, rest, discharge at a stated C-rate to cut-off; repeat at several temperatures.
3. **OCV vs SOC:** low-rate (C/25 or so) discharge and charge, or incremental steps with long rests; use the average of charge and discharge for hysteresis-free chemistries, handle hysteresis explicitly for LFP.
4. **HPPC (hybrid pulse power characterisation):** pulse charge/discharge at set SOC steps (10%) after rest; extract R0 from the instantaneous step and RC pairs from the relaxation; repeat at temperatures.
5. **Thermal:** heat generation from calorimeter or adiabatic test; heat capacity.
6. **EIS:** impedance spectra for fine ageing and model structure.
7. **Ageing:** calendar and cycle matrices, see ageing skills.
8. Quality: rest times long enough to settle, consistent preconditioning, data logging at 1-10 Hz, record the cycler offsets.

**Gotchas:** cell-to-cell variation: test several cells, report mean and spread.

## Verify
- [ ] Repeat test on one cell shows capacity within a stated tolerance.
- [ ] Parameter set validated against a drive-cycle profile not used in fitting.
