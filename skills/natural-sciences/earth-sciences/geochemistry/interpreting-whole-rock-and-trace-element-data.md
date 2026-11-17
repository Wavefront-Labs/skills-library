---
id: natural-sciences.earth-sciences.geochemistry.interpreting-whole-rock-and-trace-element-data
name: interpreting-whole-rock-and-trace-element-data
category: natural-sciences
field: earth-sciences
product: geochemistry
tags: [geochemistry, whole-rock, xrf, icp-ms, major-elements, trace-elements, ree, rare-earth-elements, spider-diagram, chondrite-normalised, primitive-mantle, tas-diagram, harker-diagram, loi, loss-on-ignition, detection-limit, reference-materials, crm, mobile-elements, alteration, tectonic-discrimination, gcdkit, isotopes]
level: practitioner
status: gated
description: "Check and interpret XRF/ICP-MS whole-rock data: QA with standards and totals, handling LOI and alteration, TAS and Harker plots, normalised REE and spider diagrams."
sources: ["Rollinson & Pease, Using Geochemical Data (CUP, 2nd ed.)", "Sun & McDonough 1989 normalising values", "GCDkit documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpreting whole-rock and trace-element data

**Goal:** turn a lab spreadsheet of oxides and ppm values into defensible statements
about rock type, source and process — after proving the numbers are trustworthy.

## 1. QA before any plot
- **Totals:** major oxides + LOI should sum to roughly 99–101 wt% (gated: unconfirmed, source is paywalled or blocked). Outside that, ask the
  lab (missed element, weighing error, sulphide/carbonate-rich sample).
- **Reference materials:** the lab should run certified standards (e.g. USGS BHVO-2,
  BCR-2; the USGS information sheet of June 2022 says AGV-2 is no longer available, so check what your lab actually ran) alongside your samples. Compare measured vs certified; >5–10% off for a
  major element or >10–20% for a trace element is a warning (*thresholds vary by element
  and method*).
- **Duplicates and blanks:** a split duplicate tells you precision; blanks tell you
  contamination (e.g. Co, W from tungsten-carbide mills; Cr, Ni from steel mills — know
  how your samples were crushed).
- **Below detection limit:** keep it as "<DL" with the DL value; don't write zero and
  don't silently drop it. Flag elements near DL as unreliable.
- **Method fit:** XRF is good for majors and some traces (Zr, Sr, Rb, Ni, Cr); ICP-MS is
  needed for REE, Th, U, Nb/Ta at low levels. Zircon-hosted Zr/Hf may be under-reported
  by acid digestion that doesn't dissolve zircon — use fusion for felsic rocks.

## 2. Alteration and LOI
- High **LOI** (>2–3 wt% in an igneous rock (gated: unconfirmed, source is paywalled or blocked) signals hydration, carbonation or weathering.
- Recalculate majors **volatile-free to 100%** before classification plots.
- **Mobile vs immobile:** Na, K, Rb, Ba, Sr, Cs and sometimes U move during alteration;
  Ti, Zr, Nb, Y, Th, the HREE and Al are relatively immobile. For altered rocks,
  classify with immobile-element plots (e.g. Zr/Ti vs Nb/Y) rather than TAS.

## 3. Standard plots
1. **TAS** (Na2O+K2O vs SiO2) for fresh volcanic rocks — classification only, not origin.
2. **Harker diagrams** (oxide vs SiO2 or vs MgO): curved or kinked trends mark
   fractionation of different phases (e.g. falling CaO and Al2O3 → plagioclase; falling
   MgO/Ni → olivine).
3. **REE plots**: normalise to chondrite (state which values; Sun & McDonough 1989 and
   McDonough & Sun 1995 differ, e.g. Lu 0.0254 vs 0.0246 ppm and Eu 0.058 vs 0.0563 ppm per the pyrolite reference tables; Palme & O'Neill 2014 differs again). Read slope (La/Yb)N, Eu anomaly (Eu/Eu*), and HREE
   flattening (garnet absent) vs depletion (garnet in source).
4. **Multi-element (spider) diagrams** normalised to primitive mantle or N-MORB:
   negative Nb-Ta with Pb spike is the classic subduction signature.
5. **Tectonic discrimination diagrams** — use as supporting evidence only. They were
   calibrated on limited datasets; altered, cumulate or crustally contaminated samples
   plot misleadingly.

## 4. Isotope ratios (brief)
Report with 2σ uncertainty and the standard measured (e.g. NIST SRM 987 for Sr; certificate 87Sr/86Sr = 0.71034 ± 0.00026, 95 %, confirm on the current certificate). Initial
ratios need an age: εNd and 87Sr/86Sr(i) are age-corrected values — state the age used.

## Tools
GCDkit (R), PyRolite (Python), ioGAS, or a carefully built spreadsheet. Whatever you use,
keep raw lab data untouched in one sheet and every transformation in another.

## Gotchas
- Plotting raw (wet) oxides on TAS — always volatile-free.
- Averaging values that include "<DL" as zero.
- Cumulate rocks don't represent melt compositions; don't model them as liquids.
- Mixing normalisation schemes between figures in one paper.

## Verify
- [ ] Standards, duplicates and blanks reviewed and reported.
- [ ] Totals within range; high-LOI samples flagged.
- [ ] Altered samples classified only on immobile elements.
- [ ] Every normalised plot states the normalising reference.
- [ ] Interpretations rest on more than one diagram.
