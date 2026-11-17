---
id: business-finance.insurance.actuarial-pricing.chain-ladder-reserving
name: chain-ladder-reserving
category: business-finance
field: insurance
product: actuarial-pricing
tags: [insurance, actuarial-pricing, actuarial, reserving, loss-reserving, loss-triangle, development-triangle, chain-ladder, link-ratios, age-to-age-factors, tail-factor, ibnr, ultimate-loss, bornhuetter-ferguson, bf-method, loss-ratio, rate-making, ratemaking, pricing, mack, p-and-c]
level: advanced
status: gated
description: "Estimate insurance reserves from a loss triangle with the chain-ladder method: link factors, tail, ultimates and IBNR, cross-checked against Bornhuetter-Ferguson."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chain-ladder reserving from a loss triangle

**Goal:** estimate the ultimate cost of claims already incurred (including those not
yet reported or not fully developed), so reserves — and therefore pricing and
reported profit — are right.

*Worked numbers recomputed (link factors 1.524 and 1.100, ultimates 187.0 and 201.1, total reserve 98.1, CDF 1.676). Textbook deterministic method. Real reserving uses several methods, judgement
and actuarial standards of practice; sign-off belongs to a qualified actuary.*

## 1. Build the triangle
Rows = **origin period** (accident year, or underwriting year); columns = **development
age** (12, 24, 36 months...). Cells = cumulative paid (or incurred = paid + case
reserves) to date. Example, cumulative paid, $000:

| AY | 12 | 24 | 36 |
|---|---|---|---|
| 2023 | 100 | 150 | 165 |
| 2024 | 110 | 170 | |
| 2025 | 120 | | |

Check the data first: reconcile triangle diagonals to the ledger, and confirm no
changes in claims handling, case-reserving philosophy or mix that would break the
pattern.

## 2. Age-to-age (link) factors
Volume-weighted average: sum of column *n+1* ÷ sum of the same rows in column *n*.
- 12→24: (150 + 170) ÷ (100 + 110) = **1.524**
- 24→36: 165 ÷ 150 = **1.100**
Look at the individual factors too (1.50 and 1.55 here) — outliers and trends matter
more than the average. Select factors with judgement (exclude a distorted year, use
the latest 3–5 diagonals).

## 3. Tail factor
If the triangle doesn't reach full development, apply a **tail** beyond the last age
(from curve fitting, benchmarks or a longer-history triangle). Long-tail lines
(liability, workers' comp) develop over many years (gated: unconfirmed, source is paywalled or blocked); ignoring the tail is a classic
under-reserving error. Example assumes tail = 1.000.

## 4. Project ultimates and reserves
Cumulative development factor (CDF) to ultimate = product of remaining link factors.
- AY2024: 170 × 1.100 = **187.0** → reserve 17.0
- AY2025: 120 × 1.524 × 1.100 = **201.1** → reserve 81.1
- Total reserve ≈ **98.1**. On a paid triangle this is case reserves + IBNR; on an
  incurred triangle the indicated amount above current incurred is IBNR.

## 5. Cross-check with other methods
- **Bornhuetter–Ferguson:** blends an a-priori expected loss ratio with development;
  more stable for immature years where chain-ladder leverages a small number
  (AY2025 above is multiplied by 1.68 — one large early claim would swing it).
- **Expected loss ratio** method for the very latest year.
- Compare paid vs incurred chain-ladder results; big divergence → investigate
  case-reserve strength changes.

## 6. Feed into pricing
Ultimate loss ratios by year, trended to the future policy period (claims inflation,
exposure change) and on-levelled for past rate changes, give the base for
**rate-making**: indicated rate change = (projected loss + LAE ratio) ÷ (permissible
loss ratio) − 1 (loss-ratio method; confirm in the actuarial text or standard of practice your jurisdiction uses; gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- **Changing case-reserve practice** distorts incurred triangles.
- **Inflation spikes** are partially embedded in historical factors only; explicit
  adjustment may be needed.
- Large losses: cap or remove them and load separately.
- Mixing products with different tails in one triangle.
- Small triangles have huge uncertainty; use stochastic methods (Mack, bootstrap) to
  quantify variability if you need ranges.

## Verify
- [ ] Triangle diagonals reconcile to the ledger.
- [ ] Individual link factors inspected; selections documented.
- [ ] Tail factor justified for the line's development length.
- [ ] Chain-ladder results compared with BF and paid vs incurred.
- [ ] Reserve split into case and IBNR with stated assumptions.
