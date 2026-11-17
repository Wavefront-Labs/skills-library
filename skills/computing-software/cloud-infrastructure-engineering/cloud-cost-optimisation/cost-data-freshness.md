---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-data-freshness
name: cost-data-freshness
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, data-freshness, data-latency, cost-data-pipeline, finops-principles, data-quality]
level: practitioner
status: docs-checked
description: "Set and monitor freshness targets for cost data using the FinOps Data Ingestion measures: data currency, ingest time, ETL time and cost visibility delay."
sources: ["https://www.finops.org/framework/principles/", "https://www.finops.org/framework/capabilities/data-ingestion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timely, accurate cost data (freshness targets)

The FinOps principle is "FinOps data should be accessible, timely, and accurate": process and share
cost data as soon as it becomes available, because fast feedback loops produce more efficient
behaviour and consistent visibility should reach all levels of the organisation.

## Measures from the Data Ingestion capability
- **Data currency**: time since the last update from each data source, compared with the expected
  update time.
- **Ingest time**: time from receipt of a new version of data from a source to storing the raw data
  in the FinOps data repository, compared with the expected time.
- **ETL / normalisation / correlation time**: time from storing raw data to finishing the adjusted
  data, compared with expected time. Keep it faster than the update frequency so obsolete data is
  not presented.
- **Cost visibility delay**: time between a cost occurring and it being ingested, normalised and
  displayed to stakeholders. It is shorter at higher maturity; the page suggests about a month at
  Crawl and, at Run, as frequently as the cloud provider can supply accurate data (it gives AWS
  at about 2 days as an example).
- **Frequency of data updates**: time between updates. At Run it may match provider updates (AWS up
  to 3 times a day) or be deliberately slower to reduce ETL cost.
- **Percentage of total cost available for reporting in normalised form.**

## Steps
1. **Set expected update times per source and per use** with the people who consume the data, and
   record them with the policy and governance requirements for ingestion frequency, currency and
   granularity.
2. **Success baseline**: the framework expects the major provider billing exports (AWS CUR, CUR
   2.0 or Data Exports output, Azure billing export, Google Cloud billing export) to be generated
   at least once a day.
3. **Monitor and alert** when ingestion exceeds established boundaries, and notify data source owners
   and data users of availability, quality or consistency problems. The framework KPI is to
   investigate reports within 1 business day and resolve them within 3 business days.
4. **Detect source changes** within 1 business day and adjust storage or processing within 3.
5. **Reconcile**: Finance typically reconciles invoices and usage data monthly or periodically,
   and compares native provider tool data with normalised data, recording any changes made outside
   source systems and reconciling them back to source.

## Verify
- [ ] Each source has an expected update time and a currency measurement.
- [ ] Alerts exist for ingestion outside boundaries.
- [ ] Reconciliation to invoices or native tools is performed and recorded.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework Principles page and the Data Ingestion capability page (maturity, activities, success measures and KPIs read).
Removed as unconfirmed: the per-provider latency table (provider docs unreadable), anomaly detection by 10:00 and working-day-5 close targets, the SQL lag query, the 0.5 percent accuracy target, the 7-day median completeness rule and the timezone and partial-day gotchas.
