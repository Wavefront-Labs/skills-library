---
id: computing-software.messaging-and-integration.apache-zookeeper.quotas
name: quotas
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, quotas, setquota, listquota, delquota, hard-quota, soft-quota]
level: practitioner
status: docs-checked
description: "ZooKeeper quotas: count and bytes limits via setquota, soft versus hard enforcement, one quota per path, /zookeeper/quota ACL protection and chroot pairing."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperQuotas.html
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quotas

- Types: namespace (node count under a path including itself) and bytes (data size).
- CLI: `setquota -n|-b|-N|-B val path` (`-n`/`-b` soft count/bytes, `-N`/`-B` hard); `listquota path`; `delquota [-n|-b|-N|-B] path`. Setting on a path with no quota creates one, otherwise updates it.
- Stored under `/zookeeper/quota`; restrict its ACL so only admins can read and write it. A quota cannot be set on a path under `/zookeeper/quota`.
- A quota covers the path and all descendants; only one quota per root-to-leaf path, and `setquota` rejects conflicts, naming the parent or child path, so you can delete or move quotas.
- Soft: warning in the server log only (`Quota exceeded: ...`). Hard: also throws `QuotaExceededException`. Hard wins if both set on the same path.
- Pair with a chroot to isolate apps (example: `-n 100000` on `/apps/app1`).

Verify: `listquota /path` shows the limits and current count/bytes; exceeding a hard quota is rejected (CLI prints `Count Quota has exceeded` or `Bytes Quota has exceeded`).

## Checked
Confirmed against the ZooKeeper Quota's Guide and the zkCli page examples (setquota, listquota, delquota), 2026-11-08.
Method: docs-only read of cited pages, 2026-11-08
