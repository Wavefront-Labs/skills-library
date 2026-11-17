---
id: computing-software.systems-network-administration.nix.install-pinned-version
name: install-pinned-version
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, pinned-version, releases-nixos-org, install-version]
level: practitioner
status: docs-checked
description: "Install a specific Nix release by using the version-specific installer URL on releases.nixos.org instead of the moving nixos.org/nix/install script."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/installing-binary.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Version-specific installer URLs exist for every Nix release since 1.11.16 and are listed at releases.nixos.org. Each version's directory includes its SHA-256 hash.

```
export VERSION=2.19.2
curl -L https://releases.nixos.org/nix/nix-$VERSION/install | sh
```

(`2.19.2` is the manual's example; substitute the release you need.)

Use this in provisioning scripts and CI where a reproducible installer matters, rather than the default `https://nixos.org/nix/install`.

The same flags apply as for the default installer, for example `--daemon` or `--no-daemon`, passed after `sh -s --` when piping.

## Checked

2026-11-04. Confirmed against the Nix manual Installing a Binary Distribution page: version-specific installer URLs for all versions since 1.11.16 listed at releases.nixos.org, the per-version SHA-256 hash, the `VERSION=2.19.2` example, and the `--help` flag pattern. Removed an unsourced database-schema gotcha and a verify line.

Method: documentation only; no commands were run.
