---
id: engineering-technology.biomedical-engineering.device-verification-validation.iso-11607-validation
name: iso-11607-validation
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [iso-11607, packaging-validation, sterile-barrier-validation, forming-sealing-assembly, package-integrity]
level: practitioner
status: gated
description: "Validate sterile barrier packaging per ISO 11607-1 and -2: material qualification, process IQ OQ PQ for forming and sealing, integrity tests, stability and records."
sources: ["ISO 11607-1 Packaging for terminally sterilized medical devices - Requirements for materials, sterile barrier systems and packaging systems (confirm edition)", "ISO 11607-2 Validation requirements for forming, sealing and assembly processes (confirm edition)", "https://www.iso.org/standard/70799.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ISO 11607 package validation

**Goal:** show the sterile barrier system maintains sterility to point of use, and that the sealing process is validated.

Edition and clause content of ISO 11607-1/-2 (gated: unconfirmed, source is paywalled or blocked); confirm in the current text.

## Part 1: design and qualification of the packaging system
- Select materials and design the sterile barrier system and protective packaging; evaluate compatibility with the sterilisation process, device and labelling.
- **Performance testing** after sterilisation and distribution simulation (see distribution-testing), and **stability testing** (aged real-time and accelerated; see accelerated-aging-astm-f1980) to support the shelf life.
- **Test methods** for integrity (dye penetration, bubble emission, vacuum decay), seal strength and visual inspection; validate the methods (see tmv-procedure).

## Part 2: process validation
1. **IQ:** installation of forming, sealing or assembly equipment with calibrated critical parameters (temperature, pressure, dwell time for heat sealing).
2. **OQ:** challenge the operating window: low and high limits for parameters, show seal quality across the range; establish process parameters.
3. **PQ:** production runs under normal conditions, repeatability and the capability of seal strength; check each lot.
4. **Ongoing control:** periodic revalidation, process monitoring, change control, and operator training; calibrate equipment.

## Traps
- Validating the package but not the sealer, or the reverse.
- Testing only new packages and not aged ones.
- Changing material suppliers without requalification.

## Verify
- [ ] Package qualification report covers sterilisation, distribution and aging.
- [ ] Sealing process IQ OQ PQ reports available.
- [ ] Routine controls (parameter monitoring, seal tests) defined and recorded.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
