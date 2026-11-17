---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-delete
name: etcdctl-delete
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [del, delete, prefix, prev-kv, delete-range, from-key]
level: intro
status: docs-checked
description: "Delete keys with etcdctl del, including prefix, range, --from-key and --prev-kv, and how deletes affect versions and revisions."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
  - "https://etcd.io/docs/v3.5/learning/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`etcdctl del` removes a key or range of keys and prints the number deleted.

```bash
etcdctl del foo                 # 1
etcdctl del foo foo9            # range [foo, foo9)
etcdctl del --prefix zoo
etcdctl del --from-key b        # keys greater than or equal to b
etcdctl del --prev-kv zoo       # also prints the deleted key and value
```

- A range is the half-open interval from the first key up to but excluding the end key.
- `--prefix` deletes all keys beginning with the prefix.
- `--from-key` deletes keys greater than or equal to the byte value of the given key.
- `--prev-kv` returns the contents of the deleted key-value pairs.

Semantics from the API overview:

- Deleting is a modification of the key space, so it increments the store revision. A delete event is generated for watchers, carrying the deleted key with its modification revision set to the revision of deletion.
- A deletion resets the key's `version` to zero; creating the key again gives a PUT event with `kv.Version=1`.
- Etcd keeps superseded revisions until compaction, and a read at a compacted revision fails with ErrCompacted.
- `DeleteRange` can also be placed in a transaction's then or else block. Within one transaction a delete may not share keys with any put or other delete.

## Checked

2026-11-08. Read the v3.5 interacting-with-etcd guide and the API overview in full. Confirmed: del forms (--prefix, --from-key, --prev-kv, range), version reset, DELETE event semantics, transaction key-sharing rule. Removed: the space-reclaim and bulk-delete size advice and the lock-key example, which the pages do not state.

Method: documentation only; no commands were run.
