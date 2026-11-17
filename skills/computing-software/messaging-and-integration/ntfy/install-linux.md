---
id: computing-software.messaging-and-integration.ntfy.install-linux
name: install-linux
category: computing-software
field: messaging-and-integration
product: ntfy
tags: [ntfy, install, linux, systemd, packages]
level: intro
status: docs-checked
description: "Install the ntfy server and CLI on Linux from the release tarball, apt repo, deb or rpm, and run it as a systemd or OpenRC service."
sources:
  - https://raw.githubusercontent.com/binwiederhier/ntfy/main/docs/install.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Installing on Linux

You only need to install anything to self-host the server or use the CLI; curl is enough to publish to ntfy.sh.

## Binary

Pick the architecture (`amd64`, `armv6`, `armv7`, `arm64`) from the GitHub releases page:

```
tar zxvf ntfy_<version>_linux_amd64.tar.gz
sudo cp -a ntfy_<version>_linux_amd64/ntfy /usr/local/bin/ntfy
sudo mkdir /etc/ntfy && sudo cp ntfy_<version>_linux_amd64/{client,server}/*.yml /etc/ntfy
sudo ntfy serve
```

This runs the server but not at boot.

## Permanent service

```
useradd --system --home-dir /var/lib/ntfy --shell /bin/false --comment "User for the simple HTTP-based pub-sub notification service" ntfy
```

- systemd: put `server/ntfy.service` in `/etc/systemd/system/` (mode 644), then `systemctl daemon-reload` and `systemctl start ntfy`.
- OpenRC: `server/ntfy.openrc` to `/etc/init.d/ntfy` (mode 755), then `rc-service ntfy start` and `rc-update add ntfy default`.

## Packages

- Debian/Ubuntu: apt repo at `archive.ntfy.sh/apt` (keyring to `/etc/apt/keyrings/ntfy.gpg`, then `apt install ntfy`), or `dpkg -i ntfy_*.deb`.
- Fedora/RHEL/CentOS: `rpm -ivh <ntfy .rpm URL>`.
- Arch: `paru -S ntfysh-bin` (AUR). NixOS: package `ntfy-sh`.

The page's apt, deb and rpm steps use `sudo systemctl enable ntfy` then `sudo systemctl start ntfy`.

## Checked

2026-11-04. Confirmed against the ntfy install page (Linux binary, Debian/Ubuntu, Fedora/RHEL, Arch, NixOS): architectures, tarball steps, system user, systemd and OpenRC steps and modes, apt repo at archive.ntfy.sh and keyring path, dpkg and rpm commands, enable/start commands. Removed: the combined `enable --now` form and the Verify step.
Method: documentation only; no commands were run.
