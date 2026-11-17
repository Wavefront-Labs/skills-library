---
id: engineering-technology.petroleum-engineering.reservoir-engineering.decline-curve-analysis-and-reserves
name: decline-curve-analysis-and-reserves
category: engineering-technology
field: petroleum-engineering
product: reservoir-engineering
tags: [decline-curve-analysis, dca, arps, exponential-decline, hyperbolic-decline, harmonic-decline, b-factor, terminal-decline, modified-hyperbolic, eur, reserves, prms, sec-reserves, 1p-2p-3p, proved-reserves, pud, material-balance, p-over-z, havlena-odeh, unconventional, shale, type-curve, rate-time]
level: practitioner
status: gated
description: "Fit Arps exponential/hyperbolic/harmonic declines, apply terminal decline for shale wells, compute EUR and classify 1P/2P/3P under PRMS and SEC rules with material-balance checks."
sources:
  - "Arps, J.J., Analysis of Decline Curves (Trans. AIME, 1945)"
  - "SPE/WPC/AAPG/SPEE/SEG/SPWLA/EAGE Petroleum Resources Management System (PRMS, 2018)"
  - "US SEC Modernization of Oil and Gas Reporting (Regulation S-X Rule 4-10, 2008)"
  - "SPEE Monograph 3, Guidelines for the Practical Evaluation of Undeveloped Reserves in Resource Plays"
  - "Ahmed, Reservoir Engineering Handbook"
  - "Havlena & Odeh, The Material Balance as an Equation of a Straight Line (JPT, 1963)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decline-curve analysis and reserves — from rate history to a defensible EUR and category

**Goal:** turn a well's (or group's) production history into a forecast and EUR you can book under PRMS or SEC rules, and sanity-check it against volumetrics and material balance.

## 1. Prepare the data

- Use rate per producing day (calendar rate understates during downtime). Flag shut-ins, workovers, choke changes, artificial-lift installs and offset frac hits; decline only fits periods of constant operating conditions.
- Plot log(q) vs t, log(q) vs cumulative Np, and log-log q vs t. A straight line on semilog q–t is exponential; on q–Np it is also exponential (q = qi − D·Np).
- Normalise to pressure (q/Δp) if flowing pressure changed a lot; Arps assumes roughly constant BHP and boundary-dominated flow.

## 2. Arps equations (nominal decline Di, per unit time)
Checked numerically (qi 1000, Di 0.5/yr, b 0.8, t 3 yr): the hyperbolic Np closed form 1789.03 equals the numerical integral of q(t); effective decline 1 − (1 + b·Di)^(−1/b) = 0.343 versus exponential 0.393.

| Type | b | Rate | Cumulative |
|---|---|---|---|
| Exponential | 0 | q = qi·e^(−Di·t) | Np = (qi − q)/Di |
| Hyperbolic | 0<b<1 (≥1 shale) | q = qi/(1 + b·Di·t)^(1/b) | Np = qi^b/((1−b)Di)·(qi^(1−b) − q^(1−b)) |
| Harmonic | 1 | q = qi/(1 + Di·t) | Np = (qi/Di)·ln(qi/q) |

Effective annual decline: exponential De = 1 − e^(−D); hyperbolic secant-effective De = 1 − (1 + b·Di)^(−1/b). State which convention you use; software differs (software differs in tangent versus secant effective inputs (gated: unconfirmed, source is paywalled or blocked)).

Typical b in boundary-dominated conventional flow: solution-gas drive 0.3–0.5, gravity drainage ~0.5, water drive/strong pressure support 0.5–1, depletion gas 0.4–0.5 (gated: unconfirmed, source is paywalled or blocked). b > 1 is physically transient flow, not boundary-dominated.

## 3. Unconventionals: modified hyperbolic

Shale/tight wells show linear flow (b ≈ 2 in the transient regime) for years. Fitting b = 1.5–2 forever gives infinite-looking EURs. Use a **modified hyperbolic**: hyperbolic with fitted b (commonly 0.8–1.5 for regulators/auditors (gated: unconfirmed, source is paywalled or blocked)) until the instantaneous decline falls to a terminal Dmin, then exponential at Dmin. Common Dmin choices are 5–10%/yr effective for oil, 5–8% for gas; reviewers often expect about 6% (gated: unconfirmed, source is paywalled or blocked). These are conventions, not physics — check your auditor's or company's guideline. Alternatives: Duong, stretched-exponential (SEPD), or transient-hyperbolic models, and type-wells built from analogues for undeveloped locations (SPEE Monograph 3).

## 4. EUR and economic limit

EUR = cumulative to date + forecast to the economic limit q_el, where q_el = operating cost / (net price × net revenue interest) per unit. Cap by well life or licence expiry. Record the forecast segments (qi, Di, b, Dmin, switch time) so others can reproduce it.

## 5. Classify reserves

**PRMS:** reserves must be discovered, recoverable, commercial and remaining, with a development plan. 1P (proved) — reasonable certainty, ≥90% probability that actual ≥ estimate if probabilistic; 2P (proved + probable) — best estimate, P50; 3P (+ possible) — P10 (PRMS text not fetched, (gated: unconfirmed, source is paywalled or blocked); the 90% figure for SEC reasonable certainty was confirmed in 17 CFR 210.4-10(a)(24)). Sub-classify by maturity: developed producing (PDP), developed non-producing (PDNP), undeveloped (PUD).

**SEC (Rule 4-10, 17 CFR 210.4-10, eCFR checked):** price is the unweighted arithmetic average of first-day-of-month prices over the prior 12 months ((a)(22)(v)); undrilled locations qualify as undeveloped only if scheduled to be drilled within five years, unless specific circumstances justify longer ((a)(31)(ii)); reserves on undrilled acreage are limited to locations directly adjacent to development spacing areas reasonably certain to produce, and reach farther only where reliable technology establishes reasonable certainty ((a)(31)(i)). Whether filings may include probable and possible reserves was not in the section text read; check the current SEC rules ((gated: unconfirmed, source is paywalled or blocked)). Check the current SEC guidance and C&DIs for edge cases.

## 6. Material balance and volumetric sanity checks

- Gas: plot p/z vs Gp. A straight line extrapolated to p/z = 0 gives OGIP; upward curvature suggests water drive or compaction. DCA EUR should be below OGIP × a plausible RF (70–90% volumetric depletion gas (gated: unconfirmed, source is paywalled or blocked)).
- Oil: Havlena–Odeh F = N(Eo + m·Eg + Efw) + We; F/Eo vs We/Eo or a straight-line plot identifies drive mechanism and N. Compare EUR/N with typical recovery: solution-gas 5–30%, waterflood 30–50%, strong water drive up to ~60% (gated: unconfirmed, source is paywalled or blocked).
- Unconventional: compare against analogue type-well percentiles in the same bench/landing zone and completion vintage.

Cross-check full-field forecasts with simulation (engineering-technology.petroleum-engineering.petrel-eclipse.building-an-eclipse-simulation-deck).

## Gotchas

- Fitting through early flush/cleanup or choke-managed periods gives absurd b and Di.
- Unit confusion: nominal vs effective, monthly vs annual decline — a 70%/yr effective is not 70%/yr nominal.
- Hyperbolic cumulative formula fails at b = 1 (use harmonic) and b = 0 (use exponential).
- Rate-limited (facility-constrained) wells show flat rate, not decline; don't fit until decline starts.
- Do not aggregate wells of different vintage and then fit one curve; the sum of exponentials looks hyperbolic.

## Verify

- [ ] Fit window excludes operational changes and is stated.
- [ ] Parameters (qi, Di convention, b, Dmin, q_el) are recorded and reproducible.
- [ ] EUR ≤ in-place × reasonable recovery factor for the drive mechanism.
- [ ] Shale forecasts switch to terminal decline; b > 1 not extrapolated indefinitely.
- [ ] Category (1P/2P/3P, PDP/PUD) satisfies PRMS or SEC criteria, including the 5-year PUD rule for SEC.
- [ ] Economic limit uses the correct price deck for the reporting basis.
