---
id: computing-software.systems-network-administration.linux.debian-ubuntu-backports
name: debian-ubuntu-backports
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, backports, debian-backports, apt-pinning, apt-default-release, newer-packages, stable-updates]
level: practitioner
status: docs-checked
description: "Get newer packages on Debian stable/Ubuntu LTS safely from backports: enabling the suite, default pin priority 100, installing with -t, upgrades and when not to use backports."
sources:
  - https://backports.debian.org/Instructions/
  - https://manpages.debian.org/bookworm/apt/apt_preferences.5.en.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Debian and Ubuntu backports

**What:** newer packages recompiled for Debian stable (for example `bookworm-backports`). Ubuntu also has a `<release>-backports` pocket; this skill documents the Debian archive only.

## Enable (deb822 format)
```
# /etc/apt/sources.list.d/backports.sources
Types: deb
URIs: http://deb.debian.org/debian
Suites: bookworm-backports
Components: main
Signed-By: /usr/share/keyrings/debian-archive-keyring.gpg
```
`apt update`. The Debian backports archive is marked `NotAutomatic: yes` and `ButAutomaticUpgrades: yes`, giving its packages priority 100 (apt_preferences(5)): nothing comes from it unless asked.

## Install
```bash
apt install -t bookworm-backports <package>      # form shown on backports.debian.org
apt install <package>/bookworm-backports         # a single package
apt policy <package>                              # shows priorities and the candidate
```

## Pinning only some packages permanently
```
# /etc/apt/preferences.d/backports-podman
Package: podman buildah skopeo
Pin: release n=bookworm-backports
Pin-Priority: 500
```

## When not to
- Backports are supported on a best-effort basis; subscribe to debian-backports-announce for security announcements.

## Verify
- [ ] `apt policy <pkg>` shows the backports version installed and stable versions still default for everything else.

## Checked

Checked against backports.debian.org/Instructions (2026-10-25) and apt_preferences(5) (Debian/apt doc/, last commit 2025-11-10).
Confirmed: deb822 `.sources` layout with `Suites: <release>-backports`, `apt install -t <release>-backports`, priority 100 from NotAutomatic plus ButAutomaticUpgrades, `Pin: release n=` syntax, best-effort support and the announce list.
Fixed: the install syntax now follows the documented form. Removed as unconfirmed: Ubuntu pocket behaviour, contrib/non-free-firmware components (the page shows main), kernel and package examples, auto-follow upgrade claim, FrankenDebian remark.

Method: documentation only; no commands were run.
