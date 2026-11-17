---
id: computing-software.cloud-infrastructure-engineering.etcd.why-etcd-use-cases
name: why-etcd-use-cases
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [why-etcd, use-cases, kubernetes, service-discovery, configuration, coordination, consistency, comparison]
level: intro
status: docs-checked
description: "What etcd is for: a strongly consistent store for configuration, discovery and coordination, with Kubernetes as the main user."
sources:
  - "https://etcd.io/docs/v3.5/learning/why/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd is a general substrate for large-scale distributed systems that will never tolerate split-brain and will sacrifice availability to avoid it. It stores metadata consistently and fault-tolerantly. The name is the unix `/etc` folder plus "distributed".

Typical uses (from the Why page): configuration management, service discovery and coordinating distributed work; patterns such as leader election, distributed locks and monitoring machine liveness; production systems such as container schedulers, discovery services and distributed data storage.

- Kubernetes stores configuration data in etcd for service discovery and cluster management; its API server persists cluster state there and uses the watch API to monitor the cluster and roll out critical configuration changes.
- Container Linux's locksmith implements a distributed semaphore over etcd so only a subset of a cluster reboots at once.

When it fits: metadata or metadata ordering, up to a few GB. All data lives in one consistent replication group; every modification gets a revision from a monotonically increasing counter and needs only the raft protocol to commit. When it does not fit: more than a few GB, full SQL queries, or a large store spanning data centers without heavy global ordering needs. Replication cannot scale horizontally because there is no sharding; choose a NewSQL database (Cloud Spanner, CockroachDB, TiDB) instead.

Versus alternatives (the page says its authors favor etcd):

- ZooKeeper: etcd adds dynamic membership reconfiguration, MVCC, watches that never silently drop events, leases that decouple connections from sessions and safe lock APIs. Its gRPC client protocol can also be reached as JSON over HTTP, for example with curl.
- Consul: an end-to-end service discovery framework with health checking and DNS; its KV store lacks multi-version keys, conditional transactions and reliable streaming watches. For a consistent KV store choose etcd; for end-to-end discovery choose Kubernetes, Consul or SmartStack.

Locks and leases: etcd has watches, leases, elections and shared locks built in. The lock API cannot be a mutual exclusion mechanism by itself, because a lease TTL is physical time measured on separate clocks, so a client can still believe it holds a lease the server has revoked. Mutual exclusion comes from version-number validation (revision and lease ID conditions on Put or Txn). The revision acts as a fencing token. The lock cannot protect resources outside etcd unless they also validate version numbers.

## Checked

2026-11-08. Read in full: etcd v3.5 "etcd versus other key-value stores" page. Confirmed everything above. Removed: the FAQ source (not read for these claims), the claim that etcd is written in Go, the 2 GiB default quota, 3-versus-5-node failure tolerance, throughput figures, the TLS and API quality list and the "low-latency storage" advice (not on this page).
Method: documentation only; no commands were run.
