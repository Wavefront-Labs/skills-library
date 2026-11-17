---
id: computing-software.systems-network-administration.linux.firmware-updates-with-fwupd-lvfs
name: firmware-updates-with-fwupd-lvfs
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, fwupd, lvfs, fwupdmgr, uefi-capsule, firmware-updates, bios-update]
level: practitioner
status: docs-checked
description: "Update system, SSD, dock and peripheral firmware on Linux with fwupd and the LVFS: fwupdmgr refresh, get-updates, UEFI capsule updates, offline cabinets and fleet policy."
sources:
  - https://github.com/fwupd/fwupd/blob/main/src/fwupdmgr.md
  - https://github.com/fwupd/fwupd/blob/main/docs/fwupd.conf.md
  - https://github.com/fwupd/fwupd/blob/main/plugins/uefi-capsule/README.md
  - https://github.com/fwupd/fwupd/blob/main/docs/fwupd-remotes.d.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Firmware updates with fwupd/LVFS

fwupd is the daemon and `fwupdmgr` the client; vendors publish signed firmware cabinets to the Linux Vendor Firmware Service (LVFS). Device support comes from plugins (`fwupdmgr get-plugins` lists them), including UEFI capsules for system firmware.

## Check and update
```bash
fwupdmgr get-devices                 # devices fwupd can update, current versions, flags
fwupdmgr refresh                     # download LVFS metadata (signed)
fwupdmgr get-updates                 # available versions with release notes
fwupdmgr update                      # all; or fwupdmgr update <device-id>
fwupdmgr get-history                 # results of previous updates
fwupdmgr security                    # host security attributes used to rate the machine
```
UEFI updates are staged as capsules and applied on reboot. Keep AC power connected; `IgnorePower` in `fwupd.conf` exists for overriding the power checks.

## Requirements for UEFI capsule updates
- System booted in UEFI mode, ESP mounted: fwupd autodetects it at `/boot/efi`, `/boot` or `/efi` (UDisks needed), otherwise set `EspLocation` in `/etc/fwupd/fwupd.conf`; `RequireESPFreeSpace` sets the free space needed.
- Secure Boot: the companion `fwupdx64.efi` must be signed by an authority trusted by shim or the host; the `use-shim-for-sb` flag makes fwupd load it via shim.
- Disk encryption tied to firmware measurements (TPM-sealed LUKS or BitLocker keys): check your vendor's procedure and have the recovery key ready before a firmware update.

## Offline / air-gapped
```bash
fwupdmgr get-details firmware.cab
fwupdmgr install firmware.cab --allow-reinstall
```
Or mirror LVFS metadata by adding a remote in `/etc/fwupd/remotes.d/*.conf` whose `MetadataURI=` points at your server (`http://`, `https://` and `file://` are supported).

## Fleet policy
- `fwupdmgr` supports `--json` for parsing (terminal output is not stable between versions) and `--no-reboot-check`; `--allow-reinstall`, `--allow-older` and `--assume-yes` also exist.
- `set-approved-firmware` / `ApprovedFirmware` allow-lists cabinet checksums (SHA-1 or SHA-256); it only affects updates from remotes with `ApprovalRequired=true`, and `fwupdmgr install` can still install manually.
- Test on one machine of each model; firmware updates can change boot order or reset BIOS settings.
- `/etc/fwupd/fwupd.conf` also has `DisabledPlugins` and `DisabledDevices` (GUIDs, semicolon-separated).

## Verify
- [ ] `fwupdmgr get-updates` reports no updates (or only deliberately held ones) after reboot.
- [ ] `fwupdmgr get-history` shows a successful result for each device updated.

## Checked

Checked 2026-10-26 against fwupd/fwupd main (last commit 2026-10-23): src/fwupdmgr.md, docs/fwupd.conf.md, docs/fwupd-remotes.d.md, plugins/uefi-capsule/README.md, data/bash-completion/fwupdmgr (flag list) and src/fu-cli.c. Confirmed: fwupdmgr actions, --json, --no-reboot-check, --allow-reinstall, --allow-older, --assume-yes flags, ESP autodetection paths and EspLocation, RequireESPFreeSpace, use-shim-for-sb and fwupdx64.efi signing requirement, remote MetadataURI schemes, ApprovedFirmware semantics with ApprovalRequired, DisabledPlugins and DisabledDevices. Removed: the fwupd.conf 1.9 version claim, the BitLocker/PCR detail, systemd-cryptenroll advice, server vendor tool names, the local-metadata refresh command form and the invented UpdateError hint; the --no-reboot-check flag belongs to fwupdmgr, not fwupd.

Method: documentation only; no commands were run.
