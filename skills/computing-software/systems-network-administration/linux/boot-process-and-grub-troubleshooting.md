---
id: computing-software.systems-network-administration.linux.boot-process-and-grub-troubleshooting
name: boot-process-and-grub-troubleshooting
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, boot, grub, grub2, uefi, bios, initramfs, initrd, dracut, update-initramfs, kernel-panic, rescue-mode, emergency-mode, systemd-analyze, mbr, efi, grub-rescue, sysadmin, grub-install, lsinitrd, grub-mkconfig, efibootmgr, boot-failure]
level: advanced
status: docs-checked
description: "Trace the Linux boot sequence from firmware to userspace, and recover a broken GRUB config, missing initramfs module, or failed mount at boot."
sources:
  - https://github.com/rhboot/grub2/blob/master/docs/grub.texi
  - https://www.freedesktop.org/software/systemd/man/latest/bootup.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.html
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.cmdline.7.adoc
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Boot process and GRUB troubleshooting — firmware to login prompt

**Goal:** know which stage of boot failed from the symptom alone (black
screen vs grub prompt vs kernel panic vs emergency shell), and have the
exact recovery command for each without reaching for a reinstall.

## 1. The stages, in order
1. **Firmware** (UEFI or legacy BIOS) — POST, then hands off to a boot
   loader found via UEFI boot entries (`efibootmgr`) or the MBR boot sector.
2. **GRUB stage 1/2** — reads `/boot/grub2/grub.cfg` (or `/boot/grub/grub.cfg`),
   shows the menu, loads the selected kernel + initramfs into memory.
3. **Kernel + initramfs (initrd)** — kernel starts, hands control to the
   initramfs's `init` script, which finds and mounts the real root
   filesystem (handles LVM activation, RAID assembly, LUKS unlock, network
   root for diskless boot) then `switch_root`s onto it.
4. **systemd (PID 1) on the real root** — runs `sysinit.target` →
   `basic.target` → `multi-user.target`/`graphical.target`, mounting
   `/etc/fstab` entries, starting services in dependency order.

Knowing which stage you're stuck at narrows the fix immediately:
- Nothing on screen at all / firmware logo loops → stage 1 (firmware/boot entry), not Linux's problem yet.
- `grub rescue>` prompt → stage 2, GRUB can't find its own files.
- Kernel messages then a panic → stage 3, bad kernel/initramfs/root device.
- Dropped to an initramfs shell, or to the systemd emergency/rescue prompt asking for the root password → stage 3 or early stage 4, a required device/filesystem is missing.

## 2. GRUB rescue prompt
```
grub rescue> ls                       # lists detected devices, (hd0,gpt1) etc
grub rescue> ls (hd0,gpt2)/            # browse a partition's filesystem to find /boot
grub rescue> set root=(hd0,gpt2)
grub rescue> set prefix=(hd0,gpt2)/boot/grub2        # or /boot/grub, depending on the distro
grub rescue> insmod normal
grub rescue> normal                   # drops into the full GRUB menu if files are found
```
This means GRUB's own stage1 can't locate `grub.cfg`/the normal module —
usually a disk that moved (partition renumbered, RAID reassembled
differently) or a corrupted/missing `/boot`. Once booted via rescue,
reinstall GRUB properly rather than leaving it limping:
```bash
# from a live USB or booted system with the root mounted at /mnt
grub2-install --boot-directory=/mnt/boot /dev/sda      # BIOS/MBR
grub2-mkconfig -o /mnt/boot/grub2/grub.cfg
# UEFI systems instead need the ESP mounted and:
grub-install --target=x86_64-efi --efi-directory=/mnt/boot/efi --bootloader-id=GRUB
```

## 3. Editing the boot menu at boot time (no file edit needed)
At the GRUB menu, press `e` on an entry to edit it for one boot only —
useful for a quick single-use kernel parameter without touching config:
```
linux ... ro quiet splash
```
Common edits: append `single` (systemd boots to rescue mode, equivalent to `systemd.unit=rescue.target`) or `init=/bin/bash` (the kernel runs that binary instead of /sbin/init, bypassing systemd entirely — the classic "forgot root password"
recovery, combined with remounting read-write and `passwd` before reboot);
remove `quiet splash` to see actual boot messages when diagnosing a hang. With dracut, `rd.break` drops to a shell before the initramfs switches to the real root.
Press `Ctrl+X` to boot the edited entry once (the GRUB manual; `ESC` returns to the menu); it reverts on next boot.

## 4. initramfs problems
```bash
lsinitrd /boot/initramfs-$(uname -r).img | grep -i <module>   # dracut-based systems (image path varies)
lsinitramfs /boot/initrd.img-$(uname -r) | grep -i <module>    # initramfs-tools (Debian/Ubuntu)
dracut --force --add-drivers <module>          # rebuild with a missing driver baked in
update-initramfs -u -k all                       # initramfs-tools: update the initramfs of all installed kernels
```
An initramfs shell after a failed root-device search usually
means: the root device moved (disk added/removed changing `/dev/sdX`
numbering — use UUIDs in `/etc/fstab` and GRUB's `root=` to avoid this
entirely), a LVM/RAID/LUKS module needed to assemble the root device wasn't
included in the initramfs, or a storage driver (NVMe, virtio, RAID
controller) is missing after a bare-metal-to-VM (or vice versa) migration.
```bash
blkid                                # confirm the actual UUID of the intended root device from the initramfs shell
mount /dev/mapper/vg-root <the initramfs's root mount point>   # manually assemble/mount (dracut and initramfs-tools use different mount points; see the shell's banner), then `exit` to continue
```

## 5. systemd stuck in emergency/rescue mode after initramfs succeeds
```bash
systemctl --failed                   # which unit(s) blocked multi-user.target
journalctl -xb                        # full boot log for this boot
mount -a                              # replay fstab; a bad entry shows exactly which line failed
```
The most common cause here is a bad `/etc/fstab` entry (typo'd UUID, a
network mount with no `_netdev`/`nofail` option that blocks boot waiting
for a filer that isn't up yet). Add `nofail` to any mount that shouldn't be
allowed to block the whole boot, and always test an `/etc/fstab` edit with
`mount -a` on a live system before trusting it to work unattended on reboot.

## 6. Measuring/explaining slow boots
```bash
systemd-analyze                       # total boot time, split kernel/initrd/userspace
systemd-analyze blame                 # which unit took longest to start
systemd-analyze critical-chain        # the dependency chain that determined total boot time
```

## Gotchas
- `grub2-mkconfig`/`update-grub` regenerate `grub.cfg` from
  `/etc/default/grub` and `/etc/grub.d/` scripts — **never hand-edit
  `grub.cfg` directly**, the next kernel update regenerates it and silently
  discards manual edits.
- On a dual-boot box another operating system's installer or update can change the UEFI boot entries or boot order, leaving GRUB installed but not the default
  boot target — `efibootmgr -v` then `efibootmgr -o <bootnum>[,<bootnum>...]` (`-o` sets the BootOrder) to
  restore GRUB's priority, no reinstall needed.
- Secure Boot adds a signature-checking layer UEFI itself enforces before
  GRUB even runs — a self-compiled/unsigned kernel or out-of-tree module
  (common with Nvidia/VirtualBox) can fail silently under Secure Boot in
  ways that look like a GRUB problem but aren't; `mokutil --sb-state`
  confirms whether it's enabled.
- Check `df -h /boot` when kernel or initramfs installs fail: a full `/boot` stops the new files being written (see the kernel-retention-and-old-kernel-removal skill).

## Verify
- [ ] `efibootmgr -v` (UEFI) or `fdisk -l` + MBR check (BIOS) shows the intended boot loader as the active/first entry.
- [ ] `grub2-mkconfig`/`update-grub` output lists every installed kernel with no errors, and `grub.cfg`'s timestamp updates after a kernel install.
- [ ] `lsinitrd`/`lsinitramfs` on the current kernel's initramfs includes every module needed to assemble the actual root device (LVM/RAID/LUKS/storage driver as applicable).
- [ ] `systemctl --failed` is empty on a normal boot; any `nofail`-eligible mount is marked so a transient network/storage hiccup can't block the whole boot.
- [ ] A rescue drill (boot to `(initramfs)` or GRUB rescue deliberately, e.g. via a snapshot/test VM) is recoverable using the commands above before relying on them during a real incident.

## Checked
Checked 2026-10-27 against the GRUB manual source (texinfo in github.com/rhboot/grub2), systemd man page sources (systemd(1), bootup(7), systemd.mount(5)), the dracut-ng man pages, the Debian update-initramfs(8) manual, mokutil(1), efibootmgr(8) and the kernel's kernel-parameters.txt. The gnu.org GRUB manual could not be fetched, so the source link points to the mirrored source.
- GRUB rescue sequence `set root`, `insmod normal`, `normal`; `grub2-install --boot-directory=`; `e` edits an entry and `Ctrl-x` boots it; `ESC` returns to the menu.
- systemd: `single` and `1` boot into rescue mode (same as `systemd.unit=rescue.target`); `init=` runs the given binary instead of /sbin/init; `nofail` and `_netdev` in mount options; boot targets sysinit.target, basic.target.
- dracut: `--add-drivers`, `--force`, `rd.break`, `lsinitrd`; initramfs-tools: `update-initramfs -u -k all` ("all" operates on every installed kernel); `mokutil --sb-state`; `efibootmgr -o`.
- Removed unconfirmed claims: F10 as a boot key, the `/sysroot` mount point, exact shell banner texts, Windows Update replacing boot entries, and `/boot` fullness corrupting grub.cfg.
Method: documentation only; no commands were run.
