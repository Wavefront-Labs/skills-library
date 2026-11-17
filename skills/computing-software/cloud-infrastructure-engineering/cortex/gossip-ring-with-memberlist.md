---
id: computing-software.cloud-infrastructure-engineering.cortex.gossip-ring-with-memberlist
name: gossip-ring-with-memberlist
category: computing-software
field: cloud-infrastructure-engineering
product: cortex
tags: [memberlist, gossip, hash-ring, single-binary, kv-store]
level: practitioner
status: docs-checked
description: "Run Cortex with a memberlist gossip ring instead of Consul or Etcd, shown with two single-binary instances."
sources:
  - https://github.com/cortexproject/cortex/blob/master/docs/guides/gossip-ring-getting-started.md
  - https://github.com/cortexproject/cortex/blob/master/docs/architecture.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Cortex stores its ring in a key-value store. Besides Consul and Etcd it can build its own store on the memberlist gossip library, which removes the external dependency.

The getting-started example runs two single-binary Cortex instances on one machine with blocks storage and no external shipping, each using its own config file from the repository (`single-process-config-blocks-gossip-1.yaml` and `-2.yaml`):

```
go build ./cmd/cortex
./cortex -config.file docs/configuration/single-process-config-blocks-gossip-1.yaml
./cortex -config.file docs/configuration/single-process-config-blocks-gossip-2.yaml
```

Point Prometheus remote_write at the first instance, `http://localhost:9109/api/v1/push`. The distributor spreads samples across both instances. For querying, configure Grafana to use `http://localhost:9109/prometheus` as a Prometheus data source.

The storage engine and external storage configuration do not depend on the ring configuration. The two instances find each other through the `memberlist` block (`node_name`, `bind_port: 7946`, `cluster_label`, `join_members` pointing at the other instance's port, `abort_if_cluster_join_fails: false`); ingester `join_after` and `observe_period` of 10 seconds reduce the chance of two instances generating conflicting tokens before they see each other. Ring state is visible at `/ring` on each instance.

A third instance needs unique HTTP, gRPC and memberlist bind ports, a unique ingester ID and `node_name`, and its own TSDB and sync directories; it only needs to join one existing peer. On Kubernetes, point `join_members` at a headless service covering the pods. In production set `memberlist.cluster_label` identically on every process of the cluster so rings of other Cortex, Mimir or Loki deployments are not merged by accident.

Memberlist is a supported KV store for the hash ring, but not for the HA tracker: gossip is too slow there, so different distributors may see different elected replicas. Use Consul or Etcd for the HA tracker.

## Checked

Method: docs-checked 2026-11-09 against the Cortex gossip ring getting-started guide and the architecture page (raw markdown, both read in full). The live migration from Consul or Etcd was not covered by these pages and has been dropped.
