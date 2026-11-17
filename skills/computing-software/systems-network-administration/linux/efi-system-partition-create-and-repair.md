---
id: computing-software.systems-network-administration.linux.efi-system-partition-create-and-repair
name: efi-system-partition-create-and-repair
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, efi-system-partition, esp, uefi, mkfs-vfat, grub-install, efibootmgr, fallback-bootloader]
level: advanced
status: docs-checked
description: "Create, size, mount and repair the EFI system partition: type EF00, FAT32, fstab options, reinstalling the bootloader and the fallback BOOTX64.EFI path."
sources:
  - https://wiki.archlinux.org/title/EFI_system_partition
  - https://wiki.archlinux.org/title/GRUB
  - https://www.rodsbooks.com/gdisk/sgdisk.html
  - https://docs.kernel.org/filesystems/vfat.html
  - https://man.archlinux.org/man/efibootmgr.8
  - https://manpages.debian.org/unstable/dosfstools/fsck.fat.8.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# EFI system partition (ESP)

## Create
```bash
sgdisk -n 1:0:+1G -t 1:EF00 -c 1:"EFI system partition" /dev/nvme0n1   # parted: set 1 esp on
mkfs.fat -F 32 -n EFI /dev/nvme0n1p1
```
Size: the GPT fdisk documentation recommends 550 MiB (smaller ESPs are common, but some firmware has flaky FAT drivers that need a larger one); allow more if kernels or unified kernel images live on it. Use FAT32 (`mkfs.fat -F` selects the FAT size; `-n` sets the label).
Mount point depends on the bootloader and distro: `/boot/efi`, `/efi` or `/boot` are the usual choices (Arch wiki, "Typical mount points").
fstab: `UUID=XXXX-XXXX /boot/efi vfat umask=0077 0 2`; the vfat driver also accepts `shortname=lower|win95|winnt|mixed` (kernel vfat documentation).

## Is the system booted in UEFI mode?
`cat /sys/firmware/efi/fw_platform_size` prints 64 or 32 on a UEFI boot; if the file does not exist you did not boot in UEFI mode (Arch wiki, kernel 4.0 or newer). Boot the live system in UEFI mode before installing an EFI bootloader so it can write the NVRAM boot entries.

## Repair: bootloader files missing / NVRAM entry gone
```bash
mount /dev/nvme0n1p1 /boot/efi
ls /boot/efi/EFI/                         # one directory per installed bootloader, plus BOOT for the fallback
efibootmgr -v                             # list the NVRAM boot entries and the loader paths they point at
# GRUB systems
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=<name>
# Secure Boot via shim: reinstall the distro's shim and GRUB EFI packages instead of running grub-install (package names vary), then recreate the entry:
efibootmgr -c -d /dev/nvme0n1 -p 1 -L "<label>" -l '\EFI\<vendor>\shimx64.efi'
```
`efibootmgr -c` creates a boot entry (`-d` disk, `-p` partition number, `-L` label, `-l` loader path).
Fallback path: with `grub-install --removable`, GRUB goes to `esp/EFI/BOOT/BOOTX64.EFI`, so you can boot if the EFI variables are reset or the drive is moved to another computer (Arch wiki, GRUB). Make sure that file exists for the architecture you boot.

## RAID1 for the ESP
Create the array with `--metadata=1.0`, which keeps the RAID metadata at the end of the partition so the firmware can read the FAT filesystem; or keep two ESPs and copy the primary to the secondary on updates (Arch wiki, EFI system partition).

## Gotchas
- Windows dual-boot: avoid reformatting an existing ESP, which may hold files other operating systems need (Arch wiki); an old ESP may be smaller than you want.
- Filesystem errors after crashes: run `fsck.fat -a /dev/nvme0n1p1` on the unmounted partition (`-a` repairs automatically, using the least destructive method).
- Check the boot entries again after replacing disks: `efibootmgr -v`.

## Verify
- [ ] `efibootmgr -v` shows an entry pointing at an existing file; `lsblk -o NAME,PARTTYPENAME,FSTYPE` shows EFI System + vfat.

## Checked
Checked 2026-10-27 against the Arch wiki (EFI system partition, GRUB, UEFI pages), the GPT fdisk sgdisk manual, the kernel vfat documentation, the efibootmgr(8), mkfs.fat(8) and fsck.fat(8) manuals.
- sgdisk `-n`, `-t` (hex code such as EF00) and `-c`; GPT fdisk says an ESP must be FAT-32 and recommends 550 MiB.
- `mkfs.fat -F` (FAT size) and `-n` (label); `fsck.fat -a` repairs automatically.
- vfat mount options `umask=` and `shortname=lower|win95|winnt|mixed`.
- efibootmgr `-c`, `-d`, `-p`, `-L`, `-l`; `grub-install --removable` installs `esp/EFI/BOOT/BOOTX64.EFI`; `/sys/firmware/efi/fw_platform_size` exists only on a UEFI boot; RAID1 ESP needs mdadm `--metadata=1.0`.
- Removed unconfirmed claims: 512 MiB/1 GiB sizing, distro-specific mount points, Red Hat package names and paths, vendor directory names and the 100 MB Windows ESP figure.
Method: documentation only; no commands were run.
