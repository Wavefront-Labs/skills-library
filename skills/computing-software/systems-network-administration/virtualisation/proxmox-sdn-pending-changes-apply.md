---
id: computing-software.systems-network-administration.virtualisation.proxmox-sdn-pending-changes-apply
name: proxmox-sdn-pending-changes-apply
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [sdn-pending-changes, sdn, proxmox, networking, change-management]
level: practitioner
status: docs-checked
description: "Review, apply and back out Proxmox VE SDN pending changes, understand where running config is generated, and check per-node SDN status after apply."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pvesdn.html
  - https://github.com/proxmox/pve-docs/blob/master/pvesdn.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SDN pending changes: apply and rollback

**Goal:** network changes reach all nodes deliberately, with a way back.

## How SDN changes flow
1. SDN configuration lives in `/etc/pve/sdn`, shared with the cluster by pmxcfs. Edits are not applied immediately but recorded as **pending**.
2. **Apply** (Datacenter -> SDN -> *Apply*) rolls out all pending changes to the whole cluster as one atomic change; the configuration is translated to the formats of the tools that manage the network stack (`ifupdown2`, `frr`).
3. The rolled-out state is tracked in `/etc/pve/sdn/.running-config` and `/etc/pve/sdn/.version`.

## Before applying
- Review the pending state of every object: Apply rolls out all pending changes, including ones made by someone else.
- Change one zone at a time in production and keep console access to the nodes.
- Fabric and route-filtering edits also go to the pending state and become active only after Apply.

## Backing out
- The documentation describes no rollback command: before apply, edit the objects back (or delete newly created ones) so the pending configuration matches what you want rolled out.
- After apply: re-create the previous state and apply again. Keep a copy of `/etc/pve/sdn/` (it is shared via pmxcfs) to compare against.

## After applying
```bash
vtysh -c 'show bgp l2vpn evpn summary'        # EVPN zones
```
A guest needs a restart for a changed VNet `Isolate Ports` setting to take effect.

## Gotchas
- The line `source /etc/network/interfaces.d/*` must be at the end of `/etc/network/interfaces` on all nodes so the SDN configuration is included and activated.
- Generated files are overwritten on apply: put node-local FRR additions in `/etc/frr/frr.conf.local` instead of editing `/etc/frr/frr.conf`.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, pvesdn.adoc, last pushed 2026-10-17). Confirmed: pending-then-apply model, atomic roll-out, `/etc/pve/sdn` location, `.running-config` and `.version` files, the required `source` line, `frr.conf.local`, Isolate Ports needing a guest restart, tech-preview status of FRR integration. Removed: `pvesh set /cluster/sdn`, `ifreload -a` as part of apply, the interfaces.d file name, the zone `available`/`error` states, `ifreload -a -s`, the pvesh resources query and the rollback API claim (not in the chapter; the API viewer page is generated and was not read).

Method: documentation only; no commands were run.
