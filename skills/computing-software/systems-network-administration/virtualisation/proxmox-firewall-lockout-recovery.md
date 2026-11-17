---
id: computing-software.systems-network-administration.virtualisation.proxmox-firewall-lockout-recovery
name: proxmox-firewall-lockout-recovery
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [firewall-lockout, pve-firewall, management-ipset, pve-firewall-stop, console-recovery, proxmox, proxmox-ve]
level: practitioner
status: docs-checked
description: "Avoid and recover from Proxmox firewall lockouts: the management IP set and localnet, default allowed services, stopping pve-firewall from console, and editing cluster.fw."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-pve-firewall.html
  - https://pve.proxmox.com/pve-docs/pve-firewall.8.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox firewall lockout: prevention and recovery

**Goal:** turn on DROP policies without losing access to the GUI, SSH or the cluster.

## What PVE allows by default
With the firewall enabled, traffic to all hosts is blocked by default except documented allowances: loopback, established connections, IGMP, and TCP from `management` hosts to 8006 (GUI), 5900-5999 (VNC), 3128 (SPICE), 22 (SSH) and 60000-60050 (migration), plus corosync UDP 5405-5412 in the cluster network. The `local_network` alias (see `pve-firewall localnet`) is auto-detected, and the local cluster network is added to the `management` IP set automatically. Everything else hits your rules and the default policy.

## Prevention
1. Define `[IPSET management]` in `cluster.fw` with your admin and jump-host addresses before enabling, so remote hosts get GUI, SSH and console access.
2. Add explicit allow rules for monitoring, backup server, Ceph and any other services; on a single host on a public network, set `local_network` explicitly in `[ALIASES]`.
3. Open an SSH connection to a host before enabling (the documentation tip), ideally with a console session as well.
4. Test from a second session before closing the first.

## Recovery
From the node console (IPMI, physical):
```sh
pve-firewall stop                       # removes all PVE firewall rules on this node
nano /etc/pve/firewall/cluster.fw       # set enable: 0 in [OPTIONS] or fix rules
pve-firewall start
```
`pve-firewall stop` leaves the host unprotected until the firewall is started again.

## Gotchas
- Blocking corosync causes quorum loss, and `/etc/pve` becomes read-only without quorum; keep corosync traffic allowed.
- `cluster.fw` is a cluster-wide file, so one bad edit affects every node.
- The nftables backend (`proxmox-firewall`, tech preview, `nftables: 1` in `host.fw`) uses the same configuration files but a different service: use `systemctl stop proxmox-firewall` instead of `pve-firewall stop` on such a node (stopping it removes all generated rules).

## Verify
`pve-firewall localnet` shows the expected local network; GUI and SSH work from the admin PC; `pvecm status` stays quorate after enabling.

## Checked

Checked 2026-10-25 against pve-docs master (github.com/proxmox/pve-docs, last pushed 2026-10-17). Confirmed: the list of traffic allowed by default under DROP/REJECT policies; automatic `cluster_network` entry in `management`; `local_network` alias and `pve-firewall localnet`; `pve-firewall stop` removing rules; `nftables` host option, tech-preview status and `systemctl stop proxmox-firewall` removing generated rules. Removed: the PVE 8.2 introduction version, the claim that `management` overrides localnet, the multi-node quorum-recovery recipe, the claim that edits apply within seconds, and the fencing-reboot claim (none documented in the firewall chapter).

Method: documentation only; no commands were run.
