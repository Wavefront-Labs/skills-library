---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.hounsfield-calibration
name: hounsfield-calibration
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [hounsfield-units, ct-reconstruction, filtered-backprojection, ct-number, ct-calibration, water-calibration, electron-density-curve, ct-qc]
level: practitioner
status: gated
description: "Calibrate and QC CT numbers: Hounsfield definition, air and water checks and tolerances, kVp dependence, density phantom curves for radiotherapy and bone density."
sources: ["Bushberg et al., The Essential Physics of Medical Imaging (CT chapter)", "AAPM Report 39 Specification and acceptance testing of computed tomography scanners (and later AAPM CT QC reports; confirm current)", "ACR CT QC requirements https://accreditationsupport.acr.org/support/solutions/articles/11000056188-quality-control-ct"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Hounsfield unit calibration and QC

**Goal:** CT numbers that are accurate and stable, so that tissue measurements and treatment planning are reliable.

## Definition
HU = 1000 x (mu - mu_water) / mu_water. By definition water is 0 and air is about -1000. Typical values: fat about -100, soft tissue 20-60, cortical bone several hundred to over 1000 (depends on kVp).

## Routine QC
1. **Water calibration (air and water):** scan a uniform water phantom (daily or per the manufacturer protocol) to adjust detector gains and set water to zero HU.
2. **Verification:** measure mean HU of water at the centre; common tolerances are within about plus or minus 4 to 5 HU (the ACR water tolerance is (gated: unconfirmed, source is paywalled or blocked); confirm for your accreditation in the current ACR CT QC manual).
3. **Uniformity:** centre versus periphery ROI difference within a few HU (see beam-hardening-artifacts).
4. **Noise:** standard deviation in the water ROI compared against baseline.
5. **Linearity:** scan a phantom with inserts (air, polyethylene, acrylic, bone-equivalent, etc.) and compare to expected values at each kVp.

## kVp dependence
HU of materials with atomic number different from water (bone, iodine, calcium) change with tube voltage; water and soft tissue change little. Record calibrations for every clinical kVp.

## Applications
- **Radiotherapy planning:** build a CT-number-to-electron-density table from a tissue-equivalent phantom (inserts of known density) scanned with the same protocol as patients; confirm per kVp and for any change of scanner or protocol.
- **Quantitative bone mineral density:** include a calibration phantom with the patient scan.
- **Dosimetry and attenuation correction** (PET/CT) rely on HU to attenuation conversion.

## Verify
- [ ] Water, air and phantom insert HU recorded with dates and trends.
- [ ] Phantom scanned with the clinical reconstruction used for the calibration.
- [ ] Re-calibrate after tube replacement and major service.
