---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-api-refresh-and-caching-settings
name: karpenter-api-refresh-and-caching-settings
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [ami-refresh-interval, subnet-refresh-interval, describeimages, describesubnets, api-throttling, staleness]
level: advanced
status: docs-checked
description: "AMI_REFRESH_INTERVAL and SUBNET_REFRESH_INTERVAL: default 1m, minimum 1m, reducing DescribeImages and DescribeSubnets calls at the cost of staleness in discovery and drift."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/settings.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AMI and subnet refresh intervals

Two settings control how often Karpenter re-reads EC2 data:

| Environment variable | Flag | Default | Minimum |
|---|---|---|---|
| `AMI_REFRESH_INTERVAL` | `--ami-refresh-interval` | `1m0s` | `1m` |
| `SUBNET_REFRESH_INTERVAL` | `--subnet-refresh-interval` | `1m0s` | `1m` |

- `AMI_REFRESH_INTERVAL`: how often AMI data is refreshed from EC2. A larger value means fewer `DescribeImages` calls but staler AMI discovery and staler drift detection.
- `SUBNET_REFRESH_INTERVAL`: how often subnet data is refreshed. A larger value means fewer `DescribeSubnets` calls but staler subnet discovery.

Both must be at least 1m.

Related setting: `ISOLATED_VPC` (`--isolated-vpc`), when true, assumes AWS services without a VPC endpoint are unreachable, which also disables look-ups to the AWS on-demand pricing endpoint.

## Checked

2026-11-08. Confirmed against the Settings reference (v1.13) (names, flags, defaults, minimums, descriptions). Removed the unsupported guidance on when to raise the intervals, the monitoring advice, the example argument values and the subnet-choice claim.

Method: documentation only; no commands were run.
