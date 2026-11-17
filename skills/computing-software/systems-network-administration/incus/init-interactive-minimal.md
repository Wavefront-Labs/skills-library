---
id: computing-software.systems-network-administration.incus.init-interactive-minimal
name: init-interactive-minimal
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, admin-init, initialisation, storage-pool, bridge, minimal]
level: intro
status: docs-checked
description: "Initialise Incus with incus admin init: the interactive questions and defaults, and --minimal, which uses the dir storage driver."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/initialize.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# incus admin init

`incus admin init` starts the interactive setup. Simple setups can run as a normal user; joining a cluster needs root or `sudo`.

Questions, in order:
1. Clustering (default no; otherwise join or create a cluster).
2. Networking: create a new bridge (recommended) or use an existing bridge or interface.
3. Storage pools: a loop-backed pool is fine for testing; for production use an empty partition or whole disk. Recommended backends are `zfs` and `btrfs`.
4. Remote access (default no); clients can be added manually or by token.
5. Automatic image updates (default yes).
6. Print the answers as a preseed YAML.

`incus admin init --minimal` skips the questions and uses defaults, including the `dir` storage driver. That driver is slower and lacks fast snapshots, fast copy and launch, quotas and optimised backups.

Extra bridges and pools can be added later.

## Checked

2026-11-09. Confirmed against the Incus doc howto/initialize.md (Interactive configuration, Minimal setup): the question areas, defaults, root/sudo note, recommended backends and the dir driver limits. Removed: nothing needed removing.

Method: documentation only; no commands were run.
