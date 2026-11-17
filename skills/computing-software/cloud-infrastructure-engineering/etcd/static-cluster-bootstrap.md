---
id: computing-software.cloud-infrastructure-engineering.etcd.static-cluster-bootstrap
name: static-cluster-bootstrap
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [clustering, static-bootstrap, initial-cluster, initial-cluster-token, initial-cluster-state, bootstrap, three-node]
level: practitioner
status: docs-checked
description: "Bootstrap a cluster with known members using --initial-cluster, --initial-cluster-state and a unique --initial-cluster-token."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/clustering/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Static bootstrapping needs the IP and name of every member in advance.

```bash
etcd --name infra0 --initial-advertise-peer-urls http://10.0.1.10:2380   --listen-peer-urls http://10.0.1.10:2380   --listen-client-urls http://10.0.1.10:2379,http://127.0.0.1:2379   --advertise-client-urls http://10.0.1.10:2379   --initial-cluster-token etcd-cluster-1   --initial-cluster infra0=http://10.0.1.10:2380,infra1=http://10.0.1.11:2380,infra2=http://10.0.1.12:2380   --initial-cluster-state new
```

Run the equivalent on each host with its own `--name` and addresses.

Rules:

- `--initial-cluster` lists every member as `name=peerURL`; the URLs are the advertised peer URLs and must match `--initial-advertise-peer-urls` on the respective members.
- `--initial-cluster-token` gives the cluster a unique ID so etcd generates unique cluster and member IDs even when clusters have the exact same configuration, protecting against cross-cluster interaction that might corrupt them; the page recommends a unique token per cluster when creating several or recreating one for testing.
- `--initial-cluster-state` is `new` or `existing`; the static example uses `new`.
- Command line parameters starting with `--initial-cluster` are ignored on subsequent runs of etcd, so you can remove them after the first bootstrap. Later membership changes use runtime reconfiguration.

A member whose `--initial-cluster` differs from the others reports `conflicting cluster ID to the target cluster` and exits. A member whose `--initial-advertise-peer-urls` differs from its entry in `--initial-cluster` fails with `has different advertised URLs in the cluster and advertised peer URLs list`.

The guide also has a TLS section (self-signed certificates and automatic certificates).

## Checked

2026-11-03. Confirmed on the v3.5 clustering guide (Static section): the example command and flags, advertised peer URL match rule, unique --initial-cluster-token purpose, initial-cluster flags ignored on subsequent runs, the two error messages, and the TLS section. Removed: the --name match rule and the failed-bootstrap cleanup advice, which the page does not state.

Method: documentation only; no commands were run.
