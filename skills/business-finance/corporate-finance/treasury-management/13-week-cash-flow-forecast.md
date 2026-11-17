---
id: business-finance.corporate-finance.treasury-management.13-week-cash-flow-forecast
name: 13-week-cash-flow-forecast
category: business-finance
field: corporate-finance
product: treasury-management
tags: [treasury-management, treasury, cash-flow-forecast, 13-week-cash-flow, twcf, direct-method, liquidity, liquidity-management, cash-runway, headroom, covenants, revolving-credit-facility, rcf, minimum-cash, receipts-and-disbursements, variance-to-forecast, working-capital, cash-management, restructuring, fx-exposure]
level: practitioner
status: draft
description: "Build and run a direct-method 13-week cash flow forecast: receipts and payments by week, opening-to-closing cash, facility headroom and covenants, weekly actual-vs-forecast."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# 13-week cash flow forecast

**Goal:** know, week by week for the next quarter, how much cash you'll have, how
close you get to your minimum or facility limits, and what to do before it bites. The
13-week forecast (TWCF) is the standard short-term liquidity tool for treasurers,
lenders and turnaround teams.

## 1. Use the direct method
Forecast **actual receipts and payments**, not profit. Indirect (profit ± working
capital) is fine for months and years but useless for "can we make payroll in week 6".

## 2. Layout (one column per week, Monday–Sunday or matching payment runs)
```
Opening cash (= prior week closing; week 1 = bank balance)
RECEIPTS
  Customer receipts (from AR aging + new sales)
  Other receipts (tax refunds, asset sales, intercompany)
DISBURSEMENTS
  Payroll and payroll taxes (exact dates)
  Suppliers – trade (from AP aging + new purchases × terms)
  Rent, utilities, insurance
  Taxes (VAT/GST, income tax instalments)
  Capex
  Interest and debt repayments
Net operating cash flow
Facility drawdown / (repayment)
Closing cash
Facility: limit, drawn, available headroom
Minimum cash requirement, covenant tests
```

## 3. Building each line
- **Customer receipts:** start from the AR aging by customer; apply each major
  customer's **actual payment behaviour** (days past terms historically), not the
  contractual terms. Add new invoicing from the sales forecast × collection lag.
  Large customers: forecast individually.
- **Supplier payments:** AP aging plus forecast purchases, timed to your **payment
  run** dates. This is the main lever — stretching or accelerating it is a decision,
  so make it visible.
- **Payroll, rent, debt service, taxes:** known amounts on known dates. Get these
  exactly right; they're non-negotiable and lumpy.
- **One-offs:** list separately with a description.

## 4. Run it weekly
1. Roll forward: drop the past week, add week 14.
2. **Actual vs forecast** for the past week by line. Explain any variance over a
   threshold. Persistent misses on one line (usually receipts) mean the method for
   that line is wrong — fix the method, not just the number.
3. Reconcile **opening cash to bank balances** (all accounts, including restricted
   or trapped cash, which should be shown separately).
4. Check headroom against the **minimum liquidity** level and facility covenants.

## 5. When the low point is too low
Levers, roughly by speed: delay discretionary capex; chase overdue debtors (top 10
by value); draw committed facilities *before* covenants tighten; negotiate supplier
terms; sell surplus inventory or assets; tax payment arrangements; equity or new
debt. Show each lever's effect as a separate scenario line.

## Gotchas
- **Month-end and quarter-end lumps** (payroll, rent, VAT) hide in monthly forecasts
  — the weekly view exists to find them.
- **Uncleared cheques / payment float** make bank balance ≠ ledger cash; forecast
  from the bank.
- **Trapped cash** in other countries or subsidiaries isn't available for group
  payments without cost or delay.
- **Multi-currency:** forecast in transaction currency, convert at a stated rate;
  show the FX exposure separately.
- Covenant definitions (e.g. minimum liquidity, leverage) come from the facility
  agreement, not the forecast template — read the document.

## Verify
- [ ] Week 1 opening cash ties to actual bank balances (all accounts).
- [ ] Payroll, rent, debt service and tax dates are exact.
- [ ] Receipts use observed customer payment behaviour.
- [ ] Weekly actual-vs-forecast reviewed and variance causes logged.
- [ ] Low-point week, headroom and covenant tests visible on the summary.
