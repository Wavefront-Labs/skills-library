---
id: computing-software.systems-network-administration.virtualisation.v2v-post-conversion-driver-fixups
name: v2v-post-conversion-driver-fixups
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [v2v-drivers, inaccessible-boot-device, v2v, 0x7b, virtio-drivers, dracut, ghost-nic, driver-injection]
level: advanced
status: docs-checked
description: "Fix guests after V2V conversion: INACCESSIBLE_BOOT_DEVICE from missing storage drivers, offline driver injection, Linux initramfs rebuilds, and ghost NICs holding static IPs."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/dism-driver-servicing-command-line-options-s14
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/pnputil-command-syntax
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/install/specifying-driver-load-order
  - https://man7.org/linux/man-pages/man8/dracut.8.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Post-conversion driver and NIC fixups

## Windows: INACCESSIBLE_BOOT_DEVICE (0x7B)
The new storage controller's driver is not set to load at boot.

**Prevent (on the source before cutover):** install the target drivers (virtio-win guest tools for KVM/Proxmox) while still on VMware.

**Fix offline (boot WinRE or attach the disk to a helper VM):** DISM adds INF drivers to an offline image with `/Image:` and `/Add-Driver`, where `/Driver` is an INF file or a folder (add `/Recurse` to search subfolders). A driver needed to start the system must have start type `SERVICE_BOOT_START` (0x0), which is `Start` = 0 in the service key.
```cmd
dism /Image:<OFFLINE_WIN>\ /Add-Driver /Driver:<FOLDER_WITH_VIOSTOR_INF>
reg load HKLM\OFFSYS <OFFLINE_WIN>\Windows\System32\config\SYSTEM
reg add HKLM\OFFSYS\ControlSet001\Services\viostor /v Start /t REG_DWORD /d 0 /f
reg unload HKLM\OFFSYS
```
Pick the driver folder matching the guest OS version from the virtio-win media.

## Linux: dropped to dracut/initramfs shell
The initramfs lacks the new controller module.
```bash
# from the old platform before cutover, or chroot from rescue
dracut -f --regenerate-all --no-hostonly                       # RHEL family
dracut -f --add-drivers "hv_vmbus hv_storvsc hv_netvsc" /boot/initramfs-$(uname -r).img $(uname -r)
update-initramfs -u -k all                                     # Debian family (add modules to /etc/initramfs-tools/modules)
```
`--regenerate-all` rebuilds every installed kernel's image, `-N`/`--no-hostonly` disables host-only mode and `--add-drivers` takes module names without `.ko`. Use UUIDs or labels in `/etc/fstab`, not `/dev/sdX`.

## NICs
- **Windows**: the old NIC can remain as a hidden, disconnected device that still holds the static IP configuration. List disconnected network devices and remove the stale one (both `pnputil` switches are documented):
```powershell
pnputil /enum-devices /disconnected /class Net
pnputil /remove-device "<instance id>"
```
- **Linux**: interface names change (`ens192` to `ens18`/`eth0`). Update netplan, NetworkManager or ifcfg files; remove `HWADDR=` MAC pins.

## Clean up the old platform
Uninstall VMware Tools (`apt purge open-vm-tools`, or Windows Programs list; if MSI removal fails, use VMware's cleanup guidance), and install the new guest agent.

## Verify
Clean boot, one active NIC with the intended IP, no hidden ghost adapters, guest agent reporting to the hypervisor.

## Checked

Checked 2026-10-27 against Microsoft's DISM driver servicing page, the PnPUtil command syntax page and the driver load order page (windows-driver-docs), the dracut 8 and dracut.conf 5 manuals (dracutdevs/dracut), and the Linux kernel Makefiles for the module names (virtio_blk, virtio_scsi, virtio_net, virtio_pci, hv_vmbus, hv_storvsc, hv_netvsc). Confirmed: `/Image` with `/Add-Driver` and `/Recurse`, `Start` 0 as SERVICE_BOOT_START, `pnputil /enum-devices /disconnected /class` and `/remove-device`, and the dracut options `-f`, `--regenerate-all`, `-N`/`--no-hostonly`, `--add-drivers` and `--kver`. The previous Proxmox wiki source is not readable here and its claims are no longer used; the virtio-win folder layout and the Hyper-V IDE boot-start remark were removed as unconfirmed.

Method: documentation only; no commands were run.
