---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cloud-accruals
name: cloud-accruals
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, chargeback, cloud-accruals, invoice-processing, month-end-close]
level: practitioner
status: docs-checked
description: "Process cloud invoices and accruals: invoice timing, estimating before the invoice, true-up, invoice types, PO matching and currency handling."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cloud invoice processing and accruals

## Timing problem
The FinOps Framework Invoicing and Chargeback page says invoices typically arrive monthly, about 3 to 12 days after
month end, so finance often needs an estimate before the invoice exists. Estimates are trued up when the actual
invoice arrives.

## Steps
1. **Estimate**: at close, estimate the month's charges from cost data, and record the basis used.
2. **True-up**: when the invoice arrives, compare it with the estimate, record the variance and adjust.
3. **Know the invoice types**: the Framework lists prepaid commitments, usage, marketplace and credit memos as
   different invoice types. Reconcile each type separately.
4. **Match to purchase orders**: the Framework includes purchase order management; match invoices to the PO and
   track remaining PO balance.
5. **Currency**: the Framework notes currency conversion; use the finance team's rate policy consistently and record
   the rate used.
6. **Allocate or recharge**: decide with finance whether internal teams see showback (visibility only) or chargeback
   (costs actually billed to them). The Framework describes Crawl, Walk and Run as increasingly automated, accurate
   and allocated invoicing.
7. **Document**: close checklist with data sources, owners and the agreed variance tolerance (set it with finance;
   the Framework gives none).

## Gotchas
- Marketplace and credit memo invoices follow different patterns from usage invoices; do not assume one timetable.
- Estimates that are never compared with the invoice stay wrong; track the variance monthly.

## Verify
- [ ] Estimate versus invoice variance is recorded each month and reviewed.
- [ ] Every invoice type is matched to a PO or recorded exception.

## Checked
Confirmed on the FinOps Framework Invoicing and Chargeback page: invoice timing (monthly, roughly 3 to 12 days after
month end), estimates and true-up, invoice types, currency conversion, PO management, showback versus chargeback and
the Crawl/Walk/Run descriptions. Removed: provider-specific invoice dates, the prepayment amortisation and tax
treatment (accounting rules not on the page), the 0.5% style tolerances, and the AWS and Azure sources (unreadable).
Method: docs-checked 2026-11-09 against finops.org Framework Invoicing and Chargeback capability page
