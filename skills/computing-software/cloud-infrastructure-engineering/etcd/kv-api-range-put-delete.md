---
id: computing-software.cloud-infrastructure-engineering.etcd.kv-api-range-put-delete
name: kv-api-range-put-delete
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [kv-api, range, put, deleterange, revision, response-header, sort, count-only, serializable]
level: advanced
status: docs-checked
description: "The KV gRPC API: Range, Put, DeleteRange and Txn requests, response headers and the key-value fields."
sources:
  - "https://etcd.io/docs/v3.5/learning/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The KV service creates, updates, fetches and deletes key-value pairs through `Range`, `Put`, `DeleteRange` and `Txn`.

Every response carries a `ResponseHeader` with `cluster_id`, `member_id`, `revision` (the store revision when the response was generated) and `raft_term`. Applications use the revision to learn the latest store revision, which matters for historical (time travel) queries, and the raft term to detect a completed leader election.

A key-value pair holds `key` (non-empty bytes), `value`, `create_revision` (last creation), `mod_revision` (last modification), `version` (a deletion resets it to zero, any modification increases it) and `lease` (0 means no lease).

`RangeRequest` fields: `key`, `range_end`, `limit` (0 means no limit), `revision` (zero or less means the latest store; a compacted revision returns ErrCompacted), `sort_order` (NONE, ASCEND, DESCEND), `sort_target` (KEY, VERSION, CREATE, MOD, VALUE), `serializable`, `keys_only`, `count_only`, and `min_mod_revision`, `max_mod_revision`, `min_create_revision`, `max_create_revision` filters. The `RangeResponse` has `kvs` (empty when `count_only` is set), `more` (whether more keys remain when a limit is set) and `count`.

`PutRequest` has `key`, `value`, `lease` (0 means none), `prev_kv` (return the pair before the update), `ignore_value` and `ignore_lease` (update without changing the current value or lease; an error if the key does not exist).

`DeleteRangeRequest` has `key`, `range_end` and `prev_kv`; the response has `deleted` and `prev_kvs`.

Keys live in a flat binary key space addressed by `[key, range_end)` intervals. By default reads are linearizable; `serializable` requests are served locally without consensus, which is faster and more available but may be stale.

In a transaction the inner responses' headers should not be interpreted; read the revision from the top-level `TxnResponse` header.

## Checked

2026-11-08. Read the v3.5 API overview in full. Confirmed: RangeRequest, PutRequest, DeleteRangeRequest fields and responses, response header, KeyValue fields, flat key space, linearizable default and serializable option. Removed: the Compact RPC and the JSON gateway remark, which the page does not state.

Method: documentation only; no commands were run.
