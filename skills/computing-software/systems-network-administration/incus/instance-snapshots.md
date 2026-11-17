---
id: computing-software.systems-network-administration.incus.instance-snapshots
name: instance-snapshots
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, snapshot, restore, stateful, expiry, criu, backup]
level: practitioner
status: docs-checked
description: "Create, inspect, restore and delete Incus instance snapshots, including stateful snapshots for VMs and editing only the expiry date."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Instance snapshots

```
incus snapshot create <instance> [<snapshot name>]
incus info <instance>
incus config show <instance>/<snapshot>
incus config edit <instance>/<snapshot>
incus snapshot restore <instance> <snapshot>
incus snapshot delete <instance> <snapshot>
```

- `incus info` lists the snapshots.
- `--stateful` on create (VMs) captures running state as well as volume data; on restore it restores that state. Containers are not fully supported because of CRIU limitations.
- Only the expiry date can be changed through `config edit`; other edits are silently ignored.
- Snapshots live in the same storage pool as the instance volume.
- Custom volumes attached to an instance are not part of its snapshot or backup; back them up separately.

## Checked

2026-11-04: confirmed against the Incus instance backup how-to (snapshot create/show/edit/delete/restore commands, `--stateful` for VMs and CRIU caveat, expiry-only edits, same storage pool, custom volumes excluded). Nothing removed.

Method: documentation only; no commands were run.
