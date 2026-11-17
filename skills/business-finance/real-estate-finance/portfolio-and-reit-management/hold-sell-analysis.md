---
id: business-finance.real-estate-finance.portfolio-and-reit-management.hold-sell-analysis
name: hold-sell-analysis
category: business-finance
field: real-estate-finance
product: portfolio-and-reit-management
tags: [portfolio-and-reit-management, real-estate-finance, hold-sell-analysis, disposition, asset-management, forward-irr, hold-irr, opportunity-cost, capital-recycling, reit, ffo, affo, nav, net-asset-value, portfolio-strategy, concentration-risk, capex, lease-rollover, transaction-costs, tax-basis, 1031-exchange, investor-reporting, fund-life]
level: advanced
status: gated
description: "Decide whether to hold or sell an asset in a real estate portfolio: forward hold IRR vs sale proceeds redeployed, capex and rollover ahead, taxes and costs, and fit with portfolio strategy."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hold/sell analysis — should this asset stay in the portfolio?

**Goal:** make each annual hold/sell call on forward-looking numbers. The question is not
"did this asset do well?" but "from today's value, does holding it beat selling it and
putting the money somewhere else?"

## 1. Frame the comparison correctly
- **Sell today:** net proceeds = today's market value − selling costs − debt repayment
  (including prepayment penalties / swap break costs) − tax on sale.
- **Hold:** future cash flows from today to a later sale date (typically 3–5 years forward)
  plus net sale proceeds then.
- **Forward (hold) IRR** = the IRR of *today's net sale proceeds* as the notional investment
  against the hold cash flows. Ignore the historic purchase price — it's sunk.
- Compare forward IRR with the **target return for reinvestment**: what the capital would
  earn in its next-best use (a new acquisition at today's pricing, debt paydown, a share
  buyback for a REIT, distribution to investors in a fund).

## 2. Model the next few years honestly
- **Lease rollover** — major expiries in the hold window and their TI/LC/downtime cost.
- **Capex** — roof, plant, ESG/energy-performance upgrades (increasingly mandatory in some
  markets — *check local minimum energy standards*). Assets facing a big capex bill often
  sell better before it, if buyers don't price it fully, or after it, if the upgrade
  unlocks rent.
- **Market view** — rent growth, cap-rate direction for this sector and location.
- **Debt** — upcoming maturity and refinance terms; a loan that refinances at a much higher
  rate changes the levered hold return.

## 3. Count the frictions
Selling costs (agents, legal, transfer taxes for the buyer reflected in price), break costs,
tax on the gain (and depreciation recapture where applicable), and the time and cost to
redeploy the cash (cash drag). In the US, a **1031 like-kind exchange** can defer tax for
private owners (gated: unconfirmed, source is paywalled or blocked); REITs and funds have their own rules. *Tax treatment is jurisdiction- and
structure-specific — take tax advice.*

## 4. Portfolio-level lens
An asset with an acceptable standalone forward IRR may still be a sale if:
- it creates **concentration** (one tenant, one city, one sector) beyond the strategy's limits;
- it no longer fits the stated strategy (core fund holding a value-add asset, or vice versa);
- it is sub-scale and costs disproportionate management time;
- the **fund's life** requires disposals before the end of the term.
And a weak-IRR asset may be held if selling now would crystallise a loss in a thin market
that is likely to recover — document that as a market call, not a default.

## 5. REIT angle
For listed REITs, the decision also shows up in reported metrics:
- **FFO** (funds from operations — net income excluding gains/losses on property sales and
  real estate depreciation, per the Nareit definition (gated: unconfirmed, source is paywalled or blocked)) falls when income-producing assets are sold.
- **AFFO** further deducts recurring capex and straight-line rent adjustments — company
  definitions vary.
- **NAV** per share: selling above book/NAV and buying back shares trading at a discount to
  NAV can be accretive; selling below NAV is dilutive.
Communicate the capital-recycling logic to investors, not just the gain.

## 6. Decide and document
Present: forward hold IRR vs reinvestment hurdle; sale proceeds; key risks of holding;
portfolio fit; recommendation; and what would change it (e.g. "sell if the anchor tenant
doesn't renew by Q2"). Re-run annually or on a trigger.

## Gotchas
- Anchoring on purchase price ("we can't sell below what we paid").
- Comparing a levered hold IRR with an unlevered reinvestment return — match the basis.
- Ignoring that the broker's opinion of value may differ from what a buyer will pay in a
  thin market; consider a range.
- Forgetting debt prepayment penalties (yield maintenance, defeasance) that can wipe out the gain.

## Verify
- [ ] Hold IRR calculated from today's net sale value, not historic cost.
- [ ] Rollover, capex and refinancing in the hold window modelled.
- [ ] All selling frictions and taxes included.
- [ ] Reinvestment hurdle stated on the same (levered/unlevered) basis.
- [ ] Portfolio concentration and strategy fit assessed; recommendation with triggers documented.

Related: business-finance.real-estate-finance.acquisition-underwriting.rent-roll-to-pro-forma-and-returns.
