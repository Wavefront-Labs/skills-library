---
id: computing-software.systems-network-administration.virtualisation.proxmox-disk-health-smart-and-wearout
name: proxmox-disk-health-smart-and-wearout
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [pve-disk-health, smart, ssd-wearout, smartctl, proxmox]
level: intro
status: docs-checked
description: "Monitor disk health on Proxmox VE nodes: smartctl status and self-tests, what smartd scans and mails by default, smartd.conf schedules, NVMe warnings and Ceph device health."
sources:
  - https://pve.proxmox.com/pve-docs/chapter-sysadmin.html
  - https://docs.ceph.com/en/latest/rados/operations/devices/
  - https://github.com/smartmontools/smartmontools/blob/master/smartmontools/smartctl.8.in
  - https://github.com/smartmontools/smartmontools/blob/master/smartmontools/smartd.conf.5.in
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk health: SMART and SSD wearout

**Goal:** replace failing or worn disks before they take data with them.

## smartctl
Proxmox VE installs and requires smartmontools (since 4.3). To read a disk:
```bash
smartctl -a /dev/sdX
smartctl -s on /dev/sdX              # if the output says "SMART support is: Disabled"
smartctl -H /dev/sdX                 # overall health assessment
smartctl -t long /dev/sdX            # extended self-test; it can take a long time, read results later with -a
smartctl -d megaraid,N -a /dev/sdX   # disks behind a MegaRAID controller (N = disk number)
```
For disks behind a hardware RAID controller the Proxmox guide advises using the controller vendor's tools for the array itself.

## smartd alerting
By default the smartmontools daemon `smartd` is active and enabled on Proxmox VE. It scans devices matching `/dev/sd[a-z]`, `/dev/sd[a-z][a-z]`, `/dev/hd[a-t]` and `/dev/nvme[0-99]` every 30 minutes for errors and warnings and e-mails root if it finds a problem. Configure it in `/etc/smartd.conf`; see `man smartd` and `man smartd.conf`.

A `DEVICESCAN` line scans all devices; add scheduled self-tests with the `-s` regular expression, in the form `T/MM/DD/d/HH` (type S short or L long; the man page example runs a long test on Saturdays at 03:00 with `L/../../6/03`):
```
DEVICESCAN -a -s (S/../.././02|L/../../6/03) -m root
```
`-a` turns on the default set of checks. For NVMe, recent smartd (7.5, marked experimental) logs and mails a warning if "Percentage Used" has changed and exceeds 95 percent, or "Media and Data Integrity Errors" has increased, and `-p` reports when "Available Spare" changes and falls below its threshold.

## Ceph
Ceph can collect SMART/health metrics through `smartctl`:
```bash
ceph device ls
ceph device monitoring on
ceph device get-health-metrics <DEVID>
```
Metrics are scraped every 24 hours by default (`mgr/devicehealth/scrape_frequency`). Failure prediction is off (`none`) by default; `local` needs the `diskprediction_local` Manager module.

## Gotchas
- A passing overall health status is not a guarantee: read the raw attributes and trend them.
- Wear figures and thresholds for acting on them depend on the drive model; use the vendor's endurance rating.

## Checked
Checked 2026-11-08 against the Proxmox VE host system administration guide (disk health monitoring), the Ceph devices page and the smartctl and smartd.conf man page sources. Removed (not stated in those pages): the GUI Disks / Wearout description, specific attribute numbers 5/187/197/198, the 80 percent wear threshold, `nvme smart-log`, `zpool status` advice and the consumer-SSD remark.
Method: documentation only; no commands were run.
