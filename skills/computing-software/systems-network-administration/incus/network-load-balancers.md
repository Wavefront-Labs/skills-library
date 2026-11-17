---
id: computing-software.systems-network-administration.incus.network-load-balancers
name: network-load-balancers
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, load-balancer, ovn, backend, listen-address, ports]
level: practitioner
status: docs-checked
description: "Configure Incus network load balancers on OVN networks: create, add backends and port rules, listen address constraints and target port mapping."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/network_load_balancers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network load balancers (OVN only)

```
incus network load-balancer create <network> <listen_address> [options...]
incus network load-balancer backend add <network> <listen_address> <backend> <target_address> [<target_ports>]
incus network load-balancer port add <network> <listen_address> <protocol> <listen_ports> <backend>[,<backend>...]
incus network load-balancer edit <network> <listen_address>
incus network load-balancer delete <network> <listen_address>
```

- One external listen address per load balancer, allowed by the uplink's `ipv{n}.routes` or the project's `restricted.networks.subnets`, with no overlap with other subnets.
- Backend: name, target address (same subnet as the network), optional target ports and description. No target port means the listen port is used.
- Port rule: protocol `tcp` or `udp`, listen port or set (`80,90-100`), list of backends, optional description.
- Port mapping: one target port for all listen ports, or a set matching the listen ports in number and position.

## Checked

2026-11-04: confirmed against the Incus network load balancers how-to (OVN only, command syntax, listen address rules, backend and port properties, target port mapping). Nothing removed.

Method: documentation only; no commands were run.
