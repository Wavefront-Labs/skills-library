---
id: computing-software.cloud-infrastructure-engineering.etcd.lease-api-and-expiry
name: lease-api-and-expiry
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [lease, lease-api, ttl, keepalive, checkpoint, expiry, lease-checkpoint, liveness]
level: advanced
status: docs-checked
description: "The Lease service: grant, revoke and keepalive semantics, key attachment and the lease checkpoint flag."
sources:
  - "https://etcd.io/docs/v3.5/learning/api/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Leases detect client liveness. The cluster grants a lease with a time-to-live, and the lease expires if the cluster does not receive a keepAlive within the TTL period.

Behaviour:

- `LeaseGrant`: `TTL` is advisory, in seconds; `ID` is the requested lease ID, and 0 lets etcd choose one. The response returns the `ID` and the server-selected `TTL` in seconds, so do not assume the granted TTL equals the requested one.
- `LeaseKeepAlive` is a bidirectional stream. The client sends a `LeaseKeepAliveRequest` with the lease `ID`; the response carries the `ID` and the new TTL remaining, in seconds.
- `LeaseRevoke` takes the lease `ID`; revoking deletes all attached keys.
- Each key may be attached to at most one lease (the `lease` field of a key-value pair; 0 means none, and a Put's `lease` field attaches one).
- When a lease expires or is revoked, all keys attached to it are deleted, and each expired key generates a delete event in the event history.

Experimental flag `--experimental-enable-lease-checkpoint` (default `false`) enables the primary lessor to persist the lease remaining TTL, to prevent indefinite auto-renewal of long-lived leases.

## Checked

2026-11-08. Read in full: etcd v3.5 API overview page and Configuration options page. Confirmed the grant, revoke and keep-alive fields, the one-lease-per-key rule, expiry deletes and events, and the checkpoint flag. Removed: LeaseTimeToLive and LeaseLeases, etcdctl --keys, the election-timeout minimum TTL, leader-change TTL reset behaviour, the keep-alive-at-a-third-of-TTL advice, and the Raft and quota remarks (not on the pages read).
Method: documentation only; no commands were run.
