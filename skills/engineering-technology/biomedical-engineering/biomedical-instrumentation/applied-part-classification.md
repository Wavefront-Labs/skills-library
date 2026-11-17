---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.applied-part-classification
name: applied-part-classification
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [applied-part, electrical-safety, iec-60601-1, patient-electrical-safety, type-b, type-bf, type-cf, defibrillation-proof, medical-symbols]
level: practitioner
status: verified
description: "Classify applied parts as type B, BF or CF under IEC 60601-1: definition, contact criteria, defibrillation-proofing and consequences for design and leakage limits."
sources: ["IEC 60601-1:2005+AMD1:2012+AMD2:2020 (definitions of applied part and classification; confirm edition)", "IEC 60601-1 Annex on application of requirements to applied parts (rationale)", "Webster (ed.), Medical Instrumentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Applied part classification (B, BF, CF)

**Goal:** assign each applied part the correct protection type so leakage limits and isolation match how it touches the patient.

## Definition
An **applied part** is the part of the equipment that in normal use necessarily comes into physical contact with the patient for the equipment to perform its function (or can be brought into contact, or needs to be touched by the patient). Items like electrodes, probes, cuffs and handles may be applied parts.

## Types
- **Type B:** the basic level of protection (the applied part need not be isolated from earth). Used where there is low risk (for example some external, non-electrical contact).
- **Type BF:** floating applied part isolated from earth and from other parts; used for electrical contact with the patient's body surface or internal non-cardiac sites.
- **Type CF:** floating with the lowest leakage limits; for direct cardiac application (cardiac catheters, intracardiac leads) and other uses where very low current limits are needed.
Defibrillation-proof versions are marked with an additional symbol and must pass the defibrillation test.

## Decision
1. Does the part make electrical contact (conductive path) or is it insulated?
2. Is contact to the heart, central circulatory system or an internal path possible (including through fault)?
3. Is the applied part at risk of defibrillation in use? If yes, add defibrillation-proof requirements.
4. Check the relevant particular standard, which often fixes the type (for example ECG monitors with BF or CF depending on intended use).

## Consequences
- Isolation: F-type (BF and CF) applied parts need isolation from mains (MOPP) and from other circuit parts; see means-of-protection.
- CF applied parts have much lower patient leakage limits than B and BF, and F-types are tested with mains voltage applied to the part; confirm the exact limits in the current IEC 60601-1 (paywalled).
- Labelling: markings on the equipment, symbols in the instructions.
- Cables, accessories and connectors: type-B parts connected to a type-CF part can compromise the classification.

## Verify
- [ ] Classification rationale recorded for each applied part.
- [ ] Marking on the device matches the classification.
- [ ] Mixed systems checked (the lowest-protection connected part determines the system's patient risk).
