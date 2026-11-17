---
id: computing-software.systems-network-administration.incus.move-and-copy-instances
name: move-and-copy-instances
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, move, copy, migration, remotes, transfer-mode, target, cluster]
level: practitioner
status: docs-checked
description: "Move or copy Incus instances between remotes or cluster members, choose pull/push/relay mode, and adapt config on the target."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/move_instances.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Move and copy instances

```
incus move [<src_remote>:]<src_instance> <target_remote>:[<target_instance>]
incus copy [<src_remote>:]<src_instance> <target_remote>:[<target_instance>]
incus move <instance> --target <cluster_member>
```

- Omit the source remote if it is your default; omit the target name to keep the name.
- With `--target`, do not give source or target remotes.
- Containers must be stopped before a move. VMs must be stopped or have live migration enabled.
- `--mode`: `pull` (default; target pulls from source), `push` (source pushes), `relay` (client connects to both).
- Adapt the copy with `--config`, `--device`, `--storage`, `--target-project`, `--no-profiles` or `--profile`.
- VMs moving inside a cluster take custom volumes on a local pool along if `migration.follow_instance` is `true`; such a volume attaches to only one VM.

## Checked

2026-11-09. Confirmed against the Incus doc howto/move_instances.md (top section): move and copy forms, --target rule, stop requirements, transfer modes, adaptation flags and the migration.follow_instance volume note. Removed: nothing needed removing.

Method: documentation only; no commands were run.
