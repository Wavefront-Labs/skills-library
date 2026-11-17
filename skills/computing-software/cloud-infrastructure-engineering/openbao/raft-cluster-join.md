---
id: computing-software.cloud-infrastructure-engineering.openbao.raft-cluster-join
name: raft-cluster-join
category: computing-software
field: cloud-infrastructure-engineering
product: openbao
tags: [openbao, raft, integrated-storage, retry-join, non-voter]
level: practitioner
status: docs-checked
description: "Form an OpenBao Integrated Storage cluster: cluster port 8201, bao operator raft join, retry_join and auto_join, non-voters and peer removal."
sources:
  - https://raw.githubusercontent.com/openbao/openbao/main/website/content/docs/concepts/integrated-storage/index.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Raft cluster join

Integrated Storage keeps data on each server's filesystem and replicates by consensus; no third-party system. Traffic uses mTLS on the cluster port (default 8201). `cluster_addr` is required. Init creates a cluster of size 1; other nodes join the active node. A majority of voters must be alive.

## Joining

```
bao operator raft join
bao operator raft join -non-voter
bao operator raft list-peers
bao operator raft remove-peer
```

- A joiner must use the same seal mechanism: same KMS provider and key for auto-unseal, or supplied unseal keys for Shamir.
- A joined node cannot be re-joined to a different cluster.
- Use the leader's API address; setting `api_addr` everywhere simplifies this.
- Automatic joins: `retry_join` blocks with `leader_api_addr` or `auto_join`. Discovered peers default to HTTPS on 8200 (`auto_join_scheme`, `auto_join_port`).
- Non-voters get all data but do not count for quorum; useful for read scaling.

## Gotcha

Auto-join over TLS can fail when discovered IPs are missing from certificate IP SANs. Use `leader_tls_servername`, a constrained CIDR, or a load balancer.

Config keys: `path`, `node_id`, `retry_join`, `leader_api_addr`, `auto_join`, `leader_tls_servername`.

## Checked

2026-11-04. Read the OpenBao Integrated Storage concepts page in full. Confirmed: mTLS on cluster port 8201, `cluster_addr` requirement, size-1 cluster at init, same-seal join rule, no re-join, leader API address, `retry_join` with `leader_api_addr` or `auto_join`, default HTTPS and 8200, `-non-voter`, `remove-peer`, `list-peers` and the TLS SAN workarounds. Removed: nothing.
Method: documentation only; no commands were run.
