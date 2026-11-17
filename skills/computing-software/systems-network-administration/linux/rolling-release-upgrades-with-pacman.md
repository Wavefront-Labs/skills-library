---
id: computing-software.systems-network-administration.linux.rolling-release-upgrades-with-pacman
name: rolling-release-upgrades-with-pacman
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, pacman, archlinux-keyring, pacman-syu, pacnew, arch-news, downgrade]
level: practitioner
status: docs-checked
description: "Keep Arch Linux rolling-release systems healthy: full -Syu upgrades, keyring refresh, reading Arch news, pacnew merging, partial upgrade traps, downgrades and recovery."
sources:
  - https://wiki.archlinux.org/title/System_maintenance
  - https://wiki.archlinux.org/title/Pacman
  - https://wiki.archlinux.org/title/Pacman/Package_signing
  - https://archlinux.org/news/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Rolling release upgrades with pacman

## The rule: always full upgrades
```bash
pacman -Syu          # sync databases AND upgrade everything
```
Never `pacman -Sy <pkg>` (sync without upgrading) and never `pacman -S <pkg>` on stale databases followed by skipping the upgrade: that's a **partial upgrade**, which breaks shared library dependencies (`error while loading shared libraries: <library>.so.<N>`). Installing a package = `pacman -Syu <pkg>`.

## Before upgrading
- Read https://archlinux.org/news/ for manual interventions.
- Upgrade often (weekly); months-old systems hit keyring and dependency issues.
- Make a snapshot if on btrfs (snapper `snap-pac` hook) or have a live USB ready.

## Keyring problems
`signature from "X" is unknown trust` / `invalid or corrupted package (PGP signature)`:
```bash
pacman -Sy archlinux-keyring && pacman -Su
# still broken:
pacman-key --init && pacman-key --populate archlinux
pacman-key --refresh-keys     # slow; usually unnecessary
```
Clock skew also breaks signature checks; verify `timedatectl`.

## After upgrading
```bash
pacdiff                       # (pacman-contrib) merge .pacnew/.pacsave config files
find /etc -name '*.pacnew'
checkupdates                  # safe check without touching the sync db
pacman -Qdtq | pacman -Rns -  # remove orphans (review the list first)
paccache -rk2                 # keep 2 old versions in the cache
journalctl -p 3 -b            # errors after reboot
```
Kernel upgrades: reboot soon; modules for the running kernel are gone after the upgrade (USB devices may fail to load drivers until reboot). Keep `linux-lts` installed as a fallback boot entry.

## Mirrors
Reflector (package `reflector`) filters the most up-to-date mirrors, sorts them by speed and overwrites `/etc/pacman.d/mirrorlist`; see `reflector --help` for the options.
An out-of-sync mirror gives failed downloads or partial updates; `pacman -Syyu` forces a database refresh, which is never needed under normal circumstances.

## Downgrade / recover
```bash
pacman -U /var/cache/pacman/pkg/<package>-<version>-x86_64.pkg.tar.zst   # from cache
# Arch Linux Archive for older versions: https://archive.archlinux.org/
IgnorePkg = <package>         # temporarily in /etc/pacman.conf; remember to remove
```
Unbootable after upgrade: boot ISO, `mount` root and boot, `arch-chroot /mnt`, `pacman -Syu` to finish an interrupted upgrade, `mkinitcpio -P`, reinstall bootloader if needed.
`unable to lock database`: another pacman is running, or remove stale `/var/lib/pacman/db.lck` after confirming none is.

## Verify
- [ ] `pacman -Qk 2>&1 | grep -v ' 0 missing'` shows no packages with missing files.
- [ ] No unmerged `.pacnew` files; system boots on both linux and linux-lts.

## Checked

2026-10-28

Confirmed: Arch wiki pages System maintenance (read the news before upgrading, avoid pacman -Sy without upgrading), Pacman (full upgrade, -Syyu), Pacman/Package_signing (archlinux-keyring refresh, pacman-key --refresh-keys), Pacman/Pacnew_and_Pacsave, Pacman/Tips and tricks (paccache, checkupdates, db.lck), Reflector, Downgrading packages, Arch Linux Archive, snap-pac and linux-lts.

Removed or corrected: The yay -Pw command, a specific libicu version in the error example, specific mesa package versions, and the reflector command line with country and rate options (replaced by a pointer to reflector --help).

Method: documentation only; no commands were run.
