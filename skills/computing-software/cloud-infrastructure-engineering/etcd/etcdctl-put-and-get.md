---
id: computing-software.cloud-infrastructure-engineering.etcd.etcdctl-put-and-get
name: etcdctl-put-and-get
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [etcdctl, put, get, key-value, v3, api-version, lease]
level: intro
status: docs-checked
description: "Write and read keys with etcdctl put and get using the v3 API, including ETCDCTL_API, hex and value-only output and attaching a lease."
sources:
  - "https://etcd.io/docs/v3.5/dev-guide/interacting_v3/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

etcdctl is the command line tool for talking to an etcd server. Its API version is chosen with the `ETCDCTL_API` environment variable (`2` or `3`). From 3.4 it uses the v3 API by default; 3.3 and earlier default to v2. Keys created through the v2 API cannot be queried through the v3 API: a v3 `get` of a v2 key exits with 0 and returns no key data.

```bash
export ETCDCTL_API=3
etcdctl version
etcdctl put foo bar
# OK
etcdctl get foo
# foo
# bar
etcdctl get foo --hex
etcdctl get foo --print-value-only
etcdctl get mykey -w=json
```

- Every stored key is replicated to all cluster members through Raft.
- Plain `get KEY` prints the key line and then the value line. `--print-value-only` prints only the value. `--hex` prints both in hex escapes.
- `-w=json` (write-out) prints the response including its header. A `get` of a nonexistent key in JSON shows just the header, which is a way to read the current store revision.
- `etcdctl put KEY VALUE --lease=LEASEID` attaches the key to a lease, so it lives only for the lease's TTL. The lease ID comes from `etcdctl lease grant`.
- `etcdctl version` prints the etcdctl version and the server API version, useful for choosing the right commands.
- For ranges, prefixes and past revisions see the etcdctl get skill.

## Checked

2026-11-08. Read the v3.5 interacting-with-etcd guide in full. Confirmed: ETCDCTL_API behaviour and v2 key caveat, put, get, --hex, --print-value-only, -w=json, put --lease, etcdctl version. Corrected: v3 became the default in 3.4. Removed: --endpoints defaults, stdin multi-line values, put --prev-kv and the KV.Put mapping, none stated on the page.

Method: documentation only; no commands were run.
