---
id: computing-software.systems-network-administration.incus.install-linux-packages
name: install-linux-packages
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, install, packages, apt, dnf, pacman, apk, zabbly, debian, ubuntu]
level: intro
status: docs-checked
description: "Install the Incus daemon from distribution packages on Linux: per-distro commands for Debian, Ubuntu, Fedora, Arch, Alpine, openSUSE, NixOS, Void, plus VM extras."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/installing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Incus from Linux packages

The daemon runs only on Linux. Some distros package it; others rely on third parties.

- Debian 13: `apt install incus` (containers and VMs) or `apt install incus-base` (containers only). Zabbly packages cover Debian 11, 12 and 13.
- Ubuntu 24.04 and later: `apt install incus`; for VMs also `apt install qemu-system`. Zabbly covers 22.04, 24.04 and 26.04.
- Fedora: `dnf install incus`.
- Arch: `pacman -S incus`.
- openSUSE (Tumbleweed, Leap 15.6+): `zypper in incus`.
- Rocky Linux 9/10: unofficial `neelc/incus` COPR, then `dnf install incus incus-tools`.
- Alpine: enable the edge main and community repos in `/etc/apk/repositories`, `apk update`, `apk add incus incus-client` (add `incus-vm` for VMs), then `rc-update add incusd` and `rc-service incusd start`.
- Void: `xbps-install incus incus-client`, link `/etc/sv/incus` and `/etc/sv/incus-user` into `/var/service`, then `sv up` both.
- Gentoo: `emerge -av app-containers/incus`; add `app-emulation/qemu` for VMs and set up `/etc/subuid` and `/etc/subgid`.
- NixOS: set `virtualisation.incus.enable = true;`.
- Chimera: `apk add incus`, `dinitctl enable incus`; for VMs add `qemu-edk2-firmware` and launch with `security.secureboot=false`.

Next steps: grant access (see incus-admin-group-and-subuid) and run `incus admin init`.

## Checked

2026-11-09. Confirmed against the Incus How to install page (Linux package tabs): Debian 13 packages and Zabbly releases, Ubuntu 24.04 and Zabbly releases, Fedora, Arch, openSUSE, Rocky COPR, Alpine, Void, Gentoo, NixOS, Chimera commands. Reworded: Gentoo subuid/subgid ordering (the page does it after install).
Method: documentation only; no commands were run.
