---
id: computing-software.cloud-infrastructure-engineering.aws.compute-optimizer-recommendation-preferences
name: compute-optimizer-recommendation-preferences
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, compute-optimizer, recommendation-preferences, external-metrics, enhanced-infrastructure-metrics, lookback-period, rightsizing]
level: practitioner
status: docs-checked
description: "Tune Compute Optimizer: lookback period, CPU and memory thresholds and headroom, enhanced infrastructure metrics, external memory metrics from APM tools, and scopes."
sources: ["https://docs.aws.amazon.com/compute-optimizer/latest/ug/viewing-recommendation-preferences.html", "https://docs.aws.amazon.com/compute-optimizer/latest/ug/rightsizing-preferences.html", "https://docs.aws.amazon.com/compute-optimizer/latest/ug/enhanced-infrastructure-metrics.html", "https://docs.aws.amazon.com/compute-optimizer/latest/ug/external-metrics-ingestion.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute Optimizer recommendation preferences

**Why:** the default lookback is 14 days, so recommendations can miss monthly peaks, and EC2 memory is
only considered when the CloudWatch agent or an external source supplies it. Preferences tune this.

## Preferences
| Preference | Options | Use |
|---|---|---|
| Lookback period | 14 days (default), 32 days, 93 days | 32 days captures monthly cycles at no extra cost; 93 days needs enhanced infrastructure metrics (paid) |
| Enhanced infrastructure metrics | Active / Inactive | paid; extends lookback to up to 93 days for EC2, Auto Scaling groups and RDS |
| CPU utilization threshold (EC2 only) | P90, P95, P99.5 (default) | P99.5 for sensitive production; P90 for non-production |
| CPU headroom (EC2 only) | 0%, 20% (default), 30% | extra CPU capacity for growth |
| Memory headroom (EC2 only) | 10%, 20% (default), 30% | extra memory capacity for growth |
| External metrics | Datadog, Dynatrace, Instana, New Relic | EC2 memory metrics from an observability product |
| Preferred EC2 instances | custom consideration set | e.g. only families covered by Savings Plans or RIs; do not over-restrict |
| Other | inferred workload type, savings estimation mode, Graviton-based recommendations | see the Recommendation preferences page |

Presets in the console: Maximum savings (P90, 0% CPU headroom, 10% memory headroom), Balanced (P95, 30%, 30%),
Default (P99.5, 20%, 20%), Maximum performance (P99.5, 30%, 30%).

## Set
```bash
aws compute-optimizer put-recommendation-preferences --resource-type Ec2Instance \
  --enhanced-infrastructure-metrics Active \
  --look-back-period DAYS_93 \
  --external-metrics-preference source=Datadog
aws compute-optimizer get-effective-recommendation-preferences --resource-arn <instance-arn>
```
- Use `--scope` to target the organization, an account or a resource; resource-level overrides account-level, which overrides organization-level. An Auto Scaling group preference overrides that of its instances.
- Use `--utilization-preferences` for the CPU threshold and headroom.
- A new preference applies at the next recommendation refresh, which can take up to 24 hours; until then the status shows a pending value such as `Active-pending`.

## Memory data
Without memory metrics, recommendations cannot see memory pressure: either enable memory utilization with
the CloudWatch agent, or ingest from an observability product via external metrics.
- External ingestion needs at least 30 consecutive hours of memory data, prefers the external data over CloudWatch while enabled, and does not support instances in Auto Scaling groups.

## Gotchas
- Enhanced infrastructure metrics is a paid feature; enable it at organization scope only if you will act on the recommendations.
- Too narrow a preferred-instance list hides better options.
- Headroom raises recommended size; do not stack app-level safety margins on top.
- CPU and memory preferences apply to EC2 instances only; for RDS, EBS volumes and ECS services only the lookback period is configurable.

## Verify
- [ ] Effective preferences show org defaults; critical workloads have resource-level overrides.
- [ ] Recommendations show memory utilization populated for instances with the agent or external metrics.

## Checked
2026-10-28. Confirmed against the Compute Optimizer User Guide pages in `sources` (recommendation preferences, rightsizing preferences, enhanced infrastructure metrics, external metrics ingestion) and the botocore model (`PutRecommendationPreferences` flags and enums).
Fixed: CPU headroom options are 0/20/30 and memory headroom 10/20/30 (previously a single 0-30 list); P99.5 default, 20% default headroom added; override order stated from the docs.
Removed: the "migration effort" preference, the savings-mode wording, CloudWatch agent metric names, a utilization-preferences example value and the scope example values (not confirmed on the fetched pages), and the "small charge" wording (docs say paid).
Method: documentation only; no commands were run.
