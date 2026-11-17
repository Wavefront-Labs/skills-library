---
id: business-finance.real-estate-finance.development-finance.residual-land-value-appraisal
name: residual-land-value-appraisal
category: business-finance
field: real-estate-finance
product: development-finance
tags: [development-finance, real-estate-finance, development-appraisal, residual-land-value, rlv, residual-valuation, gdv, gross-development-value, build-costs, developer-profit, profit-on-cost, profit-on-gdv, finance-costs, s-curve, construction-loan, ltc, loan-to-cost, ltgdv, contingency, planning-obligations, affordable-housing, sensitivity-analysis, argus-developer, estate-master]
level: advanced
status: gated
description: "Run a development appraisal to find what a site is worth: GDV less build, fees, finance and target profit leaves residual land value, then stress it with sensitivities and an S-curve."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Residual land value appraisal — what can you afford to pay for the site?

**Goal:** work backwards from what the finished scheme will be worth to the maximum price
you can pay for the land while still earning your target profit — and see how fragile
that number is.

## 1. The residual equation
```
Gross development value (GDV)
− construction costs (incl. external works, contingency)
− professional fees
− planning / statutory costs (obligations, levies, affordable-housing contribution)
− marketing, letting and sales costs
− finance costs
− developer's target profit
= residual land value (including land acquisition costs: tax, legal, agent)
```
Back out land acquisition costs (e.g. stamp duty / transfer tax, legal, agents) to get the
net price you can offer.

## 2. Each input, and where it goes wrong
- **GDV** — for sale: unit-by-unit prices from current comparable new-build sales (not
  asking prices), less incentives. For investment: rent ÷ yield, less purchaser's costs.
  Don't assume market growth unless you label the appraisal "growth-explicit".
- **Construction costs** — from a cost consultant / QS, per m² of gross internal area,
  with **contingency** (often ~5% for new build on a clean site, more for refurbishment
  or poor ground — a judgement, state it). Include demolition, abnormals, utilities.
- **Professional fees** — architects, engineers, project manager, often quoted ~8–15% of
  build cost depending on complexity.
- **Finance** — model the actual cash-flow timing (below). Interest on land from day one,
  on build costs as they're drawn; plus arrangement and exit fees.
- **Developer's profit** — expressed as a % of **GDV** or of **cost**. Lenders and
  local planning viability guidance often quote ranges like **15–20% of GDV** for private
  residential; commercial and lower-risk schemes may use lower. *Know which basis your
  stakeholders mean: 20% on cost = 16.7% on GDV (computed: 0.2/1.2).* The 15–20% of GDV range and the 8–15% fee and ~5% contingency figures are unsourced (gated: unconfirmed, source is paywalled or blocked).

## 3. Use a cash-flow, not a single-line finance estimate
A quick appraisal approximates finance as interest on half the build cost over the build
period. A proper one uses a monthly cash flow:
- Land paid at month 0; pre-construction period (planning discharge, procurement).
- Build costs spread on an **S-curve** (slow start, peak mid-build, tail).
- Sales receipts after practical completion at an assumed sales rate (units per month),
  with deposits if applicable.
- Interest compounded monthly on the negative balance.
The residual land value is solved so the scheme hits target profit (goal-seek), or you
report profit for a given land price. Specialist tools (e.g. ARGUS Developer, Estate
Master) do this; a spreadsheet works for simple schemes.

## 4. Lender view
Construction lenders size by **loan-to-cost (LTC)** and **loan-to-GDV (LTGDV)**, require
equity in first (land often counts), drawdowns certified monthly by a monitoring
surveyor against work done, and a cost-to-complete test before each draw. Mezzanine raises
leverage at a much higher price. Model the facility limits so you know when equity must go in.

## 5. Sensitivities
Residual land value is highly geared: small changes in GDV or cost move land value a lot.
Run a two-way table of **sales values ±5–10%** vs **build costs ±5–10%**, plus a delay
scenario (+3–6 months build, slower sales). Show the land price at which profit falls to zero.

## Gotchas
- Using today's GDV with tomorrow's (inflated) build costs, or vice versa — be consistent.
- Gross vs net area confusion: GDV on net saleable area, costs on gross internal area.
- Forgetting VAT/sales-tax treatment of costs and sales (recoverable or not).
- Ignoring planning obligations that only emerge in negotiation with the local authority.
- Treating contingency as profit. It will be spent.
- Exit strategy: if units don't sell, can the loan be refinanced onto a rental (investment) basis?

## Verify
- [ ] GDV supported by comparable evidence, unit by unit.
- [ ] Build costs from a cost consultant, with explicit contingency.
- [ ] Profit target and its basis (GDV or cost) stated.
- [ ] Monthly cash flow with S-curve and realistic sales rate; finance costs from the cash flow.
- [ ] Sensitivity table produced; break-even land price known.

Related: business-finance.real-estate-finance.argus; business-finance.real-estate-finance.commercial-mortgage-underwriting.loan-sizing-dscr-ltv-debt-yield.
