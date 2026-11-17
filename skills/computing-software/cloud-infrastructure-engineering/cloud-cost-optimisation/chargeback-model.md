---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.chargeback-model
name: chargeback-model
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, chargeback, chargeback-model, internal-billing, tariff-model]
level: advanced
status: docs-checked
description: "Design the chargeback model with finance: what to charge, shared-cost and commitment treatment, timing, true-ups and who owns corrections."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/", "https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chargeback model design

Chargeback is the formal step of sending expenses to official accounting budgets, so each profit and loss owner bears the
cost of what it consumes. It is optional: when technology costs go to a single or easily allocated set of cost centres,
the extra cost of official chargeback may not be warranted. Showback is always required; neither is more mature.

## Decisions to make with finance
1. **Granularity and cost centres**: the cost centre hierarchy and general ledger codes come from finance and accounting;
   a flat hierarchy limits chargeback detail.
2. **Allocation method**: tagging and allocation strategy sets how finely ownership can be assigned (Allocation capability).
3. **Shared costs**: decide whether each shared item is held centrally or allocated on consumption. The Allocation page
   names fixed, proportional and proxy-metric methods, and the "informed ignore" choice to budget a shared item centrally.
4. **Commitment discounts**: charge them to the account that bought them, hold them centrally, or charge teams by their
   consumption of the discount. The maturity model moves towards consumption-based charging.
5. **Cost metric**: which cost elements and metrics appear in the chargeback report, and the currency of the chargeback
   file (currency conversion kept distinct at higher maturity).
6. **Timing and estimates**: invoices arrive some days after month end and usage data can arrive late, so an estimate
   may be charged first and trued up when data is complete.
7. **Corrections**: how chargeback is corrected after the period has closed.

## Gotchas
- Estimates with no true-up leave a persistent gap between charges and the ledger.

## Verify
- [ ] The written model is agreed by finance and accounting.
- [ ] Chargeback totals reconcile to provider invoices (the capability tracks the general ledger recharge rate: spend
      recorded as a journal divided by total provider spend for the month).

## Checked
Confirmed against the FinOps Invoicing and Chargeback and Allocation capability pages: optionality of chargeback and
that showback is always required, finance-owned cost centre hierarchy and GL codes, shared cost choices including
"informed ignore" and fixed, proportional and proxy-metric methods, commitment discount charging at Crawl, Walk and Run,
estimates with true-up, corrections after close, currency conversion, and the general ledger recharge rate KPI.
Removed: the model table (pass-through, tariff, fixed, hybrid), amortised versus net amortised guidance, tariff rate
setting formula and quarterly review, year-end true-up, intercompany and transfer pricing, and the perverse-incentive
and chargeback-before-showback claims. The cited how-to-build-a-chargeback-model page returned 404 and was dropped from sources.
Method: docs-checked 2026-11-09 against the FinOps Framework Invoicing and Chargeback and Allocation pages.
