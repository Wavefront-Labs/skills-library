---
id: computing-software.cloud-infrastructure-engineering.google-cloud.billing-reports-and-cost-table-analysis
name: billing-reports-and-cost-table-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, billing-reports, cost-table, cost-breakdown, cost-reports-analysis, billing-reports-filter, billing-console, sku-analysis, credits, cost-trend, invoice-reconciliation, group-by-sku]
level: practitioner
status: docs-checked
description: "Use the Billing Reports, Cost Table and Cost Breakdown pages to answer 'why did the bill change': filter by project/SKU/label, reconcile to the invoice, and share saved views."
sources: ["https://cloud.google.com/billing/docs/how-to/reports", "https://cloud.google.com/billing/docs/how-to/cost-table", "https://cloud.google.com/billing/docs/how-to/cost-breakdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Billing reports and cost table analysis

**Goal:** explain a month-over-month change, attribute it to a SKU and project, and hand finance
a view they can reopen themselves.

## 1. Three pages, three questions
| Page | Answers | Notes |
|---|---|---|
| **Reports** | trend over time, grouped by service, project, SKU and other dimensions; forecast line | stacked bar chart; preset and saved reports |
| **Cost table** | the costs that reconcile to one invoice or statement | pick one invoice by Invoice month; downloadable to CSV |
| **Cost breakdown** | on-demand cost, then discounts, credits, invoice-level charges, total | waterfall chart |

Access: Reports and Cost breakdown need permissions on the billing account such as
`billing.accounts.getSpendingInformation`, which Billing Account Administrator, Costs Manager and
Viewer include. A user with only project-level permissions sees a limited Reports view (no
invoice-level charges, some Group by options, filters and features unavailable).

## 2. Reports page workflow
1. Start from a preset such as "Services - this month" or "Projects - this month", or choose a
   Time range of **Charge period** (formerly Usage date; data back to January 2017) or
   **Billing period** (formerly Invoice month; complete invoice months only).
2. Change **Group by** (Service, Project, SKU, or a combination such as Date > Project) to find the
   biggest mover, then add filters (for example SKU or Project) to narrow it.
3. Share or bookmark the URL (it carries your settings), save the view, generate a SQL query,
   or download CSV.
- Usage-specific views exclude invoice-level charges such as tax and adjustments; set the time
  range to Billing period to include them.
- The chart shows forecasted costs in light grey, with a forecast total in the header.
- A 24-hour period in the report starts at midnight US and Canadian Pacific Time (UTC-8),
  observing US daylight saving, so a report day differs from your local day.
- Billing Reports aggregates by invoice month, not by individual invoice; if you get more than one
  invoice in a month use the Cost table.

## 3. Cost table (invoice reconciliation)
With filters in their default state the totals match the invoice or statement total; the Reset
button returns filters to default. Choose the invoice with the **Invoice month** selector (it
shows the invoice number, so two invoices in one month can be told apart). Use a nested view with a
Group by such as Project > Service > SKU > Consumption model, or **No grouping** for a flat itemised
list. Labels can be a grouping dimension through a Custom grouping, but project labels cannot be
selected in the label filter. Select rows to see a summary bar with costs, credits and savings.
Tax is separated by project from the September 2020 invoice month; group with Project first to see it.

## 4. Cost breakdown
For the chosen range it shows base usage cost at on-demand prices, then credits and savings by
type (for example committed use and sustained use discounts), then invoice-level charges
(tax, adjustments) only when the time range is a Billing period. For a custom pricing contract,
costs from May 1, 2021 onward use list prices as the on-demand rate and the contract saving shows as a
negotiated savings credit. Use it to see what discounts are worth.

## Gotchas
- A credit or discount that stops applying changes the net numbers; compare views with the same
  savings settings.
- For analysis beyond the console, use the BigQuery billing export (see `billing-accounts-and-budgets`).

## Verify
- [ ] Cost table total for the last invoice month, with default filters, equals the invoice total.
- [ ] A shared Reports URL opens with the same settings for a colleague with a billing role.

## Checked
Date: 2026-11-07.
Method: documentation only; no commands were run.
Read in full: "Understand your savings with cost breakdown reports" (first 60 lines: overview, permissions, chart reading, on-demand rates, time range). The Reports page (about 79 KB) and Cost table page (about 62 KB) were searched by keyword (permissions, Group by, forecast, time zone, invoice month, CSV, labels, reset, tax), not read end to end; several long table rows on the Reports page were omitted by the search tool and not read.
Corrections: removed the example SKU names, "Common findings" list, "up to 24 h delay", "linear extrapolation" forecast claim, "Include credits toggle" and "typically PST" wording (page: US and Canadian Pacific Time, UTC-8, with daylight saving); `roles/billing.viewer` alone corrected to the roles the page lists; "the UI cannot group by two dimensions" removed (multi-dimension Group by such as Date > Project exists); Cost table column names and "a few cents rounding" removed as unconfirmed. The Reports page gives conflicting availability dates for invoice-month data, so none is stated.
