---
id: mathematics.actuarial-science.loss-reserving.bornhuetter-ferguson-and-reserve-ranges
name: bornhuetter-ferguson-and-reserve-ranges
category: mathematics
field: actuarial-science
product: loss-reserving
tags: [loss-reserving, claims-reserving, ibnr, run-off-triangle, development-triangle, bornhuetter-ferguson, bf-method, chain-ladder, cape-cod, expected-loss-ratio, a-priori, percent-unreported, mack-method, bootstrap-odp, reserve-range, reserve-uncertainty, triangle-diagnostics, chainladder-r, actuarial-science, casualty-actuarial]
level: practitioner
status: gated
description: "Estimate unpaid claims with Bornhuetter-Ferguson alongside chain ladder, diagnose the triangle first, and put a defensible range on the reserve with Mack or bootstrap."
sources: ["Friedland, Estimating Unpaid Claims Using Basic Techniques (CAS)", "Mack (1993) distribution-free chain ladder", "ChainLadder R package documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bornhuetter-Ferguson and reserve ranges

**Goal:** a reserve estimate for immature accident years that does not swing wildly
with a few early claims, plus an honest range around the total.

Chain-ladder mechanics are covered in
`business-finance.insurance.actuarial-pricing.chain-ladder-reserving`; this skill
assumes you can produce age-to-age factors and cumulative development factors (CDFs).

## 1. Diagnose the triangle before any method
Chain ladder and BF both assume the past development pattern applies to the future.
Look for breaks:
- **Paid vs incurred** ultimates diverging → case-reserve strength or settlement speed changed.
- **Ratio of paid to incurred** by diagonal drifting → case reserving change.
- **Closed / reported counts** by diagonal → claims-handling speed changed.
- **Average case reserve** per open claim trending faster than inflation → strengthening.
- Large one-off losses in a cell: cap or remove and add back separately.
If a diagonal effect is present, plain chain ladder will mis-project; adjust
(e.g. Berquist-Sherman (gated: unconfirmed, source is paywalled or blocked)) or lean harder on BF.

## 2. Bornhuetter-Ferguson
For each accident year:
1. A-priori ultimate = earned premium × expected loss ratio (ELR). The ELR comes from
   pricing, plan, or an older-year average adjusted for rate change and trend —
   **not** from this year's chain-ladder result (that is circular).
2. Percent unreported (or unpaid) = `1 − 1/CDF`.
3. IBNR = a-priori ultimate × (1 − 1/CDF).
4. BF ultimate = reported to date + IBNR.

Behaviour: BF is a credibility blend — weight `1/CDF` on chain ladder,
`1 − 1/CDF` on the a-priori. Mature years ≈ chain ladder; immature years ≈ a-priori.
A large early claim does not get multiplied by a big CDF.

**Cape Cod (Stanard-Buhlmann)** derives the ELR from the data itself:
`ELR = Σ reported / Σ (premium × 1/CDF)` across years, then runs BF. Use it when you
distrust the plan ELR but want stability.

## 3. Choosing per year
Typical selection: chain ladder for mature years, BF or Cape Cod for the latest 2–3,
and expected-loss-ratio for the very latest if almost nothing is reported. Write down
why for each year; reviewers will ask.

## 4. Reserve ranges
- **Mack:** analytic standard error of chain-ladder reserves (process + parameter),
  by year and total. R: `ChainLadder::MackChainLadder(triangle)`.
- **Bootstrap ODP:** resample scaled Pearson residuals of an over-dispersed Poisson
  GLM, re-fit, add process noise; gives a full distribution. R:
  `ChainLadder::BootChainLadder(triangle, R = 999, process.distr = "od.pois")`.
- Both measure only the uncertainty **inside** the model. Model/selection risk (which
  method, tail factor, ELR) is often larger — show a scenario range alongside.
- Report the 75th/95th percentiles, not just the standard error; the distribution is skewed.

## Uncertainty notes
`ChainLadder` signatures confirmed against the CRAN reference manual: `BootChainLadder(Triangle, R = 999, process.distr = c("gamma","od.pois"))` (default is gamma, so pass od.pois explicitly) and `MackChainLadder(Triangle, ...)`. Statutory booking rules (best estimate vs margin, discounting) vary by regime and
are not covered.

## Verify
- [ ] Paid/incurred, closure-rate and case-average diagnostics reviewed before projecting.
- [ ] BF a-priori ELR is independent of the current year's chain-ladder ultimate.
- [ ] BF ultimate − reported = IBNR = a-priori × (1 − 1/CDF) for each year.
- [ ] Mature-year BF ≈ chain ladder (sanity check on the CDFs).
- [ ] Range reported with percentiles and a note on model risk not captured.
