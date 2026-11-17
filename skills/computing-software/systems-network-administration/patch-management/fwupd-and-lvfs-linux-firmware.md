---
id: computing-software.systems-network-administration.patch-management.fwupd-and-lvfs-linux-firmware
name: fwupd-and-lvfs-linux-firmware
category: computing-software
field: systems-network-administration
product: patch-management
tags: [fwupd, lvfs, fwupdmgr, uefi-capsule, firmware-patching, linux, hsi]
level: practitioner
status: docs-checked
description: "Update system and device firmware on Linux with fwupd and LVFS: fwupdmgr workflow, UEFI capsule prerequisites, offline and enterprise remotes, and firmware security (HSI)."
sources:
  - https://fwupd.org/lvfs/docs/users
  - https://github.com/fwupd/fwupd/blob/main/src/fwupdmgr.md
  - https://fwupd.github.io/libfwupdplugin/hsi.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fwupd and LVFS on Linux

**Goal:** apply vendor firmware (UEFI/BIOS, SSD, docks, Thunderbolt, TPM) on Linux laptops and many servers with a standard tool.

## Workflow
```bash
fwupdmgr refresh                 # fetch metadata from LVFS
fwupdmgr get-devices             # what fwupd can see and update
fwupdmgr get-updates
fwupdmgr update                  # applies; UEFI updates stage a capsule and need a reboot
fwupdmgr get-history
```
Single device: `fwupdmgr update <device-id>`. Downgrade (when the vendor allows): `fwupdmgr downgrade`.

## UEFI capsule prerequisites
- Booted in UEFI mode, ESP mounted (usually `/boot/efi`), enough free space.
- BitLocker-style concerns: if the disk uses TPM-sealed LUKS keys, firmware changes alter PCR values; have the recovery passphrase ready.

## Enterprise use
- Mirror LVFS metadata and firmware to an internal remote for offline sites and control which versions are approved (see the fwupd documentation for remote configuration).
- Automate `fwupdmgr refresh` and `fwupdmgr update` from config management (check `fwupdmgr --help` for the non-interactive options in your version), then schedule reboots.
- Many enterprise servers are better served by vendor tools (Dell DSU/iDRAC, HPE SUM/SPP, Lenovo XClarity), which update BMC and controller firmware fwupd may not cover.

## Security posture
`fwupdmgr security` lists the host security attributes used to evaluate the machine's Host Security ID (HSI) level; `security-fix` and `security-undo` act on individual failures. The HSI specification is marked as still in active development.

## Gotchas
- Keep laptops on mains power during firmware updates.
- A device missing from `get-devices` may have no fwupd plugin or LVFS firmware for it.

## Verify
`fwupdmgr get-devices` shows the new version after reboot and `get-history` records success.

## Checked

Checked 2026-10-27 against the fwupdmgr manual page (fwupd main branch) and the Host Security ID specification (libfwupdplugin 2.1.2).
- `fwupdmgr refresh`, `get-devices`, `get-updates`, `update`, `downgrade`, `get-history`, `security`, `security-fix`: confirmed; `refresh` then `update` may ask for a reboot to apply updates.
- HSI attributes and the specification's development status: confirmed.
- Removed unconfirmed: the signed `fwupdx64.efi` statement, `/etc/fwupd/remotes.d/` and the `--no-reboot-check` flag, the battery statement.
Method: documentation only; no commands were run.
