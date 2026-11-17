---
id: business-finance.procurement-and-supply-management.purchasing-operations.three-way-match-and-p2p-controls
name: three-way-match-and-p2p-controls
category: business-finance
field: procurement-and-supply-management
product: purchasing-operations
tags: [procurement-and-supply-management, purchasing-operations, procure-to-pay, p2p, purchase-order, po, requisition, approval-workflow, approval-matrix, three-way-match, two-way-match, goods-receipt, grni, invoice-matching, accounts-payable, tolerances, segregation-of-duties, duplicate-payments, vendor-master, payment-fraud, no-po-no-pay, purchasing]
level: intro
status: draft
description: "Run procure-to-pay cleanly: requisitions and approval matrix, no-PO-no-pay, receipting, two- and three-way matching with tolerances, duplicate and bank-change controls."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Procure-to-pay hygiene: purchase orders, approvals and three-way matching

**Goal:** make every purchase traceable from need to payment — approved before
commitment, received before payment, paid once at the agreed price — so spend is
controlled and invoices flow without manual chasing.

## 1. The cycle
```
requisition → approval → purchase order → goods/service receipt → invoice
→ match → approval of exceptions → payment → (accrual / reconciliation)
```
Each step happens in the ERP/P2P system so the trail is automatic.

## 2. Requisitions and approvals
- Requisition states item/service, quantity, price or estimate, supplier (preferably
  contracted/catalogue), cost centre, GL account, required date, and justification.
- **Approval matrix** by value and category: budget holder for budget, procurement
  for supplier/contract compliance above thresholds, specialist approvals for IT,
  capex, or regulated items.
- **No PO, no pay:** suppliers are told invoices without a valid PO number will be
  returned. Exceptions (utilities, rent, taxes, some subscriptions) are listed
  explicitly and handled by other controls.

## 3. Purchase orders
- PO references the contract and its prices; free-text, non-catalogue POs should be
  the minority — track their share as a KPI.
- **Blanket/framework POs** for recurring services, with value cap and expiry.
- Raise POs *before* the commitment. Retrospective POs ("after-the-fact") defeat the
  control; report them by requester and cost centre.

## 4. Receipt
- Goods: the receiver records quantity received and condition against the PO in the
  system (not just a signed delivery note).
- Services: the requester confirms service delivered (service entry sheet / receipt)
  for the period.
- Never let the same person raise the PO, receipt it and approve the invoice
  (segregation of duties).

## 5. Matching
- **Two-way match:** invoice vs PO (price, quantity) — for low-risk services.
- **Three-way match:** invoice vs PO vs receipt — standard for goods.
- **Tolerances:** e.g. price within ±2% or a small absolute amount, quantity within
  receipt. *(Set by finance policy; too wide hides overbilling, too narrow floods the
  exception queue.)*
- Exceptions route to the buyer/requester with a reason code (price variance, quantity
  variance, no receipt, PO closed). Track exception reason codes to fix root causes.

## 6. Payment and close
- Pay on agreed terms; capture early-payment discounts where worth it.
- **Duplicate-invoice checks:** same supplier + invoice number, and fuzzy checks on
  amount/date (invoice number typos defeat exact-match).
- **Supplier master data changes** (bank account especially) require independent
  verification by calling a known contact — the main route for payment fraud.
- Month end: accrue goods/services received not yet invoiced (GRNI); review aged
  GRNI and close stale POs.

## KPIs
PO compliance % (spend with a PO raised before invoice), first-time match rate,
exception aging, invoice cycle time, % catalogue spend, duplicate payments recovered.

## Gotchas
- **Split requisitions** to stay under an approval threshold — look for same-day,
  same-supplier, same-requester POs.
- Receipting in bulk at month end "to get invoices paid" without checking delivery.
- Blanket POs with no cap become blank cheques.
- Changing the PO after the invoice arrives to force a match.

## Verify
- [ ] Approval matrix documented and enforced in the system.
- [ ] Retrospective POs and no-PO invoices are measured and falling.
- [ ] Three-way match applied to goods with documented tolerances.
- [ ] Raiser, receiver and invoice approver are different people for each purchase.
- [ ] Bank-detail changes verified independently; duplicate checks run before payment.
