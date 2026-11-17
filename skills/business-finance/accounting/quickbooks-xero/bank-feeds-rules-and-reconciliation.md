---
id: business-finance.accounting.quickbooks-xero.bank-feeds-rules-and-reconciliation
name: bank-feeds-rules-and-reconciliation
category: business-finance
field: accounting
product: quickbooks-xero
tags: [quickbooks-xero, quickbooks, quickbooks-online, qbo, xero, bank-feeds, bank-rules, bank-reconciliation, reconcile, for-review, match-vs-add, transfer, duplicate-transactions, lock-date, closing-date, chart-of-accounts, small-business-accounting, smb-accounting, bookkeeping-software, undeposited-funds, payment-processor, stripe, paypal]
level: practitioner
status: draft
description: "Keep QuickBooks Online or Xero bank feeds clean: match before you add, safe bank rules, transfers, processor clearing accounts, statement reconciliation and lock dates."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bank feeds, rules and reconciliation in QuickBooks Online and Xero

**Goal:** process the bank feed so every line is matched to the right invoice, bill
or account exactly once, then reconcile to the bank statement and lock the month.
Menu names drift with UI releases — the ones below were current when written but
**not re-checked against the latest builds**.

## Where things live
| Task | QuickBooks Online | Xero |
|---|---|---|
| Feed queue | Banking / Transactions › *For review* | Bank account › *Reconcile* tab |
| Rules | Banking › *Rules* | Bank account › *Bank rules* |
| Statement reconciliation | Settings/Tools › *Reconcile* | Bank account › *Reconciliation report* (statement balance check) |
| Period lock | Account and settings › Advanced › *Close the books* (closing date + password) | Settings › Advanced › Financial settings › *Lock dates* |

Note the difference: in **Xero**, "reconciling" a feed line means matching it; the
statement-balance comparison is a separate report. In **QuickBooks**, accepting feed
lines categorises them, and *Reconcile* is the separate statement tick-off.

## 1. Process the feed: match first, add last
For every line, ask in order:
1. **Is there already a matching document?** A customer payment against an open
   invoice, a bill payment against an open bill, an existing transfer. **Match** it.
   Adding a new transaction instead leaves the invoice open and duplicates income —
   the single most common SMB-books error.
2. **Is it a transfer between own accounts** (bank to savings, card repayment)?
   Record as a transfer, not income/expense. Both feeds will show it — match the second
   side to the first.
3. **Only then add/categorise** a new spend or receive transaction with the right
   account, tax code and contact.

## 2. Bank rules without regret
- Make rules specific: match on payee **and** a text fragment or amount range; avoid
  "contains 'AMZN'" mapping everything to office supplies.
- Prefer rules that *suggest* (QBO without auto-add; Xero rules still need OK) rather
  than auto-post, until the rule has proven itself for a few months.
- Never set rules for customer receipts — they should match invoices.
- Review rules quarterly; old rules keep miscoding after a supplier changes what they sell.

## 3. Payment processors and deposits
Stripe, PayPal, Square and similar pay out net of fees, batched. Use a **clearing
account** (a bank-type account for the processor): record gross sales into it, fees
out of it, and the payout as a transfer to the real bank. In QBO, multiple payments
deposited together go via *Undeposited Funds / Payments to deposit* then grouped in a
deposit. A clearing account with a growing balance means payouts or fees are missing.

## 4. Statement reconciliation
Monthly, per account: enter the statement end date and closing balance, tick the
cleared items, and finish only with a **zero difference**. Never accept a system
"adjustment" to force it. Then set the closing/lock date.

## Gotchas
- **Feed duplicates** after a bank reconnection — check for doubled lines around the
  reconnection date before accepting anything.
- **Feed start date** set too early re-imports already-entered history.
- Deleting a matched feed line in QuickBooks can unmatch reconciled history; *exclude*
  is safer for genuine duplicates.
- Card feeds: refunds show as credits; categorise to the original expense account.
- Personal spend on the business account → owner drawings / director's loan, not expenses.

## Verify
- [ ] No feed lines older than a week unprocessed.
- [ ] Receivables and payables reports show no invoices paid in the bank but still open.
- [ ] Transfers net to zero between own accounts; processor clearing accounts near zero.
- [ ] Each account reconciled to its statement with zero difference.
- [ ] Lock/closing date set for the last reconciled month.
