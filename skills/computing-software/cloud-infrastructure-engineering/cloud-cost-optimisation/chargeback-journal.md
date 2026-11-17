---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.chargeback-journal
name: chargeback-journal
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, invoicing-and-chargeback, chargeback, chargeback-journal, general-ledger, month-end-close]
level: practitioner
status: docs-checked
description: "Prepare cloud chargeback data for the general ledger: chargeback file contents, cost centre mapping, estimates and true-ups at close, and reconciliation."
sources: ["https://www.finops.org/framework/capabilities/invoicing-chargeback/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chargeback data for the general ledger

Chargeback becomes official when finance posts it to the organisation's accounting systems. The FinOps Invoicing and
Chargeback capability describes the chargeback file as containing metadata and data, in a predetermined currency,
aligned to the organisation's general ledger, for ingestion and processing by the financial system. Finance and
accounting own the ledger rules; the FinOps team supplies consistent, timely and accurate data.

## Steps
1. **Agree the requirements with finance and accounting**: chart of accounts, cost centres, business unit codes, capital
   budget codes and location codes (the page lists these as accounting inputs), the cost elements and metrics to include,
   and the currency of the file.
2. **Build the mapping** from allocation keys (account, tag, team) to the cost centre hierarchy that finance supplies.
   Use the allocation data from the FinOps tooling as the source for the file.
3. **Plan for close timing**: invoices typically arrive between 3 and 12 days after month end and usage data can arrive
   after the month ends, so a close may need estimates for total and line-item spend. Put a process in place to
   reconcile estimates to the journal entries once data and invoices are complete, with finance making true-up entries.
4. **Reconcile**: validate that chargeback data matches the costs expected from provider invoices plus added costs. The
   capability's General Ledger Recharge Rate KPI is spend recorded as a journal in the general ledger divided by total
   provider spend for the month (per cost centre as well as in total).
5. **Keep integrity controls** the organisation requires (the page notes some will need SOC compliance or similar) and
   document period close and invoice processing requirements.

## Gotchas
- Estimates made with incomplete data and never trued up leave a gap between the ledger and actual cost.
- Commitment discounts may not appear on the invoice as wanted; decide how they are charged (see chargeback-model).

## Verify
- [ ] The chargeback file maps every line to a finance-approved cost centre in the agreed currency.
- [ ] Estimates are reconciled and trued up after invoices arrive.

## Checked
Confirmed against the FinOps Invoicing and Chargeback capability page (read in full): chargeback file contents and
currency, accounting inputs (chart of accounts, cost centres, business unit, capital budget and location codes), invoice
timing of 3 to 12 days after month end, estimates with true-up, validation against invoices, General Ledger Recharge
Rate formula, SOC-type integrity requirement. Removed: the debit and credit journal design, zero-sum and rounding rules,
working day 2-3 accrual timing, ERP upload formats (SAP, Oracle, NetSuite), maker-checker and SOX controls, intercompany
guidance, unblended cost warning. The how-to-build-a-chargeback-model page returned 404 and was dropped from sources.
Method: docs-checked 2026-11-09 against the FinOps Framework Invoicing and Chargeback page.
