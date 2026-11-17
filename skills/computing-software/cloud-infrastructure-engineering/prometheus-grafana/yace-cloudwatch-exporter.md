---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.yace-cloudwatch-exporter
name: yace-cloudwatch-exporter
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [yace-cloudwatch-exporter, cloudwatch-exporter, aws, exporters, cloudwatch, prometheus]
level: practitioner
status: docs-checked
description: "Export AWS CloudWatch metrics to Prometheus with YACE: discovery jobs, tag filtering, period/length/delay, nilToZero, flags and IAM."
sources: ["https://github.com/prometheus-community/yet-another-cloudwatch-exporter", "https://github.com/prometheus-community/yet-another-cloudwatch-exporter/blob/master/docs/configuration.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# YACE (yet-another-cloudwatch-exporter)

YACE runs scrape jobs of three types: `discovery` (auto-discovery of tagged resources only), `static` and
`customNamespace`. At least one block must exist. Flags configure runtime-fixed settings; the YAML file (`-config.file`,
default `config.yml`) holds jobs and can be reloaded at runtime.

## Config
```yaml
apiVersion: v1alpha1               # must be v1alpha1
sts-region: eu-west-1              # optional
discovery:
  exportedTagsOnMetrics:
    kafka: [Name]                  # tags exported on metrics, keyed by service (docs example)
  jobs:
    - type: AWS/SQS                # service alias such as ec2 or a namespace such as AWS/SQS
      regions: [eu-west-1]
      searchTags:                  # all must match; key is case-sensitive, value is a regex
        - {key: env, value: prod}
      period: 60                   # seconds
      length: 300                  # how far back to request, seconds
      metrics:
        - {name: ApproximateNumberOfMessagesVisible, statistics: [Maximum]}
        - {name: ApproximateAgeOfOldestMessage, statistics: [Maximum]}
```
Job-level `statistics`, `period`, `length`, `delay` (request data up to now minus delay), `nilToZero` (report 0 instead of
NaN when CloudWatch returns nothing), `addCloudwatchTimestamp` and `exportAllDataPoints` are overridable per metric.
Statistics: Maximum, Minimum, Sum, SampleCount, Average, or percentiles such as `p90`. Other job options include
`roles` (assume IAM roles, with optional `externalId`), `customTags`, `dimensionNameRequirements`, `roundingPeriod`
and `recentlyActiveOnly`.

Output names follow `aws_<service>_<metric>_<statistic>` (for example `aws_ec2_cpuutilization_maximum`); join with the
`aws_<service>_info` metric to pull tags in, for example
`aws_ec2_cpuutilization_average + on (name) group_left(tag_Name) aws_ec2_info`.

## Flags (defaults from the docs)
`-listen-address` 127.0.0.1:5000, `-scraping-interval` 300 (seconds), `-cloudwatch-concurrency` 5, `-tag-concurrency` 5,
`-metrics-per-query` 500 (metrics per GetMetricData request), `-disable-account-alias-lookup`, `-labels-snake-case`.

## IAM
The quick-start policy in the README grants `tag:GetResources`, `cloudwatch:GetMetricData`,
`cloudwatch:GetMetricStatistics`, `cloudwatch:ListMetrics`, `apigateway:GET` and `iam:ListAccountAliases` (the last is
skipped with `-disable-account-alias-lookup`); some services need more describe permissions, so check the README. On
EC2 YACE tries to assume the instance role (disable with `AWS_EC2_METADATA_DISABLED=true`).

## Gotchas
- Sparse metrics: with `addCloudwatchTimestamp` or `exportAllDataPoints`, Prometheus will not scrape samples with
  timestamps older than 2-3 hours, so S3-style sparse metrics can be dropped. `exportAllDataPoints` needs
  `addCloudwatchTimestamp` and a destination that accepts out-of-order timestamps.
- Raise `-scraping-interval`, narrow `searchTags` and `recentlyActiveOnly` to cut the number of metrics requested; see the
  AWS CloudWatch pricing page for current API costs (not checked here).

## Verify
- [ ] `aws_<service>_info` series exist for the tagged resources and the metric series appear after one scrape interval.

## Checked

2026-11-08. Confirmed against the YACE README (IAM policy, output examples, join queries) and docs/configuration.md
(flags and defaults, job fields). Removed as unconfirmed: the billing formula and 1-5 minute lag claim, the
`yace_cloudwatch_requests_total` self-metric, IRSA/Pod Identity advice, the 15s scrape warning, and the
dimension/series-cost note. The AWS pricing page is JavaScript only and was not used.
Method: documentation only; no commands were run.
