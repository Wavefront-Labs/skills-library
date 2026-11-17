---
id: computing-software.systems-network-administration.virtualisation.esxcli-software-offline-depot-patching
name: esxcli-software-offline-depot-patching
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxcli-software, offline-bundle, esxcli, esxi-patching, vib, image-profile, standalone-host, vsphere-upgrade, vmware, esxi]
level: practitioner
status: draft
description: "Patch standalone ESXi hosts with esxcli software: offline depot zips, profile update vs install, dry runs, VIB/component management, and acceptance level errors."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patching ESXi with esxcli software and offline depots

**Goal:** patch or upgrade a host without vCenter (standalone hosts, labs, recovery of a
host vCenter cannot remediate).

## Steps
1. Download the **offline bundle** (`VMware-ESXi-8.0U3x-depot.zip`, or the OEM custom depot)
   and upload it to a datastore.
2. Evacuate VMs and enter maintenance mode:
   `esxcli system maintenanceMode set --enable true`
3. List profiles in the depot:
```sh
esxcli software sources profile list -d /vmfs/volumes/<ds>/VMware-ESXi-<ver>-depot.zip
```
4. **Dry run**, then apply:
```sh
esxcli software profile update -d /vmfs/volumes/<ds>/<depot>.zip -p <profile-name> --dry-run
esxcli software profile update -d /vmfs/volumes/<ds>/<depot>.zip -p <profile-name>
reboot
```
`profile update` keeps installed third-party VIBs that are newer; `profile install`
replaces everything with the profile (can remove OEM drivers, use with care).
5. Exit maintenance mode after checking the build.

## Components and VIBs
```sh
esxcli software component list | grep -i <driver>
esxcli software component apply -d /vmfs/volumes/<ds>/<driver-component>.zip
esxcli software vib list | grep -i <name>
esxcli software vib remove -n <vibname> --dry-run
esxcli software acceptance get     # PartnerSupported default; CommunitySupported for lab VIBs
```

## Common errors
- **"[DependencyError] VIB ... requires ..."**: a third-party driver depends on an older
  base; use the OEM depot or update the driver component together with the image.
- **Acceptance level**: a CommunitySupported VIB fails on PartnerSupported hosts; raising
  acceptance is a support decision, and Secure Boot hosts refuse unsigned VIBs anyway.
- **Hardware precheck failure** (CPU not supported on 8.x): `--no-hardware-warning` only
  overrides warnings; unsupported CPUs need different hardware.
- Insufficient space in OSDATA/bootbank: remove old staged payloads, check `vdf -h`.

## Rollback
The previous image remains in the alternate bootbank: at boot press **Shift+R** to
revert to it (one level only).

## Verify
`vmware -vl` and `esxcli software profile get` show the new build; `esxcli software vib
list` still contains the needed OEM drivers; host reconnects to vCenter if present.
