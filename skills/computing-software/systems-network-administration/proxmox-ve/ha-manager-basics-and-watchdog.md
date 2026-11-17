---
id: computing-software.systems-network-administration.proxmox-ve.ha-manager-basics-and-watchdog
name: ha-manager-basics-and-watchdog
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [ha-manager, ha-resource, watchdog, fencing]
level: advanced
status: docs-checked
description: "Put VMs and containers under HA with ha-manager, understand requested states, and how the watchdog fences a node on Proxmox VE."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Requirements: at least three cluster nodes for reliable quorum, shared storage for VMs and containers, and redundant hardware. A hardware watchdog is optional, and the Linux software watchdog (softdog) is the fallback.

An HA resource is a VM or container identified by a service ID such as `vm:100`.

```
ha-manager add vm:100
ha-manager set vm:100 --state stopped
ha-manager set vm:100 --state started
ha-manager status
ha-manager migrate vm:100 node2
ha-manager relocate vm:100 node2
ha-manager remove vm:100
```

Plain `qm start` and `qm stop` forward to the HA stack by setting the requested state. The stack is asynchronous, so results take a few seconds. `migrate` is an online migration, while `relocate` stops, moves and restarts, which can be faster when moving the memory is slow. `remove` also drops the resource from rules referencing it unless `--purge 0` is given, and does not start or stop it.

A resource should only use cluster-wide dependencies (shared storage, networks and devices present on all nodes). If something exists only on some nodes, restrict it with a strict node affinity rule.

Fencing: when a node loses quorum and the local resource manager is active, or an LRM or CRM process is not scheduled, the watchdog is no longer reset and the node reboots after 60 seconds. The CRM then takes over the lock and restarts its services on another node. With no service configured for more than 15 minutes, the CRM goes idle and closes the watchdog.

## Checked

2026-11-09. Compared with the requirements, management, fencing and watchdog sections of https://pve.proxmox.com/pve-docs/chapter-ha-manager.html; commands, the 60 second watchdog timeout, the 15 minute idle rule and the --purge 0 behaviour match.

Method: documentation only; no commands were run.

