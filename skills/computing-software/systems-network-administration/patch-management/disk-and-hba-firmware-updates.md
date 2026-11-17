---
id: computing-software.systems-network-administration.patch-management.disk-and-hba-firmware-updates
name: disk-and-hba-firmware-updates
category: computing-software
field: systems-network-administration
product: patch-management
tags: [disk-firmware, hba-firmware, storage-firmware, raid-controller, nvme-cli, storcli, firmware-patching]
level: advanced
status: draft
description: "Update disk, SSD, NVMe, HBA and RAID controller firmware safely: compatibility lists, critical vendor bulletins, vendor tools and CLIs, rolling cluster updates and verification."
sources:
  - https://www.dell.com/support/kbdoc/en-us/000134013/dell-emc-poweredge-how-to-update-firmware
  - https://techdocs.broadcom.com/us/en/storage-and-ethernet-connectivity/enterprise-storage-solutions/storcli-12gbs-megaraid-tri-mode/1-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Disk and HBA firmware

**Goal:** apply storage firmware fixes (including ones that prevent data loss) without taking down storage.

## Why it matters
Drive and controller firmware bugs have caused fleet-wide failures (for example SSDs bricking after a fixed number of power-on hours). Vendors publish critical bulletins; subscribe to them for every storage model you run.

## Compatibility first
- Hypervisor and SDS stacks certify **driver + firmware pairs** (VMware Compatibility Guide, Azure Local catalog). Updating firmware alone can leave you unsupported.
- vSAN/vSphere: use vLCM with a Hardware Support Manager to keep firmware and drivers aligned per cluster image.

## Tools
| Layer | Tool |
|---|---|
| Whole server | Dell iDRAC/Lifecycle Controller or DSU, HPE SPP/SUM/iLO, Lenovo XClarity |
| Broadcom MegaRAID/HBA | `storcli /c0 show`, `storcli /c0 download file=fw.rom` |
| NVMe | `nvme fw-log /dev/nvme0`, `nvme fw-download /dev/nvme0 -f fw.bin`, `nvme fw-commit /dev/nvme0 -s 1 -a 1` |
| SATA/SAS drives | Vendor utility; check with `smartctl -i /dev/sda` |

## Rolling procedure for clusters
1. Read release notes for prerequisites and ordering (controller before drives, BMC first).
2. Put one node in maintenance (evacuate VMs; vSAN "ensure accessibility"; Ceph `noout`).
3. Update, reboot, verify the device is healthy and resync is complete.
4. Next node only after storage health is green.

## Gotchas
- Some drive firmware updates are not online-capable; plan reboots.
- Mixed drive firmware within a RAID set is usually tolerated briefly but not long term.

## Verify
Inventory (`storcli /c0 show all`, `smartctl -i`, vendor console) shows the target versions on every node, and storage health checks are green.
