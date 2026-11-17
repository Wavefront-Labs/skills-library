---
id: computing-software.systems-network-administration.nix.uninstall-linux-multi-user
name: uninstall-linux-multi-user
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, uninstall-nix, systemd-uninstall, build-users-removal]
level: practitioner
status: docs-checked
description: "Remove a multi-user Nix install from Linux with systemd: stop the daemon, delete files, remove nixbld users and group, clean shell rc files."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/uninstall.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
1. Stop the daemon and disable its units:

```
sudo systemctl stop nix-daemon.service
sudo systemctl disable nix-daemon.socket nix-daemon.service
sudo systemctl daemon-reload
```

2. Delete what Nix created:

```
sudo rm -rf /etc/nix /etc/profile.d/nix.sh /etc/tmpfiles.d/nix-daemon.conf /nix ~/.local/share/nix ~/.local/state/nix ~/.cache/nix ~/.nix-defexpr ~/.nix-profile ~/.nix-channels ~root/.nix-channels ~root/.nix-defexpr ~root/.nix-profile ~root/.cache/nix
```

3. Remove build users and group:

```
for i in $(seq 1 32); do
  sudo userdel nixbld$i
done
sudo groupdel nixbld
```

4. Optionally remove Nix references from `/etc/bash.bashrc`, `/etc/bashrc`, `/etc/profile`, `/etc/zsh/zshrc` and `/etc/zshrc`.

Note: step 2 deletes `/nix`, which is the whole store.

## Checked

2026-11-04: the systemd stop and disable commands, the file list, the build-user loop with groupdel and the rc file list confirmed against the Uninstalling Nix manual page (Linux section). Removed the Verify line and the word irreversible, which the page does not state.

Method: documentation only; no commands were run.
