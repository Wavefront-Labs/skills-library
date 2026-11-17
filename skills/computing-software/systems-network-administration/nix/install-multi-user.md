---
id: computing-software.systems-network-administration.nix.install-multi-user
name: install-multi-user
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, install-nix, multi-user-install, daemon-install]
level: intro
status: docs-checked
description: "Install Nix with the official script, choose multi-user (daemon) mode, check what the installer does by default per platform and read its flags."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/installing-binary.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Default install:

```
curl -L https://nixos.org/nix/install | sh
```

The default depends on the platform:
- Multi-user: Linux with systemd and without SELinux, and macOS.
- Single-user: Linux without systemd, and Linux with SELinux.

Multi-user is recommended if your platform supports it and you can authenticate with `sudo`. It creates system users and a system service for the Nix daemon.

Force multi-user:

```
bash <(curl -L https://nixos.org/nix/install) --daemon
```

Run it as your normal user or as `root`; the script calls `sudo` when needed.

See the installer flags:

```
curl -L https://nixos.org/nix/install | sh -s -- --help
```

To customise further, download and edit the second-stage installation script.

Gotcha: on macOS 15 Sequoia, an error that user `_nixbld1` in group `nixbld` does not exist is tracked in GitHub issue NixOS/nix#10892, which explains how to repair without reinstalling.

## Checked

2026-11-04. Confirmed against the Nix manual Installing a Binary Distribution page: the default install command, the platform defaults, the multi-user recommendation, the `--daemon` command, running as a normal user or `root`, `--help`, the second-stage script, and the macOS 15 `_nixbld1` issue. Removed an unsourced verify line.

Method: documentation only; no commands were run.
