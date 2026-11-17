---
id: computing-software.systems-network-administration.nix.install-from-tarball
name: install-from-tarball
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, binary-tarball, offline-install, install-script]
level: practitioner
status: docs-checked
description: "Install Nix from a binary tarball: pick version and system type, unpack, run the bundled install script, and customise it through install-multi-user variables."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/installation/installing-binary.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Steps: choose a version and system type, download and unpack the tarball, run the installer.

```
pushd $(mktemp -d)
export VERSION=2.19.2
export SYSTEM=x86_64-linux
curl -LO https://releases.nixos.org/nix/nix-$VERSION/nix-$VERSION-$SYSTEM.tar.xz
tar xf nix-$VERSION-$SYSTEM.tar.xz
cd nix-$VERSION-$SYSTEM
./install
popd
```

(The values are the manual's examples.)

The manual's own example unpacks with `tar xfj`; check the flags your `tar` needs for a `.tar.xz` file.

The installer can be customised with environment variables documented in the `install-multi-user` file shipped in the tarball.

Distribution packaging: the community maintains installers in some Linux distributions' native package formats, documented at nix-community.github.io/nix-installers.

## Checked

2026-11-04. Confirmed against the Nix manual Installing a Binary Distribution page: the three steps, the example commands with `VERSION=2.19.2` and `SYSTEM=x86_64-linux`, the `./install` step, the `install-multi-user` environment variables and the nix-community installers link. Removed an unsourced claim about the `j` tar flag and a verify line; the page's example uses `tar xfj`.

Method: documentation only; no commands were run.
