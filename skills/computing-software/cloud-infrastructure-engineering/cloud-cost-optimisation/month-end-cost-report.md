---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.month-end-cost-report
name: month-end-cost-report
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, reporting-and-analytics, month-end-cost-report, month-end-close, variance-analysis, finops-reporting, executive-reporting]
level: practitioner
status: docs-checked
description: "Produce the month-end cloud cost report: reconcile to the invoice, show actual against budget and forecast, top movers, savings and unit cost."
sources: ["https://www.finops.org/framework/capabilities/reporting-analytics/", "https://www.finops.org/framework/capabilities/invoicing-chargeback/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Month-end cost close report

The report should be on time, tie to the invoice and explain movements before anyone asks. The FinOps Framework
Reporting and Analytics page covers tailoring reports to each persona and audience; the Invoicing and Chargeback
page covers invoice timing and true-up.

## Timing
Invoices typically arrive about 3 to 12 days after month end (Framework), so publish a labelled provisional view
first and a final view after the invoice is reconciled. Fix the working-day schedule with finance; the Framework
gives none.

## Contents
1. **Headline**: total cost for the month against budget and forecast, with a one-sentence explanation.
2. **Reconciliation**: estimate to invoice, with bridging items by invoice type (usage, prepaid commitments,
   marketplace, credit memos) and the true-up.
3. **By team or product**: actual, budget variance and forecast, using the allocation your organisation has agreed.
4. **Top movers**: the biggest increases and decreases, each with a cause written by the owner.
5. **Optimisation and unit economics**: savings and rate metrics your practice already tracks, and cost per business
   unit trended over time (see `unit-cost-dashboard`).
6. **Risks**: known launches and other planned changes that will move spend.

## Steps
1. Snapshot the month's data once it is final enough, and label the basis (billed or amortised) on every view.
2. Reconcile to invoices per billing account and record unexplained gaps.
3. Send the top movers to owners for explanations before publishing.
4. Publish in the same format each month and archive each version.

## Gotchas
- Publishing before data is final means corrections later; label provisional views.
- Mixing billed and amortised bases in one table confuses readers.
- Explanations written by the FinOps team are guesses; get them from owners.

## Verify
- [ ] Report published by the agreed date each month.
- [ ] Reconciliation line ties to invoices.
- [ ] Every top mover has an owner-written explanation.

## Checked
Confirmed on the FinOps Framework Reporting and Analytics and Invoicing and Chargeback pages: audience-specific
reporting, trend and variance reporting, invoice timing and true-up, invoice types. Removed: the WD1/WD3-6 timetable,
the 0.5% reconciliation tolerance, the 10 top movers count, the 2-day owner review, the SQL query, and the AWS CUR
and Budgeting sources (unreadable or not used).
Method: docs-checked 2026-11-09 against finops.org Framework Reporting and Analytics and Invoicing and Chargeback capability pages
