---
id: computing-software.it-support-helpdesk.desktop-support.boot-loops-reset-this-pc-and-grub-repair
name: boot-loops-reset-this-pc-and-grub-repair
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, boot-loop, reset-this-pc, grub, undoing-changes, startup-repair, linux-boot]
level: practitioner
status: draft
description: "Get machines out of boot loops: Windows 'undoing changes' and update loops, Startup Repair and safe mode, Reset this PC options, and GRUB rescue on Linux desktops."
sources:
  - "https://support.microsoft.com/en-us/windows/windows-startup-settings-1af6ec8c-4d4a-4b23-adb7-e76eef0b847f"
  - "https://support.microsoft.com/en-us/windows/reset-your-pc-0ef73740-b927-549b-b7c9-e6f2b48d275e"
  - "https://www.gnu.org/software/grub/manual/grub/grub.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# boot-loops-reset-this-pc-and-grub-repair

## Windows boot loops
| Loop | Approach |
|---|---|
| "Undoing changes made to your computer" / "We couldn't complete the updates" repeating | Let it finish once (can take an hour); if it repeats, WinRE > Uninstall Updates (latest quality), then pause updates |
| Restart before the logo after a driver/app install | WinRE > Startup Settings > Safe Mode; uninstall the driver/app; or System Restore |
| Automatic Repair couldn't repair your PC | Advanced options > Command Prompt: check disk, BCD (`bcdedit`), `sfc /scannow /offbootdir=<WIN_DRIVE>:\ /offwindir=<WIN_DRIVE>:\Windows` |
| BSOD loop | Note the stop code (disable automatic restart in Startup Settings, option 9) |
| BitLocker prompts each boot | Recovery key, then suspend and resume protection |
- Getting into WinRE when Windows won't start: interrupt boot three times (power off at
  the logo) or boot from install media > Repair your computer.
- Before invasive steps, check for a pending update: `dism /image:C:\ /get-packages`
  showing "Install Pending" and `%SystemRoot%\WinSxS\pending.xml`. Reverting:
  `dism /image:C:\ /cleanup-image /revertpendingactions`.
  In WinRE the Windows volume is often not C; find it with `dir` or `bcdedit` first.

## Reset this PC
| Option | Keeps | Use when |
|---|---|---|
| Keep my files | User files; removes apps and settings | Windows corrupt, data not backed up |
| Remove everything | Nothing (optionally clean the drive) | Reassigning device, malware |
| Cloud download | Fetches fresh image | Local recovery image corrupt |
| Local reinstall | Builds from WinSxS | Offline |
- Corporate devices: prefer Autopilot Reset / Fresh Start via Intune so management and
  apps come back; Reset this PC removes line-of-business apps.
- Have the BitLocker key before starting; list removed apps (saved to the desktop).

## Linux: GRUB problems
- `grub rescue>` prompt: GRUB can't find its modules (partition changed, disk moved). At
  `grub>`: `ls` to find partitions, `set root=(hd0,gpt2)`, `linux /vmlinuz root=/dev/sda2`,
  `initrd /initrd.img`, `boot`.
- Permanent fix from a live USB (chroot into the installed system):
```bash
sudo mount /dev/sda2 /mnt; sudo mount /dev/sda1 /mnt/boot/efi
for d in dev proc sys; do sudo mount --bind /$d /mnt/$d; done
sudo chroot /mnt
grub-install /dev/sda && update-grub     # Debian/Ubuntu
# RHEL/Fedora: grub2-mkconfig -o /boot/grub2/grub.cfg
```
- Kernel update broke boot: choose the previous kernel from the GRUB "Advanced options"
  menu, then remove or fix the new one.
- Dual-boot: Windows updates can replace the boot entry; fix boot order in UEFI or with
  `efibootmgr`.

## Verify
The machine boots normally twice in a row, updates are paused or the bad update hidden,
and the cause is recorded.
