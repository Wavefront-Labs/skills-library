---
id: business-finance.accounting.double-entry-bookkeeping.month-end-close-and-bank-reconciliation
name: month-end-close-and-bank-reconciliation
category: business-finance
field: accounting
product: double-entry-bookkeeping
tags: [double-entry-bookkeeping, bookkeeping, double-entry, debits-and-credits, journal-entries, general-ledger, trial-balance, chart-of-accounts, bank-reconciliation, month-end-close, period-close, accruals, prepayments, deferred-revenue, suspense-account, cut-off, balance-sheet-reconciliation, close-checklist, accounts-payable, accounts-receivable]
level: practitioner
status: draft
description: "Close a month in a double-entry ledger: debit/credit rules, bank reconciliation, accruals and prepayments, balance-sheet recs, trial balance checks and locking the period."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Month-end close and bank reconciliation

**Goal:** turn a month of raw transactions into a ledger you would sign: every bank
line matched, every balance-sheet account explained, income and costs in the right
month, and the period locked so nobody changes it afterwards.

## 1. The rules you apply on every entry
- Every entry has equal debits and credits. Debits increase **assets and expenses**;
  credits increase **liabilities, equity and income**. (Mnemonic: DEAD CLIC — Debit
  Expenses, Assets, Drawings; Credit Liabilities, Income, Capital.)
- Post to the most specific account in the chart of accounts; never to "Sundry" or
  "Suspense" except as a temporary parking place you clear before close.
- Every manual journal carries a narrative (what and why), a date in the right period,
  and a supporting document reference.

## 2. Close sequence (run it in this order)
1. **Cut-off:** make sure all sales invoices for goods/services delivered this month
   are raised, and supplier bills received are entered with the *invoice* date.
2. **Bank reconciliation** for every bank, card and payment-processor account (below).
3. **Sub-ledgers to control accounts:** aged receivables total = AR control in the GL;
   aged payables total = AP control. A difference means someone posted directly to the
   control account — find and reverse it.
4. **Accruals:** costs incurred but not yet invoiced (utilities, contractor hours,
   audit fee). Dr Expense / Cr Accruals. Set to **auto-reverse** on day 1 of next month
   so the real bill doesn't double-count.
5. **Prepayments:** costs paid in advance (annual insurance, software). Post to
   Prepayments and release monthly: Dr Expense / Cr Prepayments, 1/12 each month.
6. **Deferred revenue:** cash received for work not yet delivered. Dr Income /
   Cr Deferred revenue for the undelivered part.
7. **Depreciation**, payroll journals, loan interest, FX revaluation where relevant.
8. **Balance-sheet reconciliations:** every balance-sheet account gets a one-line
   schedule showing what makes up the balance (list of items, loan statement, fixed
   asset register). If you can't list what's in it, it's wrong.
9. **Review the trial balance and P&L** against last month and budget; investigate
   anything that moved more than you can explain in one sentence.
10. **Lock the period** (set the lock/closing date in the software).

## 3. Bank reconciliation, done properly
Start from the **bank statement closing balance**, not the ledger:
```
Statement closing balance
+ deposits in transit (in ledger, not yet on statement)
- unpresented payments (cheques/transfers in ledger, not yet cleared)
= Adjusted bank balance  → must equal the GL bank account balance
```
- Items on the statement but not in the ledger (bank fees, interest, direct debits)
  are **entered in the ledger**, not listed as reconciling items.
- Reconciling items should be young. An unpresented cheque older than ~3 months, or a
  deposit in transit older than a few days, is usually an error or a stale item.
- A difference that is divisible by 9 often means a **transposition** (e.g. 54 vs 45);
  a difference equal to twice one transaction usually means it was posted on the
  wrong side.

## Gotchas
- **Reconciling in the software is not the same as being reconciled.** Ticking items
  off with a forced "adjustment" line hides the problem; never post a balancing plug.
- **Back-dated entries after close** silently change a reported month. That's why you
  lock the period; adjustments found later go in the current month with a note.
- **Accruals that never reverse** inflate costs twice. Check the accruals account
  returns to roughly zero before new accruals each month.
- **Suspense with a balance at close** is unfinished work, not an answer.
- **Owner/personal spending on a business card** goes to drawings or a director's
  loan account, not to expenses.
- Treatment of VAT/GST on accruals and the exact lock-date behaviour vary by
  jurisdiction and software — confirm locally (unverified across all packages).

## Verify
- [ ] Trial balance debits = credits, and suspense/clearing accounts are zero.
- [ ] Every bank, card and processor account reconciles to its statement with only
      young, explainable reconciling items.
- [ ] AR and AP aged reports equal their GL control accounts.
- [ ] Every balance-sheet account has a supporting schedule that ties to the GL.
- [ ] Accruals are set to auto-reverse; prepayment and deferred-revenue schedules tie.
- [ ] P&L movements vs last month are explained; the period is locked.
