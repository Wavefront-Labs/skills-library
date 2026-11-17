---
id: computing-software.systems-network-administration.virtualisation.proxmox-ha-resources-and-groups
name: proxmox-ha-resources-and-groups
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ha-manager, pve-ha, ha-group, ha-resource, ha-rules, node-affinity, max-restart, max-relocate, proxmox, proxmox-ve, cluster-resource-scheduler]
level: practitioner
status: docs-checked
description: "Make Proxmox guests highly available with ha-manager: add resources, requested states, restart/relocate limits, HA groups or node-affinity rules (PVE 9), and the CRS scheduler."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html
  - https://pve.proxmox.com/pve-docs/ha-manager.1.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Proxmox HA resources and groups

**Goal:** important guests restart automatically on another node after a node failure,
landing where you want them.

## Requirements
At least three cluster nodes (for reliable quorum), shared storage for VMs and containers, hardware redundancy and reliable server components. A hardware watchdog is optional; `softdog` is the fallback (see the fencing skill). Dependencies such as storage, networks and passthrough devices must exist on every node the resource may run on, or be restricted with rules.

## Add a resource
```sh
ha-manager add vm:120 --state started --max_restart 1 --max_relocate 1 --comment "web01"
ha-manager status
ha-manager config
```
Requested states: `started` (default; `enabled` is an alias), `stopped` (kept stopped, still relocated on node failure), `disabled` (stopped, not relocated; the way out of `error`) and `ignored` (resource removed from HA tracking, API calls bypass HA). `max_restart` and `max_relocate` both default to 1. Once HA-managed, start and stop guests through HA, since the CRM enforces the requested state.

## Placement
- **HA rules** (current): *node affinity* rules (which nodes, optional priorities, `--strict`, positive or negative affinity) and *resource affinity* rules (positive keeps resources on the same node, negative keeps them apart; strict by default):
```sh
ha-manager rules add node-affinity ha-rule-vm120 --resources vm:120 --nodes "pve1:2,pve2:2,pve3:1"
ha-manager rules set node-affinity ha-rule-vm120 --strict 1
ha-manager rules add resource-affinity keep-separate --affinity negative --resources vm:200,ct:300
```
  Rules that conflict are disabled until fixed (for example a resource may be in only one node affinity rule, and a resource affinity rule needs at least two resources).
- **HA groups** (`ha-manager groupadd`, `--nodes`, `--restricted`, `--nofailback`) are deprecated and were migrated to node affinity rules in Proxmox VE 9.0.
- **CRS** (cluster resource scheduler, Datacenter → Options → Cluster Resource Scheduling): mode `basic` (default; counts active guests), `static` (configured CPU and memory) or `dynamic` (adds average usage) picks recovery targets; the option `ha-rebalance-on-start` places a resource on the best node when it starts.

## Behaviour on failure
Node loses quorum → its watchdog resets it after 60 seconds → the CRM on a quorate node places the resources on other nodes (lowest load per the CRS mode, within the rules). The documentation quotes typical error detection and failover times of about 2 minutes; HA is restart, not lockstep.

## Gotchas
- Guests bound to local-only disks or passthrough devices cannot run elsewhere unless restricted to nodes that have them.
- `max_restart` and `max_relocate` control how often a failed start is retried on the same node and relocated to others.
- On node failure the CRM concentrates services on the remaining nodes; design the cluster for that worst case.

## Verify
`ha-manager status` shows the resources `started` on expected nodes and `ha-manager rules list` lists the rules; rehearse failures in the HA simulator before testing on real nodes.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, ha-manager.adoc and generated option files, last pushed 2026-10-17). Confirmed: minimum three nodes and shared storage requirement; resource options `state` (values, aliases, defaults), `max_restart`, `max_relocate` (default 1), `comment`; `ha-manager add|status|config|rules add|rules set|rules list` syntax; node and resource affinity rule behaviour and conflict rules; HA groups deprecated and migrated in Proxmox VE 9.0; CRS modes (basic default, static, dynamic) and `ha-rebalance-on-start`; typical failover about 2 minutes. Removed: the 2 + QDevice claim and the 2-3 minute estimate (not documented).

Method: documentation only; no commands were run.
