---
id: computing-software.systems-network-administration.linux.systemd-swap-units
name: systemd-swap-units
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, swap-unit, systemd-swap, swap, fstab-generator, swapfile, systemd-makefs]
level: practitioner
status: docs-checked
description: "Manage swap through systemd: fstab-generated .swap units, writing native swap units with Priority and Options, ordering, and debugging swap that won't activate."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.swap.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-fstab-generator.html
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/swapon.c
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# systemd .swap units

## From fstab
systemd-fstab-generator turns each swap line into a unit named after the escaped path:
`/swapfile` → `swapfile.swap`, `/dev/mapper/vg-swap` → `dev-mapper-vg\x2dswap.swap`.
```bash
systemctl list-units --type=swap --all
systemctl status 'dev-mapper-vg\x2dswap.swap'
systemd-escape -p --suffix=swap /dev/mapper/vg-swap
```
## Native unit (no fstab)
`/etc/systemd/system/swapfile.swap`:
```ini
[Unit]
Description=Swap file
[Swap]
What=/swapfile
Priority=10
Options=discard
TimeoutSec=5min
[Install]
WantedBy=swap.target
```
`systemctl daemon-reload && systemctl enable --now swapfile.swap`.
The unit name must match the escaped `What=` path.

## Ordering
`swap.target` collects swap units. A missing swap device makes boot wait for the device timeout — add `nofail`
in fstab.

## Debug failures
```bash
journalctl -b -u swapfile.swap
```
Messages come from swapon (util-linux): `insecure permissions 0644, 0600 suggested` means the swap file must be made private (`chmod 600`); `skipping - it appears to have holes` means the file is sparse and must be recreated without holes. A device that never appears makes the start job wait for the device timeout.

## Verify
- [ ] `swapon --show` lists the device with intended priority; `systemctl is-active <unit>.swap` after reboot.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: swap units are generated from fstab at boot and on reload, must be named after the escaped path, and `Priority=`, `Options=`, `TimeoutSec=` exist (`systemd.swap`); `swap.target`; swapon source (util-linux `sys-utils/swapon.c`) prints the permissions and holes messages quoted. Removed the claim about automatic LUKS/LVM dependencies, the `x-systemd.device-timeout` option on swap lines (documented for mount lines only) and two speculative failure causes.

Method: documentation only; no commands were run.
