---
id: computing-software.cloud-infrastructure-engineering.rook.mon-health-failover-timing
name: mon-health-failover-timing
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [mon-failover, quorum, paxos, health-check, mon-health, externalmonids, endpointslice]
level: advanced
status: docs-checked
description: "How Rook keeps mons healthy: the 45s check, 10m failover timeout, quorum maths, forcing or disabling failover, and external mons."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Advanced/ceph-mon-health/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A mon's identity is its IP address, so Rook creates a Kubernetes service per mon and its clusterIP is the stable identity; the pod binds to its podIP but is addressed via the service IP. Mons use a Paxos variant requiring a super-majority for quorum. Three mons tolerate one loss, five tolerate two, and one tolerates none; 50 percent is not enough, so two mons cannot lose one. Because the operator starts a replacement automatically, three mons are typically enough, and more mons add overhead to every cluster change.

Mitigation layers: each mon runs as a Deployment so Kubernetes restarts it, and mon metadata persists under `dataDirHostPath` or the `volumeClaimTemplate` volume so it can restart with its data. It is always better to revive an existing mon than fail over.

Failover timing: the operator checks mon health every 45 seconds, and if a mon is down it waits 10 minutes before failing it over. In the CephCluster CR:
```
healthCheck:
  daemonHealth:
    mon:
      interval: 45s
      timeout: 10m
```
Too short risks over-aggressive failover; too long risks losing quorum.

- To force failover for testing, scale the mon deployment to 0 and wait for the timeout; a reconcile or operator restart may scale it back.
- A mon stuck Pending (for example during a node drain) doubles the wait.
- Setting the timeout to 0 disables automatic failover, useful for planned maintenance.
- Changing `network.hostNetwork`, `network.provider` to host, or `network.multiClusterService` makes Rook fail over all mons.
- `mon.externalMonIDs` protects mons outside Rook (2-AZ setups); `mon.count` ignores them.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (ceph-mon-health) against this skill: 12 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
