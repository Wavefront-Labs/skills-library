---
id: health-medicine.medical-genetics-and-genomics.clinical-genetic-diagnosis.dysmorphology-examination-and-genetics-workup
name: dysmorphology-examination-and-genetics-workup
category: health-medicine
field: medical-genetics-and-genomics
product: clinical-genetic-diagnosis
tags: [clinical-genetic-diagnosis, medical-genetics-and-genomics, dysmorphology, syndrome-recognition, three-generation-pedigree, hpo, human-phenotype-ontology, growth-parameters, chromosomal-microarray, exome-sequencing, genome-sequencing, karyotype, fragile-x, face2gene, orphanet, omim, developmental-delay, congenital-anomalies]
level: advanced
status: draft
description: "Genetics consult workup: three-generation pedigree, systematic dysmorphology exam with measurements, HPO phenotyping, and choosing first-tier tests (microarray, exome/genome, targeted)."
sources: ["Jones KL, Smith's Recognizable Patterns of Human Malformation, 8th ed.", "Manning M, Hudgins L, ACMG practice guideline: array-based technology (2010)", "Manickam K et al., ACMG guideline: exome and genome sequencing for pediatric patients with congenital anomalies or ID (2021)", "Elements of Morphology standard terminology, Am J Med Genet 2009", "Human Phenotype Ontology (hpo.jax.org)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dysmorphology examination and genetics workup

> General clinical/professional reference, not a substitute for independent clinical judgement, current guidelines, or verified dosing references.

**Goal:** turn "this child looks different and is delayed" into a structured phenotype,
a ranked differential and the single most efficient test — so the family gets a
diagnosis (or a clear "not yet") with the fewest blood draws.

## 1. History that matters
- **Pregnancy:** exposures (alcohol, valproate, isotretinoin, maternal diabetes),
  infections, scans, growth, fetal movements, polyhydramnios.
- **Birth:** gestation, weight/length/head circumference with centiles, neonatal course.
- **Development:** milestones by domain, regression (a red flag for metabolic or
  neurodegenerative disease), behaviour, seizures.
- **Three-generation pedigree** with standard symbols: consanguinity, miscarriages,
  stillbirths, early deaths, similar features, ethnicity (founder variants). Ask
  directly — families rarely volunteer consanguinity or pregnancy losses.

## 2. Systematic examination
- **Measure, don't guess:** height, weight, OFC, plus inner/outer canthal distance,
  palpebral fissure length, ear length/position, philtrum, hand/foot lengths, arm span.
  Plot on syndrome-appropriate or population charts; note proportionality
  (macro/microcephaly relative to height).
- **Head to toe in fixed order:** skull shape, hair pattern, face (forehead, eyes,
  nose, philtrum, lips, palate, jaw), ears, neck, chest, heart, abdomen, genitalia,
  spine, limbs (palmar creases, digit number/shape, nails, joint laxity/contractures),
  skin (café-au-lait macules — count and measure — hypopigmentation, haemangiomas),
  neurology.
- Distinguish **malformation** (intrinsic, e.g. cleft lip), **deformation** (external
  force, e.g. positional talipes), **disruption** (breakdown, e.g. amniotic band) and
  **sequence** (one anomaly cascading, e.g. Pierre Robin) — they imply different
  recurrence risks.
- Examine parents: a "dysmorphic" feature present in a parent may be familial.
- Photograph (with consent) face front/profile, hands, feet for follow-up and
  reanalysis.

## 3. Phenotype in HPO terms
Record findings as **Human Phenotype Ontology** terms (e.g. HP:0000316 hypertelorism).
Lab variant interpretation and tools (Phenomizer, Exomiser, Face2Gene, PubCaseFinder)
depend on precise HPO lists; vague "dysmorphic features" wastes exome analysis.

## 4. Build the differential
- Look for a **"handle"**: the rarest, most specific feature (e.g. aniridia, polysyndactyly),
  not the commonest (e.g. developmental delay).
- Search OMIM, Orphanet, London Medical Databases/POSSUM, and gestalt tools; consider
  recognisable patterns (trisomy 21, 22q11.2 deletion, Noonan, Williams, Angelman/Prader–Willi,
  Kabuki, fetal alcohol spectrum).

## 5. Choose the test
| Situation | First-tier test (typical, verify local pathway) |
|---|---|
| Strong clinical suspicion of a specific syndrome | Targeted test (single gene, methylation study for imprinting disorders, FISH) |
| Suspected aneuploidy (e.g. trisomy) | Rapid aneuploidy test/karyotype (karyotype also detects balanced translocations) |
| Non-specific ID/DD ± anomalies | **Exome or genome sequencing** (ACMG 2021 first/second-tier) or **chromosomal microarray** where ES/GS not accessible |
| Male (or female) with ID and family history of X-linked ID | Fragile X (FMR1 repeat — **not detected** by exome/microarray) |
| Mitochondrial or repeat expansion suspected | Specific assays (mtDNA, repeat-primed PCR) |
| Regression/metabolic features | Biochemical screen in parallel (see metabolic genetics skill) |
**Trio** sequencing (proband + both parents) increases yield and speeds de novo
interpretation.

## 6. Pre-test counselling and follow-up
Explain possible results (positive, negative, VUS, secondary findings and the opt-in
choice, non-paternity/consanguinity revelations), turnaround, cost. Book result
disclosure. Unsolved cases: plan **reanalysis** every 1–3 years or when new features
appear.

## Gotchas
- Microarray misses balanced rearrangements, low-level mosaicism, repeat expansions
  and single-nucleotide variants; exome misses repeat expansions and many structural
  variants; genome covers more but still not methylation (imprinting).
- Features evolve with age (e.g. Prader–Willi neonatal hypotonia vs later hyperphagia) —
  re-examine at follow-up.
- Population variation: features normal in one ancestry may be flagged in another;
  compare to family and appropriate norms.

## Verify
- [ ] Three-generation pedigree documented, consanguinity and losses asked.
- [ ] Measurements plotted; anomalies classified (malformation/deformation/etc.).
- [ ] Phenotype captured as HPO terms with photos (consented).
- [ ] Test chosen matches the differential and its known blind spots.
- [ ] Pre-test counselling covered VUS and secondary findings; reanalysis plan set.
