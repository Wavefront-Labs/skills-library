---
id: computing-software.systems-network-administration.proxmox-ve.disk-health-smartd
name: disk-health-smartd
category: computing-software
field: systems-network-administration
product: proxmox-ve
tags: [smart, smartctl, smartd, disk-health, smartmontools]
level: intro
status: docs-checked
description: "Check local disk health with smartctl and the preinstalled smartd daemon on Proxmox VE hosts."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `smartmontools` package is installed and required on Proxmox VE. Query a disk with:

```
smartctl -a /dev/sdX
```

If the output says "SMART support is: Disabled", enable it with `smartctl -s on /dev/sdX`.

The `smartd` daemon is active and enabled by default. It scans devices matching `/dev/sd[a-z]`, `/dev/sd[a-z][a-z]`, `/dev/hd[a-t]` and `/dev/nvme[0-99]` every 30 minutes for errors and warnings and emails root if it detects a problem. Configuration details are in `man smartd` and `man smartd.conf`.

Disks behind a hardware RAID controller usually have vendor tools to monitor both the array and its member disks; for those, refer to the controller vendor.

The same chapter notes that ZFS ships an event daemon (ZED) that can email on pool errors, with `ZED_EMAIL_ADDR` defaulting to `root`.

## Checked

Checked 2026-11-08 against the Disk Health Monitoring section and the ZFS ZED paragraph of the pve-docs sysadmin chapter (partial read of a long page). Confirmed smartmontools, smartctl commands, smartd scan patterns, 30-minute interval, email to root and the RAID controller note. Removed the unsourced mail-forwarding claim, the Ceph status claim and the advice paragraph.

Method: documentation only; no commands were run.
