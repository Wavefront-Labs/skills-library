---
id: computing-software.systems-network-administration.incus.network-create-attach
name: network-create-attach
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, network, network-create, bridge, ovn, macvlan, sriov, physical, nic, cluster]
level: practitioner
status: docs-checked
description: "Create managed Incus networks (bridge, ovn, macvlan, sriov, physical), create them per member in a cluster with --target, and attach them to instances."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/network_create.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Create and attach networks

```
incus network create <name> --type=<type> [options...]
incus network create UPLINK --type=physical parent=br0 --target=vm01
incus network create UPLINK --type=physical
incus network attach <network> <instance> eth0
incus config device add <instance> <device> nic network=<network>
```

- Types: `bridge` (the default when `--type` is omitted), `ovn`, `macvlan`, `sriov`, `physical`.
- Cluster: create a pending network on every member with `--target=<member>` and that member's settings (same name everywhere), then run create once without `--target`.
- `network attach` takes optional device and interface names; always give the device name, otherwise the network name becomes the device name. Incus images auto-configure `eth0`.
- Extra NIC options on `config device add` override network defaults.
- Use `--help` on any `incus network` command for the rest.

## Checked

2026-11-04: confirmed against the Incus create-a-network how-to (network types, default `bridge` type, cluster pending-then-create flow, `network attach` syntax and device-name advice, NIC device alternative). Nothing removed.

Method: documentation only; no commands were run.
