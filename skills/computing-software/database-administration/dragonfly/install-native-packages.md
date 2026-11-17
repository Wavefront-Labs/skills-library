---
id: computing-software.database-administration.dragonfly.install-native-packages
name: install-native-packages
category: computing-software
field: database-administration
product: dragonfly
tags: [native-packages, apt, dnf, systemd, dragonfly]
level: intro
status: docs-checked
description: "Install Dragonfly from the signed RPM or Debian repositories, enable the systemd service, verify with PING and pin older versions."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/getting-started/native-packages.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Packages are hosted at packages.dragonflydb.io and signed with GPG keys.

## RPM (Fedora, RHEL, CentOS)

```shell
sudo dnf config-manager addrepo --from-repofile=https://packages.dragonflydb.io/dragonfly.repo
sudo dnf install -y dragonfly
```

## Debian and Ubuntu

```shell
sudo curl -Lo /usr/share/keyrings/dragonfly-keyring.public https://packages.dragonflydb.io/pgp-key.public
sudo curl -Lo /etc/apt/sources.list.d/dragonfly.sources https://packages.dragonflydb.io/dragonfly.sources
sudo apt update && sudo apt install -y dragonfly
```

## Start and verify

```shell
sudo systemctl enable --now dragonfly
sudo systemctl status dragonfly
redis-cli -p 6379 PING
```

Status should be "active (running)" and `PING` returns `PONG`.

## Versions

The YUM/DNF repository keeps the latest 5 releases, so specific versions can be installed. The APT repository contains the latest version; for an older version on Debian/Ubuntu, download the package from the GitHub releases page.

## Checked

2026-11-04: confirmed against the Install from Packages page (all commands, verification output, version availability). Softened "holds only the latest version" to the page's wording.
Method: documentation only; no commands were run.
