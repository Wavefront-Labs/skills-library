---
id: computing-software.cloud-infrastructure-engineering.etcd.system-limits
name: system-limits
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [limits, max-request-bytes, quota-backend-bytes, storage-limit, request-size, max-txn-ops, sizing]
level: intro
status: docs-checked
description: "etcd limits: 1.5 MiB request size, 2 GiB default and 8 GiB suggested storage quota, and related tunables."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/limit/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd is built for small key-value metadata.

Request size: by default the maximum size of any request is 1.5 MiB. Larger requests may work but raise latency of other requests. Change it with `--max-request-bytes` on the server (default 1572864 bytes on the configuration page).

Storage size: the default backend quota is 2 GiB, set with `--quota-backend-bytes`. 8 GiB is the suggested maximum for normal environments, and etcd warns at startup if the configured value exceeds it. When the backend size exceeds the quota etcd raises an alarm; see the space-quota skill for the NOSPACE procedure.

Related limits and defaults:

- `--max-txn-ops` 128 operations per transaction.
- `--grpc-keepalive-min-time` 5s, `--grpc-keepalive-interval` 2h, `--grpc-keepalive-timeout` 20s.
- `--election-timeout` upper limit is 50000 ms (see the tuning page).

Larger requests will work but may increase the latency of other requests, so keep values small and avoid large blobs.

## Checked

2026-11-03. Confirmed on the v3.5 System limits page: designed for small metadata key-value pairs, default maximum request size 1.5 MiB changed with --max-request-bytes, default storage limit 2 GiB changed with --quota-backend-bytes, 8 GiB suggested maximum and a startup warning above it. Confirmed on the configuration page: --max-request-bytes 1572864, --max-txn-ops 128, --grpc-keepalive-min-time 5s, interval 2h, timeout 20s. Confirmed on the tuning page: election timeout upper limit 50000 ms. Removed: the exact error string, the roughly seven member claim and the unsourced NOSPACE recovery sequence.

Method: documentation only; no commands were run.
