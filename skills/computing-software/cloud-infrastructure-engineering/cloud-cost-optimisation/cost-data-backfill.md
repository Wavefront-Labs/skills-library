---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-data-backfill
name: cost-data-backfill
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, data-ingestion, backfill, historical-data, cost-data-pipeline]
level: practitioner
status: docs-checked
description: "Plan historical cost data capture and completeness checks using the FinOps Data Ingestion capability: what history each maturity stage holds and how to validate it."
sources: ["https://www.finops.org/framework/capabilities/data-ingestion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Historical cost data and completeness

The Data Ingestion capability treats history as a maturity marker. This skill covers what the
framework says about it; the provider-specific backfill mechanics are not covered here because the
provider documentation could not be read when this was checked.

## What the framework says
- **Walk**: most historical data is captured, enough for year-over-year trends. Data is mapped back
  to the business and can change as the business changes. Data completeness checks and mechanisms
  exist.
- **Run**: all historical data is captured for deeper trend analysis. The mapping to the business
  captures historical changes as the business evolves. Completeness includes quality checks and
  automated mechanisms.
- Normalised dimensions and cost metrics across sources (through FOCUS or another specification)
  are what let history from several clouds sit in one repository.

## Steps
1. **Decide the required depth** from the reporting needs the Reporting and Analytics and Unit
   Economics capabilities place on ingestion (granularity, correlation, normalisation).
2. **Specify granularity and data elements** per source, and document each source and its
   expectations; update the documentation when ingested data changes.
3. **Define the normalisation** between sources: the data model, where it is done and which keys
   are used, so loaded history maps to the same fields as new data.
4. **Validate completeness**: reconcile invoices and usage data (typically monthly or periodically),
   and compare native provider tool data against the normalised data. Record and reconcile any
   change made outside source systems.
5. **Track coverage**: the percentage of total cost available for reporting in normalised form, and
   the percentage of matching metadata elements.
6. **Re-run and re-document** when sources change; the framework asks for changes to be noticed
   within 1 business day and handled within 3.

## Verify
- [ ] Each history load is reconciled to invoices or provider tool totals.
- [ ] The business mapping history is retained, not overwritten.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework Data Ingestion capability page (read in full).
Removed as unconfirmed: all provider backfill procedures (AWS support-case backfill and 36 months, Azure export by dates, Google no-backfill statement), the delete-and-insert SQL, immutable landing zone and replay rules, tag-activation gotcha and the invoice sources (docs.aws.amazon.com, learn.microsoft.com, cloud.google.com unreadable).
