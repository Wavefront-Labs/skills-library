---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-watch
name: etcdctl-watch
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [watch, etcdctl, prefix, rev, prev-kv, interactive, events]
level: practitioner
status: docs-checked
description: "Watch keys and prefixes with etcdctl watch: ranges, start revisions, interactive mode, previous values and progress requests."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`etcdctl watch` monitors a key or range for updates.

```bash
etcdctl watch foo
etcdctl watch foo foo9              # range from foo to foo9
etcdctl watch --prefix foo
etcdctl watch foo --hex             # keys and values in hex
etcdctl watch --rev=2 foo           # changes since revision 2
etcdctl watch --prev-kv foo         # also show the value before the change
etcdctl watch -i                    # interactive session
```

Each event prints as `PUT`, then the key, then the value.

Notes:

- `--rev` starts from a historical revision. A watch that just stays connected is good enough, but if the application or etcd fails a change can happen unseen, so to guarantee delivery an application watches from a historical revision, as with reading past versions of keys.
- With `--prev-kv`, an event shows the key and the previous value, then the key and the new value.
- Interactive mode (`etcdctl watch -i`) takes commands: `watch foo` and `watch zoo` in the same session watch several keys at once.
- `progress` in an interactive session asks the server to send a progress notify update, such as `progress notify: 3`, so you can tell how up to date the watch stream is. This is useful when a watch feeds a cache: compare it with the revision from a quorum read.
- The revision in a progress notify comes from the member the watch is connected to. If that member is partitioned from quorum it can be lower than the revision a quorum read returns from a healthy member.

## Checked

2026-11-08. Read the v3.5 interacting-with-etcd guide in full. Confirmed: watch of key, range, prefix, --hex, --rev, --prev-kv, interactive mode, progress command and the partitioned-node caveat. Removed: --progress-notify flag, watch --rev inside interactive mode, compaction-failure advice and stream multiplexing remarks, none stated on that page.

Method: documentation only; no commands were run.
