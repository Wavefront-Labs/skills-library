---
id: computing-software.systems-network-administration.cisco-networking.ios-xe-install-mode-upgrade
name: ios-xe-install-mode-upgrade
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, ios-xe, catalyst-9000, install-mode, bundle-mode, ios-xe-upgrade, software-upgrade, install-add, install-activate, install-commit, install-remove-inactive, packages-conf, rommon-upgrade, stack-upgrade, ios-file-system]
level: practitioner
status: draft
description: "Upgrade Catalyst 9000 / IOS XE in install mode: pre-checks, install add/activate/commit, auto-rollback window, stack behaviour, freeing flash and recovering a failed boot."
sources:
  - https://www.cisco.com/c/en/us/support/docs/switches/catalyst-9300-series-switches/216231-upgrade-guide-for-cisco-catalyst-9000-sw.html
  - https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9300/software/release/17-9/release_notes/ol-17-9-9300.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IOS XE upgrade in install mode

Catalyst 9000 and most IOS XE routers should run in **install mode** (boot from
`packages.conf`), not bundle mode (boot the .bin directly). Install mode boots faster, supports
ISSU/rollback and is required for some features.

## Pre-checks
```
show version | i Installation mode|Version|uptime
show boot                                 ! BOOT var should be flash:packages.conf
dir flash: | i free|bytes
show install summary
show switch                               ! stacks: all members Ready, same version
```
- Read the release notes upgrade path: some jumps need an intermediate release or a ROMMON
  upgrade (done automatically on 9300/9400 from 16.x but adds a reload).
- Need about 1 GB free on flash. Clean first: `install remove inactive` (prompts per file).
- Verify the image hash against cisco.com: `verify /md5 flash:cat9k_iosxe.17.12.04.SPA.bin`
  (or `/sha512`).

## Copy and install
```
copy scp://<USER>@<SERVER>/cat9k_iosxe.17.12.04.SPA.bin flash:
install add file flash:cat9k_iosxe.17.12.04.SPA.bin activate commit
```
One-shot `add activate commit` reloads the switch (all stack members together). Two-step if
you want a rollback window:
```
install add file flash:cat9k_iosxe.17.12.04.SPA.bin
install activate auto-abort-timer 60     ! reloads; rolls back after 60 min unless committed
install commit                           ! after verifying
```
`install abort` before the timer ends returns to the old version (another reload).

## Converting bundle to install mode
```
install add file flash:<image>.bin activate commit
```
run from a switch booted in bundle mode does the conversion; then `boot system
flash:packages.conf`, `no boot system flash:<old>.bin`, `write memory`.

## Recovery
- Boot loop / ROMMON: `switch: dir flash:` then `boot flash:packages.conf` or boot the .bin
  directly (`boot flash:cat9k_iosxe...bin`) and redo the install.
- Stack member with a version mismatch shows `V-Mismatch` in `show switch`; `software auto-upgrade
  enable` lets the active push its packages.

## Gotchas
- `request platform software package clean` is the older equivalent of
  `install remove inactive`; do not delete `.pkg` files by hand while they are referenced
  by `packages.conf`.
- SMUs (patches) use the same `install add/activate/commit` flow.
- Schedule console access: a failed ROMMON upgrade is only recoverable from the console.

## Verify
- [ ] `show version` shows the new release and `Installation mode is INSTALL`.
- [ ] `show install summary` shows the new version `C` (committed), old removed.
- [ ] `show switch` all members Ready with the same version.
