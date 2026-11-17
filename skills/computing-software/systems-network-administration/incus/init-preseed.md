---
id: computing-software.systems-network-administration.incus.init-preseed
name: init-preseed
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, admin-init, preseed, yaml, automation, storage-pools, networks, profiles]
level: practitioner
status: docs-checked
description: "Configure Incus with incus admin init --preseed: YAML sections, merge behaviour on existing installs, and the default-profile caveat."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/initialize.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preseed initialisation

Pipe a YAML document into `incus admin init --preseed`.

Top-level sections:
- `config`: server options, e.g. `core.https_address: 192.0.2.1:9999`, `images.auto_update_interval: 15` (hours).
- `networks`: `name`, `type`, `config`. Example: `incusbr0`, type `bridge`, `ipv4.address: auto`, `ipv6.address: none`.
- `storage_pools`: `name`, `driver` (e.g. `zfs`), `config.source`.
- `storage_volumes`: `name`, `pool`.
- `profiles`: `name`, `description`, `config` (e.g. `limits.memory`), `devices`. A `root` disk device takes `path`, `pool`, `type: disk`; a NIC takes `name`, `nictype: bridged`, `parent`, `type: nic`.

Behaviour:
- Unlike interactive mode, preseed does not change the default profile unless the YAML does.
- On an existing installation, missing entities are created and existing ones are merged with the new configuration.
- A conflict triggers a rollback attempt, which can rarely fail.

## Checked

2026-11-09. Confirmed against the Incus doc howto/initialize.md (Non-interactive configuration): the sections, example keys and values, merge rules, rollback note and default-profile behaviour. Removed: nothing needed removing.

Method: documentation only; no commands were run.
