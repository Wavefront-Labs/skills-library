---
id: natural-sciences.ecology.ecosystem-ecology.litterbag-decomposition-study
name: litterbag-decomposition-study
category: natural-sciences
field: ecology
product: ecosystem-ecology
tags: [ecosystem-ecology, decomposition, litter-decomposition, litterbag, leaf-litter, mass-loss, decay-constant, olson-k, exponential-decay, nutrient-cycling, carbon-cycling, soil-fauna, mesh-size, ash-free-dry-mass, afdm, tea-bag-index, home-field-advantage, stream-ecology, leaf-packs, carbon-nitrogen-ratio, lignin, nls, r, field-experiment, biogeochemistry]
level: practitioner
status: gated
description: "Run a litterbag decomposition experiment: litter collection and drying, mesh size, deployment design, retrieval schedule, ash-free mass loss and fitting decay constant k."
sources: ["J. S. Olson, Energy storage and the balance of producers and decomposers, Ecology 44 (1963) 322", "J. A. Keuskamp et al., Tea Bag Index, Methods Ecol. Evol. 4 (2013) 1070", "M. A. S. Graça, F. Bärlocher & M. O. Gessner (eds.), Methods to Study Litter Decomposition (2nd ed., 2020)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Litterbag decomposition study

**Goal:** a decomposition rate (k, per year or per day) for plant litter under
treatments or sites you care about, with a design that separates the effects of
litter quality, environment and decomposer community.

## 1. Litter
- Collect **freshly senesced** leaves (abscised or ready to drop; shake branches or use
  litter traps), not green leaves or old ground litter.
- Air-dry (or oven-dry at ~40–60 °C; higher temperatures change chemistry), mix
  thoroughly so each bag gets a representative sample.
- Weigh a fixed mass per bag (commonly 2–10 g) to ±0.01 g; record initial mass on
  a tag.
- Keep ~5–10 subsamples to determine the **air-dry to oven-dry (e.g. 65 °C)
  conversion** and initial chemistry (C, N, lignin, P).

## 2. Bags
- Mesh size is a treatment, not a detail:
  - fine (~0.05–0.1 mm) excludes most mesofauna — microbes only;
  - medium (~1–2 mm) admits mesofauna;
  - coarse (~4–10 mm) admits macrofauna (earthworms, isopods) but loses fragments.
  Use two mesh sizes to partition fauna effects. Coarse-top/fine-bottom bags reduce fragment loss.
- Use UV-stable, inert material (nylon, polyester, fibreglass). Label with durable tags.

## 3. Design and deployment
- Replicates: ≥ 4–5 bags per treatment × site × retrieval date (more if variance is high).
- Retrievals: 4–6 dates spread to capture early fast loss and later slow phase
  (e.g. 1, 2, 4, 8, 12 months in temperate forests; days–weeks in streams/tropics).
  Total bags = treatments × sites × dates × replicates — this escalates quickly.
- Place on the soil surface in contact with the litter layer, pinned down; map and flag.
- **Handling-loss bags:** a set taken to the field and immediately returned, to correct
  for transport losses.
- Standard substrates (e.g. Tea Bag Index: green and rooibos tea) allow cross-site comparison.

## 4. Processing
1. Retrieve into individual bags; process within days (or refrigerate).
2. Gently remove soil, roots and invertebrates; brush or rinse quickly (rinsing leaches).
3. Oven-dry to constant mass (65 °C, ≥ 48 h), weigh.
4. **Ash-free dry mass (AFDM):** combust a subsample at ~500–550 °C for 4 h. Soil
   contamination can add large errors in mineral soils — correct all masses to AFDM.

## 5. Analysis
- % mass remaining = AFDM_t / AFDM_0 × 100.
- Single exponential (Olson): M_t = M_0·e^(−kt). Fit by nonlinear regression on
  proportion remaining (`nls(prop ~ exp(-k*t))` in R), or log-linear as a check.
- If loss levels off (recalcitrant fraction), fit an asymptotic model
  M_t = A + (1 − A)e^(−kt) or a double exponential; compare with AIC.
- Compare treatments with mixed models (site as random effect) on k or on mass
  remaining over time.

## Gotchas
- Bags alter microclimate and exclude fauna; absolute k from litterbags tends to be
  lower than natural rates — compare treatments within a study rather than across.
- Animals and floods remove bags; overplant replicates by ~10–20%.
- *Uncertainty note:* mesh sizes, drying temperatures, replicate counts, retrieval schedules and AFDM combustion temperatures are protocol-dependent (gated: unconfirmed, source is paywalled or blocked); state yours and keep them constant. Olson single-exponential fit checked on simulated data (nonlinear and log-linear fits both recover k); Tea Bag Index uses green and rooibos tea (Methods in Ecology and Evolution blog).

## Verify
- [ ] Initial oven-dry mass derived from measured conversion factor, not assumed.
- [ ] Handling-loss bags processed and applied.
- [ ] All masses corrected to AFDM.
- [ ] Fit residuals examined; asymptotic model tested if mass loss plateaus.
- [ ] Initial litter chemistry reported alongside k.
