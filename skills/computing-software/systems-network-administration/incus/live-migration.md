---
id: computing-software.systems-network-administration.incus.live-migration
name: live-migration
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, live-migration, migration-stateful, criu, incremental-memory, vm, pre-copy]
level: advanced
status: docs-checked
description: "Live-migrate running Incus instances: migration.stateful for VMs, CRIU limits for containers, and migration.incremental.memory pre-copy."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/move_instances.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live migration

Moves a running instance. Full support for VMs, limited for containers.

VMs:
- Set `migration.stateful=true` on the instance to move with no downtime.
- Moving a VM to a different project inside a cluster: combine `--target-project` with `--target`. The instance must land on a different member, its devices must resolve to the same set in the target project, and custom volumes follow only if marked `dependent`.

Containers:
- CRIU must be installed on both systems.
- Only basic containers (non-systemd, no network device) migrate reliably; in most cases stop, move, and restart instead.
- `migration.incremental.memory=true` enables CRIU pre-copy. Transfer ends when the synced percentage hits `migration.incremental.memory.goal` or the loop count reaches `migration.incremental.memory.iterations`.

## Checked

2026-11-09. Confirmed against the Incus doc howto/move_instances.md (Live migration): VM stateful setting, cross-project rule, CRIU and basic-container limits, and the pre-copy options. Removed: nothing needed removing.

Method: documentation only; no commands were run.
