---
id: natural-sciences.biology.flow-cytometry.compensation-and-gating-strategy
name: compensation-and-gating-strategy
category: natural-sciences
field: biology
product: flow-cytometry
tags: [flow-cytometry, facs, compensation, spillover, single-stain-controls, compensation-beads, fmo, fluorescence-minus-one, gating, gating-strategy, fsc, ssc, singlets, doublet-discrimination, viability-dye, live-dead, isotype-control, panel-design, spectral-cytometry, unmixing, flowjo, spreading-error, fluorochrome-brightness, voltage-optimisation, mfi]
level: practitioner
status: gated
description: "Set up compensation from proper single-stain controls and gate a flow cytometry panel defensibly: cells, singlets, live, then markers, with FMO controls setting positive boundaries."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compensation and gating strategy in flow cytometry

**Goal:** populations whose boundaries are set by controls rather than by eye, on
correctly compensated (or unmixed) data, so the percentages you report mean what you
say they mean.

## 1. Controls you need
| Control | Purpose |
|---|---|
| Unstained cells | Autofluorescence; voltage setting |
| **Single-stain controls**, one per fluorochrome | Calculate compensation/spillover |
| **FMO** (fluorescence minus one) for each dim/continuous marker | Set the positive gate in a full panel |
| Viability dye | Exclude dead cells, which bind antibodies non-specifically |
| Biological positive/negative samples | Confirm the antibody actually stains |

Isotype controls are of limited value for setting gates (different antibody, different
F/P ratio); many core facilities now recommend FMOs instead. Isotypes can still
indicate Fc-binding problems — use Fc block.

## 2. Single-stain controls that give correct compensation
The rules (from standard flow practice):
1. **Same fluorochrome as the sample** — for tandem dyes (PE-Cy7, APC-Cy7), the **same
   vial/lot**, because tandems degrade and vary lot to lot.
2. **At least as bright** as the brightest sample signal in that channel.
3. **Same autofluorescence** for positive and negative within each control (beads with
   beads, cells with cells).
4. Enough events in the positive population (a few thousand is a common target).
5. Same instrument settings as the samples; treated the same way (fixation changes tandems).
Compensation is a linear unmixing: observed = true × spillover matrix, so corrected = observed × inverse(spillover) (checked numerically with a 3-channel matrix: the inverse recovers the true signals exactly). Compensation beads satisfy (2) easily for antibodies; viability dyes usually need
heat-killed cells.

## 3. Compensation in practice
- Let the software (instrument or FlowJo-style analysis) compute the matrix from controls;
  avoid manual tweaking by eye — "making it look right" introduces errors.
- Inspect N×N plots: compensated populations should have the same median in the
  spillover channel as the negative population. A "diagonal lean" means under-compensation;
  a negative-curving population means over-compensation.
- **Spreading error** after compensation is real and not a mistake: bright signals in one
  channel widen the negative in another, which is why FMOs are needed.
- Spectral cytometers use full-spectrum **unmixing** with single-stain reference controls;
  the same control rules apply, plus an unstained reference for autofluorescence extraction.

## 4. Panel design shortcuts
Pair **bright fluorochromes with dim or rare antigens** and dim fluorochromes with highly
expressed antigens. Put markers that are co-expressed on the same cells in channels with
little spillover between them. Use the instrument's spillover-spreading matrix or the
vendor's panel tools if available.

## 5. Gating hierarchy
1. **Time** gate (optional) — remove fluidic hiccups.
2. **FSC-A vs SSC-A** — cells, excluding debris.
3. **Singlets:** FSC-H vs FSC-A (doublets fall off the diagonal); optionally SSC-H vs SSC-W.
4. **Live:** viability dye negative.
5. Lineage markers, then subsets — each positive boundary placed using the **FMO** for that marker.
Show the full hierarchy with numbers in figures; reviewers ask.

## Gotchas
- Setting voltages so the brightest population is on scale but the negative is above the
  electronic noise matters more than "centring". Re-use saved settings across a study.
- Run daily QC beads (CS&T-type) and keep settings fixed for longitudinal studies.
- Fixed and permeabilised samples shift scatter and can degrade tandem dyes; make the
  compensation controls with the same treatment.
- Report frequency of parent and of live singlets; "% positive" without a denominator is
  uninterpretable.
- Rare populations need many events: to report a 0.1 % population with ~10 % CV you need
  ~100 events in the gate, so ≥ 100,000 events acquired (Poisson CV = 1/√n: 100 events gives 10%; 0.1% of 100,000 is 100; computed).

Checked 2026-10-19: matrix algebra and Poisson arithmetic computed. Instrument-, fluorochrome- and facility-specific advice (tandem lot rules, CS&T QC, bead choices, event targets) was not checked against vendor documents (gated: unconfirmed, source is paywalled or blocked).

Uncertain here: exact control-event counts and bead choices vary by facility; check your
core's SOP.

## Verify
- [ ] One single-stain control per fluorochrome, tandem from the same lot, as bright as the sample.
- [ ] Compensated N×N plots show no lean between channel pairs.
- [ ] Debris, doublets and dead cells excluded before marker gates.
- [ ] Each dim-marker gate placed on its FMO, and FMOs saved with the data.
- [ ] Enough events acquired for the rarest reported population.
