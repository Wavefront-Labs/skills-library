---
id: computing-software.systems-network-administration.virtualisation.proxmox-ha-lrm-crm-troubleshooting
name: proxmox-ha-lrm-crm-troubleshooting
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ha-lrm, ha-crm, ha-manager, pve-ha, ha-state, pve-fencing, proxmox]
level: advanced
status: docs-checked
description: "Troubleshoot Proxmox HA with ha-manager status, LRM/CRM roles and states, resources stuck in error or fence, and safe recovery without triggering extra fencing."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html
  - https://pve.proxmox.com/pve-docs/ha-manager.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox HA: LRM and CRM troubleshooting

## Components
- **CRM** (`pve-ha-crm`): runs on each node; the node holding the manager lock is the master and decides what the LRMs execute.
- **LRM** (`pve-ha-lrm`): on each node; executes start/stop/migrate commands (at most 4 parallel workers by default, `max_worker` in the datacenter configuration) and holds a **watchdog**. With active services and lost quorum the watchdog resets the node (self-fencing) after 60 seconds.

## Status
```sh
ha-manager status            # quorum, master, fencing and LRM state per node, each service state
ha-manager status --verbose
journalctl -u pve-ha-lrm      # on the node that hosts the service
journalctl -u pve-ha-crm      # on the current master node
```
LRM and CRM states: `wait for agent lock` (also used as the idle state when no service is configured), `active` (holds its lock and has services) and `lost agent lock` (a failure happened and quorum was lost). The LRM status reads `maintenance` once it has picked up a maintenance request.

## Service states and what to do
| State | Meaning | Action |
|---|---|---|
| `started`/`stopped` | as requested | none |
| `fence` | service node is not in the quorate partition; waiting for fencing | wait for the node to be fenced |
| `recovery` | finding a new node after fencing | wait; the service is placed on the new node in `stopped` state and started if configured to run |
| `error` | the service failed after all `max_restart` and `max_relocate` attempts | bring it to a safe state, `ha-manager set vm:101 --state disabled`, fix the cause, then `--state started` |
| `freeze` | HA does not touch the service during a node reboot or LRM restart | clears when the node or LRM is back |
| `migrate` | live migration in progress | wait or check the task log |
| `queued` | newly added, CRM has not seen it yet | wait |
| `ignored` | resource removed from HA tracking | manage it directly |

## Common problems
- **Unexpected node reboots**: quorum loss while the LRM has active services triggers the watchdog. Fix the cluster network (dedicated corosync link) rather than HA, and read the LRM and CRM journals around the reboot.
- **Service stuck in error after a storage outage**: once storage is back, disable then start as above; `disabled` is the only way out of `error`.
- **No master CRM**: the CRM waits for the manager lock, which needs a quorate cluster; check `pvecm status`.

## Maintenance without fencing
- `ha-manager crm-command node-maintenance enable pve02` marks the node unavailable and migrates its HA services away; disable it to bring them back.
- `ha-manager remove vm:101` deletes the resource from HA.
- For corosync or network work that may cause quorum loss, use `ha-manager crm-command disarm-ha freeze` (or `ignore`), then `ha-manager crm-command arm-ha` afterwards. Do not kill `pve-ha-crm`, `pve-ha-lrm` or `watchdog-mux`.
- Upgrade ha-manager one node at a time: the LRM asks the CRM to freeze its services before it restarts, and without an active master CRM the update can take long enough for the watchdog to reset the node.

## Verify
`ha-manager status` shows no LRM in `lost agent lock`, services in their requested states, and no fencing events in the journals over the observation window.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, ha-manager.adoc and generated option files, last pushed 2026-10-17). Confirmed: LRM and CRM roles, three daemon states, 4 default workers and `max_worker`; service states fence, recovery, freeze, ignored, migrate, error, queued, disabled and their meanings; error recovery through `disabled`; 60 second watchdog; maintenance-mode and disarm commands; package-update behaviour; `ha-manager status --verbose` and `remove`. Removed: `idle` and `wait_for_agent_lock` as distinct state names, the `relocate` state row, the 7.3 version marker, the claim that a removed VM keeps running, and the manual `systemctl stop pve-ha-lrm` procedure (not documented; the documentation warns against stopping these services).

Method: documentation only; no commands were run.
