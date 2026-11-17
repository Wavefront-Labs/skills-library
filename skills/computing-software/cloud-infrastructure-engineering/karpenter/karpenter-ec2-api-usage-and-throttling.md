---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-ec2-api-usage-and-throttling
name: karpenter-ec2-api-usage-and-throttling
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [ec2-api, throttling, requestlimitexceeded, metrics, refresh-interval, cloudtrail]
level: advanced
status: docs-checked
description: "Monitor Karpenter EC2 API call volume and throttling with aws_sdk_go_request metrics, PromQL examples, Service Quotas, multi-account isolation and refresh interval tuning."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/tasks/monitoring-ec2-api-usage.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Monitoring EC2 API usage and throttling

EC2 enforces per-account, per-Region request-rate limits; excess calls fail with `RequestLimitExceeded` (HTTP 503). Volume scales with the number of EC2NodeClasses and clusters, scaling frequency, and Karpenter version.

APIs Karpenter calls:
- Launch (hot path): `CreateFleet`, `CreateLaunchTemplate`, `RunInstances`, `CreateTags`.
- Terminate/cleanup: `TerminateInstances`, `DeleteLaunchTemplate`.
- Refresh per EC2NodeClass: `DescribeSubnets`, `DescribeSecurityGroups`, `DescribeImages`, `DescribeCapacityReservations`, `DescribeInstanceTypes`, `DescribeInstanceTypeOfferings`, `DescribeSpotPriceHistory`.
- Discovery: `DescribePlacementGroups`, `DescribeInstances`, `DescribeInstanceStatus`, `DescribeLaunchTemplates`.

Metrics (labels `service`, `action`, `code`): `aws_sdk_go_request_total`, `aws_sdk_go_request_attempt_total`, `aws_sdk_go_request_retry_count`. Sustained retries are an early throttling signal.

```
sum by (action) (rate(aws_sdk_go_request_total{service="EC2"}[5m]))

sum(rate(aws_sdk_go_request_total{service="EC2", code="503"}[5m]))
  / sum(rate(aws_sdk_go_request_total{service="EC2"}[5m]))
```

Attribution: Karpenter sets the User-Agent `karpenter.sh-<version>`; filter CloudTrail `userAgent` on that prefix.

Limits: compare against Service Quotas for EC2 in each Region; all clusters in one account share the same limits. Best practice is one cluster per account (multi-account) to spread load.

Workaround only: raise `SUBNET_REFRESH_INTERVAL` and `AMI_REFRESH_INTERVAL` (both default `1m`). Going from 1m to 5m cuts that call rate about 5x but makes Karpenter act on stale subnet IP counts or AMIs.

## Checked

2026-11-04. Confirmed against the Monitoring EC2 API usage task page (v1.13) (identifiers, defaults, limits and prose). Nothing material removed.

Method: documentation only; no commands were run.
