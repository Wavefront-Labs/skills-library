---
id: engineering-technology.automotive-vehicle-engineering.matlab-simulink.calibration-data-and-a2l-export
name: calibration-data-and-a2l-export
category: engineering-technology
field: automotive-vehicle-engineering
product: matlab-simulink
tags: [a2l-export, a2l, asap2, calibration, inca, canape, storage-class]
level: practitioner
status: gated
description: "Mark parameters and signals for calibration, export an ASAP2 A2L from generated code, and verify addresses against the linked ECU image."
sources:
  - "Embedded Coder: Generate ASAP2 and CDF calibration files (https://www.mathworks.com/help/ecoder/ug/asap2-cdf-calibration.html)"
  - "Embedded Coder: Configure model data elements for ASAP2 (https://www.mathworks.com/help/ecoder/ug/a2l-cal-profile.html)"
  - "ASAM standards overview (https://www.asam.net)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Calibration data and A2L export

1. Calibration parameters: define with `Simulink.Parameter`, give a non-inlined storage class (e.g. exported global or a custom class), set min/max, unit and description. Elements on the default `Auto` storage class are excluded from the A2L; a non-auto storage class is required so the generator produces an addressable variable.
2. Measurement signals: tag with a storage class so they appear as variables in memory.
3. After code generation, generate the A2L with the Generate Calibration Files tool (Embedded Coder; C Code > Share) or `coder.asap2.export`; it writes the latest supported ASAM MCD-2 MC version unless you choose another. Whether your release still generates the A2L through the `GenerateASAP2` build option (reportedly switched off from R2025a): check your release notes (gated: unconfirmed, source is paywalled or blocked).
4. Link the production image and give the A2L real addresses: pass an ELF, PDB or DWARF symbol file to the tool, or merge map-file addresses with a utility from your toolchain.
5. Open in the calibration tool (INCA or CANape), check that the image matches the A2L (checksum or version check in the calibration tool (gated: unconfirmed, source is paywalled or blocked)), and compare a few values with the model.
6. Control A2L version with the software release.

**Gotchas:** inlined parameters vanish from calibration; compiler-reordered variables if map not regenerated.

## Verify
- [ ] Calibration tool shows the correct values for several known parameters.
- [ ] A2L addresses correspond to the exact build being flashed.
