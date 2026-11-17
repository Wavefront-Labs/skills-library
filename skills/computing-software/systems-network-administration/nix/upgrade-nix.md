---
id: computing-software.systems-network-administration.nix.upgrade-nix
name: upgrade-nix
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, upgrade-nix, nix-env-install, daemon-restart]
level: practitioner
status: docs-checked
description: "Upgrade an installed Nix from a nixpkgs channel with nix-env, then restart the daemon on Linux or macOS multi-user, or just update single-user."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/upgrading.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
These instructions apply only if Nix was installed using the manual's installation instructions.

Check which version you would get:

```
nix-shell -p nix -I nixpkgs=channel:nixpkgs-unstable --run "nix --version"
```

Linux multi-user:

```
sudo su
nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
systemctl daemon-reload
systemctl restart nix-daemon
```

macOS multi-user:

```
sudo nix-env --install --file '<nixpkgs>' --attr nix cacert -I nixpkgs=channel:nixpkgs-unstable
sudo launchctl remove org.nixos.nix-daemon
sudo launchctl load /Library/LaunchDaemons/org.nixos.nix-daemon.plist
```

Single-user, all platforms: run the `nix-env --install` line without sudo.

Warning: writing to the local store with a newer Nix, for example `nix-build` or `nix-store --realise`, may change the database schema. If you revert to an older version you may need to purge the store database before it works.

## Checked

2026-11-04: applicability note, the version check command, the schema warning and the Linux, macOS and single-user commands confirmed against the Upgrading Nix manual page. Removed the Verify line, which the page does not state.

Method: documentation only; no commands were run.
