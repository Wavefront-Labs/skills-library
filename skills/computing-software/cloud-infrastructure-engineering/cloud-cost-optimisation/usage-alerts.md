---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.usage-alerts
name: usage-alerts
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-anomaly-detection, usage-alerts, leading-indicators, cloudwatch-alarms, azure-monitor-alerts, cloud-monitoring-alerts, egress-alerts, log-ingestion-alerts, llm-token-alerts]
level: practitioner
status: docs-checked
description: "Catch fast-moving spend within minutes using usage metrics (requests, egress bytes, log GB, instance counts, LLM tokens) because billing data lags hours to a day."
sources: ["https://www.finops.org/framework/capabilities/anomaly-management/", "https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html", "https://learn.microsoft.com/azure/azure-monitor/alerts/alerts-overview", "https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics-types.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-concurrency.html", "https://docs.aws.amazon.com/AmazonS3/latest/userguide/metrics-dimensions.html", "https://learn.microsoft.com/en-us/azure/azure-monitor/logs/daily-cap"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Leading usage alerts for fast-moving spend

Billing-based anomaly detection is a day late. For services that can burn money quickly, alert on
the **usage metric that drives the bill**.

## High-risk meters and metrics
| Cost driver | Metric to alarm on |
|---|---|
| Serverless runaway / recursion | invocations, concurrent executions (Lambda `ConcurrentExecutions`), Functions execution count |
| Egress / NAT | NAT gateway bytes, load balancer processed bytes, CDN bytes |
| Log ingestion | log ingestion volume per workspace or log group (Log Analytics also has a daily cap) |
| Compute fleet | instance/node count, GPU instance count, autoscaling group desired capacity |
| Storage requests | S3 request metrics (`AllRequests`) on hot buckets |
| Managed AI/LLM | tokens per minute/day per key, provider usage API |
| Data warehouse | bytes scanned / slot-ms (BigQuery), warehouse credits (Snowflake resource monitors) |

## Steps
1. Convert a currency tolerance into a metric threshold using the current unit price from the vendor's
   pricing page (tolerance per day divided by price per unit gives units per day; alarm on the hourly rate).
2. Alarm on a rate over a window short enough to act on, routed to the owning team.
3. Add **hard limits where the platform offers them**: Lambda reserved concurrency, Log Analytics
   daily cap, BigQuery custom quotas, Snowflake resource monitors with suspend, API key spend limits,
   autoscaling max sizes.
4. Document the expected range in the alarm description.

## Gotchas
- Hard caps can cause outages (dropped logs, throttled functions); choose per environment.
- Metric thresholds drift as traffic grows — review with the anomaly thresholds.

## Verify
- [ ] Each top cost driver has a usage alarm or a hard cap.
- [ ] A synthetic spike in staging triggers the alarm in good time.

## Checked
2026-11-01. Confirmed in the Lambda metrics page (`ConcurrentExecutions`), the Lambda concurrency page (reserved
concurrency), the S3 metrics page (`AllRequests`), the Azure Monitor daily cap page and the FinOps anomaly management
page. Removed: the NAT `BytesOutToDestination` and CloudWatch `IncomingBytes` metric names (pages returned no text),
the worked pricing example, and fixed alarm window and time figures.
Method: documentation only; no commands were run.
