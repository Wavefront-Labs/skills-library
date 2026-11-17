---
id: defence-public-safety.forensic-science.dna-analysis.str-profiling-and-mixture-interpretation
name: str-profiling-and-mixture-interpretation
category: defence-public-safety
field: forensic-science
product: dna-analysis
tags: [dna-analysis, forensic-dna, str, short-tandem-repeat, dna-profiling, capillary-electrophoresis, electropherogram, allele, stutter, drop-out, drop-in, analytical-threshold, stochastic-threshold, mixture-interpretation, number-of-contributors, probabilistic-genotyping, strmix, truallele, euroformix, likelihood-ratio, random-match-probability, hp-hd, propositions, activity-level, source-level, codis, ndnad, low-template, touch-dna, contamination, elimination-database, y-str]
level: advanced
status: draft
description: "Interpret forensic STR profiles: read the electropherogram (stutter, drop-out, thresholds), estimate contributors, use probabilistic genotyping and report a likelihood ratio properly."
sources: ["SWGDAM Interpretation Guidelines for Autosomal STR Typing", "ISFG DNA Commission recommendations on mixtures and on evaluative reporting", "PCAST, Forensic Science in Criminal Courts (2016)", "Butler, Advanced Topics in Forensic DNA Typing: Interpretation (textbook)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# STR profiling and mixture interpretation

**Goal:** go from a casework sample to a statistically supported, honestly limited
statement about who could have contributed DNA — without overstating what a mixed or
low-level profile can show.

## 1. The laboratory pipeline (what each step can go wrong on)
1. **Screening / sampling** — presumptive tests and targeted sampling (blood, saliva,
   semen; or "touch" areas). Record exactly where each swab was taken.
2. **Extraction** — with reagent blanks carried through every step.
3. **Quantification** (qPCR) — total human DNA, male DNA and a degradation index. This
   drives the amplification input and warns you early of low template or inhibition.
4. **Amplification** — commercial multiplex kits (~20+ autosomal STR loci plus
   amelogenin; core loci set by your database: CODIS in the US, the UK/European set for
   NDNAD). Include positive and negative controls.
5. **Capillary electrophoresis** → electropherogram (EPG), alleles called against the
   ladder in analysis software.

Contamination control throughout: separated pre-/post-PCR areas, staff and consumable
**elimination databases**, and investigation of any unexpected profile in a blank.

## 2. Reading the EPG
- **Analytical threshold (AT):** below it, a peak isn't called. Set by validation, in RFU.
- **Stochastic threshold:** above it you can trust that a sister allele didn't drop out;
  below it a single peak may be a heterozygote with drop-out, not a homozygote.
- **Stutter:** peaks one repeat shorter (and sometimes longer) than the true allele, at
  locus-specific ratios. A minor contributor's allele can hide in a stutter position.
- **Drop-out / drop-in:** low template causes alleles to vanish or sporadic alleles to
  appear. Degradation shows as declining peak heights with molecule size.
- Artefacts: pull-up (spectral bleed), spikes, dye blobs — recognise before calling.

## 3. Mixtures
- **Number of contributors (NoC):** start from the maximum allele count at any locus
  (÷2, rounded up) as a *minimum*, then consider peak-height balance and the whole
  profile. NoC is an assumption — test sensitivity to ±1 contributor.
- **Avoid the old binary methods** (CPI/RMNE) for complex or low-level mixtures; they
  discard peak-height information and can't handle drop-out properly.
- **Probabilistic genotyping (PG)** software (e.g. STRmix, TrueAllele, EuroForMix)
  models peak heights, stutter, drop-out and drop-in to compute a likelihood ratio.
  Use only within the range your lab has **internally validated** (NoC, template level).

## 4. Reporting a likelihood ratio
LR = P(evidence | Hp) / P(evidence | Hd), e.g. Hp "the DNA came from Mr X and an unknown
person", Hd "two unknown, unrelated people".
- State the propositions, the population database and sub-population correction (θ/Fst)
  used, and that the LR is **not** the probability that the person is guilty or the source
  (avoid the **prosecutor's fallacy**).
- Many labs give a verbal scale alongside (e.g. "very strong support") — use your lab's.
- Distinguish **source level** ("whose DNA is this?") from **activity level** ("how did it
  get there?"). With trace DNA, secondary transfer is real; activity-level questions need
  separate evaluation and are often where the case actually turns.
- Consider relatives as alternative contributors when the defence raises it.

## 5. Database searching
- Upload only profiles meeting the database's quality and loci rules; mixtures usually only
  as deconvoluted major/single-source profiles (rules vary by system).
- A database hit is an **investigative lead**, confirmed by a fresh reference sample
  before it's evidence. Partial/low-stringency or familial searching needs specific
  authorisation in most jurisdictions.

## Gotchas
- "No DNA found" ≠ "person never touched it" — shedding varies widely.
- Y-STR matches are shared by paternal relatives; the statistics are lineage-based and much weaker.
- Rerunning a sample until a "better" profile appears, and reporting only that, is a
  documentation and bias failure — report the process.
- Contextual information (suspect's name, confession) should be managed so analysts don't
  interpret mixtures with a suspect profile in mind — compare after deconvolution.

## Verify
- [ ] Blanks and controls clean, or contamination investigated and recorded.
- [ ] AT, stochastic threshold and stutter filters are the validated values.
- [ ] NoC justified and sensitivity tested; PG used within validated range.
- [ ] Report states propositions, database, θ, and avoids transposing the conditional.
- [ ] Database hits flagged as leads pending confirmation.
