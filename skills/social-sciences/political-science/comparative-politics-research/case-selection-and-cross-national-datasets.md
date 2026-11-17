---
id: social-sciences.political-science.comparative-politics-research.case-selection-and-cross-national-datasets
name: case-selection-and-cross-national-datasets
category: social-sciences
field: political-science
product: comparative-politics-research
tags: [comparative-politics-research, comparative-politics, case-selection, small-n, most-similar-systems-design, most-different-systems-design, mill-methods, method-of-difference, process-tracing, qca, fsqca, typical-case, deviant-case, selection-on-the-dependent-variable, v-dem, polity, polity5, freedom-house, qog, quality-of-government, world-bank-wgi, regime-classification, democracy-indices, country-year-panel, vdemdata, democracy-measurement]
level: practitioner
status: draft
description: "Designing comparative studies: most-similar/most-different case selection, process tracing, and using V-Dem, Polity, QoG and other cross-national data."
sources: ["Seawright & Gerring, 'Case Selection Techniques in Case Study Research' (2008)", "King, Keohane & Verba, Designing Social Inquiry (1994)", "Beach & Pedersen, Process-Tracing Methods", "V-Dem Codebook and methodology documents", "Quality of Government Institute, QoG Standard Dataset codebook"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Case selection and cross-national datasets

**Goal:** pick countries (or regions, parties, regimes) so that the comparison can
actually support the causal claim, and use cross-national indicators without being
fooled by how they were built.

## 1. Small-N case-selection strategies
- **Most-similar systems (MSSD / Mill's method of difference):** cases alike on many
  background factors but different on the outcome; look for the factor that also
  differs. Gotcha: "similar" countries are never similar on everything; list the
  controls explicitly in a table.
- **Most-different systems (method of agreement):** diverse cases sharing the outcome;
  find the common factor. Weak at ruling out alternative causes.
- **Typical case** (well-predicted by a cross-national model) to probe mechanisms;
  **deviant case** (badly predicted) to find omitted variables; **diverse cases** to
  span the range of X; **crucial / least-likely cases** for theory tests.
- **Selecting on the dependent variable** (studying only revolutions that happened)
  biases inference about causes. Include negative cases where the outcome was possible
  but did not happen (the *possibility principle*).

## 2. Within-case leverage: process tracing
Lay out the causal chain predicted by each rival explanation, then hunt for evidence
whose presence or absence discriminates: *hoop tests* (must pass to stay alive),
*smoking-gun tests* (confirm strongly if found). Source triangulation — archives,
interviews, press — matters more than case count.

## 3. Medium-N: QCA
Qualitative Comparative Analysis (crisp- or fuzzy-set) for 10–50 cases with
conjunctural causation. Calibration thresholds drive results; report them and run
sensitivity checks.

## 4. Cross-national datasets you will meet
- **V-Dem:** expert-coded, hundreds of indicators, latent-variable estimates with
  uncertainty intervals; high-level indices (electoral, liberal, participatory...).
  Use the `vdemdata` R package or the website downloads.
- **Polity (Polity5):** −10 to +10 autocracy–democracy scale; historically dominant.
  Gotcha: special codes −66, −77, −88 (interruptions, anarchy, transitions) must be
  recoded or dropped — leaving them in as numbers wrecks means.
- **Freedom House:** political rights and civil liberties ratings; partly perceptual,
  changed methods over time.
- **QoG Standard Dataset:** merges hundreds of sources at country-year level —
  convenient, but always cite the original source variable.
- **World Bank WGI**, **Boix-Miller-Rosato** and **Regimes of the World** for binary
  or categorical regime types.
*Exact current versions/coverage change yearly — check each codebook.*

## 5. Working with country-year panels
- Country codes differ (ISO3, COW, V-Dem's own ids); use a crosswalk such as the
  `countrycode` R package rather than matching names.
- Watch country births/deaths (USSR, Yugoslavia, Sudan/South Sudan).
- Indicators correlate highly — high democracy scores partly reflect the same
  underlying coding; don't treat two indices as independent confirmation.
- Measurement error is not random: expert coders may know the outcome you study.

## Verify
- [ ] Case-selection logic stated and a controls table shown for MSSD designs.
- [ ] Negative cases included or their absence justified.
- [ ] Rival explanations each have a discriminating test in process tracing.
- [ ] Polity special codes and country-code crosswalks handled.
- [ ] Original data source and version cited for every indicator.
