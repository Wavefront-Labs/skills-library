---
id: business-finance.accounting.tax-accounting.vat-gst-return-preparation-and-reconciliation
name: vat-gst-return-preparation-and-reconciliation
category: business-finance
field: accounting
product: tax-accounting
tags: [tax-accounting, vat, gst, vat-return, gst-return, bas, sales-tax, output-tax, input-tax, input-tax-credit, reverse-charge, tax-codes, tax-invoice, partial-exemption, zero-rated, exempt-supplies, making-tax-digital, mtd, indirect-tax, vat-reconciliation]
level: practitioner
status: draft
description: "Prepare a VAT/GST return you can defend: tax codes, output vs input tax, reverse charge, invoice validity, reconciling the return to the ledger and fixing errors."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# VAT/GST return preparation and reconciliation

**Goal:** file a periodic VAT/GST return whose boxes tie to the ledger, where every
input-tax claim is backed by a valid invoice, and where errors are corrected the way
the tax authority expects. The mechanics below are common to most VAT/GST systems;
rates, box numbers, thresholds and deadlines are **jurisdiction-specific — check your
authority's current guidance** (UK HMRC, Australian ATO BAS, EU member-state rules,
etc.).

## 1. Get the tax codes right at source
Every sales and purchase line carries a tax code. A minimal set:
- **Standard-rated**, **reduced-rated**, **zero-rated** (taxable at 0% — still
  reported, and input tax still recoverable).
- **Exempt** (not taxable — and the related input tax is generally *not* recoverable).
- **Outside scope / no VAT** (wages, dividends, most bank transfers, intercompany
  loans).
- **Reverse charge** (services bought from abroad, some domestic sectors such as
  construction or electronics in certain countries): you account for output *and*
  input tax yourself — net zero for a fully taxable business, but both must appear.
- **Imports** under postponed accounting or import VAT certificates.
Most return errors are miscoded lines, so fix codes in the ledger, never by editing
the return.

## 2. Preparation sequence
1. Close the period's sales and purchases (cut-off on **tax point** — usually invoice
   or supply date, not payment date, unless you're on cash accounting).
2. Run the VAT/GST detail report by tax code. Scan for: zero-VAT lines on
   standard-rated suppliers, VAT charged on exempt or out-of-scope items, large
   one-offs, missing supplier tax numbers.
3. Check **invoice validity** for material input-tax claims: supplier's tax number,
   date, description, net, rate and tax amount. A receipt or pro-forma usually isn't
   enough.
4. Remove **blocked input tax** (commonly: business entertainment, some cars,
   private use) per local rules.
5. If you make exempt supplies, apply the **partial exemption** method to residual
   input tax.
6. Produce the return from the software and save the box report.

## 3. Reconcile the return to the ledger
```
Output tax per return            = credit side of VAT control for the period
Input tax per return             = debit side of VAT control for the period
Net payable per return           = movement on VAT control (excl. payments)
VAT control balance after filing = amount on the return still to pay/refund
```
Also reconcile **net sales per return** to turnover in the P&L (differences:
exempt/out-of-scope income, timing). An unexplained gap is a finding.

## 4. Correcting errors
- Small errors from earlier periods can usually be corrected on the next return
  within a threshold; above it, a separate voluntary disclosure is required. The
  threshold and window differ by country — **unverified here, check locally**.
- Never reopen a filed period in the software and change it silently; the ledger
  would then disagree with what was filed.

## Gotchas
- Cash vs accrual (invoice) basis changes which period a transaction lands in.
- Credit notes reduce output/input tax in the period they're issued.
- Foreign-currency invoices: use the authority's approved exchange rate method.
- Bad-debt relief usually has a time condition before you can reclaim.
- Digital filing regimes (e.g. UK Making Tax Digital) require an unbroken digital link
  from records to the submission — no retyping.

## Verify
- [ ] VAT detail report reviewed by tax code; miscodings fixed in the ledger.
- [ ] Material input-tax claims have valid tax invoices on file.
- [ ] Return boxes reconcile to the VAT control account and to P&L turnover.
- [ ] Reverse-charge transactions show both output and input tax.
- [ ] Filing deadline, payment date and filed-box report are saved with the period.
