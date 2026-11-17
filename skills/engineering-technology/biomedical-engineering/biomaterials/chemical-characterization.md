---
id: engineering-technology.biomedical-engineering.biomaterials.chemical-characterization
name: chemical-characterization
category: engineering-technology
field: biomedical-engineering
product: biomaterials
tags: [chemical-characterization, foreign-body-response, protein-adsorption, host-response, iso-10993-18, analytical-evaluation-threshold, extractables, toxicological-risk-assessment, gc-ms]
level: advanced
status: verified
description: "Plan ISO 10993-18 chemical characterisation: extraction design, analytical methods, analytical evaluation threshold, uncertainty factors and link to toxicological risk assessment."
sources: ["ISO 10993-18 Biological evaluation of medical devices - Chemical characterization of medical device materials within a risk management process (confirm edition and amendment)", "ISO 10993-17 Toxicological risk assessment of medical device constituents", "ISO 10993-12 Sample preparation and reference materials (extraction conditions)", "ICH M7(R2) Assessment and control of DNA reactive (mutagenic) impurities (source of the 1.5 microgram per day TTC; https://database.ich.org)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Chemical characterisation (ISO 10993-18)

**Goal:** identify and quantify what can leach from a device so a toxicologist can judge the risk, sometimes replacing animal testing.

Biological evaluation planning and toxicological conclusions require qualified toxicologists; confirm current editions and regulator expectations (FDA and EU).

## Steps
1. **Gather material information:** formulation, suppliers' data, processing aids, sterilisation, manufacturing residues (mould release, cleaning agents). Consider the full list of constituents; use supplier disclosure agreements.
2. **Define the contact:** type (surface, externally communicating, implant), duration and tissue.
3. **Design extraction:** exhaustive, simulated-use or exaggerated extraction; solvents with a range of polarity (for example water or saline, ethanol or isopropanol mixtures, hexane or other non-polar), conditions that exceed clinical exposure (typical examples are 50 C for 72 h or 70 C for 24 h (gated: unconfirmed, source is paywalled or blocked); take the conditions and surface area to volume ratios from ISO 10993-12 and -18). Use the final sterilised device.
4. **Analytical methods** for broad screening:
   - GC-MS for volatile and semi-volatile organics.
   - LC-MS (high resolution) for non-volatile organics.
   - ICP-MS or ICP-OES for elements (metals).
   - Supplementary methods (FTIR, NVR) as appropriate.
5. **Set the analytical evaluation threshold (AET):** the concentration above which an extractable must be identified and quantified, derived from the dose-based threshold (for example the threshold of toxicological concern, 1.5 micrograms per day for lifetime exposure as used in ICH M7, with scaling by exposure duration and uncertainty factors) and the extraction volume and device dosing; use method uncertainty factor to adjust.
6. **Identify and quantify** compounds above the AET with standards or surrogates; report unknowns.
7. **Toxicological risk assessment** (ISO 10993-17): compare estimated exposure with tolerable intake for each compound (including cumulative effects).

## Pitfalls
- Method sensitivity above the required AET.
- Missing extractables classes (volatile or inorganic) if one method only.
- Not repeating after material or process changes.

## Verify
- [ ] Extraction conditions and AET calculation documented and justified.
- [ ] Method validation (limits of detection and quantification) reported.
- [ ] Toxicologist's report concludes on each compound.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
