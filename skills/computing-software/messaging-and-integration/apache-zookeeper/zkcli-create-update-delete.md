---
id: computing-software.messaging-and-integration.apache-zookeeper.zkcli-create-update-delete
name: zkcli-create-update-delete
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, zkcli, zkcli-create, zkcli-set, zkcli-delete, deleteall, version-check]
level: intro
status: docs-checked
description: "zkCli write commands: create with -s -e -c -t flags, set with -v version check, delete, deleteall, and the sample create/get/set/delete session."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
  - https://zookeeper.apache.org/doc/current/zookeeperStarted.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zkCli: create, update, delete

- `create [-s] [-e] [-c] [-t ttl] path [data] [acl]`: `-s` sequential (the server appends a counter, e.g. `/persistent_sequential_node0000000176`), `-e` ephemeral, `-c` container (deleted once its last child is deleted), `-t` TTL (example `-t 3000` expired after 3 s). TTL nodes need `zookeeper.extendedTypesEnabled=true`, otherwise `KeeperErrorCode = Unimplemented`.
- `set [-s] [-v version] path data`: `-v` is a compare-and-set against `dataVersion` (from `stat`); a mismatch prints `version No is not valid`.
- `delete [-v version] path`; `deleteall path` removes everything under a path.
- `sync path`: asynchronously syncs a node between leader and followers.

Sample session from the Getting Started guide:
```
create /zk_test my_data      -> Created /zk_test
get /zk_test                 -> my_data (dataVersion = 0)
set /zk_test junk            -> dataVersion = 1
delete /zk_test
```

Verify: after `set`, `get` shows the new data, a higher `dataVersion` and a new `mZxid`.

## Checked
Confirmed against the zkCli reference and the Getting Started guide, 2026-11-08. Removed: the claim that delete requires a childless node and that sync should run before reading, which the pages do not state.
Method: docs-only read of cited pages, 2026-11-08
