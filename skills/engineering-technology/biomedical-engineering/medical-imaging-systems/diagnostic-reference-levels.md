---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.diagnostic-reference-levels
name: diagnostic-reference-levels
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [diagnostic-reference-level, ct-dose, ctdi, drl, dose-optimization, icrp-135, dose-survey, ssde]
level: practitioner
status: verified
description: "Set and use diagnostic reference levels: quantities by modality, survey method, 75th percentile approach, local review and optimisation, and why DRLs are not dose limits."
sources: ["ICRP Publication 135 Diagnostic reference levels in medical imaging (2017) https://www.icrp.org/publication.asp?id=ICRP+Publication+135", "Council Directive 2013/59/Euratom Article 56 https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013L0059", "ACR-AAPM-SPR practice parameters and national DRL publications (confirm current national values)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Diagnostic reference levels (DRLs)

**Goal:** identify unusually high doses for a common examination so that practice can be reviewed and optimised.

## What a DRL is
A DRL is a investigation level for typical examinations of standard-sized patients. It is **not** a dose limit and not a target; exceeding it triggers a local review, and being well below it can also warrant checking image quality.

## Quantities
- **CT:** CTDIvol (mGy) and DLP (mGy cm), for standard protocols by body region (see ct-dose-and-image-quality-tradeoffs).
- **Radiography:** entrance surface air kerma (ESAK) or air kerma-area product (KAP, also called DAP).
- **Fluoroscopy and interventional:** KAP, cumulative air kerma at reference point, fluoroscopy time.
- **Mammography:** average glandular dose per image.
- **Nuclear medicine:** administered activity.

## Setting a DRL
1. **Survey** a representative sample of facilities or scanners with the same protocol and standard-sized patients (adults in a narrow weight range; paediatric by weight or age band).
2. Collect the quantity per patient or phantom, per protocol, over many examinations (ICRP 135: at least 20 patients per examination and facility, preferably 30 for CT and diagnostic fluoroscopy).
3. Use the **75th percentile** of the distribution of facility medians as the DRL (ICRP 135: national DRL values should be set as the 75th percentile of the median values from a sample of representative centres).
4. Update periodically (several years) and when technology changes.
5. National or regional DRLs exist in many countries; use the current published values for your jurisdiction. In the EU, Directive 2013/59/Euratom Article 56(2) requires Member States to establish, regularly review and use DRLs for radiodiagnostic examinations.

## Using DRLs locally
1. Compare your median to the DRL for each protocol (use patient weight or size-band data).
2. If above, review protocol settings (kVp, mA modulation, pitch, number of phases, reconstruction), clinical indication, and equipment function; adjust and re-measure.
3. Document the review and changes.
4. Maintain image quality: lower dose without damaging diagnostic performance.

## Gotchas
- Using DRLs for individual patients.
- Mixing protocols and sizes in one median.
- Dose indices that do not equal patient dose (CTDIvol is a scanner output, see ct-dose-and-image-quality-tradeoffs).

## Verify
- [ ] Local median doses calculated per protocol with a sample size of at least 20 patients (ICRP 135).
- [ ] Review documented when above the DRL.
- [ ] Records retained as required by local regulation.
