---
id: agriculture-environment.forestry.forest-inventory.plot-sampling-and-timber-cruising
name: plot-sampling-and-timber-cruising
category: agriculture-environment
field: forestry
product: forest-inventory
tags: [forestry, forest-inventory, mensuration, timber-cruise, cruising, plot-sampling, fixed-area-plot, variable-radius-plot, prism, relascope, basal-area-factor, baf, dbh, diameter-at-breast-height, diameter-tape, clinometer, hypsometer, vertex, tree-height, volume-table, form-factor, sampling-error, coefficient-of-variation, standard-error, stocking, trees-per-hectare]
level: practitioner
status: gated
description: "Run a timber cruise: design plot grid and sample size, measure DBH and height correctly, use fixed-area or prism plots, expand to per-hectare figures and report volume with sampling error."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Plot sampling and timber cruising

**Goal:** estimate stems, basal area and volume per hectare (and for the stand) to a
stated precision, cheaply enough that the estimate is worth having.

> Plot radii, the sample-size formula, the BAF limiting-distance factor and the expansion arithmetic were recomputed (r = 5.64, 7.98, 11.28 m; 37.2 ft; 0.354 m per cm for BAF 2; n = 64). Metric shown; imperial equivalents in brackets. Volume equations are regional
> and species-specific — use your agency's published tables.

## 1. Design
1. Stratify: split the property into stands that are reasonably uniform (species, age,
   density). Cruise each stratum separately.
2. Choose plot type:
   - **Fixed-area circular plots:** 0.01 ha (r = 5.64 m) for dense young stands; 0.02 ha
     (7.98 m) or 0.04 ha (11.28 m) for mature stands. [1/10 acre = 37.2 ft radius.]
   - **Variable-radius (prism/relascope) plots:** a tree is "in" if its stem looks wider
     than the prism offset. Each in-tree represents BAF m²/ha of basal area. BAF 2 or 4
     (metric) / BAF 10 or 20 (imperial) are common. Aim for ~5-10 in-trees per point (gated: unconfirmed, source is paywalled or blocked).
3. **Sample size:** from a pilot of ~10 plots compute the coefficient of variation (CV%).
   n ≈ (t × CV / E)², where E is the allowable error % (often 10% at 95% confidence) and
   t ≈ 2 (rounding of 1.96). CV 40%, E 10% → n ≈ 64 plots. Add a few for slack.
4. Lay plots on a systematic grid with a random start; pre-load coordinates in a GPS.

## 2. Measure
- **DBH** at 1.3 m (4.5 ft in US) on the uphill side, with a diameter tape perpendicular
  to the stem; on leaning trees measure along the stem; forked below 1.3 m = two trees;
  buttresses/swellings: measure just above. Record to the nearest 0.1 cm / 1 cm class.
- **Borderline trees** on fixed plots: measure distance to the stem *centre*. On prism
  plots, check with a tape: limiting distance = DBH(cm) × plot radius factor
  (for BAF 2 metric, factor ≈ 0.354 m per cm DBH).
- **Height** with a clinometer/hypsometer (e.g. Haglöf Vertex): stand at roughly one
  tree-height away, take top and base readings; on slopes sum or subtract the angles'
  tangents correctly. Measure heights on a subsample (e.g. 2–3 per plot) and fit a
  height–diameter curve for the rest.
- Record species, DBH, height (if sampled), quality class/defects, dead/alive.

## 3. Compute
- **Fixed plot:** per-ha value = plot sum × (1 / plot area in ha). 0.02 ha plot → ×50.
- **Prism plot:** BA/ha = BAF × count of in-trees. Trees/ha represented by each in-tree =
  BAF / (tree basal area), where tree BA (m²) = π × (DBH_m / 2)².
- **Volume:** apply a volume equation or table (DBH, height → m³), or BA × height × form
  factor (~0.4-0.5 for conifers as a rough stand-level check (gated: unconfirmed, source is paywalled or blocked)).
- Average plots in a stratum; standard error = SD / √n; report ±(t × SE) as % of the mean.
- Stand total = per-ha mean × stratum area; property total = sum of strata.

## 4. Report
Per stratum: area, plots, stems/ha, BA/ha, QMD, mean height (or top height), volume/ha,
volume by product, sampling error at 95%. Give the method and the equations used.

## Gotchas
- Moving plot centres to "a more typical spot" biases everything; stay on the grid.
- Edge plots: use the mirage or walkthrough method rather than dropping them.
- Prism counts on slopes need slope correction (tilt the prism or use a relascope).
- Height is the most error-prone measurement; check the instrument and lean.

## Verify
- [ ] Strata defined; plot number derived from pilot CV and target error.
- [ ] DBH at 1.3 m with tape; borderline trees checked with a tape.
- [ ] Per-plot expansion factors correct (spot-check one plot by hand).
- [ ] Volume equations named and appropriate for species/region.
- [ ] Report shows sampling error; if over target, more plots added.
