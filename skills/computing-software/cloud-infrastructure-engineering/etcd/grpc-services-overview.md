---
id: computing-software.cloud-infrastructure-engineering.etcd.grpc-services-overview
name: grpc-services-overview
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [grpc, services, kv, watch, lease, auth, cluster, maintenance, lock, election, protobuf]
level: intro
status: docs-checked
description: "The etcd v3 gRPC services: KV, Watch, Lease, Auth, Cluster, Maintenance, Lock and Election, and what each is for."
sources:
  - "https://etcd.io/docs/v3.5/learning/api/"
  - "https://etcd.io/docs/v3.5/dev-guide/api_concurrency_reference_v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

All etcd APIs are defined as gRPC services, which categorise the remote procedure calls the server understands. Every request to the server is a gRPC call. (The v2 API is deprecated as of v3.5.)

Services for the key space:

- KV: creates, updates, fetches and deletes key-value pairs (Range, Put, DeleteRange, Txn).
- Watch: monitors changes to keys.
- Lease: primitives for consuming client keep-alive messages (grant, revoke, keep alive).

Services that manage the cluster:

- Auth: role-based authentication of users.
- Cluster: membership information and configuration facilities.
- Maintenance: takes recovery snapshots, defragments the store and returns per-member status.

Concurrency services (from the concurrency reference):

- Lock: `Lock` acquires a named distributed shared lock and `Unlock` releases it.
- Election: `Campaign`, `Proclaim`, `Leader`, `Observe` and `Resign`.

Every RPC follows the same shape: a function `Name` takes a `NameRequest` and returns a `NameResponse`. Every response has a `ResponseHeader` with `cluster_id`, `member_id`, `revision` and `raft_term`. Applications can check the cluster and member IDs to be sure they reached the intended cluster or member.

The full RPC listing is in the gRPC API reference; the definitions live in the protobuf files.

## Checked

2026-11-08. Read the v3.5 API overview and the concurrency reference in full. Confirmed: service list and purposes, request and response naming, response header, Lock and Election methods. Removed: Compact RPC, Cluster and Maintenance method lists, Go client, error strings and port numbers, none stated on those pages.

Method: documentation only; no commands were run.
