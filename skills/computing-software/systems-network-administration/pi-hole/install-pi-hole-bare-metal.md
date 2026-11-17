---
id: computing-software.systems-network-administration.pi-hole.install-pi-hole-bare-metal
name: install-pi-hole-bare-metal
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [pihole-install, installer-script, review-before-run]
level: intro
status: docs-checked
description: "Install Pi-hole on a host with the one-step installer, or review the installer first using a clone or a download."
sources: ["https://docs.pi-hole.net/main/basic-install/", "https://docs.pi-hole.net/main/post-install/", "https://docs.pi-hole.net/main/pihole-command/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Install Pi-hole on a host

**One-step install**

```bash
curl -sSL https://install.pi-hole.net | bash
```

Piping to `bash` stops you reading the code before it runs, so the project documents three alternatives.

**Alternative 1: clone the repository and run**

```bash
git clone --depth 1 https://github.com/pi-hole/pi-hole.git Pi-hole
cd "Pi-hole/automated install/"
sudo bash basic-install.sh
```

**Alternative 2: download the installer, inspect it, then run**

```bash
wget -O basic-install.sh https://install.pi-hole.net
sudo bash basic-install.sh
```

**Alternative 3: Docker.** Use the official images instead of the installer; see the Docker skills.

**Before you start**

1. Check hardware, OS and ports against the requirements skill.

**After the installer finishes**

1. Point your network at Pi-hole (router DHCP DNS setting, or Pi-hole's own DHCP server).
2. Add your user to the `pihole` group so CLI commands authenticate without a password prompt.
3. Optionally make the host itself use Pi-hole.

Remove everything later with `pihole uninstall`, which lets you decline removal of each dependency.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Installation (main/basic-install); Post-Install (main/post-install); The pihole Command (main/pihole-command). Removed the static IP and free-port-53 pre-install steps (not on the install pages).
Method: documentation only; no commands were run.
