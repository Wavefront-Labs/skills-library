---
id: computing-software.devops-ci-cd.nomad.snapshot-save-restore
name: snapshot-save-restore
category: computing-software
field: devops-ci-cd
product: nomad
tags: [nomad, snapshot-save, snapshot, operator-snapshot, restore, inspect, redact, stale, backup, disaster-recovery, raft, cli]
level: advanced
status: docs-checked
description: "Back up and restore Nomad server state with nomad operator snapshot save, restore and inspect, including -stale for leaderless clusters and -redact for keyring material."
sources: ["https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/operator/snapshot/save.mdx", "https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/operator/snapshot/restore.mdx", "https://github.com/hashicorp/web-unified-docs/blob/main/content/nomad/v1.10.x/content/commands/operator/snapshot/inspect.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nomad operator snapshot save / restore / inspect

A snapshot is an atomic, point-in-time copy of server state: jobs, nodes, allocations, periodic jobs and ACLs, plus the keyring. With ACLs on, a **management token** is required.

## Save
```
nomad operator snapshot save backup.snap
nomad operator snapshot save -stale backup.snap
```
- Default reads from the leader.
- `-stale` takes the data from any server; use when the cluster has no leader.
- `-redact` edits the snapshot locally to remove cleartext key material from the root keyring (only the AEAD keyring provider stores cleartext key material in Raft). It loads the whole snapshot into memory. Use it before sending a snapshot to HashiCorp Support if no KMS provider protects the keyring. The snapshot otherwise contains the keyring.

## Restore
```
nomad operator snapshot restore backup.snap
```
The docs call this a potentially dangerous low-level Raft operation that is not designed to survive server failures mid-restore. Intended for disaster recovery into a fresh cluster of Nomad servers.

## Inspect (local file, no cluster needed)
```
nomad operator snapshot inspect backup.snap
nomad operator snapshot inspect -json backup.snap
```
Prints Created, ID, Size, Index, Term, Version, then a per-type table (Job, Alloc, Node, Eval, ACLToken, Variables and others) with counts and sizes.

## Checked

2026-11-03. Confirmed against the Nomad 1.10 operator snapshot save, restore and inspect pages: management token, -stale and -redact semantics, restore danger warning, inspect output fields and per-type table. Removed: the mention of snapshot agent, redact and state subcommands and the backup-non-empty advice.

Method: documentation only; no commands were run.
