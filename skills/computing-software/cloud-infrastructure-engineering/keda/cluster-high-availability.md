---
id: computing-software.cloud-infrastructure-engineering.keda.cluster-high-availability
name: cluster-high-availability
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [high-availability, leader-election, enable-aggregator-routing, operator-replicas, metrics-server-replicas]
level: advanced
status: docs-checked
description: "Run KEDA operator and metrics server replicas: only one operator is active, and only one metrics server may serve external.metrics.k8s.io."
sources:
  - https://keda.sh/docs/2.17/operate/cluster/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Summary of the support table: Metrics Server lists 1 supported replica and Operator lists 2. The table concerns availability, not throughput.
KEDA states it does not provide full high availability because of upstream limitations. Per deployment:

Metrics Server: the support table says 1 replica. You can run several replicas and the page recommends adding the `--enable-aggregator-routing=true` flag to the kube-apiserver so requests to the metrics servers are load balanced. But only one active metrics server can serve `external.metrics.k8s.io` in a Kubernetes cluster, and it has to be KEDA's. So you cannot combine KEDA with another provider of the external metrics API.

Operator: 2 replicas. Multiple replicas may run, but only one instance is active; the rest stand by. Extra replicas do not improve performance, they only reduce downtime during failover.

Leader election tuning uses controller-runtime properties set through environment variables on the Operator:
- `KEDA_OPERATOR_LEADER_ELECTION_LEASE_DURATION`, default 15s;
- `KEDA_OPERATOR_LEADER_ELECTION_RENEW_DEADLINE`, default 10s;
- `KEDA_OPERATOR_LEADER_ELECTION_RETRY_PERIOD`, default 2s.

## Checked

2026-11-03. Confirmed on the 2.17 Operate Cluster page: the HA table, enable-aggregator-routing, the three leader election variables and defaults.

Method: documentation only; no commands were run.
