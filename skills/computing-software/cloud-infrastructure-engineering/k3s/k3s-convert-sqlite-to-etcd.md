---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-convert-sqlite-to-etcd
name: k3s-convert-sqlite-to-etcd
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, sqlite, cluster-init, datastore-migration]
level: practitioner
status: docs-checked
description: "Convert an existing single-node SQLite K3s cluster to embedded etcd by restarting with --cluster-init."
sources:
  - https://docs.k3s.io/datastore/ha-embedded
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn a default single-node cluster into one that can take more servers.

Conversion: restart the K3s server with the `--cluster-init` flag. After that, add servers exactly as in a normal embedded etcd HA setup, joining with `--server https://<server1>:6443` and the shared token (`K3S_TOKEN`).

If an etcd datastore is already on disk (the node has initialized or joined a cluster), the datastore arguments (--cluster-init, --server, --datastore-endpoint and so on) are ignored.

An embedded etcd HA cluster needs an odd number of servers (three or more) to keep quorum, and embedded etcd may be slow on slow disks such as Raspberry Pi SD cards.

## Checked

2026-11-08: read the whole High Availability Embedded etcd page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/datastore/ha-embedded). Confirmed the --cluster-init restart conversion and the ignored-arguments rule. Removed unsupported claims: SQLite selection rules, the config.yaml form and the backup paths are not on this page.

Method: documentation only; no commands were run.
