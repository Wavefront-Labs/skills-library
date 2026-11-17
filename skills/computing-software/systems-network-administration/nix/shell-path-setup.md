---
id: computing-software.systems-network-administration.nix.shell-path-setup
name: shell-path-setup
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-sh, path-setup, nix-profile-bin]
level: intro
status: docs-checked
description: "Put Nix on PATH by sourcing profile.d/nix.sh so both the Nix tools and the ~/.nix-profile user environment are found."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/env-variables.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Nix needs two directories on `PATH`:
- `prefix/bin`, which holds the Nix tools.
- `~/.nix-profile/bin`. `~/.nix-profile` is a symlink to the current user environment, an auto-generated package of symlinks to installed packages.

The simplest approach is to source the provided script from `~/.profile` or a similar file:

```
source prefix/etc/profile.d/nix.sh
```

(`prefix` is the Nix installation prefix.)

## Checked

2026-11-04: the two PATH directories, the nix.sh source line and the user-environment description confirmed against the Environment Variables manual page. Removed the fresh-shell verification, the missing-nix advice and the NIX_REMOTE multi-user note, none of which the page states.

Method: documentation only; no commands were run.
