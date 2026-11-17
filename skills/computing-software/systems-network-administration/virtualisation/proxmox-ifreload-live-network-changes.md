---
id: computing-software.systems-network-administration.virtualisation.proxmox-ifreload-live-network-changes
name: proxmox-ifreload-live-network-changes
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [ifreload, ifupdown2, vmbr0, pve-network, interfaces-new, proxmox]
level: practitioner
status: docs-checked
description: "Change Proxmox host networking live with ifupdown2: pending interfaces.new, Apply Configuration, ifreload -a dry runs, out-of-band safety and rollback."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html#sysadmin_network_configuration
  - https://github.com/proxmox/pve-docs/blob/master/pve-network.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Live network changes with ifreload

PVE recommends **ifupdown2** (default for new installations since Proxmox VE 7.0). Network changes are not written directly to `/etc/network/interfaces`: the GUI writes the staging file `/etc/network/interfaces.new`, so you can make many related changes and check them first. **Apply Configuration** moves them to `/etc/network/interfaces` and applies them live. If you installed Proxmox VE on top of Debian or upgraded from before 7.0, make sure `apt install ifupdown2` was done.

## Workflow
```sh
diff -u /etc/network/interfaces /etc/network/interfaces.new   # review pending GUI changes
cp /etc/network/interfaces /root/interfaces.bak               # your own backup
ifreload -a             # apply manual changes made directly in /etc/network/interfaces
```
For CLI edits, edit `/etc/network/interfaces` directly and run `ifreload -a`. Another way to apply is a reboot: the `pvenetcommit` service activates `interfaces.new` before networking is configured.

## Safety net for remote work
A wrong network configuration can render a node inaccessible, and changes to the management bridge can cut you off. Keep a console (IPMI/iDRAC/iLO or physical) session open before touching `vmbr0` or bonds, and keep the backup copy so you can restore it from the console.

## What reloads cleanly
- ifupdown2 applies network configuration changes without a reboot.
- The traditional Debian tools `ifup` and `ifdown` are discouraged: for example `ifdown vmbrX` interrupts all guest traffic on that bridge, and a later `ifup` on the same bridge does not reconnect those guests.

## Gotchas
- SDN configuration is included through `source /etc/network/interfaces.d/*`, which must be present at the end of `/etc/network/interfaces` on all nodes.
- Systems installed on Debian or upgraded from before 7.0 need `apt install ifupdown2` for live apply.

## Verify
`ip -br a` shows the expected addresses, cluster links are up (`corosync-cfgtool -s`), and a test VM on each bridge pings its gateway.

## Checked

Checked 2026-10-25 against pve-docs master (pve-network.adoc and pvesdn.adoc; last pushed 2026-10-17). Confirmed: `interfaces.new` staging and Apply Configuration, `ifreload -a` for manual changes, ifupdown2 default since 7.0 and install note for older systems, `pvenetcommit` on reboot, warning against `ifup`/`ifdown`, SDN `source` line. Removed: `ifreload -a -s`, `ifquery -a -c`, the timed auto-rollback script, the per-change-type reload behaviour and the `auto` remark (not in the Proxmox VE documentation; ifupdown2 man pages were not read).

Method: documentation only; no commands were run.
