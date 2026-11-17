---
id: computing-software.cloud-infrastructure-engineering.hashicorp-consul.consul-snapshot-restore
name: consul-snapshot-restore
category: computing-software
field: cloud-infrastructure-engineering
product: hashicorp-consul
tags: [consul, snapshot-restore, disaster-recovery, consul-restore]
level: practitioner
status: docs-checked
description: "Restore a snapshot with consul snapshot restore into a fresh cluster running the same Consul version, with its ACL needs and a peers check."
sources: ["https://developer.hashicorp.com/consul/commands/snapshot/restore", "https://developer.hashicorp.com/consul/commands/snapshot/inspect", "https://developer.hashicorp.com/consul/commands/operator/raft"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`consul snapshot restore FILE` restores the key/value entries, service catalog, prepared queries, sessions and ACLs from a snapshot. The page calls it a potentially dangerous low-level Raft operation that is not designed to handle server failures during a restore, intended primarily for disaster recovery. It restores into a fresh cluster of Consul servers as long as the new cluster runs the same Consul version as the cluster that took the snapshot. With ACLs, it needs a `management` token.

```sh
consul snapshot inspect backup.snap     # ID, Size, Index, Term, Version, data type counts
consul snapshot restore backup.snap     # prints "Restored snapshot"
consul operator raft list-peers         # needs no ACL; shows leader and voters
```

For a total loss, stand up new servers and bootstrap them as usual, then restore into the new cluster.

Gotchas:
- Treat the restore as replacing server state with the snapshot's, so changes made after the snapshot was taken are not in it.
- `list-peers` prints Node, ID, Address, State, Voter, RaftProtocol, Commit Index and "Trails Leader By"; use it to confirm a stable leader and expected voters afterwards.
- Agent re-registration after a restore is handled by anti-entropy (see `consul-anti-entropy-consistency`).

## Checked

2026-11-03. Confirmed against the Consul v1.22 docs source: commands/snapshot/restore (warning, same-version requirement, `management` ACL, output), commands/snapshot/inspect (fields), commands/operator/raft (`list-peers`, ACL none, output columns). Removed: the claim that the cluster must already be healthy with a leader, advice to stop writers, the "confirm in upgrade docs" hedge, and the Verify step relying on `consul acl token list`.
Method: documentation only; no commands were run.
