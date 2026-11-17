---
id: health-medicine.medical-genetics-and-genomics.genomic-test-interpretation.acmg-amp-variant-classification
name: acmg-amp-variant-classification
category: health-medicine
field: medical-genetics-and-genomics
product: genomic-test-interpretation
tags: [genomic-test-interpretation, medical-genetics-and-genomics, acmg-amp, variant-classification, variant-interpretation, vus, pathogenic, likely-pathogenic, gnomad, clinvar, clingen, spliceai, revel, pvs1, pm2, ps3, bayesian-points, exome-reanalysis, segregation, de-novo, hgvs-nomenclature]
level: advanced
status: gated
description: "Classifying sequence variants with ACMG/AMP: frequency, variant type and PVS1, computational and functional evidence, segregation/de novo, combining rules or Bayesian points, reanalysis."
sources: ["https://pmc.ncbi.nlm.nih.gov/articles/PMC9748256/", "https://pubmed.ncbi.nlm.nih.gov/32720330/", "https://www.clinicalgenome.org/tools/clingen-variant-classification-guidance/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ACMG/AMP variant classification

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** assign a reproducible five-tier class — pathogenic (P), likely pathogenic
(LP), uncertain significance (VUS), likely benign (LB), benign (B) — to a germline
sequence variant for a stated condition, with every evidence code justified.

Note: the ClinGen Sequence Variant Interpretation working group was retired in April 2025 and
its recommendations are consolidated on the ClinGen variant classification guidance page;
check which framework version your lab uses. The logic below follows the 2015 standard plus
ClinGen SVI refinements.

## 0. Prerequisites
- **Gene–disease validity:** is the gene definitively/strongly linked to *this*
  phenotype (ClinGen gene curation)? A variant can't be pathogenic for a disease the
  gene doesn't cause.
- Correct **HGVS** nomenclature on the MANE Select transcript; confirm zygosity and
  quality (read depth, allele fraction; Sanger/orthogonal confirmation per lab policy).
- Mechanism: loss-of-function vs gain-of-function/dominant-negative, inheritance mode.

## 1. Population frequency
- Check gnomAD (correct ancestry group, filtering allele frequency, homozygotes).
- **BA1** (stand-alone benign): allele frequency > 5% (or gene-specific lower threshold) (gated: unconfirmed, source is paywalled or blocked).
- **BS1**: frequency greater than expected for the disorder (use disease prevalence,
  penetrance and allelic heterogeneity — e.g. Whiffin/Ware calculator).
- **BS2**: observed in healthy adults (homozygous for recessive, heterozygous for
  fully penetrant dominant early-onset).
- **PM2** (absent/extremely rare): ClinGen recommends applying at **supporting**
  strength only (gated: unconfirmed, source is paywalled or blocked).

## 2. Variant type and location
- **PVS1** (null variant in a gene where LoF is the mechanism): follow the ClinGen
  PVS1 decision tree — downgrade for NMD escape (last exon / last 50 bp of
  penultimate exon (gated: unconfirmed, source is paywalled or blocked)), alternative start codons, in-frame exon skipping, exons absent
  from biologically relevant transcripts.
- **PS1/PM5**: same amino-acid change / different missense at a residue with known
  pathogenic missense.
- **PM1**: mutational hotspot or critical functional domain without benign variation.
- **PM4/BP3**: protein-length changes outside/inside repetitive regions.
- **PP2/BP1**: gene-level missense constraint patterns.

## 3. Computational evidence
- **PP3/BP4** using a single calibrated predictor rather than a vote of many: e.g.
  REVEL with ClinGen-calibrated thresholds (Pejaver et al. 2022, Table 2): PP3 supporting
  [0.644, 0.773), moderate [0.773, 0.932), strong ≥ 0.932; BP4 supporting (0.183, 0.290],
  moderate (0.016, 0.183], strong (0.003, 0.016], very strong ≤ 0.003 — check current
  calibrations. For splicing, SpliceAI (≥ 0.2 suggests possible impact) (gated: unconfirmed, source is paywalled or blocked). Don't count PP3 alongside PVS1 for the same effect.

## 4. Functional, segregation and de novo data
- **PS3/BS3**: well-established functional assays (validated with controls; ClinGen
  OddsPath framework). Patient RNA studies can confirm splicing.
- **PS2/PM6**: de novo with/without confirmed parentage, phenotype consistent.
- **PP1/BS4**: co-segregation with disease in families (strength by number of
  informative meioses); non-segregation is strong benign evidence.
- **PM3**: for recessive disorders, in trans with a pathogenic variant (phase confirmed).
- **PS4**: prevalence in affecteds significantly higher than controls.
- **PP4**: phenotype highly specific for the gene (use cautiously).

## 5. Combine
Use the 2015 combining rules (e.g. P = 1 very strong + ≥1 strong; LP = 1 strong + 1–2
moderate) or the **Bayesian points** system: supporting 1, moderate 2, strong 4, very
strong 8 (benign negative). Typical bins: ≥ 10 P, 6–9 LP, 0–5 VUS, −1 to −6 LB, ≤ −7 B (gated: unconfirmed, source is paywalled or blocked); published tables differ at the VUS/likely-benign boundary, so confirm in the paper.
Conflicting strong evidence → VUS until resolved.

## 6. Report and reanalysis
State condition, inheritance, evidence codes applied, class and recommended actions
(e.g. parental testing to establish de novo or phase). VUS should not drive clinical
management. Re-evaluate on new evidence; consider systematic exome/genome reanalysis
(interval per lab policy) — diagnostic yield rises with new gene discoveries (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Double-counting: the same observation used for PM2 and PS4, or PP3 and PVS1.
- Using the overall gnomAD frequency when a founder population inflates one ancestry.
- ClinVar assertions are evidence to check, not a classification to copy — look at the
  submitter, date and stars.
- Mosaicism and low allele fraction may indicate somatic or clonal haematopoiesis.

## Verify
- [ ] Gene–disease validity established for the patient's phenotype.
- [ ] HGVS on MANE transcript; variant quality confirmed.
- [ ] Each code applied with strength and source; no double counting.
- [ ] Class derived by rules or points, with the version cited.
- [ ] Report gives clinical actions and reanalysis plan; VUS not used for management.

## Checked

- Date checked: 2026-10-25. Jurisdiction: International germline variant interpretation (ACMG/AMP 2015, ClinGen).
- Sources read: Pejaver et al. 2022 (AJHG) via Europe PMC full text; Tavtigian 2020 abstract; ClinGen guidance page; search summaries.
- Confirmed: REVEL PP3/BP4 thresholds as published in Table 2 of Pejaver et al. 2022; the ClinGen guidance page lists PM2, PVS1 and BA1 documents; Tavtigian converts evidence strengths to additive points proportional to log odds.
- Corrected or removed: The REVEL line was wrong or muddled (">= 0.773 supporting to moderate"): supporting starts at 0.644 and 0.773 is the moderate cut-off; replaced with the published table. The unsupported "v4 in rollout" claim was replaced by the ClinGen SVI retirement notice (April 2025, seen on the ClinGen site via search).
- Gated: BA1 5%, PM2 at supporting, the NMD-escape rule, SpliceAI 0.2, the points per strength and bins (published tables differ at VUS/likely benign: Tavtigian original vs a ClinGen panel reproduction), and reanalysis interval: the original papers are paywalled and the ClinGen PDFs returned binary.

Method: documentation only; no commands were run.
