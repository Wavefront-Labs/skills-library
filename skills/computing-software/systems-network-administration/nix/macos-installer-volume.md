---
id: computing-software.systems-network-administration.nix.macos-installer-volume
name: macos-installer-volume
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, macos, apfs-volume, launchdaemon, synthetic-conf]
level: advanced
status: docs-checked
description: "What the Nix macOS installer changes: APFS volume, synthetic.conf, fstab options, FileVault key and LaunchDaemon, for troubleshooting a broken install."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/installing-binary.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The macOS installer:
- Creates a new APFS volume for the Nix store.
- Adds an entry to `/etc/synthetic.conf` so macOS creates an empty synthetic root directory to mount the volume on.
- Adds `/etc/fstab` mount options for the volume:
  - `rw`: read-write.
  - `noauto`: prevents automatic mounting, so the LaunchDaemon controls mounting.
  - `nobrowse`: hides the volume from the desktop and keeps Spotlight from indexing it.
- If FileVault is enabled, generates an encryption password, stores it in the System Keychain, and uses it to encrypt the volume.
- Creates a system LaunchDaemon that mounts the volume early in boot, before programs that need the store start.

The installer handles the read-only root filesystem automatically for new installs.

You do not need these details to run the installer, but the manual says they may help if you run into trouble.

After updating to macOS 15 Sequoia, an error that user `_nixbld1` in group `nixbld` does not exist is tracked in NixOS/nix#10892.

## Checked

2026-11-04. Confirmed against the Nix manual Installing a Binary Distribution page, macOS section: the APFS volume, `/etc/synthetic.conf`, the `rw`, `noauto` and `nobrowse` fstab options, the FileVault password and Keychain steps, the LaunchDaemon, and the Sequoia issue. Removed an unsourced troubleshooting order.

Method: documentation only; no commands were run.
