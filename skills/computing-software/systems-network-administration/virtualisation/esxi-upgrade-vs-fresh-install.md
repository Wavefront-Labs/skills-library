---
id: computing-software.systems-network-administration.virtualisation.esxi-upgrade-vs-fresh-install
name: esxi-upgrade-vs-fresh-install
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-upgrade-path, esxi-installation, esxi-upgrade, vmfs, vmware, esxi, vsphere]
level: advanced
status: draft
description: "Decide between upgrading ESXi in place and a fresh install that preserves VMFS: supported paths, what survives, and how to rebuild host config afterwards."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esxi-upgrade-8-0.html
  - https://interopmatrix.broadcom.com/Upgrade
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi upgrade versus fresh install

**Goal:** pick the path that ends with a supportable host and keeps the local datastore intact.

## Paths
| Path | Keeps config | Keeps local VMFS | Use when |
|---|---|---|---|
| vLCM / `esxcli software profile update` | yes | yes | normal upgrades on a supported path |
| ISO boot -> *Upgrade* | yes | yes | single host, no vCenter |
| ISO boot -> *Install, preserve VMFS* | no | yes | messy hosts, wrong partition layout, many legacy VIBs |
| ISO boot -> *Install, overwrite VMFS* | no | no | redeploy, nothing on local disks |

Check the upgrade path in the Product Interoperability Matrix (Upgrade Path tab): for example 6.7 -> 8.0 is supported, 6.5 -> 8.0 is not (go via 7.0).

## Reasons to prefer fresh install
- Host was installed on SD/USB and you are moving to a proper boot disk (7.0 partition layout with OSDATA).
- Third-party VIBs that block the upgrade (old drivers, removed vendor tools): `esxcli software vib list` and the precheck lists conflicts.
- Hosts moving to a vLCM image cluster anyway (stateless rebuild + host profile is cleaner).

## Fresh install with config rebuild
1. Put host in maintenance mode, evacuate VMs.
2. Back up config: `vim-cmd hostsvc/firmware/backup_config` (gives a URL to `configBundle.tgz`). Note: restoring it only works to the **same build**, so it is not an upgrade tool.
3. Capture a host profile from the host or a sibling.
4. Reinstall choosing *Install, preserve VMFS*; reconfigure management network at DCUI.
5. Reconnect to vCenter (remove the old host object if the thumbprint changed), apply the host profile, remediate patches via vLCM.

## Gotchas
- Fresh install creates a new host UUID; backup jobs and monitoring keyed on the host object may need relinking.
- vDS membership is lost on fresh install; plan the uplink migration (or a standard switch for management first).

## Verify
`esxcli system version get` shows the target build, local datastores mount with their VMs registered, host profile compliance is green.
