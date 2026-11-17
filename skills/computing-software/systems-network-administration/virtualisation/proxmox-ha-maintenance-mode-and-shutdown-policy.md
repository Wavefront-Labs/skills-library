---
id: computing-software.systems-network-administration.virtualisation.proxmox-ha-maintenance-mode-and-shutdown-policy
name: proxmox-ha-maintenance-mode-and-shutdown-policy
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-maintenance-mode, shutdown-policy, node-maintenance, ha-manager, pve-ha, migrate-on-shutdown, rolling-reboot, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Patch and reboot Proxmox HA nodes cleanly: node maintenance mode, the HA shutdown policy (conditional, freeze, failover, migrate), and a rolling reboot procedure."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html#ha_manager_node_maintenance
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html#ha_manager_shutdown_policy
  - https://pve.proxmox.com/pve-docs/ha-manager.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox HA maintenance mode and shutdown policy

**Goal:** reboot nodes for patching without HA guests being stopped, frozen or fenced
unexpectedly.

## Maintenance mode
```sh
ha-manager crm-command node-maintenance enable pve2
ha-manager status                 # HA guests migrate away; LRM shows maintenance
# patch, reboot ...
ha-manager crm-command node-maintenance disable pve2   # services that were on the node move back
```
The command queues a CRM command, so it can be issued on any node. Targets are chosen from the other available nodes using the HA rules and the CRS mode. The LRM status reads `maintenance` as soon as it picks up the request, not when migrations finish: check for no remaining HA services on the node or the log line `watchdog closed (disabled)`. The mode is not cleared by a reboot, only by `node-maintenance disable` or clearing the manager status.

## Shutdown policy (Datacenter → Options → HA Settings)
Set in the GUI or in `datacenter.cfg` as `ha: shutdown_policy=<value>`. It decides what happens to HA guests when a node is shut down or rebooted **without** maintenance mode:
| Policy | Behaviour |
|---|---|
| `conditional` (default, kept for backward compatibility) | Shutdown (poweroff): the LRM stops all managed services and other nodes take them over. Reboot: services are frozen and restarted on the same node afterwards |
| `freeze` | All services are stopped and frozen; not recovered until the node is back |
| `failover` | All services are stopped but recovered elsewhere if the node is not back soon |
| `migrate` | The LRM marks itself unavailable and delays shutdown until services have migrated away; they move back when the node returns |
`migrate` needs services that can run on other nodes (no local-only bindings such as hardware passthrough; strict node affinity rules can make the shutdown hang). Under `conditional` shutdown, guests are stopped and restarted rather than live-migrated; migrate manually first if you want online migration.

## Rolling reboot procedure
1. Check cluster health (`pvecm status`, and Ceph status if used) and that backups are not running.
2. Ceph (if used): set `noout` as your Ceph procedure requires.
3. Enable maintenance on one node and wait for migrations; move non-HA guests yourself.
4. `apt dist-upgrade`, reboot, verify (`pveversion`, `systemctl --failed`, quorum).
5. Disable maintenance, wait for Ceph to recover if used, then the next node.
6. Undo any `noout` flag at the end.

## Gotchas
- With the `freeze` policy and no maintenance mode, HA guests stay stopped until the node is back.
- Do one node at a time: the remaining nodes must have capacity for the displaced guests.
- Maintenance mode persists across reboots until disabled.

## Verify
During each node's reboot, HA guests run elsewhere; after the last node, `ha-manager status` shows no node in maintenance and services back on their original nodes.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, ha-manager.adoc and generated option files, last pushed 2026-10-17). Confirmed: `node-maintenance enable|disable` syntax and behaviour (services move back on disable, persistence across reboot, status wording); shutdown policy names, `conditional` default and each policy's behaviour; `datacenter.cfg` key `ha: shutdown_policy=<value>`; migrate-policy caveats. Removed: the PVE 7.3 version marker, the nofailback remark, the claim that non-HA guests are not moved, and Ceph noout specifics beyond saying to follow the Ceph procedure (Ceph is outside this chapter).

Method: documentation only; no commands were run.
