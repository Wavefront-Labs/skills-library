---
id: computing-software.systems-network-administration.linux.root-password-recovery
name: root-password-recovery
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, root-password-recovery, password-reset, lost-root, rd-break, init-bin-bash, grub, grub-edit, single-user, emergency-mode, selinux-relabel, autorelabel, rhel, rocky, ubuntu, debian, chroot, live-usb, sulogin, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Reset a lost root password from GRUB: rd.break on RHEL-family (autorelabel), init=/bin/bash on Debian/Ubuntu, live-USB chroot fallback, and the SELinux and locked-account gotchas."
sources:
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.cmdline.7.adoc
  - https://github.com/dracut-ng/dracut-ng/blob/main/man/dracut.bootup.7.adoc
  - https://docs.kernel.org/admin-guide/kernel-parameters.html
  - https://docs.kernel.org/admin-guide/sysrq.html
  - https://docs.fedoraproject.org/en-US/quick-docs/selinux-changing-states-and-modes/
  - https://manpages.debian.org/trixie/passwd/passwd.1.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Root password recovery — get a root shell before the password is asked for

**Goal:** regain root on a machine whose root password is unknown, without
reinstalling, in under five minutes and without leaving SELinux broken.

You need console access (physical, IPMI/iDRAC/iLO, or the hypervisor/cloud serial
console) and GRUB must be unlocked (no GRUB password) or you know that password. If
the disk is LUKS-encrypted you still need the passphrase — this recovers the *account*,
not the *disk*.

## 1. RHEL / Rocky / Alma / Fedora (dracut initramfs): `rd.break`
1. Reboot. At the GRUB menu press `Esc` or `F4` (or hold `Shift`) to stop the countdown, highlight the kernel
   entry, press `e`.
2. Find the line beginning `linux`. Go to its end
   and append ` rd.break`. Optional but helpful: delete `quiet` so you
   can see what happens. The kernel parameter `enforcing=0` starts SELinux permissive
   (see the gotchas for why you may prefer not to).
3. Press Ctrl-X to boot. `rd.break` makes dracut drop to a shell at the end of the initramfs stage (dracut.cmdline(7); `rd.break=pre-pivot` stops just before the root switch). The real root is mounted at `/sysroot` (dracut boot sequence: `sysroot.mount`).
4. Remount read-write if needed, then chroot:
   ```bash
   mount -o remount,rw /sysroot
   chroot /sysroot
   passwd root            # type the new password twice
   ```
5. SELinux: files changed from the initramfs shell may end up with the wrong security
   context, so ask for a relabel on the next boot:
   ```bash
   touch /.autorelabel
   ```
   The `/.autorelabel` file makes the system relabel files on the next reboot (Fedora SELinux documentation).
   A relabel of a whole root filesystem adds time to that boot (more on
   big disks).
6. `exit` (leaves chroot), `exit` again (continues the boot). Log in as root.

Gotchas:
- `rd.break` behaviour differs between releases. If it does not give you a usable shell (for example it asks for a root password),
  use the `init=/bin/bash` method below with `rw` (then there is no `/sysroot` and no chroot — you are already in the
  root fs; still `touch /.autorelabel` on SELinux systems).
- `enforcing=0` (kernel parameter, SELinux permissive for that boot) lets you postpone the relabel, but you then boot once with
  SELinux permissive; fine for a workstation, note it in the change log on a server.

## 2. Debian / Ubuntu (and any distro): `init=/bin/bash`
1. GRUB menu → `e` on the entry. If the menu is hidden, press `Esc` or `F4`, or hold `Shift`,
   during the timeout to show it.
2. On the `linux` line change `ro` to `rw` (the kernel parameters `ro` and `rw` mount the root device read-only or read-write) and append ` init=/bin/bash` (the kernel runs that binary instead of /sbin/init). Remove
   `quiet splash`.
3. Ctrl-X. You land in a bash prompt as root with the root filesystem mounted
   read-write (because of `rw`). If it is still read-only: `mount -o remount,rw /`.
4. `passwd root` (or `passwd <user>` for a sudo user whose password was lost).
5. There is no init running, so `reboot` will not work. Run `sync`, then `echo b > /proc/sysrq-trigger` (the sysrq `b` command reboots immediately without syncing or unmounting disks, and needs sysrq enabled; see the kernel's sysrq documentation).

Some distributions ship with a **locked** root account: `passwd root` then unlocks it by setting a password. If you only want to recover a sudo user, prefer
`passwd <user>` and leave root locked. Check lock state with `passwd -S root` (second field `L` =
locked, `NP` = no password, `P` = usable password).

## 3. Ubuntu "recovery mode" shortcut
Some distributions add a recovery-mode entry under GRUB's advanced options that offers a root shell. If the root fs is read-only, `mount -o remount,rw /` then `passwd`. Whether it asks for the root password depends on the system; if it does and you do not know it, use the methods above.

## 4. Fallback: live USB + chroot
When GRUB is password-protected and unknown, or the bootloader is broken:
```bash
lsblk -f                                   # find the root partition (and /boot, /boot/efi)
mount /dev/<rootdev> /mnt                  # LVM: vgchange -ay first, then /dev/<vg>/<lv>
mount /dev/<bootdev> /mnt/boot             # if separate
for d in dev proc sys run; do mount --rbind /$d /mnt/$d; done
chroot /mnt
passwd root
touch /.autorelabel                        # SELinux systems only
exit; umount -R /mnt; reboot
```
Btrfs roots may need `-o subvol=<name>` on the mount to reach the root subvolume.

## 5. After recovery
- Check `passwd -S root` and `chage -l root` (an expired account still blocks login).
- If SSH root login was relied on, `PermitRootLogin` in `sshd_config` is unaffected.
- Write it down: a password reset is a security event. Expect `/var/log/secure` or
  journal entries on the next boot showing the relabel.
- Prevent repeats: keep a break-glass local admin in `sudoers`, store root passwords in
  the password manager, consider a GRUB password only if you also keep its value
  somewhere safe (a GRUB password with no record just forces the live-USB route).

## Verify
- [ ] Can log in as root (or the recovered user) on the console with the new password.
- [ ] SELinux systems: `getenforce` is `Enforcing` again and `ls -Z /etc/shadow` shows a normal context after the relabel boot.
- [ ] `/.autorelabel` no longer exists after the relabel boot.
- [ ] `passwd -S root` shows `P` (or `L` if you deliberately re-locked it).

## Checked
Checked 2026-10-27 against the dracut-ng man pages (dracut.cmdline(7), dracut.bootup(7)), the kernel's kernel-parameters.txt and sysrq documentation, the GRUB manual source, the Fedora SELinux quick-doc and passwd(1). The Red Hat documentation link was replaced because that portal could not be read.
- dracut: `rd.break` drops to a shell at the end of the initramfs stage and `rd.break=pre-pivot` before the root switch; the root is mounted by `sysroot.mount` at `/sysroot`.
- Kernel parameters `ro`, `rw`, `init=`, `S` (single) and `enforcing=0`/`1` (SELinux) exist; sysrq `b` reboots immediately without syncing; `echo b > /proc/sysrq-trigger` is the documented trigger form.
- Fedora documentation: `/.autorelabel` triggers a relabel on the next reboot; `passwd -S` second field is `L`, `NP` or `P`; GRUB shows a hidden menu on `Esc`/`F4`/`Shift`, edits entries with `e` and boots with `Ctrl-x`.
- Removed unconfirmed claims: the RHEL 9 `sulogin` behaviour, `linuxefi` and `rhgb` details, the SELinux-in-initramfs explanation, `load_policy`/`restorecon` shortcut, `exec /sbin/init`, Ubuntu's locked-root default and recovery-mode menu text, exact `shadow_t` label, and Btrfs subvolume names.
Method: documentation only; no commands were run.
