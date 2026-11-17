---
id: agriculture-environment.animal-breeding.breeding-programme-design.selection-index-and-inbreeding-control
name: selection-index-and-inbreeding-control
category: agriculture-environment
field: animal-breeding
product: breeding-programme-design
tags: [animal-breeding, breeding-programme-design, genetics, ebv, epd, estimated-breeding-value, genomic-ebv, selection-index, breeding-objective, heritability, accuracy, inbreeding, inbreeding-coefficient, coancestry, optimum-contribution-selection, mating-plan, generation-interval, genetic-gain, breeder-equation, beef, dairy, sheep, pigs, livestock-breeding]
level: practitioner
status: draft
description: "Design a herd or flock breeding programme: set an economic objective, rank sires on an index of EBVs, and keep inbreeding under ~1% per generation with planned matings."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Selection index and inbreeding control — a breeding programme you can run

**Goal:** turn "I want better animals" into a written objective, a ranking you apply
every season, and a mating plan that improves the herd without inbreeding it.

## 1. Write the breeding objective first
List the 3–6 traits that actually change your profit (or your purpose, for pedigree
work), and put a **relative economic value** on each — what one unit of change is worth
to you. Example for a commercial suckler herd: calving ease, 200-day weight, mature cow
weight (negative, if feed is your limit), docility, fertility. Rules of thumb:
- Include traits you *don't* want to move (mature size, milk in a dry environment) —
  otherwise they drift with correlated traits.
- Use the national or breed-society index if one fits (e.g. dairy profit indices, sheep
  terminal/maternal indexes, beef $-indexes). They already handle genetic correlations;
  a home-made weighting usually double-counts.

## 2. Rank candidates on EBVs, not on looks or raw records
An **EBV/EPD** is the animal's predicted genetic merit, from its own records, relatives
and (for genomic EBVs) DNA. Check three numbers before trusting one:
- **Accuracy (or reliability)** — below ~50% the EBV can move a lot as data arrives;
  use such sires on a few females only.
- **Same evaluation run and breed base** — EBVs from different runs, breeds or countries
  are not directly comparable unless the society publishes a conversion.
- **Percentile band** within the breed — "top 10% for calving ease" is easier to act on.

Combine traits with the index: `index = Σ (economic weight × EBV)`. Rank sires and
replacement females on it; set **independent culling levels** only for non-negotiables
(e.g. reject any bull outside the breed's worst 20% for calving ease when joining heifers).

## 3. Know what speed of progress to expect
The breeder's equation: **response per year = (i × r × σA) / L** — selection intensity
(how small a top fraction you keep), accuracy, genetic standard deviation, and
generation interval in years. Practical levers, in order of usual payoff:
1. **Use higher-accuracy, higher-index sires** (AI gives access to the whole breed).
2. **Shorten the generation interval** — keep young, proven-by-genomics sires; don't keep
   old females purely out of sentiment.
3. **Record properly** — weights, dates, scores into the breed recording scheme; your own
   animals' EBVs get more accurate and the bottom tail becomes visible.

## 4. Control inbreeding deliberately
Inbreeding depression shows as poorer fertility, survival and growth, and exposes
recessive defects. Targets:
- Keep the **rate of inbreeding (ΔF) under ~1% per generation** (FAO's commonly quoted
  ceiling; ≤0.5% is safer in small populations).
- Compute the **coefficient of inbreeding (COI)** of each *proposed mating* — the
  future calf's COI, not the parents' — using the breed society's mating tool or
  pedigree software. Avoid matings above ~6.25% (first cousins) unless deliberate.
- Spread use: don't put one sire over more than ~10–20% of a small herd's females
  per year; rotate unrelated sire lines.
- Advanced: **optimum-contribution selection** (e.g. tools built on EVA/GENCONT
  approaches) maximises gain for a set ΔF; worth it for nucleus herds and rare breeds.

## 5. Write the mating plan
A spreadsheet with: female ID, her index, her known carrier status, chosen sire, the
predicted progeny COI and index (average of parents' EBVs), and a back-up sire.
Check every line against carrier status for known recessive conditions in the breed
— carrier × carrier matings produce ~25% affected offspring.

## Gotchas
- **Single-trait selection backfires**: pushing growth alone raises birthweight and
  mature size; pushing milk can cost fertility.
- **Phenotype ≠ genotype**: the show winner raised on a better ration may have average EBVs.
- **Small herds look inbred faster** — a closed herd of 30 females using one home-bred
  sire for years can hit ΔF of several percent per generation.
- Genomic EBVs on young animals are still predictions; accuracy figures are real
  but they shift as daughters are recorded.
- Exact index names, accuracy thresholds and recording schemes differ by country and
  breed society — **check your society's current guidance**; figures here are
  general rules of thumb, not verified for a specific breed.

## Verify
- [ ] The objective lists traits *and* economic weights, written down before choosing sires.
- [ ] Every sire chosen has an EBV accuracy you've looked at and a breed percentile.
- [ ] Each planned mating has a predicted progeny COI, all below your threshold.
- [ ] No carrier × carrier matings for known breed recessives.
- [ ] Next year, the herd's average index has moved in the intended direction.
