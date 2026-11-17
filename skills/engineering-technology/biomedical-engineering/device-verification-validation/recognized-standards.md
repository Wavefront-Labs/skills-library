---
id: engineering-technology.biomedical-engineering.device-verification-validation.recognized-standards
name: recognized-standards
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [recognized-standards, harmonized-standards, presumption-of-conformity, declaration-of-conformity, consensus-standards]
level: practitioner
status: gated
description: "Use recognised and harmonised standards for conformity: FDA recognised consensus standards, EU harmonised standards, declarations of conformity, edition control and transitions."
sources: ["FDA Recognized Consensus Standards database (confirm current at fda.gov)", "EU MDR Regulation 2017/745, Article 8 and harmonised standards lists in the Official Journal of the European Union (confirm current lists)", "https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfStandards/search.cfm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Recognised standards and presumption of conformity

**Goal:** pick the standards that regulators accept as demonstrating compliance, and keep the list current.

FDA recognition and declaration-of-conformity mechanics below (gated: unconfirmed, source is paywalled or blocked); MDR Article 8(1) presumption of conformity was confirmed on EUR-Lex.

## United States
- FDA publishes a database of **recognised consensus standards**. Declaring conformity to a recognised standard in a premarket submission can reduce the testing detail needed to be reviewed, using the FDA's declaration of conformity process; recognition is by edition and extent (full or partial) and may carry supplemental information; confirm the current recognition and version.

## European Union
- **Harmonised standards** referenced in the Official Journal under the MDR give a **presumption of conformity** with the general safety and performance requirements covered by the standard (MDR Article 8). Check the current list because publication lags standard editions and some standards are harmonised only partly or with annex Z-type notes; confirm whether the edition you use is cited.
- If you do not use a harmonised standard (or use a different edition), justify that your approach meets the requirements.

## Other jurisdictions
- Many accept ISO and IEC standards directly; some adopt national versions with differences (for example Japan JIS, Canada, Australia); confirm requirements in each market.

## Practice
1. Maintain a **standards register** per product: standard, edition, scope, applicability, status in each market, compliance evidence and gaps (see standards-gap-analysis).
2. Monitor new editions and amendments and transition dates; plan impact analysis and retesting.
3. Cite standards by designation and edition in the technical file and declaration of conformity.
4. Do not assume testing to a recognised standard is sufficient; the specific device risk may need additional evidence.

## Verify
- [ ] Register lists edition and regulatory recognition status per market.
- [ ] Declarations of conformity cite the right editions.
- [ ] Transition dates tracked with owners.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
