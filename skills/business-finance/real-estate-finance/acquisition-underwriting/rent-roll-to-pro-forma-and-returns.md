---
id: business-finance.real-estate-finance.acquisition-underwriting.rent-roll-to-pro-forma-and-returns
name: rent-roll-to-pro-forma-and-returns
category: business-finance
field: real-estate-finance
product: acquisition-underwriting
tags: [acquisition-underwriting, real-estate-finance, commercial-real-estate, cre, rent-roll, t12, trailing-twelve, operating-statement, noi, net-operating-income, cap-rate, going-in-cap-rate, exit-cap-rate, pro-forma, dcf, levered-irr, unlevered-irr, equity-multiple, cash-on-cash, vacancy, credit-loss, capex-reserve, tenant-improvements, leasing-commissions, walt, mark-to-market, sensitivity-analysis]
level: advanced
status: draft
description: "Underwrite a property acquisition: scrub the rent roll and T-12, rebuild NOI, project cash flows to an exit cap rate, and report IRR and equity multiple with sensitivities."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rent roll to pro forma and returns — underwrite what the building will really earn

**Goal:** turn the seller's marketing numbers into your own defensible view of NOI and
returns, so the price you offer reflects the actual leases and costs, not the broker's story.

## 1. Scrub the rent roll
For each unit/tenant: area, lease start and expiry, current rent, escalations, options
(renewal, break/termination, expansion), recoveries (who pays taxes, insurance, service
charges), free-rent or abatement periods, security deposit, arrears.
- **Tie it to leases** — read at least the largest tenants' leases and a sample of others.
  Rent rolls routinely omit concessions and side letters.
- Compute **WALT** (weighted average lease term, by income) and the **rollover schedule**:
  how much income expires each year. A 40% expiry in year 2 is a different deal from the
  same NOI spread evenly.
- **Mark-to-market:** compare in-place rents to market rents. Below-market leases are upside
  at expiry; above-market leases are risk.
- Check tenant credit and arrears; get **estoppel certificates** before closing.

## 2. Normalise the operating statement (T-12)
Start from the trailing-twelve-month statement and the seller's budget, then adjust:
- Remove one-offs (insurance claim income, a lawsuit settlement).
- **Re-assess property tax** — many jurisdictions reassess on sale; the buyer's bill can be much
  higher. *Check the local reassessment rules.*
- Use your own **management fee** (often a % of effective gross income) even if the seller
  self-manages.
- Insurance at today's quote, not last year's premium.
- Include **reserves for capital expenditure** below NOI or above it consistently
  (lenders and buyers differ on convention — state yours).

## 3. Build stabilised NOI
Potential gross income at contract rents
− vacancy and credit loss (market vacancy, not the building's current 0%)
+ recoveries and other income
= effective gross income (EGI)
− operating expenses
= **NOI**

**Going-in cap rate** = year-1 NOI ÷ purchase price. Compare with recent sales of
comparable properties, adjusted for quality and lease profile.

## 4. Project the cash flow (typically 5–10 years)
- Lease by lease where possible: contract rent until expiry, then **renewal probability**
  (e.g. 60–75%, by property type and market — an assumption, state it) blending a renewal
  rent with a new-tenant rent after **downtime**.
- On rollover: **tenant improvements (TI)** and **leasing commissions (LC)**, plus free rent.
- Market rent growth, expense growth, capex plan.
- **Exit value** = forward-year NOI at sale ÷ **exit cap rate**. Set the exit cap at or above
  the going-in cap (often +25–50 bps) to reflect an older building and uncertainty;
  less selling costs.

## 5. Returns
- **Unlevered IRR** on purchase price + closing costs and the property cash flows.
- **Levered IRR**, **equity multiple** (total distributions ÷ equity invested) and
  **cash-on-cash** (annual cash flow after debt service ÷ equity) once debt is layered in.
- Check that leverage is accretive: if the unlevered return is below the cost of debt,
  leverage is reducing returns and increasing risk.

## 6. Sensitivities
Run tables for exit cap rate × rent growth, and vacancy × downtime. Report the price at
which you hit your target return — that's your maximum bid, not the asking price.

## Gotchas
- Underwriting from the offering memorandum's "pro forma" NOI (with lease-up already
  assumed) instead of in-place NOI.
- Forgetting free rent: headline rent on a new lease overstates cash in early years.
- An exit cap rate *below* the going-in rate quietly manufactures most of the return.
- Annual vs monthly IRR timing and mid-year conventions change results; be consistent.
- Deferred maintenance found in the property condition report belongs in day-one capex.

## Verify
- [ ] Rent roll reconciled to leases and to the T-12 rental income.
- [ ] Rollover schedule and WALT calculated; major expiries have explicit assumptions.
- [ ] NOI rebuilt with reassessed taxes, own management fee, market vacancy.
- [ ] Exit cap ≥ going-in cap unless explicitly justified.
- [ ] Unlevered and levered IRR, equity multiple and sensitivities reported; max bid stated.

Related: business-finance.real-estate-finance.commercial-mortgage-underwriting; business-finance.real-estate-finance.argus.
