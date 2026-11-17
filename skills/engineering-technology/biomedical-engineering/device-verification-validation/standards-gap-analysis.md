---
id: engineering-technology.biomedical-engineering.device-verification-validation.standards-gap-analysis
name: standards-gap-analysis
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [standards-gap-analysis, technical-documentation, standards-conformity, harmonized-standards, recognized-consensus-standards, declaration-of-conformity, transition-period]
level: practitioner
status: gated
description: "Identify applicable standards for a device and run a gap analysis: product traits, recognised or harmonised lists, edition checks, transitions and conformity evidence."
sources: ["FDA Recognized Consensus Standards database (current at https://www.fda.gov)", "European Commission list of harmonised standards under Regulation (EU) 2017/745 (confirm current OJEU citation; see Implementing Decision (EU) 2021/1182 of 16 July 2021, OJ L 256 of 19 July 2021, confirmed on EUR-Lex as amended with a consolidated version dated 17 June 2026)", "ISO and IEC catalogues (https://www.iso.org and https://www.iec.ch)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Standards gap analysis

**Goal:** list the standards that apply to a device, confirm the edition regulators accept and show where evidence is missing.

Standards currency changes; always confirm the current edition and the recognition status in each market before relying on this list.

## Steps
1. **Characterise the device:** class, energy source (mains, battery), patient contact (applied parts), software, wireless, sterile, implant, home use, MR environment, combination with drugs.
2. **Choose families:**
   - Horizontal: ISO 13485 (QMS), ISO 14971 (risk), IEC 62366-1 (usability), ISO 15223-1 (symbols), ISO 20417 (information supplied (gated: unconfirmed, source is paywalled or blocked)), ISO 10993 series (biological), ISO 11607 and sterilisation standards.
   - Electrical: IEC 60601-1 plus collaterals (1-2 EMC, 1-6 usability, 1-8 alarms, 1-11 home) and particular standards (60601-2-xx or ISO 80601-2-xx).
   - Software: IEC 62304, IEC 82304-1 for health software, IEC 81001-5-1 security (gated: unconfirmed, source is paywalled or blocked).
   - Product-specific: for example ISO 14708 for active implants, ISO 7206 for hip stems (gated: unconfirmed, source is paywalled or blocked).
3. **Check recognition:** the FDA Recognized Consensus Standards database for the US (a declaration of conformity to a recognised standard can be used); the OJEU harmonised list for the EU, since only harmonised standards give a presumption of conformity under the MDR.
4. **Check edition and transition dates:** note when the previous edition stops being accepted.
5. **Build the matrix:** standard, edition, clauses applicable, evidence (test report, analysis, certificate), status (complete, partial, missing), owner and date.
6. **Plan the gaps:** testing, design changes or rationale for non-applicability, with justification for deviations.
7. **Maintain:** review the list at design reviews and on a schedule (for example annually), plus when a new edition is published.

## Gotchas
- Using an edition that is no longer accepted.
- Citing a standard for a feature the device does not have, and ignoring one it does.
- Treating test reports as valid after a design change.

## Verify
- [ ] Each standard in the matrix has edition, date and recognition status checked.
- [ ] Every gap has an owner and date.
- [ ] Declarations of conformity reference the correct editions.
