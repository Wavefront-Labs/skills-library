---
id: mathematics.actuarial-science.financial-mathematics.duration-convexity-and-redington-immunisation
name: duration-convexity-and-redington-immunisation
category: mathematics
field: actuarial-science
product: financial-mathematics
tags: [financial-mathematics, interest-theory, time-value-of-money, present-value, discount-factor, force-of-interest, annuity-certain, bond-valuation, yield, macaulay-duration, modified-duration, effective-duration, convexity, redington-immunisation, immunization, asset-liability-matching, alm, cash-flow-matching, interest-rate-risk, actuarial-science, soa-fm, ifoa-cm1]
level: practitioner
status: gated
description: "Value cash flows, compute Macaulay/modified duration and convexity, and test Redington immunisation so an asset portfolio protects a liability stream against small rate moves."
sources: ["Kellison, The Theory of Interest (McGraw-Hill)", "Redington (1952), Review of the principles of life-office valuations, JIA 78, 286-340, doi:10.1017/S0020268100052811"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duration, convexity and Redington immunisation

**Goal:** know how much a set of cash flows moves when interest rates move, and
build an asset portfolio whose value tracks a liability stream for small parallel shifts.

## 1. Valuation basics
- `v = 1/(1+i)`, force of interest `δ = ln(1+i)`, discount rate `d = i/(1+i)`.
- `PV = Σ CF_t v^t`. Annuity-certain in arrears: `a_n = (1 − v^n)/i`; in advance:
  `ä_n = (1 − v^n)/d`.
- Bond (face F, coupon rate r, redemption C, yield j per period):
  `P = F r a_n(j) + C v^n(j)`. Premium if coupon > yield, discount if below.
- **Gotcha:** annual effective vs nominal convertible rates. `i^(m)` compounded m
  times a year ≠ i. Convert: `1 + i = (1 + i^(m)/m)^m`. Semi-annual coupon bonds use
  the per-half-year yield.

## 2. Duration and convexity
- **Macaulay duration:** `D = Σ t CF_t v^t / PV` — PV-weighted mean time (years).
- **Modified duration:** `D_mod = D / (1+i)` = `−(1/P) dP/di` under annual compounding.
  First-order change: `ΔP/P ≈ −D_mod Δi`.
- **Convexity:** `C = (1/P) d²P/di² = Σ t(t+1) CF_t v^{t+2} / P`.
  Second-order: `ΔP/P ≈ −D_mod Δi + ½ C (Δi)²`.
- **Effective duration** (bump and reprice: `(P_− − P_+) / (2 P Δi)`) is the one to use
  when cash flows depend on rates (callable bonds, lapse-sensitive liabilities).
- Zero-coupon bond: D = maturity. Coupon bond: D < maturity. Perpetuity: D = (1+i)/i.

## 3. Redington immunisation
For assets A and liabilities L at rate i, protect surplus `S = PV_A − PV_L` against small
parallel shifts:
1. `PV_A = PV_L`
2. `D_A = D_L` (equal durations, same convention)
3. `C_A > C_L` (assets more spread out around the liability duration)
Then S has a local minimum at i: small rate moves either way increase surplus.
**Full immunisation** (single liability, parallel shifts of any size): assets with cash flows on
both sides of the liability date, meeting the three conditions above (a barbell with PV and duration matched shows non-negative surplus for the shifts tested, -400bp to +500bp).

### Worked shape
Liability 1,000 due at year 10, i = 5%. Barbell: zero-coupons at years 5 and 15.
Solve `x v^5 + y v^15 = 1000 v^10` and `5 x v^5 + 15 y v^15 = 10 · 1000 v^10`:
equal PV split between them works because 5 and 15 average to 10. Check convexity:
barbell > bullet, so condition 3 holds.

## 4. Limits — say these out loud
- Only for **small, parallel** shifts of a **flat** curve. Twists break it; use key-rate
  durations for non-parallel risk.
- Duration drifts with time and rates: rebalance.
- Cash-flow matching removes reinvestment risk entirely but costs more.
- Credit, liquidity and optionality are outside the model.

## Uncertainty notes
Formulas are standard textbook results; D, D_mod, convexity (`Σ t(t+1)CF v^{t+2}/P`) and perpetuity D = (1+i)/i were recomputed numerically (bump-and-reprice agrees to 6+ digits). Which exam syllabus covers them is not confirmed (gated: unconfirmed, source is paywalled or blocked). In the barbell example (1,000 at year 10, i = 5%, equal PV at years 5 and 15) the surplus recomputes as +0.18 at -50bp, +0.17 at +50bp and +2.3 at +200bp, so equal PV split is right when the dates are symmetric about the liability date; solve numerically for asymmetric dates.

## Verify
- [ ] Rate convention (effective vs nominal, per period) is consistent throughout.
- [ ] Bump-and-reprice ΔP matches −D_mod·Δi·P to first order for a 1bp move.
- [ ] PV_A = PV_L and D_A = D_L at the valuation rate.
- [ ] C_A > C_L; surplus rises for ±50bp test shifts.
- [ ] Non-parallel shift and rebalancing limitations stated.
