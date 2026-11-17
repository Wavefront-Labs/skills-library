---
id: computing-software.systems-network-administration.virtualisation.lxc-container-vs-vm-choice
name: lxc-container-vs-vm-choice
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [container-vs-vm, lxc, pct, system-container, kvm, isolation, workload-placement, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Decide between an LXC system container and a KVM VM on Proxmox: isolation, kernel coupling, live migration, density, backups and the workloads that belong in each."
sources:
  - https://github.com/proxmox/pve-docs/blob/master/pct.adoc
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#chapter_pct
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Choosing LXC container or VM

**Goal:** pick the right guest type per workload so you are not rebuilding it later.

## Comparison
| Aspect | LXC container | KVM VM |
|---|---|---|
| Kernel | Shares host kernel | Own kernel |
| OS | Linux only | Any (Windows, BSD, appliances) |
| Isolation | Namespaces/cgroups/AppArmor; kernel bug = shared risk | Hardware virtualisation boundary |
| Overhead | Very low (density, near-native I/O) | Higher memory and CPU overhead |
| Live migration | **No** (restart migration: brief downtime) | Yes |
| Kernel modules, sysctls, custom kernels | Not from inside | Yes |
| Application (OCI) containers | Technology preview in the container stack | Nest containers inside a VM when you need maximum isolation and live migration |
| Snapshots/backups | Yes (vzdump, storage snapshots) | Yes (vzdump, snapshots) |

## Good fits for containers
DNS/DHCP, reverse proxies, small web apps, monitoring agents and collectors, build
runners that don't need Docker, lab and dev boxes, many small single-purpose services.

## Use a VM when
- Multi-tenant or untrusted code (containers share the host kernel and expose an attack surface; the docs say full VMs give better isolation).
- Needs live migration for zero-downtime maintenance.
- Windows or other non-Linux operating systems (only Linux distributions run in containers), or a custom kernel.
- You want to run application containers with the strongest isolation: nest them in a VM.

## Gotchas
- A running container cannot be live-migrated; a restart migration shuts it down, moves it and starts it again (shutdown timeout default 180 seconds), so plan the downtime.
- Container migration, snapshot and backup set a lock; `pct unlock <CTID>` clears a stale one after a power failure, only if you are sure no action is still running.

## Verify
Each workload's placement record states why (isolation, migration, OS); maintenance
playbooks account for container restart migration downtime.

## Checked

2026-10-26 against the Proxmox VE admin guide sources (github.com/proxmox/pve-docs master, last commit 2026-10-17: pct.adoc, Introduction and Migration sections) and confirmed that containers use the host kernel, only Linux guests run, running containers cannot be live-migrated (restart migration, 180 second default timeout), VMs give better isolation, and OCI application containers are a technology preview. Removed unconfirmed claims about Docker fragility, dirty-bitmap incrementals, WireGuard, ZFS-inside, vendor support and lxcfs meminfo behaviour.

Method: documentation only; no commands were run.
