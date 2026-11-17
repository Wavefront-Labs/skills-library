---
id: engineering-technology.biomedical-engineering.device-verification-validation.gspr-checklist
name: gspr-checklist
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [gspr, technical-documentation, standards-conformity, annex-i, general-safety-and-performance-requirements, compliance-matrix, mdr]
level: practitioner
status: verified
description: "Build the EU MDR general safety and performance requirements checklist: Annex I structure, applicability, method of compliance, standards and evidence references."
sources: ["Regulation (EU) 2017/745 Annex I General safety and performance requirements and Annex II technical documentation (confirm current consolidated text)", "MDCG guidance documents on technical documentation (current list at the European Commission health website)", "EN ISO 14971 and harmonised standards lists (confirm current OJEU citations)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# GSPR checklist (EU MDR Annex I)

**Goal:** show requirement by requirement how the device meets the general safety and performance requirements, with traceable evidence.

Regulatory document; confirm the current MDR text and the notified body's expectations for format.

## Structure of Annex I
- **Chapter I General requirements** (requirements 1 to 9): performance as intended, risk management, benefit-risk acceptability, lifetime, transport and storage, side effects and benefit-risk, and so on.
- **Chapter II Requirements regarding design and manufacture** (10 to 22; headings from the EUR-Lex text of Regulation 2017/745): chemical, physical and biological properties (10), infection and microbial contamination (11), devices incorporating a medicinal substance or composed of absorbed substances (12), devices incorporating materials of biological origin (13), construction and interaction with the environment (14), diagnostic or measuring function (15), protection against radiation (16), electronic programmable systems and software (17), active devices and devices connected to them (18), particular requirements for active implantable devices (19), protection against mechanical and thermal risks (20), risks from devices supplying energy or substances (21), devices for lay persons (22).
- **Chapter III Requirements regarding information supplied with the device** (23: Label and instructions for use): labels, instructions for use, implant cards and so on.
Check the exact numbering and sub-clauses in the current text.

## How to build it
1. Create a table with one row per requirement and sub-requirement.
2. **Applicable?** yes or no, with a justification when not applicable (for example no energy supply).
3. **Method of compliance:** harmonised standards, common specifications, other solutions (test, analysis, clinical data).
4. **Evidence:** a document reference (report number, version), not a vague statement; for standards give the edition and clauses used.
5. **Status** (complete, partial, open) and owner.
6. Link to the risk file for risk-related requirements, to the clinical evaluation for the benefit-risk statements and to usability, software and cybersecurity files.
7. Maintain through the lifecycle with design changes and new standards editions.

## Gotchas
- "See technical file" without specific evidence.
- Using standards not on the harmonised list without a justification of equivalence.
- Missing requirements triggered by features (software, sterile, measuring function).

## Verify
- [ ] Every row has applicability, method and evidence.
- [ ] Standards editions match the declaration of conformity.
- [ ] Notified body queries are tracked to updates in the checklist.
