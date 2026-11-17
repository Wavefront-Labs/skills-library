---
id: computing-software.messaging-and-integration.strimzi.leader-election
name: leader-election
category: computing-software
field: messaging-and-integration
product: strimzi
tags: [leader-election, operator-replicas, lease]
level: advanced
status: docs-checked
description: "Run standby Cluster Operator replicas with leader election."
sources: ["https://strimzi.io/docs/operators/latest/deploying.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Leader election for Cluster Operator replicas

**Goal:** keep extra Cluster Operator replicas on standby.

By default one operator replica is deployed. Leader election lets additional replicas wait in standby in case of disruption.

Variables:

- `STRIMZI_LEADER_ELECTION_ENABLED`: optional, `false` by default. It is only enabled when applied on installation.
- `STRIMZI_LEADER_ELECTION_LEASE_NAME`: required when enabled; the Kubernetes `Lease` resource name.
- `STRIMZI_LEADER_ELECTION_LEASE_NAMESPACE`: the lease namespace.
- `STRIMZI_LEADER_ELECTION_IDENTITY`: the identity used for the lease.
- `STRIMZI_LEADER_ELECTION_LEASE_DURATION_MS`: default 15000 ms, how long the acquired lease is valid.
- `STRIMZI_LEADER_ELECTION_RENEW_DEADLINE_MS`: default 10000 ms, how long the leader tries to keep leadership.
- `STRIMZI_LEADER_ELECTION_RETRY_PERIOD_MS`: default 2000 ms, how often the leader updates the lock.

```yaml
env:
  - name: STRIMZI_LEADER_ELECTION_ENABLED
    value: "true"
  - name: STRIMZI_LEADER_ELECTION_LEASE_NAME
    value: strimzi-cluster-operator
```

With Helm you can also raise replicas, for example `--set replicas=2`.

**Checklist**

1. Enable leader election at install time.
2. Set the lease name and namespace.
3. Then increase replicas.

## Checked

2026-11-03. Confirmed in the Enabling leader election section: all seven STRIMZI_LEADER_ELECTION_* variables, the false default and install-time-only note, required lease name/namespace/identity, and the 15000/10000/2000 ms defaults.

Method: documentation only; no commands were run.
