---
id: computing-software.networking-hardware-and-wireless.tailscale.install-tailscale-linux
name: install-tailscale-linux
category: computing-software
field: networking-hardware-and-wireless
product: tailscale
tags: [install-linux, install-sh, static-binaries]
level: intro
status: docs-checked
description: "Install with the official script or static binaries and bring the node up."
sources: ["https://tailscale.com/kb/1031"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Tailscale on Linux

Goal: get a Linux node onto the tailnet.

**Script**
```
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
```
`tailscale up` prints a URL to authenticate. Afterwards confirm the device on the Machines page. If you do not want `curl | sh`, use the Packages stable track page for manual instructions.

**Supported by the script:** Ubuntu and Debian based distributions, RHEL, CentOS, Fedora and derivatives, Raspberry Pi OS, Amazon Linux, openSUSE and SUSE Linux Enterprise, Oracle Linux, VMware Photon OS.

**Alternative package managers:** Arch Linux and NixOS have their own instructions.

**Static binaries**

1. Download the archive for your CPU architecture.
2. Unpack:
```
tar xvf tailscale_<version>_<architecture>.tgz
```
3. Start the daemon:
```
sudo tailscaled --state=tailscaled.state
```
4. In another shell run `sudo tailscale up`.

A systemd service file ships in the `systemd/` subdirectory of the archive if you want `tailscaled` started automatically.

**Checklist**

1. Installed.
2. Authenticated via the URL printed by `tailscale up`.
3. Device visible in Machines.

## Checked

2026-11-09. Confirmed against the Tailscale Install on Linux page: install script, supported distributions, alternative package managers, static binary steps and the systemd subdirectory. Removed the auth key mention from the checklist, which the page does not cover.

Method: docs-checked 2026-11-09 against tailscale.com/kb/1031 (Install Tailscale on Linux), read in full.
