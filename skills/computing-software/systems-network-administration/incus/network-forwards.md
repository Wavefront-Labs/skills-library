---
id: computing-software.systems-network-administration.incus.network-forwards
name: network-forwards
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, network-forward, port-forward, listen-address, snat, bridge, ovn, target-address]
level: practitioner
status: docs-checked
description: "Forward external addresses and ports to instances with Incus network forwards on bridge and OVN networks: listen address rules, default target, port specs and snat."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/network_forwards.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network forwards

```
incus network forward create <network> <listen_address> [options...]
incus network forward port add <network> <listen_address> <protocol> <listen_ports> <target_address> [<target_ports>]
incus network forward edit <network> <listen_address>
incus network forward delete <network> <listen_address>
```

Supported on `bridge` and `ovn` networks.

Listen address:
- Bridge: any non-conflicting address, not overlapping another network's subnet.
- OVN: must be in the uplink's `ipv{n}.routes` (or project `restricted.networks.subnets` if set), no overlap.

Default target: `target_address=<IP>` at creation; receives traffic matching no port spec; must be in the network's subnet.

Port spec: `protocol` (`tcp`/`udp`), `listen_port` (`80,90-100`), `target_address` (differs from default, same subnet), optional `target_port`, `description`, `snat`.
- One target port takes traffic from all listen ports; otherwise counts must match, mapped in order. Empty target port equals the listen port.
- `snat` adds a matching SNAT rule; currently only managed bridge networks with the `nftables` firewall driver.

## Checked

2026-11-04: confirmed against the Incus network forwards how-to (supported network types, listen address rules, default target, port specification syntax and properties, `snat` restriction). Nothing removed.

Method: documentation only; no commands were run.
