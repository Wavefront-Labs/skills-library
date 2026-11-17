---
id: health-medicine.pathology-and-laboratory-medicine.molecular-pathology.tumour-molecular-profiling-and-variant-reporting
name: tumour-molecular-profiling-and-variant-reporting
category: health-medicine
field: pathology-and-laboratory-medicine
product: molecular-pathology
tags: [molecular-pathology, pathology-and-laboratory-medicine, molecular-diagnostics, tumour-profiling, tumor-profiling, ngs, next-generation-sequencing, targeted-panel, tumour-cellularity, tumour-content, macrodissection, variant-allele-frequency, vaf, limit-of-detection, pcr, qpcr, ddpcr, fusion-detection, rna-ngs, fish, liquid-biopsy, ctdna, amp-asco-cap-tiers, variant-classification, hgvs-nomenclature, egfr, kras, braf, alk, msi, tmb, germline-findings]
level: advanced
status: draft
description: "Tumour molecular testing workflow: specimen and tumour-content assessment, choosing PCR, NGS, RNA fusion or ctDNA, quality metrics, AMP/ASCO/CAP tiering, and clear molecular reporting."
sources:
  - "Li MM et al. Standards and Guidelines for the Interpretation and Reporting of Sequence Variants in Cancer (AMP/ASCO/CAP). J Mol Diagn 2017"
  - "Jennings LJ et al. Guidelines for Validation of NGS-Based Oncology Panels (AMP/CAP). J Mol Diagn 2017"
  - "Lindeman NI et al. Updated Molecular Testing Guideline for Lung Cancer (CAP/IASLC/AMP). Arch Pathol Lab Med 2018"
  - "den Dunnen JT et al. HGVS Recommendations for the Description of Sequence Variants. Hum Mutat 2016"
  - "Mosele F et al. ESMO recommendations for the use of NGS for patients with metastatic cancers (ESCAT). Ann Oncol 2020 and updates"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Tumour molecular profiling and variant reporting

*General professional reference. Required biomarkers, approved companion diagnostics and actionability tiers change rapidly; check current guidelines (CAP/AMP, ESMO, NCCN) and regulatory labels for each tumour type.*

**Goal:** produce a molecular result an oncologist can trust and act on: the right test
for the question, on a sample good enough to answer it, with quality metrics that reveal
a false negative, and a report that says clearly what was found and what it means.

## 1. Start with the specimen
- **Pathologist review** of the H&E: confirm tumour, choose the best block, mark the area,
  and estimate **tumour cellularity** (neoplastic nuclei as % of all nuclei — not tumour area).
  Inflammation and normal tissue dilute the signal.
- **Macrodissect** to enrich tumour when cellularity is low.
- Pre-analytic factors: formalin fixation time (overfixation fragments DNA), acid
  decalcification (destroys nucleic acids — use EDTA decalcification for bone samples
  destined for molecular testing), small biopsies and cytology cell blocks (often usable — validate).
- Know the assay's **limit of detection**: a heterozygous mutation in a tumour with 20% cellularity
  has an expected VAF of ~10% — if the LoD is 5%, you are near the edge.

## 2. Choose the method for the question
| Question | Typical method |
|---|---|
| One or a few hotspots, fast | Real-time PCR, ddPCR |
| Many genes (e.g. NSCLC driver panel) | DNA **NGS** targeted panel |
| Gene fusions (ALK, ROS1, RET, NTRK, NRG1) | **RNA-based NGS** (preferred for breadth), FISH, IHC screen for some |
| Copy-number (amplifications) | NGS with CNV calling, FISH, IHC (HER2) |
| MSI / mismatch repair | MMR IHC, PCR MSI, NGS-based MSI |
| Tissue insufficient or inaccessible | **ctDNA** liquid biopsy (negative result does not exclude — low shedding) |
- Parallel tissue + plasma testing can shorten time to result in advanced lung cancer.
- Turnaround matters: guidelines aim for results within ~10 working days for actionable lung biomarkers.

## 3. Quality metrics to check on every run
DNA/RNA quantity and quality, library yield, **mean depth and % of targets above minimum
coverage**, uniformity, controls (positive, negative, no-template), sample-identity checks.
Report **regions failing coverage** — a "negative" with uncovered hotspots is not negative.

## 4. Variant interpretation
- Name variants with **HGVS** nomenclature on a stated reference transcript (e.g. MANE Select).
- Separate likely **germline** (VAF ~50% or ~100% in all samples, known germline genes)
  from somatic findings; tumour-only testing cannot prove germline origin — recommend germline
  testing and genetic counselling per local policy.
- Classify somatic variants with the **AMP/ASCO/CAP tiers**: I (strong clinical significance —
  approved therapy/guidelines), II (potential significance), III (unknown significance),
  IV (benign/likely benign). ESCAT is an alternative actionability scale in Europe.
- Use curated knowledge bases (e.g. OncoKB, CIViC, ClinVar for germline) — cite version/date.

## 5. Reporting
- Lead with a clear summary: **actionable findings first**, with the therapy implication
  per current guidance.
- Include: specimen and tumour cellularity, method and genes tested, LoD, VAF for each variant,
  coverage failures, limitations (e.g. "fusion detection by DNA panel is incomplete"),
  germline caveats, and recommendation for further testing.
- Avoid listing every VUS prominently; separate them.

## Gotchas
- Low tumour content is the commonest cause of false negatives.
- Decalcified bone samples often fail — plan the biopsy and decalcification route.
- Clonal haematopoiesis variants (e.g. *DNMT3A*, *TET2*, some *TP53*) appear in plasma ctDNA and can be mistaken for tumour variants.
- A DNA panel may miss fusions with unusual breakpoints; use RNA.

## Verify
- [ ] Pathologist-assessed tumour cellularity recorded; macrodissection done if needed.
- [ ] Method matches the clinical question; LoD stated and achievable for this sample.
- [ ] Run QC and coverage metrics passed; uncovered regions reported.
- [ ] Variants in HGVS form with tier and evidence source (version/date).
- [ ] Germline implications flagged with recommended follow-up.
- [ ] Report leads with actionable findings and states limitations.
