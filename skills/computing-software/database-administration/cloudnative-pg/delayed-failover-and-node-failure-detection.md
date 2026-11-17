---
id: computing-software.database-administration.cloudnative-pg.delayed-failover-and-node-failure-detection
name: delayed-failover-and-node-failure-detection
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [failoverdelay, node-failure, unreachable-taint, node-monitor-grace-period, isolation-check, kubelet]
level: advanced
status: docs-checked
description: "Delay failover with spec.failoverDelay and predict how long a dead node takes to trigger CloudNativePG failover: the Ready flip, taint eviction and the isolation check."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/failover.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.spec.failoverDelay` delays the start of failover by a number of seconds after the primary is detected unhealthy (default `0`, immediate). It is useful when failing over is worse than waiting, for example for short network or node instability, or when downstream logical subscribers would be disrupted.

When a node becomes unreachable (kubelet crash, partition from the API server) the operator relies on the pod `Ready` condition. The node lifecycle controller flips it to `False` once the node is `Unknown`. With stock settings that means `--node-monitor-grace-period` (40s on Kubernetes 1.29-1.31, 50s from 1.32) plus up to one `--node-monitor-period` (5s), so roughly **40 to 55 seconds** before the operator sees the primary unready. Managed Kubernetes (GKE, EKS, AKS) may tune this. Then `failoverDelay` applies.

The `Ready` flip is not throttled by the pod eviction rate limiters (`--node-eviction-rate`, `--secondary-node-eviction-rate`, `--unhealthy-zone-threshold`).

Pod eviction itself is separate: `tolerationSeconds` on the `node.kubernetes.io/unreachable` `NoExecute` taint, 300s by default. It does not hold up promotion. Full HA, with the old primary recreated on a healthy node, still waits for that eviction.

Meanwhile PostgreSQL on the isolated node is stopped locally, provided `.spec.probes.liveness.isolationCheck.enabled` is `true` (default): the instance manager requests a fast, then immediate, shutdown once its last lease renewal is older than the renew deadline and another instance is unreachable or names a different target primary. With `enabled: false` only the second cause stops it. The step-down appears as a container restart, not a liveness failure.

## Checked

2026-11-04. failoverDelay rationale and the node-level failure timeline confirmed on the Automated failover page, section Detection of node-level failures.

Method: documentation only; no commands were run.
