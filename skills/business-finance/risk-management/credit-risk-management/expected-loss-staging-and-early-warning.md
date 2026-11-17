---
id: business-finance.risk-management.credit-risk-management.expected-loss-staging-and-early-warning
name: expected-loss-staging-and-early-warning
category: business-finance
field: risk-management
product: credit-risk-management
tags: [credit-risk-management, risk-management, credit-risk, expected-loss, pd, lgd, ead, probability-of-default, loss-given-default, exposure-at-default, ccf, ifrs-9, ecl, expected-credit-loss, stage-1, stage-2, stage-3, sicr, significant-increase-in-credit-risk, cecl, provisioning, watch-list, early-warning-indicators, concentration-risk, exposure-limits, forward-looking-scenarios]
level: advanced
status: gated
description: "Manage a loan book's credit risk: compute expected loss from PD, LGD and EAD, stage exposures under IFRS 9 (or CECL), set limits, and run an early-warning watch list that acts before default."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expected loss, staging and early warning — manage credit risk across the book

**Goal:** know how much the portfolio is expected to lose, provision for it correctly, keep
concentrations within limits, and spot deteriorating borrowers while there's still time to act.

## 1. Expected loss = PD × LGD × EAD
- **PD** — probability the borrower defaults over the horizon (12 months or lifetime).
  From internal rating models, scorecards, or external ratings mapped to default rates.
- **LGD** — share of the exposure lost if they default, after recoveries and costs. Driven
  by seniority, collateral type and haircut, time to recover, and discounting. Unsecured
  corporate LGD is often modelled around 40–50% and secured lower (gated: unconfirmed, source is paywalled or blocked) — *calibrate to your own
  recovery data where you have it*.
- **EAD** — exposure when default happens: drawn balance plus a **credit conversion factor
  (CCF)** of undrawn commitments (borrowers draw down revolving lines as they weaken).
Example: €2M drawn + €1M undrawn × 50% CCF = €2.5M EAD; PD 2%; LGD 45% → EL ≈ €22.5k a year (computed: 2.5M × 2% × 45% = 22,500).
EL is a cost of doing business to be priced in; **unexpected loss** (variance around EL) is
what capital covers.

## 2. Provisioning: IFRS 9 staging (and CECL)
Under **IFRS 9** expected credit loss:
- **Stage 1** — performing, no significant increase in credit risk since origination: 12-month ECL.
- **Stage 2** — **significant increase in credit risk (SICR)** since origination: lifetime ECL.
  The standard has a rebuttable presumption that **30 days past due** means SICR (gated: unconfirmed, source is paywalled or blocked); most banks
  also use relative PD deterioration thresholds, watch-list status and forbearance.
- **Stage 3** — credit-impaired (default; **90 days past due** is the rebuttable presumption (gated: unconfirmed, source is paywalled or blocked)):
  lifetime ECL, interest on net carrying amount.
ECL must be **probability-weighted across forward-looking macro scenarios** (e.g. base,
upside, downside) — not just the base case.
Under US GAAP **CECL**, there are no stages: lifetime expected losses from day one.
*Accounting policy details (SICR thresholds, scenario weights) are entity-specific and audited.*

## 3. Limits and concentration
- Single-name and connected-group limits (as % of capital); sector, geography, product and
  rating-grade limits.
- Monitor large exposures against regulatory thresholds (e.g. the Basel large-exposures
  framework caps exposure to a counterparty group at 25% of Tier 1 capital (gated: unconfirmed, source is paywalled or blocked) — *confirm your
  local implementation*).
- Track concentration with simple measures (top-20 exposures as % of book, HHI by sector).

## 4. Early warning and the watch list
Define **early-warning indicators** (EWIs) and review them monthly:
- Financial: covenant headroom shrinking, falling DSCR/interest cover, rising leverage,
  late financial statements, qualified audit opinion.
- Behavioural: utilisation creeping to the limit, cheque/payment returns, days past due
  even of a few days, overdraft hardcore.
- External: rating downgrades, widening CDS/bond spreads, negative news, loss of a key customer,
  management departures.
Triggered names go on the **watch list** with an owner, an action plan (more information,
tightened terms, more collateral, reduced limits, exit) and a review date. Moving early
from "watch" to restructuring or workout is where most of the recovery value is preserved.

## 5. Reporting
Monthly: portfolio by rating grade and stage, migration matrix (grade movements), stage
transfers, ECL movement analysis (new lending, repayments, stage moves, model changes,
write-offs), limit breaches, watch-list changes.

## Gotchas
- Using through-the-cycle PDs for IFRS 9, which needs point-in-time, forward-looking PDs.
- Ignoring undrawn commitments in EAD.
- Collateral values out of date — revalue on a schedule and on triggers.
- Cliff effects at the stage 1→2 boundary make provisions jump; explain them in reporting.
- Watch lists that only grow: every name needs an exit — back to normal, or to workout.
- Management overlays to ECL must be documented, justified and periodically released or embedded.

## Verify
- [ ] EL computed with PD, LGD and EAD (including CCF on undrawn) per exposure.
- [ ] Staging criteria (SICR, default) documented and applied; multiple weighted scenarios used.
- [ ] Limits defined and monitored; top exposures and sector concentration reported.
- [ ] EWIs defined; every watch-list name has an owner, plan and review date.
- [ ] Monthly report includes migration and an ECL movement walk.

Related: business-finance.risk-management.financial-risk-modelling.historical-var-and-backtesting.
