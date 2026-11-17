---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.chargeback-disputes
name: chargeback-disputes
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, invoicing-and-chargeback, chargeback, chargeback-disputes, allocation-disputes, showback]
level: practitioner
status: docs-checked
description: "Handle chargeback disputes: agree a correction process with finance, check evidence in billing data, common causes, true-ups after close and allocation fixes."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/", "https://www.finops.org/framework/capabilities/allocation/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chargeback disputes

Chargeback reporting goes to internal budget owners, so some will challenge their charges. The FinOps Invoicing and
Chargeback capability expects the practice to provide a process for correcting chargeback reporting when changes occur
after the accounting period has closed, and to help teams reconcile the portion of expense allocated to them each month.

## Process (agree the details with finance and accounting)
1. **Intake**: a defined way to raise a dispute, naming the charge line, the amount and the reason. The window for
   raising disputes and the response times are decisions for the FinOps team and finance; the framework sets none.
2. **Triage** each dispute into one of three kinds:
   - data or allocation error (wrong tag, account mapped to the wrong cost centre),
   - disagreement with a shared-cost rule (a policy question, settled with finance, see the Allocation capability),
   - genuine usage the team did not expect (show the resource-level breakdown).
3. **Resolve** errors by correcting the mapping. Finance makes any true-up entries and handles corrections after
   close using the organisation's accounting policy for adjustments to closed periods.
4. **Record** the outcome and use it to improve the allocation and tagging strategy.

## Common causes the framework points to
- Missing or inconsistent tags and labels, and unclear ownership of accounts (Allocation).
- Shared costs split by a method the team did not expect (fixed, proportional or proxy-metric split).
- Commitment discounts: the benefit may not appear on the invoice as expected, and may be charged to the account owner
  or to consumers depending on the policy.
- Credits, discount rate and one-off charges that were not validated against the invoice.
- Estimated chargeback made before invoice and usage data were complete, then trued up.
- Currency conversion included in the chargeback file.

## Steps
1. Keep showback running: the framework treats showback as always required and chargeback as dependent on accounting
   policy.
2. Give teams the underlying data so they can check charges before disputing.
3. Review disputes regularly by cause and fix systemic causes in allocation. Useful measures from the capability page:
   percentage accuracy of chargebacks and percentage variance of chargeback estimates against actuals.

## Gotchas
- Restating closed periods: follow finance policy on corrections after close.

## Verify
- [ ] Disputes have a logged outcome and an owner.
- [ ] Repeat disputes for the same cause fall over time.

## Checked
Confirmed against the FinOps Invoicing and Chargeback and Allocation capability pages (read in full): correction process
after period close, adjustments with accounting systems, finance true-up entries, reconciliation help for teams,
showback versus chargeback, invoice validation of credits, discount rate and one-off charges, commitment discount
treatment, currency conversion, chargeback accuracy and estimate variance KPIs. Removed: the 10 working day dispute
window, the 5 working day triage target, the steering committee step, the materiality threshold wording and the
uncited cause list entries (cluster namespace mapping, support and marketplace default rules).
Method: docs-checked 2026-11-09 against the FinOps Framework Invoicing and Chargeback and Allocation pages.
