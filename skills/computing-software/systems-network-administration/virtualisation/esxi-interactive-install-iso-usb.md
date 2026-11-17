---
id: computing-software.systems-network-administration.virtualisation.esxi-interactive-install-iso-usb
name: esxi-interactive-install-iso-usb
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [esxi-iso-installer, esxi-usb-installer, esxi-installation, esxi-install, vmware, esxi, vsphere]
level: practitioner
status: draft
description: "Install ESXi interactively from ISO or a USB installer stick: build the media, pick the target disk safely, set root and network, and verify the first boot."
sources:
  - https://techdocs.broadcom.com/us/en/vmware-cis/vsphere/vsphere/8-0/esxi-installation-and-setup-8-0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ESXi interactive install from ISO or USB

**Goal:** a clean ESXi host on the right boot disk, reachable on the management network, without wiping a datastore by mistake.

## Prepare the media
- Download the vendor custom ISO (Dell/HPE/Lenovo) where one exists; it carries the NIC/storage drivers the generic ISO may lack.
- Remote: mount the ISO through iDRAC/iLO/XClarity virtual media (fastest, no stick).
- USB stick: the ISO is a hybrid image. Write it with Rufus (choose "ISO mode", answer "Yes" to replace menu.c32) or on Linux:
```sh
sudo dd if=VMware-VMvisor-Installer-8.0U3-x86_64.iso of=/dev/sdX bs=4M status=progress conv=fsync
```
- Firmware: UEFI mode, Secure Boot on (if supported), VT-x/AMD-V and VT-d on, power profile "OS controlled".

## Install walk-through
1. Boot the installer, press Enter at the welcome, F11 to accept the EULA.
2. **Select the disk.** The list shows local and remote (SAN) disks. A disk holding VMFS shows a `*`. Detach FC/iSCSI LUNs (or unzone the host) before installing to avoid installing over a shared datastore.
3. If an existing ESXi/VMFS is found you get *Upgrade / Install and preserve VMFS / Install and overwrite*.
4. Keyboard layout, root password (meets the complexity rules: 7+ chars, mixed classes).
5. CPU warnings appear here (deprecated or unsupported CPU). Stop and check the compatibility guide rather than pressing on.
6. F11 to install, remove media, Enter to reboot.

## First boot
At the DCUI, F2 then:
- *Configure Management Network* -> Network Adapters (pick the right vmnics), VLAN, IPv4 static, DNS servers and FQDN hostname.
- *Test Management Network* pings gateway and DNS and resolves the hostname.
- Shift+O at the boot loader adds boot options (for example `cdromBoot` or `allowLegacyCPU=true` for lab only).

## Gotchas
- Install to an M.2 BOSS/RAID1 pair or a 128 GB+ local disk. SD cards/USB as the only boot device are deprecated in 7.0U3+ (OSDATA wear).
- Installing over a disk with an old VMFS keeps no data unless you chose *preserve VMFS*.
- No NIC detected = missing driver; use the vendor ISO or Image Builder.

## Verify
`esxcli system version get`, `esxcli network ip interface ipv4 get`, and a browser login to `https://<host>/ui` succeed.
