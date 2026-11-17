---
id: computing-software.networking-hardware-and-wireless.wireguard.wireguard-installation-by-platform
name: wireguard-installation-by-platform
category: computing-software
field: networking-hardware-and-wireless
product: wireguard
tags: [wireguard-install, apt-install-wireguard, wireguard-tools, dkms, kmod, openwrt, macos-homebrew]
level: intro
status: docs-checked
description: "Pick the right WireGuard package per OS: kernel module versus tools only, from apt, dnf, pacman, apk, opkg and RHEL variants."
sources: ["https://www.wireguard.com/install/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Installing WireGuard

The install page labels each distribution by what the package provides: the kernel module and/or the tools (`wireguard-tools`). Package names per the install page:

```bash
sudo apt install wireguard                  # Debian releases older than Bullseye need backports enabled
sudo dnf install wireguard-tools            # Fedora
sudo pacman -S wireguard-tools              # Arch; kernels < 5.6 may also choose wireguard-lts or wireguard-dkms + linux-headers
sudo zypper install wireguard-tools         # openSUSE/SLE
apk add -U wireguard-tools                  # Alpine
opkg install wireguard                      # OpenWRT
nix-env -iA nixpkgs.wireguard-tools         # Nix on Darwin (userspace go)
```

NixOS: add `boot.extraModulePackages = [ config.boot.kernelPackages.wireguard ];` and the tools to `environment.systemPackages`.

RHEL and CentOS 7 and 8 have module routes on the page: ELRepo `kmod-wireguard` (the page calls it the easiest), a DKMS package `wireguard-dkms` for non-standard kernels (the RHEL 8 steps enable EPEL and the codeready builder repo and a COPR repository), or on CentOS the signed module in `kernel-plus`. Each route also installs `wireguard-tools`.

Other platforms on the page: FreeBSD (`pkg install wireguard`, kmod or userspace Go), OpenBSD (`pkg_add wireguard-tools`), Termux, and macOS CLI via Homebrew (`brew install wireguard-tools`) or MacPorts (`port install wireguard-tools`), which use userspace Go.

Verify: continue with the quick start, where `ip link add dev wg0 type wireguard` creates the interface.

## Checked

2026-11-03. Confirmed: Package names and commands for Debian, Fedora, Arch, openSUSE/SLE, Alpine, OpenWRT, Nix on Darwin, NixOS, RHEL/CentOS module routes, FreeBSD, OpenBSD, Termux, Homebrew and MacPorts against the install page. Removed: the Ubuntu label and the Windows, iOS and Android lines (the fetched page text did not include them), the 'needing a separate module' reading of the Arch note, and the wg --version / module-load verify.

Method: documentation only; no commands were run.
