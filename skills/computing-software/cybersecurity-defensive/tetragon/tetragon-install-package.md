---
id: computing-software.cybersecurity-defensive.tetragon.tetragon-install-package
name: tetragon-install-package
category: computing-software
field: cybersecurity-defensive
product: tetragon
tags: [install-package]
level: practitioner
status: docs-checked
description: "Install Tetragon as a systemd service from a release tarball, configure it with drop-ins, upgrade, uninstall and read its events."
sources:
  - "https://tetragon.io/docs/installation/package/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install Tetragon from a release tarball

Goal: run Tetragon as a systemd service. Tarballs (amd64 and arm64 as of version 1.0) are distributed with the GitHub releases.

## Install

```shell
curl -LO https://github.com/cilium/tetragon/releases/download/<version>/tetragon-<version>-amd64.tar.gz
tar -xvf tetragon-<version>-amd64.tar.gz
cd tetragon-<version>-amd64/
sudo ./install.sh
sudo systemctl status tetragon
```

You can inspect `install.sh` first. Success prints "Tetragon installed successfully!". If Tetragon fails to start over BTF issues, see the BTF question in the FAQ.

## Configuration

Defaults are installed in `/usr/local/lib/tetragon/tetragon.conf.d/`. Override them with drop-ins in `/etc/tetragon/tetragon.conf.d/` or with command line flags. Remove the added files in `/etc/tetragon/tetragon.conf.d/` to restore defaults.

## Upgrade

Download the new tarball, stop the service, remove the old version, then rerun `install.sh` from the extracted archive:

```shell
sudo systemctl stop tetragon
sudo rm -fr /usr/lib/systemd/system/tetragon.service
sudo rm -fr /usr/local/bin/tetragon
sudo rm -fr /usr/local/lib/tetragon/
```

## Uninstall

Run `sudo ./uninstall.sh` from the tarball, or manually: `systemctl stop` and `disable` tetragon, remove the service file, run `systemctl daemon-reload`, and remove `/usr/local/bin/tetragon`, `/usr/local/bin/tetra` and `/usr/local/lib/tetragon/`. To purge custom settings: `sudo rm -fr /etc/tetragon/`.

## Operating

The tarball listens on `unix:///var/run/tetragon/tetragon.sock`. Use it with `tetra`:

```shell
sudo tetra --server-address unix:///var/run/tetragon/tetragon.sock getevents
sudo tetra --server-address "unix:///var/run/tetragon/tetragon.sock" getevents -o compact
```

JSON events are logged to `/var/log/tetragon/tetragon.log` by default and rotated in the same directory; `sudo tail -f` that file for real-time events.

## Checked

Date: 2026-11-07

Package page read in full; every claim matched, no change. The release URL uses a version placeholder.

Method: documentation only; no commands were run.
