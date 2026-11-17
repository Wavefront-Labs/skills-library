---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-settings-environment-variables
name: karpenter-settings-environment-variables
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [settings, environment-variables, cluster-name, cli-flags, interruption-queue, isolated-vpc, log-level, leader-election]
level: practitioner
status: docs-checked
description: "Karpenter controller settings (env var and CLI flag): CLUSTER_NAME required, endpoint discovery, INTERRUPTION_QUEUE, ISOLATED_VPC, ports, log level, client QPS and burst defaults."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/settings.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter controller settings

Each setting is an environment variable and a CLI flag (lowercase, hyphenated, `--` prefix).

Cluster and identity:
- `CLUSTER_NAME` (required): cluster for resource discovery.
- `CLUSTER_ENDPOINT`: if unset, discovered via `DescribeCluster`. `EKS_CONTROL_PLANE=true` tells Karpenter to discover details from DescribeCluster. `CLUSTER_CA_BUNDLE`: defaults to the controller's TLS config.
- `INTERRUPTION_QUEUE`: SQS queue name; interruption handling is disabled if unset and may need extra IAM permissions.
- `ISOLATED_VPC`: assume AWS services without a VPC endpoint are unreachable; also disables the on-demand pricing endpoint lookup.
- `RESERVED_ENIS` (default 0): ENIs not counted in max-pods or kube-reserved calculations; most often used with VPC CNI custom networking, and also needed when Security Groups for Pods reserves an ENI.
- `VM_MEMORY_OVERHEAD_PERCENT` (default 0.075): subtracted from instance memory when cached data is unavailable.

Operations:
- `LOG_LEVEL` (`debug`, `info`, `error`; default info), `LOG_OUTPUT_PATHS` (stdout), `LOG_ERROR_OUTPUT_PATHS` (stderr).
- `METRICS_PORT` 8080, `HEALTH_PROBE_PORT` 8081, `ENABLE_PROFILING`.
- `KUBE_CLIENT_QPS` 200, `KUBE_CLIENT_BURST` 300.
- `DISABLE_LEADER_ELECTION`, `LEADER_ELECTION_NAME` (default karpenter-leader-election), `LEADER_ELECTION_NAMESPACE`.
- `DISABLE_CONTROLLER_WARMUP`: warmup pre-populates caches to speed failover.
- `DISABLE_DRY_RUN`: disable dry-run validation of EC2NodeClasses.
- `DISABLE_CLUSTER_STATE_OBSERVABILITY`, `CPU_REQUESTS` (1000 millicores), `MEMORY_LIMIT` (GC soft limit is 90% of it).

Scheduling policy: `MIN_VALUES_POLICY` (`Strict` default or `BestEffort`) and `PREFERENCE_POLICY` (`Respect` default or `Ignore`, for preferred affinities and ScheduleAnyway spreads). `IGNORE_DRA_REQUESTS` skips DRA requests in simulation.

## Checked

2026-11-04. Confirmed against the Settings reference (v1.13) (identifiers, defaults, limits and prose). Removed the unconfirmed 'use RESERVED_ENIS 1' value.

Method: documentation only; no commands were run.
