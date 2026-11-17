---
id: engineering-technology.biomedical-engineering.device-verification-validation.vdmax-dose-setting
name: vdmax-dose-setting
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [vdmax, sterilization-validation, sal, iso-11137-2, gamma-sterilization, electron-beam, dose-audit, verification-dose]
level: advanced
status: gated
description: "Substantiate a radiation sterilisation dose with ISO 11137-2 Method VDmax: bioburden determination, verification dose experiment, acceptance criterion and quarterly dose audits."
sources: ["ISO 11137-1 Sterilization of health care products - Radiation - Requirements for development validation and routine control of a sterilization process for medical devices (confirm edition and amendments)", "ISO 11137-2 Establishing the sterilization dose (confirm edition)", "ISO 13004:2022 Substantiation of selected sterilization dose: Method VDmaxSD (replaces the earlier ISO/TS; for 30, 32.5, 35 kGy; https://www.iso.org/standard/82297.html)", "ISO 11137-2:2013 (+Amd 1:2022; DIS revision in progress) https://www.iso.org/standard/62442.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Radiation dose setting by Method VDmax

**Goal:** show that a chosen dose (for example 25 kGy, with variants such as 15 kGy) delivers a sterility assurance level of 10^-6 for the product's bioburden.

Method VDmax25 and VDmax15 (25 and 15 kGy) are in ISO 11137-2; ISO 13004 covers the higher VDmaxSD doses. Numbers below (10 samples, 1000 CFU, 10 units, 1 of 10 positive, quarterly audit) (gated: unconfirmed, source is paywalled or blocked).

Regulated sterilisation validation; use an accredited laboratory and the current edition of ISO 11137-1 and -2. The steps below are an outline.

## Preconditions
- Product family defined, with consistent materials and bioburden (see bioburden-testing).
- Maximum acceptable dose set by materials compatibility (see radiation-sterilization-materials).
- Radiation source qualified (installation, operational and performance qualification, including dose mapping to find minimum and maximum dose zones).

## Outline of VDmax (for dose 25 kGy or other VDmax doses)
1. **Bioburden:** determine the average bioburden on product from at least 10 samples (three batches, with timing as the standard specifies; confirm) and apply the correction for recovery efficiency.
2. **Check the bioburden limit** for the chosen method (for example the method for 25 kGy applies at average bioburden up to 1000 CFU; other VDmax doses have lower limits).
3. **Verification dose:** from the standard's table, read the dose that gives a sterility assurance level of 10^-1 for the measured average bioburden (the table is built from bioburden resistance distributions).
4. **Verification dose experiment:** irradiate **10 product units** at the verification dose (within a tolerance, using dose mapping to apply to the minimum-dose zone), then test each for sterility (ISO 11737-2) with growth promotion and controls.
5. **Acceptance:** the experiment is accepted if no more than 1 of 10 tests is positive; the standard defines how results with more than one positive are handled (follow it), and failure leads to an alternative dose-setting method or a higher dose.
6. **Substantiate the dose** (for example 25 kGy) from VDmax tables once accepted.

## Routine control
- **Dose audit** (periodic, commonly quarterly) repeats bioburden and the verification dose experiment to confirm the dose remains valid.
- Routine dosimetry on each load and monitoring that the minimum dose is met and the maximum dose is not exceeded.
- Revalidate after changes to product, materials, manufacturing, or bioburden trends.

## Gotchas
- Changing bioburden (new supplier or process) invalidates the table assumption.
- Non-representative samples (different product family).
- Using the experimental dose on the product outside dose mapping tolerance.

## Verify
- [ ] Bioburden data, verification dose and results documented.
- [ ] Dose audit schedule and results trended.
- [ ] Maximum dose compatible with product performance after irradiation and ageing.
