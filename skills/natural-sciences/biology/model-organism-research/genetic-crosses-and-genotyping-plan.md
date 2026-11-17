---
id: natural-sciences.biology.model-organism-research.genetic-crosses-and-genotyping-plan
name: genetic-crosses-and-genotyping-plan
category: natural-sciences
field: biology
product: model-organism-research
tags: [model-organism-research, genetic-crosses, breeding-scheme, mouse-genetics, mouse-colony, drosophila, fly-genetics, balancer-chromosomes, zebrafish, c-elegans, arabidopsis, mendelian-ratios, punnett-square, heterozygous-intercross, littermate-controls, cre-lox, floxed, conditional-knockout, genotyping-pcr, colony-management, backcrossing, congenic, chi-square, sex-linked, 3rs]
level: practitioner
status: verified
description: "Plan a model-organism breeding scheme: expected Mendelian ratios, how many crosses to get N experimental animals, littermate controls, Cre/flox design, genotyping and checking ratios."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Genetic crosses and genotyping plan

**Goal:** get the number of experimental and control animals you need, of the right
genotypes, in the fewest generations and with the fewest surplus animals — and know
early if something is off (lethality, mis-genotyping).

## 1. Write the target genotypes first
List exactly what the experiment compares, e.g. *Emx1-Cre; Gene^fl/fl* (conditional
knockout) vs *Gene^fl/fl* without Cre (control). Then work backwards to the parental
cross. Draw every generation as a Punnett square; with two or more loci, multiply the
independent probabilities.

## 2. Expected fractions, worked
- Het × het (A/a × A/a): ¼ A/A, ½ A/a, ¼ a/a.
- Conditional knockout, common mouse scheme: *Cre/+; fl/+* × *fl/fl* →
  P(Cre) = ½, P(fl/fl) = ½ → **¼ are Cre; fl/fl** (experimental) and ¼ are
  *+/+; fl/fl* (littermate controls).
- Cre × fl/fl from scratch takes two generations: F1 *Cre; fl/+* then back to *fl/fl*.

**Animals to breed** ≈ required number ÷ expected fraction ÷ survival. If you need 10
experimental mice of one sex at ¼ × ½ (sex), you need ~80 pups, i.e. roughly 10–12
litters at 6–8 pups (litter size is strain dependent). Build that into the timeline.

## 3. Design choices that save you later
- **Littermate controls**, not purchased wild-types: shared environment, maternal care
  and background.
- Keep the **Cre in the parent of one sex consistently** and check the line's
  documentation: some Cre drivers show germline recombination when transmitted through
  one sex (deleting the floxed allele in all offspring). Genotype for the recombined
  ("deleted") allele, not just Cre and flox.
- Include **Cre-only controls** at least once; Cre expression itself can cause phenotypes.
- **Background:** mixed backgrounds add variance. Backcrossing to an inbred strain
  takes ~10 backcross generations (N10, counting the F1 as generation 1, about 99.9% recipient background) to be considered congenic (speed congenics with marker
  selection shortens this).
- Flies: use **balancer chromosomes** to maintain lethal or sterile mutations without
  genotyping each generation; balancers carry dominant visible markers (e.g. *CyO* carries Curly wings, *TM3* carries Stubble bristles *Sb*; see the Bloomington balancer definitions at bdsc.indiana.edu/stocks/balancers)
  so genotype is read from phenotype. Choose crosses so the desired class is
  distinguishable by markers.
- Zebrafish/worms/plants: large clutches let you phenotype then genotype; worms allow
  self-fertilising hermaphrodites to maintain homozygous lines.

## 4. Genotyping
- Design PCR so each allele gives a distinct band size; run a wild-type, het and
  homozygous control every time, plus a no-template control.
- Genotype at weaning (mice) and **re-genotype experimental animals at the end** from a
  separate tissue sample — sample mix-ups are common.
- Record in a colony database (cage cards linked to IDs, parents, DOB, genotype).
  Commercial and free colony-management software exists; a spreadsheet works for
  small colonies if every animal has a unique ID.

## 5. Check the ratios
After ~50+ offspring, compare observed genotype counts with expected ratios using a
chi-square goodness-of-fit test (computed with scipy for a het intercross of 50 pups: 20/30/0 gives chi-square 18.0, p = 1.2e-4; 14/24/12 gives chi-square 0.24, p = 0.89). A deficit of homozygotes suggests embryonic/perinatal
lethality or reduced viability — the phenotype may be bigger than you designed for.
Check before weaning too, since pups can die before genotyping.

## Gotchas
- Sex-linked transgenes (X-linked Cre or reporters) change the ratios by sex — redo the
  Punnett square for each sex.
- Some transgene insertions disrupt endogenous genes; homozygous transgenics can have
  phenotypes unrelated to the transgene.
- Aged breeders produce smaller litters; plan replacement breeders.
- Ethics: animal-use protocols require numbers justified and minimised (3Rs). Your
  breeding calculation is that justification — keep it.

Checked 2026-10-19: Mendelian fractions, the 80-pup and litter arithmetic and chi-square examples were computed; congenic N10 and balancer markers from JAX/BDSC pages (via search). Uncertain here: litter sizes, Cre germline behaviour and generation times are strain-
and line-specific; consult the repository datasheet (e.g. JAX, Bloomington, ZIRC) for each line.

## Verify
- [ ] Target genotypes and controls written down before the first cross.
- [ ] Expected fraction per cross computed; number of litters estimated.
- [ ] Genotyping PCR includes all allele controls; recombined allele tested where relevant.
- [ ] Observed ratios checked by chi-square after enough offspring.
- [ ] Experimental animals re-genotyped at endpoint.
