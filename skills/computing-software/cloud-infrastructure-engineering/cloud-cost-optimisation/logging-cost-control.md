---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.logging-cost-control
name: logging-cost-control
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-aware-architecture, logging-cost-control, observability-costs, log-retention, log-sampling, log-tiers, metrics-cardinality, datadog-costs, cloudwatch-logs-costs]
level: practitioner
status: draft
description: "Control observability spend: find top log/metric/trace producers, cut at source, tiered retention and storage classes, sampling, cardinality limits, and per-team showback."
sources: ["https://www.finops.org/framework/capabilities/architecting-for-cloud/", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html", "https://learn.microsoft.com/azure/azure-monitor/logs/data-platform-logs#table-plans", "https://opentelemetry.io/docs/concepts/sampling/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Observability and logging cost control

Observability often reaches 10-30% of cloud spend in mature estates, and grows silently.

## Find the producers
- CloudWatch: `IncomingBytes` per log group; Azure: `Usage` table in Log Analytics by `DataType`;
  GCP: Logging usage by log name; Datadog/New Relic usage pages by service/index.
- Top 10 producers usually account for most volume — often debug logs, health-check access logs,
  chatty SDKs, or audit logs duplicated in several tools.

## Reduce at source
1. Log levels: INFO in prod, DEBUG behind a dynamic flag.
2. Drop/aggregate health-check and LB access logs; sample successful requests, keep all errors.
3. Remove payload dumps; truncate large fields.

## Tier the rest
- Cheaper classes: CloudWatch Logs **Infrequent Access** class; Azure Log Analytics **Basic/
  Auxiliary** table plans; GCP log buckets with routing/exclusion filters; archive to object storage
  (S3/Blob/GCS) for compliance retention.
- Retention per log class: debug days, app 30 days, audit per regulation. Set retention on every
  log group — CloudWatch defaults to **never expire**.

## Metrics and traces
- Custom metric **cardinality**: user/request ids as labels explode series count and cost; set
  limits in the pipeline.
- Trace sampling: head sampling (e.g. 5-10%) plus tail sampling in the OTel Collector to keep errors and slow traces.

## Showback
Allocate observability cost by producing service/team so owners see it.

## Verify
- [ ] Every log group/table has retention set.
- [ ] Top producers reviewed monthly; volume per request trending down.
