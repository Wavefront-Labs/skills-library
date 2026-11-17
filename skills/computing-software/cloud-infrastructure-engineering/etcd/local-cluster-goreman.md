---
id: computing-software.cloud-infrastructure-engineering.etcd.local-cluster-goreman
name: local-cluster-goreman
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [local-cluster, goreman, procfile, development, multi-member, ports, testing]
level: intro
status: docs-checked
description: "Start a three-member etcd cluster locally with goreman and a Procfile, using ports 2379, 22379 and 32379."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/local_cluster/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

For development, run a multi-member cluster on one machine. The docs use goreman, a Go process manager that reads a `Procfile`.

Install etcd, then `go install github.com/mattn/goreman@latest`. The repository provides a Procfile starting three members with different client and peer ports:

- infra1: client `localhost:2379`, peer 2380
- infra2: client `localhost:22379`, peer 22380
- infra3: client `localhost:32379`, peer 32380

The Procfile is at the base of the etcd git repository; run goreman from the root of the source tree.

Run it:

```bash
goreman -f Procfile start
etcdctl --write-out=table --endpoints=localhost:2379 member list
```

To exercise fault tolerance, stop a member with `goreman run stop etcd2`, then `etcdctl put key hello` and `etcdctl get key` still work, while `etcdctl --endpoints=localhost:22379 get key` fails with a connection error. Restart it with `goreman run restart etcd2` and the stopped member returns the key.

A single standalone member (`./etcd`) listens on `localhost:2379` for client requests.

## Checked

2026-11-03. Confirmed on the v3.5 local cluster page: goreman install command, stock Procfile at the repository root, `goreman -f Procfile start`, client ports localhost:2379, 22379 and 32379, member list command, members infra1-infra3 with peer ports, fault tolerance steps with goreman run stop and restart etcd2, standalone member on localhost:2379. Removed: per-member flag details, the TLS flags, the quorum-loss statement and the data directory cleanup advice, none of which the page contains.

Method: documentation only; no commands were run.
