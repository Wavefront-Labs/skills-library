---
id: computing-software.systems-network-administration.virtualisation.esxi-bootbank-corruption-and-boot-failures
name: esxi-bootbank-corruption-and-boot-failures
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [bootbank, esxi-boot-failure, esxi-recovery, vmware, vsphere]
level: advanced
status: draft
description: "Diagnose ESXi bootbank problems and boot failures, roll back with Shift+R, back up and restore host configuration, and reinstall while keeping VMFS."
sources:
  - https://knowledge.broadcom.com/external/article?legacyId=2042141
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bootbank corruption and ESXi boot failures

**Goal:** get a host back after boot media trouble, with its configuration intact.

## Symptoms
- Host warns *Bootbank cannot be found at path /bootbank* or *Lost connectivity to the device backing the boot filesystem* (typical with failing SD/USB media).
- `/bootbank` symlinks to `/tmp`; patching fails; config changes are lost after reboot.
- Boot stops with *Error loading /xxx.v00: Inconsistent data* or *No hypervisor found*.

## Diagnose a running host
```bash
ls -l /bootbank /altbootbank
esxcli system boot device get
vmkfstools -Ph /bootbank
grep -i -E 'bootbank|vfat|usb' /var/log/vmkernel.log | tail -50
```

## Back up configuration now
```bash
vim-cmd hostsvc/firmware/sync_config
vim-cmd hostsvc/firmware/backup_config      # prints a URL to configBundle-<host>.tgz
```
PowerCLI: `Get-VMHost esx01 | Get-VMHostFirmware -BackupConfiguration -DestinationPath <dir>`.

## Recover
1. **Recent upgrade or patch broke boot**: at the boot loader press **Shift+R** and choose the previous image in the alternate bootbank.
2. **Media failed**: replace with durable media (M.2 boot pair or local SSD), reinstall the **same build**, choose *Install, preserve VMFS datastore* if the media also holds a datastore.
3. Restore the configuration (same build, maintenance mode):
```bash
vim-cmd hostsvc/maintenance_mode_enter
vim-cmd hostsvc/firmware/restore_config 1 /tmp/configBundle-esx01.tgz
```
PowerCLI: `Set-VMHostFirmware -VMHost esx01 -Restore -SourcePath configBundle.tgz -HostUser root -HostPassword ...`. The host reboots with its old identity, networking and storage config.
4. Reconnect to vCenter and re-apply host profile/vLCM image.

## Gotchas
- Restore requires the exact same build number as the backup; patch the fresh install first.
- Config backups contain secrets; store them like credentials.
- Hosts on SD/USB: move logs, scratch and coredump off the media and configure OSDATA, or failures recur.

## Verify
`esxcli system boot device get` shows the new boot device; `/bootbank` points to a real volume; config changes survive a reboot.
