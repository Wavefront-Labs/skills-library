---
id: computing-software.systems-network-administration.nix.uninstall-single-user
name: uninstall-single-user
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, uninstall-single-user, freebsd-uninstall]
level: intro
status: docs-checked
description: "Remove a single-user Nix install with one rm command, and the FreeBSD multi-user variant using service, sysrc and pw."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/uninstall.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Single-user installation:

```
rm -rf /nix ~/.nix-channels ~/.nix-defexpr ~/.nix-profile ~/.local/share/nix ~/.local/state/nix ~/.cache/nix
```

You may also want to remove Nix references from `~/.profile`.

FreeBSD multi-user:

```
sudo service nix-daemon stop
sudo rm -f /usr/local/etc/rc.d/nix-daemon
sudo sysrc -x nix_daemon_enable
sudo rm -rf /etc/nix /usr/local/etc/profile.d/nix.sh /nix ~/.local/share/nix ~/.local/state/nix ~/.cache/nix ~/.nix-defexpr ~/.nix-profile ~/.nix-channels ~root/.nix-channels ~root/.nix-defexpr ~root/.nix-profile ~root/.cache/nix
for i in $(seq 1 32); do
  sudo pw userdel nixbld$i
done
sudo pw groupdel nixbld
```

Optionally remove Nix references from `/usr/local/etc/bashrc`, `/usr/local/etc/zshrc` and shell configuration in users' home directories.

## Checked

2026-11-04: the single-user rm command, the ~/.profile note and the full FreeBSD service, file, user and group removal steps confirmed against the Uninstalling Nix manual page. Removed the closing Gotcha about copying profiles first, which the page does not state.

Method: documentation only; no commands were run.
