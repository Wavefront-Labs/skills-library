---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-data-pipeline
name: cost-data-pipeline
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-data-pipeline, data-ingestion, focus, etl, normalisation]
level: advanced
status: docs-checked
description: "Design a cost data pipeline from the FinOps Data Ingestion capability: sources, normalisation with FOCUS, repository ownership, quality checks and metrics."
sources: ["https://www.finops.org/framework/capabilities/data-ingestion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Building a cost data pipeline

Per the framework, Data Ingestion gathers, transfers, processes, transforms and correlates datasets
into a queryable, contextualised repository. Needs vary: an organisation relying wholly on one
provider's tools may ingest nothing, one using a third-party FinOps platform may rely on it, and
one with many vendors needs complex ingestion. The goal is not the largest, most granular
real-time dataset but the data that provides value at the current maturity.

## Steps
1. **List sources from requirements.** Allocation, Reporting and Analytics and Unit Economics
   define what is needed. Cloud cost and usage is the core; add where useful: modified billing
   data, carbon data, utilisation and performance data, observability data, on-premises or private
   data, CMDB metadata, ITAM licence data, Kubernetes usage and business data such as revenue,
   customers or transactions.
2. **Specify granularity and data elements** for each source and keep contact with each data
   provider and tool vendor.
3. **Normalise.** Provider datasets are large and use proprietary schemas; FOCUS provides a common
   schema. Walk uses a third-party tool or FOCUS to normalise; Run normalises dimensions and cost
   metrics across all sources. The framework also lists the AWS, Azure, Google Cloud and Oracle
   FOCUS Converter export datasets as possible inputs.
4. **Correlate with allocation metadata.** Ensure tags and labels from cloud platforms are gathered
   and mapped to internal allocation metadata, which also provides keys for joining other datasets.
5. **Choose and maintain the repository**: access methods, responsible owner and governing policies,
   with size, cost, performance, resilience and availability managed over its lifecycle.
6. **Add quality checks and alerting**: data quality mechanisms, observability and alerts when
   ingestion goes outside boundaries, completeness checks, and a FOCUS validator where FOCUS data
   is used.
7. **Measure**: data currency, ingest time, ETL time, the share of cost available in normalised
   form, and the share of matching metadata.
8. **Feed Unit Economics**: report ingestion metrics to it and supply business data for unit
   metrics.

## Gotchas
- Do not try to amass the largest, most granular real-time dataset; add sources and granularity as
  needs and maturity grow.
- Changes made to data outside source systems should be recorded and reconciled back to source.

## Verify
- [ ] Data quality and FOCUS validator checks run and are monitored.
- [ ] Data ownership and access guidance for all personas is documented.

## Checked
Method: docs-checked 2026-11-09 against the FinOps Framework Data Ingestion capability page (read in full).
Removed as unconfirmed: the warehouse product list, per-provider export formats and partitioning (provider docs unreadable), restatement-by-partition handling, FOCUS column list, dbt testing, duplicate-append gotcha and tag-shape evolution gotcha.
