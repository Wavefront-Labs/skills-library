---
id: business-finance.accounting.erp-systems.erp-period-end-close-and-subledger-tie-out
name: erp-period-end-close-and-subledger-tie-out
category: business-finance
field: accounting
product: erp-systems
tags: [erp-systems, erp, sap, sap-s4hana, oracle, oracle-fusion, netsuite, dynamics-365, general-ledger, period-close, posting-periods, subledger, subledger-reconciliation, gr-ir, goods-receipt-invoice-receipt, intercompany, fx-revaluation, accrual-reversal, close-calendar, financial-close, journal-approval, document-flow]
level: advanced
status: draft
description: "Run period-end close in an ERP (SAP, Oracle, NetSuite, Dynamics): period controls, subledger-to-GL tie-outs, GR/IR, intercompany, FX revaluation and close calendar."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ERP period-end close and subledger tie-out

**Goal:** close the month in an enterprise ERP on a fixed calendar, with every
subledger agreeing to the general ledger and no postings sneaking into a closed
period. The concepts are the same across SAP S/4HANA, Oracle Fusion, NetSuite and
Dynamics 365; screen and transaction names differ and are given only as rough
pointers (**not verified per release**).

## 1. How postings reach the GL
Operational modules post automatically: sales orders → billing → AR; purchase orders →
goods receipt → supplier invoice → AP; inventory movements; fixed-asset depreciation;
payroll interface. Each creates a document with a **document number** and posts to
**reconciliation/control accounts** that can't take manual journals. Know your
document flow: most close problems are documents stuck between steps.

## 2. Period controls
- Posting periods are opened/closed by module and account range (SAP: posting period
  variant; Oracle: period statuses per ledger and subledger; NetSuite: accounting
  period close checklist with AP/AR/All locks).
- Close order: lock **operational subledgers** first (AR, AP, inventory) on day 1–2,
  then post GL adjustments, then close the GL. Keep a "special period" or adjustments
  period for year-end audit entries, if your ERP supports it.
- Restrict who can reopen a period; log every reopening.

## 3. A close calendar (working days)
- **WD-2 to WD0:** cut-off reminders; clear workflow queues (unapproved invoices,
  parked/held documents).
- **WD1:** goods-receipt and billing cut-off; run accrual and recurring journals;
  depreciation run; payroll journal.
- **WD2:** **FX revaluation** of open foreign-currency items and balances; intercompany
  invoicing and matching.
- **WD3:** subledger tie-outs, GR/IR analysis, balance-sheet reconciliations.
- **WD4–5:** consolidation, eliminations, reporting, review and sign-off.

## 4. Tie-outs that must hold
- **AR aging total = AR reconciliation account(s)**; **AP aging = AP account(s)**.
  Differences usually come from posting dates vs key dates, or reports run on a
  different ledger/currency.
- **Inventory valuation report = inventory GL accounts.**
- **Asset register net book value = fixed-asset accounts.**
- **GR/IR (goods received not invoiced / invoiced not received):** analyse by PO.
  Old items mean receipts without invoices (accrue or chase supplier), invoices
  without receipts (chase warehouse), or price/quantity differences that need a
  clearing run. A growing GR/IR balance is a process failure, not a reconciling item.
- **Intercompany:** receivable in entity A = payable in entity B, same currency and
  period, before eliminations. Agree a cut-off and a dispute deadline.

## Gotchas
- **Manual journals to control accounts** (if allowed by misconfiguration) break the
  subledger tie-out permanently. Block them in account settings.
- **Auto-reversing accruals** need the next period open; check reversals actually posted.
- **FX revaluation run twice** or with the wrong rate type doubles gains/losses;
  revaluation should reverse at the start of the next period if that's your method.
- **Back-dated posting** by interfaces (e.g. a late batch from a billing system) into
  a closed period may be redirected to the open period without warning — confirm the
  interface's behaviour.
- Report key-date vs posting-date options cause most "the report doesn't match" queries.

## Verify
- [ ] Close calendar published with owners; every task signed off.
- [ ] Workflow queues (parked, held, unapproved) empty or accrued.
- [ ] AR, AP, inventory and fixed-asset subledgers tie to the GL exactly.
- [ ] GR/IR aged and explained; intercompany balances agree across entities.
- [ ] Prior period locked; every reopening logged and approved.
