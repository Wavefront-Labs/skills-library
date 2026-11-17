---
id: computing-software.systems-network-administration.nix.uninstall-macos
name: uninstall-macos
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, uninstall-macos, diskutil, launchctl]
level: practitioner
status: docs-checked
description: "Uninstall multi-user Nix from macOS: restore rc backups, unload LaunchDaemons, delete build users, edit fstab and synthetic.conf, delete the APFS volume."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/uninstall.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Restore shell init files from installer backups if unchanged since install:

```
sudo mv /etc/zshrc.backup-before-nix /etc/zshrc
sudo mv /etc/bashrc.backup-before-nix /etc/bashrc
sudo mv /etc/bash.bashrc.backup-before-nix /etc/bash.bashrc
```

Otherwise remove the block sourcing `nix-daemon.sh` by hand.

2. Stop the services:

```
sudo launchctl unload /Library/LaunchDaemons/org.nixos.nix-daemon.plist
sudo rm /Library/LaunchDaemons/org.nixos.nix-daemon.plist
sudo launchctl unload /Library/LaunchDaemons/org.nixos.darwin-store.plist
sudo rm /Library/LaunchDaemons/org.nixos.darwin-store.plist
```

3. Remove the group and build users:

```
sudo dscl . -delete /Groups/nixbld
```

Then, with `dscl . -list` on the users record type, find every `_nixbld` account and remove each with `sudo dscl . -delete` on its record (the manual loops over the grep result).

4. `sudo vifs` and delete the fstab line mounting the Nix Store volume on `/nix`.
5. Remove the `nix` line from `/etc/synthetic.conf` (delete the file if it is the only line).
6. Delete `/etc/nix`, `~/.nix-profile`, `~/.nix-defexpr`, `~/.nix-channels`, the same under `/var/root`, and `~/.local/share/nix`, `~/.local/state/nix`, `~/.cache/nix`.
7. `sudo diskutil apfs deleteVolume /nix` (removes the store). If it fails, check `diskutil list` for an unmounted "Nix Store" volume and delete it by its `diskXsY` identifier; if the kernel reports in use, reboot and delete immediately.

An empty `/nix` directory remains until the next reboot; this is expected.

## Checked

2026-11-04: backup restore, launchctl unload commands, dscl group and user removal, vifs and synthetic.conf edits, the file list, diskutil deleteVolume steps and the empty /nix note confirmed against the Uninstalling Nix manual page (macOS section). Removed nothing.

Method: documentation only; no commands were run.
