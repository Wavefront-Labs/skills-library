---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-get-prefix-range-options
name: etcdctl-get-prefix-range-options
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [get, prefix, from-key, range, rev, limit, sort, keys-only, time-travel]
level: practitioner
status: docs-checked
description: "Read many keys with etcdctl get: --prefix, ranges, --from-key, --limit and --rev time travel, plus the Range API options behind them."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
  - "https://etcd.io/docs/v3.5/learning/api/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcd indexes all keys over a flat binary key space; there are no directories. Listing is by key interval `[a, b)`, and these intervals are called ranges.

```bash
etcdctl get foo foo3              # range [foo, foo3): foo3 is excluded
etcdctl get --prefix foo          # all keys prefixed with foo
etcdctl get --prefix --limit=2 foo
etcdctl get --from-key b          # keys >= the byte value of b
etcdctl get --prefix --rev=3 foo  # the key space as of revision 3
```

Options:

- `--prefix` matches every key with that prefix.
- `--from-key` returns all keys greater than or equal to the given key.
- `--limit=N` caps the number of keys returned.
- `--rev=N` reads the key space as it was at revision N (a time travel query). Reading a compacted revision fails with `etcdserver: mvcc: required revision has been compacted`, and a revision before any data existed returns nothing.

The underlying `Range` API has more options than the guide shows as etcdctl flags: `keys_only`, `count_only`, `sort_order` (NONE, ASCEND, DESCEND), `sort_target` (KEY, VERSION, CREATE, MOD, VALUE), `serializable`, and filters on min and max mod and create revision. A `limit` of 0 means no limit, and a `revision` of zero or below reads the latest store. By default Range is linearizable; a serializable request is served locally and may be stale. The cited pages do not spell out etcdctl flag names for these.

Range encoding: `range_end` empty means the single key; `range_end` equal to the key plus one means all keys with that prefix; `range_end` of `\0` means all keys greater than or equal to the key; both `\0` means all keys. The response header carries the store revision at the time, which a caller can use to start a watch.

## Checked

2026-11-08. Read the v3.5 interacting-with-etcd guide and the API overview in full. Confirmed: range, --prefix, --from-key, --limit, --rev, compacted-revision error and the Range API options and range_end encodings. Removed: --keys-only, --order, --sort-by and --consistency flag spellings and the empty-key listing trick, which neither page states (the API fields are described instead).

Method: documentation only; no commands were run.
