---
id: computing-software.messaging-and-integration.apache-zookeeper.zkcli-acl-quota-watch-commands
name: zkcli-acl-quota-watch-commands
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, zkcli, zkcli-setacl, zkcli-quota, removewatches, addauth, reconfig-cli]
level: practitioner
status: docs-checked
description: "zkCli admin commands: addauth, getAcl and setAcl, setquota/listquota/delquota, removewatches and reconfig, with flags."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zkCli: ACL, quota, watch and reconfig commands

- `addauth scheme auth`: add credentials for ACL checks (e.g. `addauth digest user1:12345`). A super user needs `zookeeper.DigestAuthenticationProvider.superDigest` set on the server.
- `getAcl [-s] path`; `setAcl [-s] [-v version] [-R] path acl` (`-R` recursive; `-v` sets the ACL only at the given `aclVersion` from `stat`). Example ACL form: `auth:user1:12345:crwad`.
- `setquota -n|-b|-N|-B val path`; `listquota path`; `delquota [-n|-b|-N|-B] path` (see the quotas skill).
- `removewatches path [-c|-d|-a] [-l]`: the page's example removes the watches on a node and prints a `DataWatchRemoved` event; flag meanings are not given on the page.
- `reconfig [-s] [-v version] [[-file path] | [-members ...]] | [-add serverId=...]* [-remove serverId,...]`: needs `reconfigEnabled=true` in `zoo.cfg`, and a super user or `skipAcl`, otherwise `Insufficient permission`. Read the Dynamic Reconfiguration guide's Security section first. `-v` applies the change only if the current config version matches.
- The help listing in the guide shows no `addWatch` command.

Verify: `getAcl /path` reflects the `setAcl` change and `listquota` shows the quota.

## Checked
Confirmed against the zkCli reference, 2026-11-08. Removed: the `-l` "local only" meaning and the child/data/any labels for removewatches flags, which the page does not define.
Method: docs-only read of cited pages, 2026-11-08
