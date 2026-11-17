---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.imaging-acceptance-testing
name: imaging-acceptance-testing
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [acceptance-testing, imaging-qa, commissioning, baseline-testing, medical-physics]
level: practitioner
status: draft
description: "Plan acceptance testing and baselines for imaging systems: scope, specification-based tests, tolerances, qualified personnel, documentation and link to routine QC."
sources: ["AAPM task group and report series on acceptance testing and QC (confirm applicable reports for the modality)", "IEC 61223 series Evaluation and routine testing in medical imaging departments (confirm applicable parts)", "https://www.aapm.org"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Acceptance testing

**Goal:** confirm that a delivered system meets its contract specification and establish baselines for later quality control. Performed by a qualified medical physicist or equivalent.

## Process
1. Before delivery: site readiness (shielding, power, room), specification and test list agreed with the vendor.
2. **Acceptance tests** check specified performance (dose, image quality, resolution, uniformity, geometric accuracy, safety interlocks) against the contract and applicable standards. Tolerances come from the specification, vendor, and professional reports.
3. **Baseline:** record initial values for each routine QC metric with the same phantoms and settings so drift is detectable.
4. **Safety checks:** radiation leakage, interlocks, emergency stops, labelling and documentation (see radiation-shielding).
5. **Report** and sign-off; list deviations and resolution before clinical use.
6. **Routine QC:** schedule tests (daily, monthly, annual) with tolerance and action levels; keep trend charts.

## Practice
- Use calibrated instruments; record versions of software and protocols.
- Re-test after major repair, upgrade or relocation.
- Regulatory requirements for acceptance and QC differ by jurisdiction; confirm for yours.

## Verify
- [ ] Test report signed by qualified person; deviations closed.
- [ ] Baseline values stored and tied to routine QC.
- [ ] Calibration certificates for test equipment on file.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
