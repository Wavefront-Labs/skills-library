---
id: computing-software.systems-network-administration.virtualisation.proxmox-time-sync-chrony
name: proxmox-time-sync-chrony
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-chrony, chrony, ntp, proxmox, time-synchronisation]
level: intro
status: docs-checked
description: "Configure chrony time synchronisation on Proxmox VE nodes with internal NTP servers and verify it, since corosync, Ceph and TOTP all depend on correct clocks."
sources:
  - https://pve.proxmox.com/pve-docs/pve-admin-guide.html#_time_synchronization
  - https://chrony-project.org/doc/4.3/chrony.conf.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Proxmox VE time synchronisation with chrony

**Goal:** every node keeps time within milliseconds of the others.

## Why it matters
- TOTP codes are time-based, and cluster nodes must have synchronized date and time.
- Logs across nodes must line up for troubleshooting.

## Configure
Proxmox VE uses `chrony` by default. Edit `/etc/chrony/chrony.conf`, replace the Debian pool line with internal servers:
```
# (comment out the default pool lines)
server ntp1.example.com iburst
server ntp2.example.com iburst
server ntp3.example.com iburst
makestep 1 3
```
```bash
systemctl restart chronyd
```
Apply the same file on all nodes (config management or a loop over `ssh`).

## Verify
```bash
chronyc sources -v     # '*' marks the selected source, reach should be 377
chronyc tracking       # 'System time' offset in microseconds
timedatectl            # 'System clock synchronized: yes'
ceph time-sync-status  # on Ceph clusters
```

## Gotchas
- Firewall: UDP 123 outbound to the NTP servers.
- VMs on the cluster acting as the NTP servers create a circular dependency at cold start; use physical or external sources.
- Large initial offsets: the `makestep` directive lets chrony step the clock instead of slewing it; fix time before joining a cluster.
- `rtcsync` makes chrony copy the system time to the hardware clock periodically.

## Checked

2026-10-28

Confirmed: Admin guide time synchronisation section (chrony default NTP daemon since PVE 7, systemctl restart chronyd) and chrony.conf docs (makestep, rtcsync).

Removed or corrected: Ceph clock-skew figures (not in the fetched pages), API-ticket claim, three-source claim, chronyc makestep command, rtcsync default claim.

Method: documentation only; no commands were run.
