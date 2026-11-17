---
id: computing-software.systems-network-administration.virtualisation.proxmox-ha-fencing-and-watchdog
name: proxmox-ha-fencing-and-watchdog
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-fencing, watchdog-mux, softdog, ipmi-watchdog, self-fencing, pve-ha, ha-manager, proxmox, proxmox-ve]
level: advanced
status: docs-checked
description: "Understand Proxmox HA self-fencing: watchdog-mux, softdog vs hardware (IPMI/iTCO) watchdogs, why nodes reboot when they lose quorum, and diagnosing unexpected fence reboots."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-ha-manager.html
  - https://pve.proxmox.com/pve-docs/ha-manager.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox HA fencing and the watchdog

**Goal:** know why an HA node rebooted itself, and make sure fencing is reliable so a
failed node can never keep writing to shared storage while its guests start elsewhere.

## How Proxmox fences
No external fence devices: each node **self-fences** with a watchdog timer. `watchdog-mux` holds the watchdog (the kernel software watchdog `softdog` by default, or a configured hardware watchdog). While a node has quorum, `ha-manager` keeps resetting the timer. If the node loses quorum, or the LRM or CRM process is not scheduled or is killed, with active services on the node, the watchdog elapses and the node resets after 60 seconds. The service is in state `fence` until the node is fenced, then moves to `recovery` and is placed on another node. A hardware watchdog is more reliable than `softdog` because it does not depend on the server's hardware and kernel.

## Hardware watchdog
Optional. All hardware watchdog modules are blocked by default; name the module to load in `/etc/default/pve-ha-manager`, which the `watchdog-mux` service reads at startup:
```
# select watchdog module (default is softdog)
WATCHDOG_MODULE=iTCO_wdt
```
Use the module that matches your server's hardware watchdog; recent server motherboards often include one but it needs to be configured.

## Unexpected reboots: diagnose
1. The HA stack logs every action: read `journalctl -u pve-ha-lrm` on the node that hosted the services and `journalctl -u pve-ha-crm` on the current master, around the reboot.
2. Check the corosync logs on all nodes at that time for link problems and quorum loss.
3. A node reboots when it loses quorum while its LRM is active, or when LRM/CRM is not scheduled for too long.
4. Fix the cluster network (dedicated corosync links, a second link) rather than disabling HA.

## When nodes do **not** fence
If a node has an active CRM but an idle LRM, a quorum loss does not trigger a self-fence reset. If no service is configured for more than 15 minutes, the CRM returns to idle and closes its watchdog completely.

## Gotchas
- Network or corosync work can cause temporary quorum loss that HA treats as node failure. Use the documented disarm mechanism (`ha-manager crm-command disarm-ha freeze` or `ignore`, then `arm-ha`) to release all watchdogs cluster-wide; while disarmed HA does not protect services, so keep the window short.
- Do not kill `pve-ha-crm`, `pve-ha-lrm` or `watchdog-mux`: they manage the watchdog and this can reset the node immediately.
- `ha-manager status` shows a fencing entry with the watchdog state: `armed`, `standby`, `disarming` or `disarmed`.

## Verify
`ha-manager status` shows the fencing entry `armed` and LRM `active` on nodes with resources. The HA simulator in the documentation can rehearse failures without a real cluster.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, ha-manager.adoc and generated option files, last pushed 2026-10-17). Confirmed: self-fencing via watchdog timers, softdog default and 60 second timeout; hardware watchdog blocked by default and `WATCHDOG_MODULE` in `/etc/default/pve-ha-manager` read by `watchdog-mux`; service states `fence` and `recovery`; CRM active with idle LRM does not self-fence; 15 minute CRM idle rule; fencing status values; disarm and arm commands; journalctl unit names. Removed: `ipmi_watchdog` example, BIOS/BMC and dmesg steps, specific log strings, the list of usual causes, and the lab reboot timing (not documented).

Method: documentation only; no commands were run.
