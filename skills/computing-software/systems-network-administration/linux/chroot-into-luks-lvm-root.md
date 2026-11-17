---
id: computing-software.systems-network-administration.linux.chroot-into-luks-lvm-root
name: chroot-into-luks-lvm-root
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, chroot-luks, vgchange-ay, chroot, live-usb, cryptsetup-open, rescue, grub-reinstall]
level: advanced
status: gated
description: "From live media, unlock a LUKS root, activate LVM, mount root/boot/ESP with bind mounts and chroot in to fix GRUB, initramfs, fstab or passwords, then cleanly unwind."
sources:
  - https://github.com/archlinux/arch-install-scripts/blob/master/doc/arch-chroot.8.asciidoc
  - https://github.com/archlinux/mkinitcpio/blob/master/man/mkinitcpio.8.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.8.adoc
  - https://github.com/latchset/clevis/blob/master/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Chroot into an encrypted LVM root

## Steps
```bash
lsblk -f                                         # crypto_LUKS partition, ESP (vfat), /boot (ext4/xfs)
cryptsetup open /dev/nvme0n1p3 cryptroot         # name must match /etc/crypttab if you rebuild initramfs
vgscan; vgchange -ay                             # activate all LVs; lvs to see names
mount /dev/mapper/vg0-root /mnt
mount /dev/nvme0n1p2 /mnt/boot                   # separate /boot if present
mount /dev/nvme0n1p1 /mnt/boot/efi               # ESP (or /mnt/efi, check the target's fstab)
for d in dev dev/pts proc sys run; do mount --bind /$d /mnt/$d; done
cp /etc/resolv.conf /mnt/etc/resolv.conf         # network inside chroot (back it up first if needed)
chroot /mnt /bin/bash                            # Arch: arch-chroot /mnt mounts the API filesystems and exposes resolv.conf for you
```
Inside: `mount -a` checks fstab; fix things:
```bash
grub-install /dev/nvme0n1   or   grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=ubuntu   # (gated: unconfirmed, source is paywalled or blocked)
update-initramfs -u   |  dracut -f --regenerate-all   |  mkinitcpio -P
passwd root
```

## Unwind cleanly
```bash
exit
umount -R /mnt
vgchange -an vg0
cryptsetup close cryptroot
```

## Gotchas
- Live system VG name colliding with target (same image) → `vgimportclone` or rename.
- Btrfs root: `mount -o subvol=@ ...` and mount other subvolumes (`@home`) as fstab lists.
- RHEL-family with SELinux: after editing files in chroot, `touch /.autorelabel` or `restorecon` (gated: unconfirmed, source is paywalled or blocked)
- Installing GRUB for UEFI from a chroot may also need the efivars filesystem bound into the chroot (gated: unconfirmed, source is paywalled or blocked)
- Reasons for the gated items: the GNU GRUB manual returned 403 to automated fetches and the Red Hat SELinux documentation is not in a public repository.

## Verify
- [ ] Reboot without live media prompts for the LUKS passphrase and boots; `findmnt` shows the expected layout.

## Checked

Checked 2026-10-25 against the arch-install-scripts arch-chroot(8) page (archlinux/arch-install-scripts), the mkinitcpio(8) page (archlinux/mkinitcpio, `-P` processes all presets), dracut-ng man/dracut.8.adoc (`--regenerate-all`) and the Clevis README (names `update-initramfs -u` for Debian-like systems and `dracut -f` for Fedora-like systems).
Confirmed: arch-chroot mounts the API filesystems and exposes resolv.conf; the three initramfs regeneration commands.
Unconfirmed and marked gated: the `grub-install` flags (including `--efi-directory` and `--bootloader-id`), the SELinux relabel advice and the efivars requirement. Removed unconfirmed claims: `update-initramfs -k all`, the dracut host-only remark and the architecture-mismatch remark.

Method: documentation only; no commands were run.
