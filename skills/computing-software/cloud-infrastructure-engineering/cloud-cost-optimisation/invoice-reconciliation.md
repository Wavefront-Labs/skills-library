---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.invoice-reconciliation
name: invoice-reconciliation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cloud-billing, invoice-reconciliation, billed-cost, billing-period, month-end-close, finance-reconciliation]
level: practitioner
status: docs-checked
description: "Reconcile cloud invoices to cost data each month: macro-level totals per provider, invoice types, credits and discounts, and who reconciles at each maturity stage."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Invoice reconciliation

Finance pays invoices; engineering sees cost dashboards. The FinOps Framework Invoicing and Chargeback capability
includes defining provider invoice reconciliation procedures and policy with Finance, with input from Product and
Engineering.

## Monthly procedure
1. **Wait for the invoice.** Invoices typically arrive about 3 to 12 days after month end (Framework); reconcile once
   the invoice and the matching cost data are available.
2. **Reconcile at macro level first** (Framework Walk behaviour): the total expected per service provider against the
   total invoiced.
3. **Check the components**: manually validate that credits, discount rate and one-off charges are correct (Framework
   Walk behaviour) and that rates, discounts and credits are validated periodically.
4. **Handle each invoice type separately**: prepaid commitments, usage, marketplace subscriptions and credit memos
   can arrive as separate invoices (Framework).
5. **Currency**: factor currency conversion into the chargeback file. Keep it distinct, so currency movement can be
   separated from usage change.
6. **Explain residuals**: note why summarised invoice data may not match tag-based or shared-cost allocation, and
   that commitment discount effects may not appear on the invoice as desired (Framework challenges).
7. **Hand over to finance**: the Framework's chargeback file carries data in the agreed currency, aligned to the
   general ledger. At Run, reconciliation and chargeback run together and Finance can reconcile without central FinOps.

## Gotchas
- Several billing accounts or providers: reconcile each separately.
- Reconciling billed totals to an amortised view without a bridge produces false breaks; label the basis.

## Verify
- [ ] Last month's totals per provider tie to invoices, or the difference is explained.
- [ ] Known residual categories are listed with explanations.

## Checked
Confirmed on the FinOps Framework Invoicing and Chargeback page (read to the KPI list): reconciliation policy,
challenges, macro-level reconciliation, manual validation of credits and discounts, currency handling, invoice types
and Run-stage integration. Removed: FOCUS column names (BilledCost, InvoiceId, ChargeClass), finalisation timing for
named providers, the rounding-only tolerance, UTC billing period and CSP-reseller claims, and the AWS, Azure and FOCUS
sources (unreadable).
Method: docs-checked 2026-11-09 against finops.org Framework Invoicing and Chargeback capability page
