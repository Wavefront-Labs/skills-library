---
id: computing-software.systems-network-administration.virtualisation.linux-initramfs-virtio-driver-fixes
name: linux-initramfs-virtio-driver-fixes
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [dracut-virtio, initramfs-drivers, v2v, v2v-drivers, virtio, hyper-v, proxmox]
level: advanced
status: docs-checked
description: "Fix Linux VMs that drop to an emergency shell after moving to KVM/Proxmox or Hyper-V: add virtio or hv drivers to the initramfs with dracut or initramfs-tools, before or after."
sources:
  - https://man7.org/linux/man-pages/man8/dracut.8.html
  - https://github.com/dracutdevs/dracut/blob/master/man/dracut.conf.5.asc
  - https://manpages.debian.org/stable/initramfs-tools-core/initramfs.conf.5.en.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linux initramfs drivers after V2V

Symptom: after conversion the VM boots the kernel, then "dracut-initqueue timeout",
"Gave up waiting for root device", or `(initramfs)` prompt. The initramfs built on
VMware lacks the target's storage driver. A **host-only** initramfs (dracut `hostonly=yes`, which dracut itself defaults to no but many distributions enable) contains only what the source machine needs.

## Required modules
| Target | Storage | Network |
|---|---|---|
| KVM/Proxmox | `virtio_blk`, `virtio_scsi`, `virtio_pci` | `virtio_net` |
| Hyper-V | `hv_vmbus`, `hv_storvsc` | `hv_netvsc` |

## Best: fix before migrating (on the source VM)
RHEL/Rocky/Alma/SUSE (dracut):
```sh
echo 'add_drivers+=" virtio_blk virtio_scsi virtio_net virtio_pci hv_vmbus hv_storvsc hv_netvsc "' > /etc/dracut.conf.d/v2v.conf
dracut -f --regenerate-all
lsinitrd /boot/initramfs-$(uname -r).img | grep -E "virtio|hv_"
```
Debian/Ubuntu (initramfs-tools):
```sh
printf "virtio_blk\nvirtio_scsi\nvirtio_net\nvirtio_pci\nhv_vmbus\nhv_storvsc\nhv_netvsc\n" >> /etc/initramfs-tools/modules
update-initramfs -u -k all
lsinitramfs /boot/initrd.img-$(uname -r) | grep -E "virtio|hv_"
```
(Debian's default is `MODULES=most`, which adds most file system, ata, sata, scsi and usb drivers; modules listed in `/etc/initramfs-tools/modules` are always included. Check the result with `lsinitramfs` rather than assuming virtio is present.)

## After the fact (VM won't boot on target)
Rescue ISO, chroot:
```sh
mount /dev/sda2 /mnt; mount /dev/sda1 /mnt/boot   # adjust; LVM: vgchange -ay first
for d in dev proc sys; do mount --bind /$d /mnt/$d; done
chroot /mnt dracut -f --kver <kernel-version> --add-drivers "virtio_blk virtio_scsi"
```
The virt-v2v manual says it copies in virtio drivers during conversion.

## Other fixups in the same pass
- `/etc/fstab` referencing `/dev/sdX` instead of UUID: switch to UUID.
- NIC names change (`ens192` → `ens18`/`eth0`): update netplan/NetworkManager/ifcfg.
- Remove `open-vm-tools`; install `qemu-guest-agent` or Hyper-V daemons.

## Verify
`lsinitrd`/`lsinitramfs` lists the modules; the VM boots on the target with VirtIO SCSI /
storvsc and the network up without console intervention.

## Checked

Checked 2026-10-27 against the dracut manuals (dracut 8, dracut.conf 5, lsinitrd 1 in dracutdevs/dracut), the Debian initramfs.conf 5 manual (trixie) and the Linux kernel Makefiles for the module names. Confirmed: `add_drivers+=` syntax with names lacking `.ko`, `-f`, `--regenerate-all`, `--kver`, `--add-drivers`, `hostonly` defaulting to no upstream, `MODULES=most` as the Debian default, `/etc/initramfs-tools/modules` always being included, and the module names virtio_blk, virtio_scsi, virtio_net, virtio_pci, hv_vmbus, hv_storvsc and hv_netvsc. Removed the SATA/IDE temporary-boot trick and the Ubuntu default claim as unconfirmed.

Method: documentation only; no commands were run.
