---
id: computing-software.systems-network-administration.nix.install-single-user
name: install-single-user
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, single-user-install, no-daemon]
level: intro
status: docs-checked
description: "Force a single-user Nix install with --no-daemon, prepare /nix when sudo is unavailable, and know which operations need the store owner."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/installing-binary.md
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/single-user.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Force a single-user install:

```
bash <(curl -L https://nixos.org/nix/install) --no-daemon
```

In this mode `/nix` is owned by the user running the installer. The script uses `sudo` to create `/nix` if it does not exist. Without `sudo`, create it manually as root:

```
su root
mkdir /nix
chown alice /nix
```

(`alice` is the manual's example user; use your own account.)

How single-user mode works: any Nix operation that touches the database at `prefix/var/nix/db` or modifies the store at `prefix/store` must run as the user who owns those directories, usually root. On a single-user machine you can change the ownership of those directories to your regular account so you do not need root for every Nix command.

## Checked

2026-11-04. Confirmed against the Nix manual Installing a Binary Distribution and Single-User Mode pages: the `--no-daemon` command, `/nix` owned by the invoking user, `sudo` creating `/nix`, the manual `mkdir` and `chown alice` steps, and the database and store ownership rule. Removed an unsourced description of the security model and a verify line.

Method: documentation only; no commands were run.
